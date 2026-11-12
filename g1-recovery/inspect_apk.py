#!/usr/bin/env python3
"""Read-only G1 APK recovery. No decompilation, signing, or publishing."""
import base64, hashlib, json, pathlib, sys, zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
PARTS=[ROOT/"games"/"downloads"/f"jungle-friends-quiz.part{i}.txt" for i in (1,2,3)]
EXPECTED="9ab2b83091a90215277b14db53885effa8f909e7ce4fd2529eb26cc3c5347c71"
OUT=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path("g1-recovery-output")
OUT.mkdir(parents=True,exist_ok=True)
apk=OUT/"Jungle-Friends-Quiz.apk"
sha=hashlib.sha256()
with apk.open("wb") as dst:
    for p in PARTS:
        if not p.is_file(): raise SystemExit(f"Missing source part: {p}")
        data=base64.b64decode(p.read_bytes().strip(),validate=True)
        dst.write(data);sha.update(data)
actual=sha.hexdigest()
if actual!=EXPECTED:
    apk.unlink(missing_ok=True)
    raise SystemExit(f"FAIL: APK SHA-256 mismatch: {actual}")
with zipfile.ZipFile(apk) as z:
    bad=z.testzip()
    if bad: raise SystemExit(f"FAIL: ZIP CRC mismatch: {bad}")
    names=z.namelist()
    info={"sha256":actual,"apk_bytes":apk.stat().st_size,
          "zip_entries":len(names),
          "dex_files":[n for n in names if n.endswith(".dex")],
          "asset_paths":[n for n in names if n.startswith("assets/")][:150],
          "native_libraries":[n for n in names if n.startswith("lib/")][:100],
          "has_android_manifest":"AndroidManifest.xml" in names,
          "has_resources_arsc":"resources.arsc" in names,
          "has_v1_signature":any(n.startswith("META-INF/") and n.endswith(".RSA") for n in names),
          "note":"v2/v3 signing, package name, target SDK, permissions, and gameplay remain unverified"}
(OUT/"apk-inventory.json").write_text(json.dumps(info,indent=2),encoding="utf-8")
print(json.dumps(info,indent=2))
