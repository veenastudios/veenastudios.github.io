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
if errors:
    print("\n".join(errors));sys.exit(1)
print("PASS: offline bundle smoke check",len(js_files),"JS",len(css_files),"CSS")
