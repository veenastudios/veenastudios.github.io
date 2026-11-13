#!/usr/bin/env python3
"""Fail closed if the experimental collage loses essential safe boundaries."""
from pathlib import Path
root=Path(__file__).resolve().parent
packer=(root/"prepare_offline.py").read_text(encoding="utf-8")
js=(root/"collage_trial.js").read_text(encoding="utf-8")
css=(root/"collage_trial.css").read_text(encoding="utf-8")
checks={
 "collage CSS injected into offline APK":'trial_css=(trial_dir/"collage_trial.css")' in packer,
 "collage JS injected into offline APK":'trial_js=(trial_dir/"collage_trial.js")' in packer,
 "approved home remains independent":".srPremiumHome" in packer and "approved-home-carousel.png" in packer,
 "top banner has destination":'srCollageTop' in js and 'https://veenastudios.in/' in js,
 "bottom banner has destination":'srCollageBottom' in js,
 "share uses native sharing when available":'navigator.share(data)' in js,
 "share has copy fallback":'navigator.clipboard.writeText(url)' in js,
 "share does not award unverified coins":'srCoins' not in js and '100' not in js,
 "banner ignores taps outside own elements":'pointer-events:none' in css and 'pointer-events:auto' in css,
 "banner hides outside Home": "layer.style.display=home?'block':'none'" in js,
 "artwork filenames are wired": 'sr_gamers_banner.webp' in js and 'sr_kids_banner.webp' in js and 'sr_gamers_banner.webp' in css and 'sr_kids_banner.webp' in css,
 "artwork fallback is accessible": "img.onerror" in js and "hasArtwork" in css,
 "packer copies approved artwork": "shutil.copy2(source,dst/banner)" in packer,
 "premium is retained and positioned": "premium.style.setProperty('top'" in js and "premium.style.setProperty('left'" in js,
}
for name,ok in checks.items():
 print(("PASS" if ok else "FAIL")+": "+name)
if not all(checks.values()):raise SystemExit(1)
