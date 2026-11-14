#!/usr/bin/env python3
"""Build Android launcher icon resources from the approved Tap Rush web icon."""
from pathlib import Path
from PIL import Image

base = Path(__file__).resolve().parent
source = base / "app/src/main/assets/icon-512.png"
if not source.is_file():
    raise SystemExit(f"Missing approved launcher icon: {source}")
with Image.open(source) as image:
    image = image.convert("RGBA")
    if image.width < 192 or image.height < 192:
        raise SystemExit("Approved launcher icon resolution is too small")
    resources = base / "app/src/main/res"
    for density, size in (("mdpi",48),("hdpi",72),("xhdpi",96),("xxhdpi",144),("xxxhdpi",192)):
        output = resources / f"mipmap-{density}" / "ic_launcher.png"
        output.parent.mkdir(parents=True, exist_ok=True)
        image.resize((size,size), Image.Resampling.LANCZOS).save(output, format="PNG")
        print(output.relative_to(base))
