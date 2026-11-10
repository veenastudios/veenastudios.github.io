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
if (root/"index.html").is_file() and "More SR Games" not in html: errors.append("Game hub launcher missing")
hub_path=root/"game-hub.html"
if hub_path.is_file():
    hub=hub_path.read_text(encoding="utf-8")
    for title in ("Tap Rush","Jungle Friends Quiz","Math Challenge","Flags &amp; Capitals","Veena"):
        if title not in hub: errors.append("Approved hub label missing: "+title)
    if 'name="viewport"' not in hub: errors.append("Portrait viewport meta missing")
    if 'Coming Soon' not in hub: errors.append("Unreleased games must show Coming Soon")
    if 'https://veenastudios.in/' not in hub: errors.append("Veena Studios promotion link missing")
if 'querySelector(\'.liveShelf\')' not in html: errors.append("Hub launcher not scoped to home shelf")
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
for marker in ('srGamesPanel','.worldMap{background:linear-gradient','.hub .premiumHome{object-fit:contain'):
    if marker not in html: errors.append("Android layout fix missing: "+marker)
if errors:
    print("\n".join(errors));sys.exit(1)
print("PASS: offline bundle smoke check",len(js_files),"JS",len(css_files),"CSS")
