"""Stage Tap Rush's existing web build into Android app assets safely."""
from pathlib import Path
import re
import shutil

root = Path(__file__).resolve().parents[2]
src = root / "tap-rush"
dst = Path(__file__).resolve().parent / "app/src/main/assets/tap-rush"
if not (src / "index.html").is_file():
    raise SystemExit("Tap Rush web entry missing")
if dst.exists():
    shutil.rmtree(dst)
shutil.copytree(src, dst)
entry = dst / "index.html"
html = entry.read_text(encoding="utf-8")
html = html.replace('src="/tap-rush/', 'src="./').replace('href="/tap-rush/', 'href="./')
entry.write_text(html, encoding="utf-8")
for attr in ("src", "href"):
    for relative in re.findall(rf'{attr}="\./([^"]+)"', html):
        asset = (dst / relative.split("?")[0]).resolve()
        if not asset.is_relative_to(dst.resolve()) or not asset.is_file():
            raise SystemExit(f"Android staged entry references missing asset: {relative}")
if 'src="/tap-rush/' in html or 'href="/tap-rush/' in html:
    raise SystemExit("Android staged entry still contains website-absolute asset paths")
print("Staged and checked local web files:", sum(p.is_file() for p in dst.rglob("*")))
