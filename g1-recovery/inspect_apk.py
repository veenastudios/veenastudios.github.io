#!/usr/bin/env python3
"""Read-only static inventory of G1's packaged web assets. Never alters APK."""
import base64, hashlib, json, pathlib, re, sys, zipfile
root=pathlib.Path(__file__).resolve().parents[1]
parts=[root/"games"/"downloads"/f"jungle-friends-quiz.part{i}.txt" for i in (1,2,3)]
expected="9ab2b83091a90215277b14db53885effa8f909e7ce4fd2529eb26cc3c5347c71"
out=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path("g1-recovery-output")
out.mkdir(parents=True,exist_ok=True)
apk=out/"Jungle-Friends-Quiz.apk"
sha=hashlib.sha256()
with apk.open("wb") as f:
    for p in parts:
        data=base64.b64decode(p.read_bytes().strip(),validate=True)
        sha.update(data);f.write(data)
actual=sha.hexdigest()
if actual!=expected:
    apk.unlink(missing_ok=True)
    raise SystemExit(f"SHA256 FAIL: {actual}")
with zipfile.ZipFile(apk) as z:
    bad=z.testzip()
    if bad: raise SystemExit(f"ZIP CRC FAIL: {bad}")
    names=z.namelist()
    report={"sha256":actual,"apk_bytes":apk.stat().st_size,"zip_entries":len(names),
            "dex_files":[n for n in names if n.endswith(".dex")],
            "web_assets":[n for n in names if n.startswith("assets/")],
            "has_manifest":"AndroidManifest.xml" in names,
            "has_resources":"resources.arsc" in names,
            "note":"Static asset inventory only; no device testing, source reconstruction or Play release verification"}
    indicators={}
    for name in names:
        if not name.startswith("assets/") or not name.endswith((".js",".html",".css")): continue
        raw=z.read(name)
        if len(raw)>2_000_000: continue
        s=raw.decode("utf-8","replace")
        indicators[name]={"bytes":len(raw),
                          "localStorage":bool(re.search(r"localStorage",s,re.I)),
                          "indexedDB":bool(re.search(r"indexedDB",s,re.I)),
                          "question_words":len(re.findall(r"question|sawal|प्रश्न",s,re.I)),
                          "language_words":len(re.findall(r"language|hindi|english|भाषा",s,re.I)),
                          "ad_indicators":bool(re.search(r"admob|adsbygoogle|gma\.sdk|rewardedAd",s,re.I)),
                          "billing_indicators":bool(re.search(r"billingclient|inappbilling|purchaseToken",s,re.I))}
    report["static_asset_indicators"]=indicators
(out/"apk-inventory.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
