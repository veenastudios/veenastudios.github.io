#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urlsplit,unquote
import argparse,re,shutil,sys
p=argparse.ArgumentParser();p.add_argument("published_tap_rush",type=Path);a=p.parse_args()
src=a.published_tap_rush.resolve();dst=Path(__file__).resolve().parent/"app/src/main/assets"
missing=[];checked=set()
def check(raw,origin,base=None):
 raw=raw.strip().strip("'\"");u=urlsplit(raw)
 if u.scheme or raw.startswith(("#","data:","//")):return
 path=unquote(u.path)
 if not path:return
 if path.startswith("/tap-rush/"):path=path[len("/tap-rush/"):];base=src
 elif path.startswith("/"):return
 elif path.startswith("./"):path=path[2:]
 target=((base or src)/path).resolve()
 if not target.is_relative_to(src):missing.append((origin,raw,"outside root"));return
 checked.add(str(target.relative_to(src)))
 if not target.is_file():missing.append((origin,raw,"not found"))
for f in ("index.html","manifest.webmanifest","sw.js"):check(f,"required")
if (src/"index.html").exists():
 html=(src/"index.html").read_text(encoding="utf-8")
 for ref in re.findall(r'(?:src|href)\s*=\s*["\']([^"\']+)',html):check(ref,"index.html")
for css in src.rglob("*.css"):
 s=css.read_text(encoding="utf-8")
 for ref in re.findall(r'url\(\s*["\']?([^\)"\']+)',s):check(ref,str(css.relative_to(src)),css.parent)
for js in src.rglob("*.js"):
 s=js.read_text(encoding="utf-8")
 for ref in re.findall(r'["\']((?:\./|/tap-rush/)[^"\']+\.(?:png|webp|jpg|jpeg|svg|mp3|wav|ogg))["\']',s,re.I):check(ref,str(js.relative_to(src)))
 for ref in re.findall(r'["\']([\w-]+-trophy\.(?:webp|png))["\']',s,re.I):check(ref,str(js.relative_to(src)))
# Audit any remote image/audio references in compiled JavaScript.
for js in src.rglob("*.js"):
 script=js.read_text(encoding="utf-8")
 remote=set(re.findall(r'https?://[^"\\'\x60\\s<>]+\\.(?:png|webp|jpe?g|svg|mp3|ogg|wav)(?:\\?[^"\\'\x60\\s<>]*)?',script,re.I))
 for url in sorted(remote):
  if site_image in url and url.startswith("https://veenastudios.in/"):continue
  missing.append((str(js.relative_to(src)),url,"external runtime asset"))
if missing:
 print("FAIL: missing offline assets")
 for origin,ref,why in sorted(set(missing)):print(origin,ref,why)
 sys.exit(1)
# The published game references one site-root image. Bundle it locally for true offline play.
site_image="file_00000000c1108207931406ed369edda6.jpg"
site_source=src.parent/site_image
if not site_source.is_file():
 print("FAIL: required site-root image missing:",site_source)
 sys.exit(1)
if dst.exists():shutil.rmtree(dst)
shutil.copytree(src,dst)
shutil.copy2(site_source,dst/site_image)
for js in (dst/"assets").glob("*.js"):
 s=js.read_text(encoding="utf-8")
 s=s.replace("https://veenastudios.in/"+site_image+"?v=2","/tap-rush/"+site_image)
 s=re.sub(r'"serviceWorker"in navigator&&window\.addEventListener\("load",\(\)=>\{navigator\.serviceWorker\.register\("\./sw\.js"\)\.catch\(\(\)=>\{\}\)\}\);?', "",s)
 js.write_text(s,encoding="utf-8")
print("PASS",len(checked),"references",sum(f.is_file() for f in dst.rglob("*")),"files")
