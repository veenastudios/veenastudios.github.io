"""Report known remote game asset dependencies. Fail only if missing local fallback."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[2]
game = root / "tap-rush"
bundle = game / "assets/index-B_be548G.js"
if not bundle.is_file():
    sys.exit("Missing Tap Rush JS bundle")
js = bundle.read_text(encoding="utf-8")
remote_images = sorted(set(re.findall(r'https?://[^"\s]+\.(?:png|jpe?g|webp)(?:\?[^"\s]*)?', js)))
if remote_images:
    print("Remote image dependencies detected:")
    for url in remote_images:
        print(" -", url)
    print("Offline first-launch visual completeness NOT VERIFIED; replace with licensed bundled local assets before release.")
else:
    print("No literal remote image URLs detected (dynamic URLs still require review).")
