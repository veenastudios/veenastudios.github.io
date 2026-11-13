#!/usr/bin/env python3
"""Offline bundle smoke checks; run after prepare_offline.py."""
from pathlib import Path
import re, sys
root=Path(__file__).resolve().parent/"app/src/main/assets"
errors=[]
html=(root/"index.html").read_text(encoding="utf-8")
js_files=list((root/"assets").glob("*.js"))
css_files=list((root/"assets").glob("*.css"))
if not js_files: errors.append("No JavaScript bundle")
if not css_files: errors.append("No CSS bundle")
if not (root/"game-hub.html").is_file(): errors.append("Game hub page missing")
if "srPremiumHome" not in html or "srHomePlay" not in html: errors.append("Premium home launcher missing")
hub_path=root/"game-hub.html"
if hub_path.is_file():
    hub=hub_path.read_text(encoding="utf-8")
    for title in ("Tap Rush","Jungle Friends Quiz","Math Challenge","Flags &amp; Capitals","Veena"):
        if title not in hub: errors.append("Approved hub label missing: "+title)
    if 'name="viewport"' not in hub: errors.append("Portrait viewport meta missing")
    if 'Coming Soon' not in hub: errors.append("Unreleased games must show Coming Soon")
    # The home shelf is injected by the offline packer, not the standalone hub page.

    if 'https://veenastudios.in/' not in hub: errors.append("Veena Studios promotion link missing")
if "document.querySelector('.hub .premiumHome')" not in html or "document.querySelector('.hub .liveShelf')" not in html: errors.append("Premium home not scoped to original home")
for ref in re.findall(r'(?:src|href)=["\']([^"\']+)["\']',html):
    p=ref.split("?")[0]
    if p.startswith("/tap-rush/"): p=p[len("/tap-rush/"):]
    elif p.startswith("./"): p=p[2:]
    elif p.startswith(("https:","http:","data:","#")): continue
    if not (root/p).is_file(): errors.append("HTML missing: "+ref)
for css in css_files:
    for ref in re.findall(r'url\(\s*["\']?([^\)"\']+)',css.read_text(encoding="utf-8")):
        p=ref.split("?")[0]
        if p.startswith("/tap-rush/"): p=p[len("/tap-rush/"):]
        elif p.startswith("./"): p=p[2:]
        if p.startswith(("data:","http:","https:")): continue
        if not (root/p).is_file(): errors.append("CSS missing: "+ref)
if js_files:
    js="\n".join(f.read_text(encoding="utf-8") for f in js_files)
    if 'https://veenastudios.in/file_00000000c1108207931406ed369edda6.jpg' in js:
        errors.append("External background image still in bundle")
    for world in ("jungle","city","space","water","himalaya"):
        if not (root/(world+"-trophy.webp")).is_file(): errors.append("Missing "+world+" trophy")

# Release gate: confirm the shipped JS contains actual pause logic, not only a visual button.
js_text="\n".join(p.read_text(encoding="utf-8") for p in root.glob("assets/*.js"))
for marker in ('srPauseButton','srPauseOverlay','pauseStarted.current','Wt.current+=elapsed','born:item.born+elapsed','if(x!=="play"||paused)return'):
    if marker not in js_text: errors.append("Pause functionality missing from shipped JS: "+marker)
for game in ('Color Slide Puzzle','Block Puzzle','Find the Face'):
    if not hub_path.is_file() or game not in hub_path.read_text(encoding='utf-8'):
        errors.append('Approved seven-game hub item missing: '+game)
approved=root/'approved-world-selection.webp'
if not approved.is_file() or approved.stat().st_size < 10000:
    errors.append('Approved 3D world-selection image missing or too small')
if 'approved-world-selection.webp' not in html:
    errors.append('Approved 3D world-selection image not wired into Android screen')
for marker in ('.worldNode:nth-child(1)', '.worldNode:nth-child(5)', '.mapTop button'):
    if marker not in html: errors.append('Approved world-selection interaction region missing: '+marker)
for marker in ('srGamesPanel','.worldMap{background:linear-gradient','.hub .premiumHome{object-fit:contain'):
    if marker not in html: errors.append("Android layout fix missing: "+marker)
if not (root/"approved-home-carousel.png").is_file(): errors.append("Approved home carousel PNG missing")
for marker in ("srCarouselPrev","srCarouselNext","srHomeSettings","srHomeCoins"):
    if marker not in html: errors.append("Premium home control missing: "+marker)
if errors:
    print("\n".join(errors));sys.exit(1)
print("PASS: offline bundle smoke check",len(js_files),"JS",len(css_files),"CSS")
