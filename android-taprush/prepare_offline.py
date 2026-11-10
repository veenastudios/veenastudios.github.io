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
.srGamesPanel{position:fixed;z-index:35;display:flex;flex-direction:column;justify-content:center;gap:5px;padding:8px 9px;background:linear-gradient(180deg,#06152dfb,#091a2ffb);border-top:2px solid #d8b15b;border-bottom:2px solid #d8b15b;box-shadow:0 0 15px #020812dd;color:#fff;overflow:hidden}
.srGamesPanel h2{font:900 clamp(13px,3.6vw,19px) system-ui;margin:0 0 3px;color:#ffdb74;letter-spacing:.5px}
.srGamesGrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:5px}
.srGamesGrid button{min-width:0;min-height:72px;border:1px solid #746c5c;border-radius:9px;background:linear-gradient(#183b43,#071a2c);color:white;padding:5px 2px;font:800 clamp(9px,2.4vw,12px) system-ui;display:flex;flex-direction:column;align-items:center;justify-content:space-around;gap:3px}
.srGamesGrid button.ready{border-color:#ffd35e;background:linear-gradient(#486b30,#123b25)}
.srGamesGrid button:disabled{opacity:1;color:#e7dce4}
.srGamesGrid .status{color:#ffd966;font-size:clamp(8px,2vw,11px)}

.worldMap{background:linear-gradient(#05251b70,#071d1e99),url(/tap-rush/jungle-scene.webp) center/cover!important}\n.worldMap .mapIntro,.worldMap .mapNote{color:#e1f3e8!important;text-shadow:0 1px 3px #001!important}\n.srPauseButton{position:absolute;z-index:40;top:calc(env(safe-area-inset-top) + 102px);right:12px;padding:10px 14px;border:2px solid #ffe19a;border-radius:16px;background:#142a36;color:white;font-weight:900}.srPauseOverlay{position:absolute;z-index:39;inset:0;display:grid;place-items:center;background:#020c1cbb;backdrop-filter:blur(4px)}.srPauseOverlay>div{text-align:center;background:#12312b;border:2px solid #f8d985;border-radius:24px;padding:32px}.srPauseOverlay button{background:#ffd65a;border:0;border-radius:12px;padding:13px 22px;font-weight:900}.game:has(.srPauseOverlay) .target{animation-play-state:paused!important;pointer-events:none!important}\n</style>"""
entry=dst/"index.html"
markup=entry.read_text(encoding="utf-8")
launcher_js="""<script>(function(){
const panel=document.createElement('section');panel.className='srGamesPanel';panel.setAttribute('aria-label','More SR Games');
panel.innerHTML='<h2>🎮 More SR Games</h2><div class="srGamesGrid"><button class="ready" type="button">🐯<span>Tap Rush</span><span class="status">▶ PLAY</span></button><button disabled>🦁<span>Jungle Friends Quiz</span><span class="status">🔒 Coming Soon</span></button><button disabled>➕<span>Math Challenge</span><span class="status">🔒 Coming Soon</span></button><button disabled>🌍<span>Flags &amp; Capitals</span><span class="status">🔒 Coming Soon</span></button></div>';
panel.querySelector('.ready').addEventListener('click',()=>{document.querySelector('.liveShelf .gameCard')?.click()});
function position(){const img=document.querySelector('.hub .premiumHome');const shelf=document.querySelector('.hub .liveShelf');if(!img||!shelf){panel.remove();return}if(!document.body.contains(panel))document.body.appendChild(panel);const r=img.getBoundingClientRect(),scale=Math.min(r.width/img.naturalWidth,r.height/img.naturalHeight);if(!Number.isFinite(scale)||!scale)return;const w=img.naturalWidth*scale,h=img.naturalHeight*scale,x=r.left+(r.width-w)/2,y=r.top+(r.height-h)/2;panel.style.left=x+'px';panel.style.width=w+'px';panel.style.top=(y+h*.645)+'px';panel.style.height=(h*.215)+'px'}
new MutationObserver(position).observe(document.getElementById('root')||document.body,{childList:true,subtree:true});
window.addEventListener('resize',position);window.addEventListener('orientationchange',position);
document.addEventListener('load',position,true);position();
})();</script>"""
if "</body>" not in markup:
 print("FAIL: no body tag for home shelf launcher")
 sys.exit(1)
entry.write_text(markup.replace("</head>",home_css+"</head>").replace("</body>",launcher_js+"</body>"),encoding="utf-8")
for js in (dst/"assets").glob("*.js"):
 s=js.read_text(encoding="utf-8")
 s=s.replace("https://veenastudios.in/"+site_image+"?v=2","/tap-rush/"+site_image)
 # Add real React-managed pause state to the offline bundle, without touching live site.
 if 'const Wt=El.useRef(0),Cl=El.useRef(1)' in s:
  changes=[
   ('const Wt=El.useRef(0),Cl=El.useRef(1)', 'const [paused,setPaused]=El.useState(!1),pauseStarted=El.useRef(0),Wt=El.useRef(0),Cl=El.useRef(1)'),
   ('Wt.current=performance.now(),cl("play")','setPaused(!1),pauseStarted.current=0,Wt.current=performance.now(),cl("play")'),
   ('if(x!=="play")return;let z=0,L=0;', 'if(x!=="play"||paused)return;let z=0,L=0;'),
   ('},[x,P]);const dl=z=>', '},[x,P,paused]);const dl=z=>'),
   ('if(x==="play"){if(Kl(o=>', 'if(x==="play"&&!paused){if(Kl(o=>'),
   ('x==="play"&&O.jsxs(O.Fragment,{children:[', 'x==="play"&&O.jsxs(O.Fragment,{children:[O.jsx("button",{className:"srPauseButton","aria-label":paused?"Resume game":"Pause game",onClick:()=>{if(paused){const elapsed=performance.now()-pauseStarted.current;Wt.current+=elapsed;Kl(items=>items.map(item=>({...item,born:item.born+elapsed})));pauseStarted.current=0;setPaused(!1)}else{pauseStarted.current=performance.now();setPaused(!0)}},children:paused?"▶ Resume":"⏸ Pause"}),paused&&O.jsx("div",{className:"srPauseOverlay",children:O.jsxs("div",{children:[O.jsx("h2",{children:"Game Paused"}),O.jsx("button",{onClick:()=>{const elapsed=performance.now()-pauseStarted.current;Wt.current+=elapsed;Kl(items=>items.map(item=>({...item,born:item.born+elapsed})));pauseStarted.current=0;setPaused(!1)},children:"▶ Resume Game"})]})}),'),
  ]
  for old,new in changes:
   if s.count(old)!=1:
    print("FAIL: pause patch anchor missing or ambiguous",old,s.count(old))
    sys.exit(1)
   s=s.replace(old,new,1)
 s=re.sub(r'"serviceWorker"in navigator&&window\.addEventListener\("load",\(\)=>\{navigator\.serviceWorker\.register\("\./sw\.js"\)\.catch\(\(\)=>\{\}\)\}\);?', "",s)
 js.write_text(s,encoding="utf-8")
print("PASS",len(checked),"references",sum(f.is_file() for f in dst.rglob("*")),"files")
