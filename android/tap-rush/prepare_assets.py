"""Stage the existing website build into Android assets without modifying public files."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[2]
src = root / "tap-rush"
dst = Path(__file__).resolve().parent / "app/src/main/assets/tap-rush"
if not (src / "index.html").exists():
    raise SystemExit("Tap Rush web entry missing")
shutil.copytree(src, dst, dirs_exist_ok=True)
entry = dst / "index.html"
html = entry.read_text(encoding="utf-8")
html = html.replace('src="/tap-rush/', 'src="./').replace('href="/tap-rush/', 'href="./')
entry.write_text(html, encoding="utf-8")
print("Staged local web files:", sum(p.is_file() for p in dst.rglob("*")))
