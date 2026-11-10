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
 for ref in re.findall(r"""["']((?:\./|/tap-rush/)[^"']+\.(?:png|webp|jpg|jpeg|svg|mp3|wav|ogg))["']""",s,re.I):check(ref,str(js.relative_to(src)))
 for ref in re.findall(r'["\']([\w-]+-trophy\.(?:webp|png))["\']',s,re.I):check(ref,str(js.relative_to(src)))
site_image="file_00000000c1108207931406ed369edda6.jpg"
# Audit any remote image/audio references in compiled JavaScript.
for js in src.rglob("*.js"):
 script=js.read_text(encoding="utf-8")
 remote=set(re.findall(r"""https?://[^\s"'<>]+\.(?:png|webp|jpe?g|svg|mp3|ogg|wav)(?:\?[^\s"'<>]*)?""",script,re.I))
 for url in sorted(remote):
  if site_image in url and url.startswith("https://veenastudios.in/"):continue
  missing.append((str(js.relative_to(src)),url,"external runtime asset"))
if missing:
 print("FAIL: missing offline assets")
 for origin,ref,why in sorted(set(missing)):print(origin,ref,why)
 sys.exit(1)
# The published game references one site-root image. Bundle it locally for true offline play.
site_source=src.parent/site_image
if not site_source.is_file():
 print("FAIL: required site-root image missing:",site_source)
 sys.exit(1)
if dst.exists():shutil.rmtree(dst)
shutil.copytree(src,dst)
shutil.copy2(site_source,dst/site_image)
# Ship the approved-structure SR GAMERS hub in the offline APK.
hub=Path(__file__).resolve().parent/"game-hub.html"
if not hub.is_file():
 print("FAIL: game hub missing:",hub)
 sys.exit(1)
shutil.copy2(hub,dst/"game-hub.html")
# Attach navigation only to the game's existing home shelf; never overlay active rounds.
home_css="""<style id="taprush-mobile-home-fix">
.hub .premiumHome{object-fit:contain!important;object-position:center center!important;background:#07111f}
.hub .liveShelf{left:0!important;right:0!important;bottom:0!important;top:0!important;pointer-events:none!important}
.hub .liveShelf h2{display:none!important}
.hub .liveShelf .gameCard{position:absolute!important;left:0!important;top:53%!important;width:34%!important;height:10%!important;min-height:44px!important;opacity:0!important;border:0!important;padding:0!important;pointer-events:auto!important;z-index:6!important}
.hub .liveShelf #sr-games-hub-launcher{position:absolute!important;left:50%!important;top:auto!important;bottom:7%!important;transform:translateX(-50%)!important;pointer-events:auto!important;white-space:nowrap!important}
.worldMap{background:linear-gradient(#05251b70,#071d1e99),url(/tap-rush/jungle-scene.webp) center/cover!important}\n.worldMap .mapIntro,.worldMap .mapNote{color:#e1f3e8!important;text-shadow:0 1px 3px #001!important}\n</style>"""
entry=dst/"index.html"
markup=entry.read_text(encoding="utf-8")
launcher_js="""<script>(function(){
const link=document.createElement('a');
link.href='/tap-rush/game-hub.html';
link.textContent='🎮 More SR Games';
link.setAttribute('aria-label','Open More SR Games');
link.style.cssText='display:block;margin:0;width:max-content;max-width:100%;padding:7px 14px;border-radius:20px;border:2px solid #00dfff;background:#17094d;color:#fff;font:700 13px system-ui;text-decoration:none;box-shadow:0 0 8px #00dfff';
function mount(){const shelf=document.querySelector('.liveShelf');if(shelf&&!shelf.contains(link))shelf.appendChild(link)}
new MutationObserver(mount).observe(document.documentElement,{childList:true,subtree:true});
mount();
})();</script>"""
if "</body>" not in markup:
 print("FAIL: no body tag for home shelf launcher")
 sys.exit(1)
entry.write_text(markup.replace("</head>",home_css+"</head>").replace("</body>",launcher_js+"</body>"),encoding="utf-8")
for js in (dst/"assets").glob("*.js"):
 s=js.read_text(encoding="utf-8")
 s=s.replace("https://veenastudios.in/"+site_image+"?v=2","/tap-rush/"+site_image)
 s=re.sub(r'"serviceWorker"in navigator&&window\.addEventListener\("load",\(\)=>\{navigator\.serviceWorker\.register\("\./sw\.js"\)\.catch\(\(\)=>\{\}\)\}\);?', "",s)
 js.write_text(s,encoding="utf-8")
print("PASS",len(checked),"references",sum(f.is_file() for f in dst.rglob("*")),"files")
