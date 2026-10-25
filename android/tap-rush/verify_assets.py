"""Validate the existing Tap Rush web bundle before Android packaging."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[2]
game = root / "tap-rush"
html = (game / "index.html").read_text(encoding="utf-8")
required = ["index.html", "manifest.webmanifest", "sw.js"]
for attr in ("src", "href"):
    required.extend(re.findall(rf'{attr}="/tap-rush/([^"]+)"', html))
missing = [name for name in required if not (game / name.split("?")[0]).is_file()]
if missing:
    sys.exit("Missing Tap Rush assets: " + ", ".join(missing))
if not (game / "assets").is_dir():
    sys.exit("Missing bundled assets directory")
print(f"Tap Rush entry dependencies verified: {len(required)} references; Android staging may proceed")
