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
 elif path.startswith("/"):
  missing.append((origin,raw,"unsupported site-root asset"))
  return
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
# Validate all required sources before replacing a previously generated bundle.
hub=Path(__file__).resolve().parent/"game-hub.html"
if not hub.is_file():
 print("FAIL: game hub missing:",hub)
 sys.exit(1)
if not (src/"index.html").is_file():
 print("FAIL: game entrypoint missing:",src/"index.html")
 sys.exit(1)
if dst.exists():shutil.rmtree(dst)
shutil.copytree(src,dst)
shutil.copy2(site_source,dst/site_image)
# Ship the approved-structure SR GAMERS hub in the offline APK.
shutil.copy2(hub,dst/"game-hub.html")
# Attach navigation only to the game's existing home shelf; never overlay active rounds.
home_css="""<style id="taprush-mobile-home-fix">
.hub .premiumHome{object-fit:contain!important;object-position:center center!important;background:#07111f}
.hub .liveShelf{left:0!important;right:0!important;bottom:0!important;top:0!important;pointer-events:none!important}
.hub .liveShelf h2{display:none!important}
.hub .liveShelf .gameCard{position:absolute!important;left:0!important;top:53%!important;width:34%!important;height:10%!important;min-height:44px!important;opacity:0!important;border:0!important;padding:0!important;pointer-events:auto!important;z-index:6!important}
.srGamesPanel{position:fixed;z-index:35;display:flex;flex-direction:column;justify-content:center;gap:5px;padding:8px 9px;background:linear-gradient(180deg,#06152dfb,#091a2ffb);border-top:2px solid #d8b15b;border-bottom:2px solid #d8b15b;box-shadow:0 0 15px #020812dd;color:#fff;overflow:hidden}
.srGamesPanel h2{font:900 clamp(13px,3.6vw,19px) system-ui;margin:0 0 3px;color:#ffdb74;letter-spacing:.5px}
.srGamesGrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:4px}
.srGamesGrid button{min-width:0;min-height:48px;border:1px solid #746c5c;border-radius:9px;background:linear-gradient(#183b43,#071a2c);color:white;padding:5px 2px;font:800 clamp(8px,2vw,11px) system-ui;display:flex;flex-direction:column;align-items:center;justify-content:space-around;gap:3px}
#srNeverUsed{display:none}.srGamesGrid button.more{border-color:#00dfff;background:linear-gradient(#203c72,#160d42)}\n.srGamesGrid button.ready{border-color:#ffd35e;background:linear-gradient(#486b30,#123b25)}
.srGamesGrid button:disabled{opacity:1;color:#e7dce4}
.srGamesGrid .status{color:#ffd966;font-size:clamp(8px,2vw,11px)}

.worldMap{background:linear-gradient(#05251b70,#071d1e99),url(/tap-rush/jungle-scene.webp) center/cover!important}\n.worldMap .mapIntro,.worldMap .mapNote{color:#e1f3e8!important;text-shadow:0 1px 3px #001!important}\n.srPauseButton{position:absolute;z-index:40;top:calc(env(safe-area-inset-top) + 102px);right:12px;padding:10px 14px;border:2px solid #ffe19a;border-radius:16px;background:#142a36;color:white;font-weight:900}.srPauseOverlay{position:absolute;z-index:39;inset:0;display:grid;place-items:center;background:#020c1cbb;backdrop-filter:blur(4px)}.srPauseOverlay>div{text-align:center;background:#12312b;border:2px solid #f8d985;border-radius:24px;padding:32px}.srPauseOverlay button{background:#ffd65a;border:0;border-radius:12px;padding:13px 22px;font-weight:900}.game:has(.srPauseOverlay) .target{animation-play-state:paused!important;pointer-events:none!important}\n.worldMap{position:relative!important;background:#061b1b!important;overflow:hidden!important}
.worldMap::before{content:"";position:absolute;inset:0;background:url('/tap-rush/approved-world-selection.webp') center center/contain no-repeat;pointer-events:none}
.worldMap .mapTop,.worldMap .mapIntro,.worldMap .mapNote{opacity:0!important;pointer-events:none!important}
.worldMap .worldTrail::before{content:none!important;display:none!important}
.worldMap .worldTrail:before,.worldMap .worldTrail::after{content:none!important;display:none!important;background:none!important}
.worldMap .worldTrail{background-image:none!important}
.worldMap .worldTrail{position:absolute!important;inset:0!important;display:block!important;margin:0!important;padding:0!important;z-index:3!important;pointer-events:none!important}
.worldMap .worldNode{position:absolute!important;left:7%!important;width:86%!important;height:11%!important;min-height:0!important;opacity:0!important;pointer-events:auto!important;border:0!important}
.worldMap .worldNode:nth-child(1){top:20%!important}
.worldMap .worldNode:nth-child(2){top:33%!important}
.worldMap .worldNode:nth-child(3){top:46%!important}
.worldMap .worldNode:nth-child(4){top:59%!important}
.worldMap .worldNode:nth-child(5){top:72%!important}
.worldMap .worldNode{opacity:1!important;background:transparent!important;color:transparent!important;font-size:0!important;box-shadow:none!important}
.worldMap .worldNode>*{visibility:hidden!important}
.worldMap .worldNode:not(:first-child):not(.srUnlocked)::after{content:attr(data-lock-price) " COINS 🔒";position:absolute;right:31%;top:33%;width:23%;height:36%;display:flex;align-items:center;justify-content:center;border:2px solid #ffe18b;border-radius:18px;background:linear-gradient(130deg,#101f35,#30425a);box-shadow:0 2px 9px #000b;color:#ffe18b;font:900 clamp(11px,3vw,20px) system-ui;z-index:5;pointer-events:none}
.srRewardAd{display:block;margin:12px auto;padding:12px 18px;border-radius:16px;border:2px solid #f4ce63;background:#122f40;color:#ffdf7b;font:900 15px system-ui;max-width:92%}\n.worldMap .mapTop button{position:absolute!important;top:5%!important;left:5%!important;opacity:0!important;pointer-events:auto!important;z-index:4!important;width:16%!important;height:9%!important}
 .srWorldLockNotice{position:fixed;z-index:100;left:7%;right:7%;bottom:12%;padding:20px;background:#071b2ff5;color:#ffe68b;border:2px solid #f9d86b;border-radius:15px;text-align:center;font:bold 18px system-ui;pointer-events:none}\n</style>"""
# Approved world-selection art is mandatory: fail rather than ship a substitute.
world_art=Path(__file__).resolve().parent/"approved-world-selection.webp"
if not world_art.is_file():
 print("FAIL: exact approved world-selection image not yet in Android source:",world_art)
 sys.exit(1)
shutil.copy2(world_art,dst/"approved-world-selection.webp")
home_art=Path(__file__).resolve().parent/"file_0000000004d88208849588bc009b398c.png"
if not home_art.is_file():
 print("FAIL: approved carousel home image not yet uploaded:",home_art)
 sys.exit(1)
shutil.copy2(home_art,dst/"approved-home-carousel.png")
entry=dst/"index.html"
markup=entry.read_text(encoding="utf-8")
launcher_js="""<style id="sr-premium-home">
.hub:has(.premiumHome){background:#061526 url('/tap-rush/approved-home-carousel.png') center center/cover no-repeat!important}
.hub:has(.premiumHome) .language,.hub:has(.premiumHome) .coinBox,.hub:has(.premiumHome) .gear,.hub:has(.premiumHome) .collectionNote{opacity:0!important;pointer-events:none!important}
.hub:has(.premiumHome) .premiumHome{opacity:0!important}
.hub:has(.premiumHome) .liveShelf{opacity:0!important;pointer-events:none!important}
body:has(.srPremiumHome)::before{content:'';position:fixed;inset:-24px;z-index:19;pointer-events:none;background:linear-gradient(#06152677,#06152699),url('/tap-rush/approved-home-carousel.png') center center/cover no-repeat;filter:blur(19px);transform:scale(1.06)}
.srPremiumHome{position:fixed;z-index:30;background:#061526 url('/tap-rush/approved-home-carousel.png') center/100% 100% no-repeat;overflow:hidden}
.srPremiumHome .srCoinValue{position:absolute;left:82.1%;top:1.05%;width:5.8%;height:3.3%;display:flex;align-items:center;justify-content:center;background:#07111e;color:#fff;font:900 clamp(12px,3.6vw,22px) system-ui;line-height:1;border-radius:5px;text-shadow:0 1px 2px #000;pointer-events:none}
.srPremiumHome button{position:absolute;background:transparent;border:0;color:transparent;font-size:0;cursor:pointer;touch-action:manipulation}
.srPremiumHome button:focus-visible{outline:3px solid #ffe078;outline-offset:-3px}
.srPremiumHome .srHomePlay{left:29%;top:46%;width:43%;height:13%}
.srPremiumHome .srHomeSettings{left:89%;top:0;width:11%;height:7%}
.srPremiumHome .srHomeCoins{left:76%;top:0;width:13%;height:7%}
.srPremiumHome .srCarouselPrev{left:0;top:67%;width:10%;height:12%}
.srPremiumHome .srCarouselNext{right:0;top:67%;width:10%;height:12%}
.srPremiumHome .srCarouselPrev:disabled,.srPremiumHome .srCarouselNext:disabled{pointer-events:none}
</style><script>(function(){
const home=document.createElement('section');home.className='srPremiumHome';home.setAttribute('aria-label','Tap Rush premium home');
home.innerHTML='<button class="srHomePlay" aria-label="Play Tap Rush">Play</button><button class="srHomeSettings" aria-label="Settings">Settings</button><button class="srHomeCoins" aria-label="Coins">Coins</button><span class="srCoinValue" aria-label="Coin balance">0</span><button class="srCarouselPrev" aria-label="Previous games" disabled>Previous</button><button class="srCarouselNext" aria-label="Next games" disabled>Next</button>';
home.querySelector('.srHomePlay').onclick=()=>document.querySelector('.liveShelf .gameCard')?.click();
home.querySelector('.srHomeSettings').onclick=()=>document.querySelector('.hub .gear')?.click();
home.querySelector('.srHomeCoins').onclick=()=>document.querySelector('.hub .coinBox')?.click();
const titles=['Jungle Friends Quiz','Math Challenge','Flags & Capitals'];let page=0;
function updateCarousel(){const pages=Math.ceil(titles.length/3);home.querySelector('.srCarouselPrev').disabled=page===0;home.querySelector('.srCarouselNext').disabled=page>=pages-1}
home.querySelector('.srCarouselPrev').onclick=()=>{page=Math.max(0,page-1);updateCarousel()};
home.querySelector('.srCarouselNext').onclick=()=>{page=Math.min(Math.ceil(titles.length/3)-1,page+1);updateCarousel()};
function position(){const coin=document.querySelector('.hub .coinBox'),display=home.querySelector('.srCoinValue');if(coin&&display){const match=(coin.textContent||'').match(/\d[\d,]*/);if(match&&display.textContent!==match[0])display.textContent=match[0]}const img=document.querySelector('.hub .premiumHome'),shelf=document.querySelector('.hub .liveShelf');if(!img||!shelf){home.remove();return}if(!document.body.contains(home))document.body.appendChild(home);const r=img.getBoundingClientRect(),nw=img.naturalWidth||1024,nh=img.naturalHeight||1536,scale=Math.min(r.width/nw,r.height/nh);const w=nw*scale,h=nh*scale;home.style.left=(r.left+(r.width-w)/2)+'px';home.style.top=(r.top+(r.height-h)/2)+'px';home.style.width=w+'px';home.style.height=h+'px';updateCarousel()}
// The Android WebView default confirm() exposes an internal URL and clashes with game styling.
window.srConfirmUnlock=(name,cost)=>new Promise(resolve=>{
 const overlay=document.createElement('div');
 overlay.setAttribute('role','dialog');overlay.setAttribute('aria-modal','true');
 overlay.setAttribute('aria-label','Unlock '+name);
 overlay.style.cssText='position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;background:#010b19bb;padding:22px';
 const panel=document.createElement('div');
 panel.style.cssText='width:min(100%,420px);border:3px solid #f5d47b;border-radius:24px;background:linear-gradient(160deg,#183d37,#071c2c);color:#ffe7a1;box-shadow:0 14px 40px #000a;padding:25px 20px;text-align:center;font:700 18px system-ui';
 const heading=document.createElement('h2');heading.textContent='Unlock '+name+'?';heading.style.cssText='font:900 25px system-ui;margin:0 0 12px';
 const message=document.createElement('p');message.textContent='Unlock permanently for '+cost+' coins?';message.style.cssText='margin:0 0 24px;font:600 16px system-ui';
 const actions=document.createElement('div');actions.style.cssText='display:flex;gap:12px';
 const finish=value=>{document.removeEventListener('keydown',escape);overlay.remove();resolve(value)};
 const escape=e=>{if(e.key==='Escape'){e.preventDefault();finish(false)}};
 for(const [label,value] of [['CANCEL',false],['UNLOCK',true]]){
  const button=document.createElement('button');button.textContent=label;button.style.cssText='flex:1;padding:14px 8px;border:2px solid #ffe39a;border-radius:13px;background:'+(value?'#f6bf42':'#203c45')+';color:'+(value?'#1c1a0b':'#fff')+';font:900 16px system-ui';button.onclick=()=>finish(value);actions.appendChild(button);
 }
 panel.append(heading,message,actions);overlay.appendChild(panel);document.body.appendChild(overlay);
 document.addEventListener('keydown',escape);actions.querySelector('button').focus();
});
// Capture-phase safety guard: no locked world can start without enough coins.
const worldPrices=[0,150,200,250,350],worldNames=['Jungle','City','Space','Underwater','Rock & Himalaya'];
document.addEventListener('click',function(e){
 const button=e.target.closest('.worldMap .worldNode');
 if(!button)return;
 const nodes=Array.from(document.querySelectorAll('.worldMap .worldNode'));
 const idx=nodes.indexOf(button),price=worldPrices[idx];
 if(idx<1||!price)return;
 const key='srWorldUnlocked_'+['jungle','city','space','underwater','himalaya'][idx];
 const already=Object.keys(localStorage).some(k=>k.endsWith(key)&&localStorage.getItem(k)==='yes');
 if(already)return;
 const coinKey=Object.keys(localStorage).find(k=>k.endsWith('srCoins'));
 const coins=Number(coinKey?localStorage.getItem(coinKey):0)||0;
 if(coins>=price)return; // React handler owns confirmed purchases and deductions.
 e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();
 let notice=document.querySelector('.srWorldLockNotice');
 if(!notice){notice=document.createElement('div');notice.className='srWorldLockNotice';notice.setAttribute('role','alert');document.body.appendChild(notice)}
 notice.textContent='🔒 '+worldNames[idx]+' requires '+price+' Coins. Available: '+coins;
 notice.style.display='block';
 clearTimeout(window.srWorldLockTimer);
 window.srWorldLockTimer=setTimeout(()=>{notice.style.display='none'},800);
},true);
new MutationObserver(()=>{const notice=document.querySelector('.srWorldLockNotice');if(notice&&!document.querySelector('.worldMap'))notice.style.display='none'}).observe(document.getElementById('root')||document.body,{childList:true,subtree:true});
function syncWorldLocks(){
 const nodes=document.querySelectorAll('.worldMap .worldNode');
 const names=['jungle','city','space','underwater','himalaya'],prices=[0,150,200,250,350];
 nodes.forEach((node,i)=>{
  if(i>=names.length)return;
  node.dataset.lockPrice=String(prices[i]);
  const unlocked=i===0||Object.keys(localStorage).some(k=>k.endsWith('srWorldUnlocked_'+names[i])&&localStorage.getItem(k)==='yes');
  node.classList.toggle('srUnlocked',unlocked);
  node.setAttribute('aria-label',unlocked?names[i]+' Play':names[i]+' locked. '+prices[i]+' coins to unlock');
 });
}
new MutationObserver(syncWorldLocks).observe(document.getElementById('root')||document.body,{childList:true,subtree:true});
syncWorldLocks();
new MutationObserver(position).observe(document.getElementById('root')||document.body,{childList:true,subtree:true});window.addEventListener('resize',position);window.addEventListener('orientationchange',position);document.addEventListener('load',position,true);position();
})();</script>"""
if "</body>" not in markup:
 print("FAIL: no body tag for home shelf launcher")
 sys.exit(1)
entry.write_text(markup.replace("</head>",home_css+"</head>").replace("</body>",launcher_js+"</body>"),encoding="utf-8")
world_patch_count=0
for js in (dst/"assets").glob("*.js"):
 s=js.read_text(encoding="utf-8")
 s=s.replace("https://veenastudios.in/"+site_image+"?v=2","/tap-rush/"+site_image)
 # Apply coin-based permanent world locks to the offline Android bundle only.
 # React owns both the coin balance and world selection, preventing stale UI after spending.
 if 'disabled:!L.ready,onClick:L.ready?()=>' in s:
  old='disabled:!L.ready,onClick:L.ready?()=>{const $=L.id;Ol($),Ll(Number(localStorage.getItem(Ta(vd($)))||0)),B()}:void 0'
  new='disabled:!L.ready,onClick:async()=>{const $=L.id,prices={city:150,space:200,underwater:250,himalaya:350},cost=prices[$]||0,key=Ta("srWorldUnlocked_"+$);if(cost&&localStorage.getItem(key)!=="yes"){const stored=Number(localStorage.getItem(Ta("srCoins"))||0);const available=Number.isFinite(stored)?Math.max(0,Math.floor(stored)):0;if(available<cost){window.alert(L.name+" unlock: "+cost+" coins. You have "+available+" coins.");return}if(!await window.srConfirmUnlock(L.name,cost))return;if(localStorage.getItem(key)==="yes")return;const latest=Number(localStorage.getItem(Ta("srCoins"))||0);if(!Number.isSafeInteger(latest)||latest<cost){window.alert("Coin balance changed. Please try again.");return}const remaining=latest-cost;localStorage.setItem(key,"yes");localStorage.setItem(Ta("srCoins"),String(remaining));ct(remaining)}Ol($),Ll(Number(localStorage.getItem(Ta(vd($)))||0)),B()}'
  if old not in s:
   print("FAIL: world click anchor not found");sys.exit(1)
  s=s.replace(old,new,1)
  s=s.replace('children:L.ready?"PLAY ▶":"SOON"','children:L.id==="jungle"||localStorage.getItem(Ta("srWorldUnlocked_"+L.id))==="yes"?"PLAY ▶":({city:150,space:200,underwater:250,himalaya:350}[L.id]+" COINS 🔒")',1)
  s=s.replace('children:L.ready?L.mark:"🔒"','children:L.id==="jungle"||localStorage.getItem(Ta("srWorldUnlocked_"+L.id))==="yes"?L.mark:"🔒"',1)
  world_patch_count+=1
  print("Applied world coin unlocks: 150 / 200 / 250 / 350")
 # Reward coins are granted only after the native AdMob rewarded callback.
 if 'const[Y,S]=El.useState(0)' in s:
  # Local one-time welcome bonus and one daily bonus. Never reward store ratings/reviews.
  bonus_effect='El.useEffect(()=>{const day=new Date().toLocaleDateString("en-CA");const welcome=Ta("srWelcome50"),daily=Ta("srDaily10");let bonus=0;if(localStorage.getItem(welcome)!=="yes"){localStorage.setItem(welcome,"yes");bonus+=50}if(localStorage.getItem(daily)!==day){localStorage.setItem(daily,day);bonus+=10}if(bonus){ct(prev=>{const next=prev+bonus;localStorage.setItem(Ta("srCoins"),String(next));return next});window.dispatchEvent(new CustomEvent("srLoginBonus",{detail:{coins:bonus}}))}},[]);'
  state_anchor='[Rl,wt]=El.useState(()=>localStorage.getItem(Ta("srSound"))!=="off");'
  state_new=state_anchor+bonus_effect+'El.useEffect(()=>{const onReward=()=>{ct(prev=>{const next=prev+20;localStorage.setItem(Ta("srCoins"),String(next));return next})};const onUnavailable=()=>{window.alert("Rewarded ad is unavailable. Please try again later. No coins deducted.")};window.addEventListener("srReward20",onReward);window.addEventListener("srAdUnavailable",onUnavailable);return()=>{window.removeEventListener("srReward20",onReward);window.removeEventListener("srAdUnavailable",onUnavailable)}},[]);'
  result_anchor='O.jsx("button",{className:"resultPlay",onClick:B,children:"▶ PLAY AGAIN"})'
  result_new='(window.TapRushAds?O.jsx("button",{className:"srRewardAd",onClick:()=>window.TapRushAds.showRewarded(),children:"▶ WATCH AD · +20 COINS (OPTIONAL)"}):null),'+result_anchor
  for old,new in ((state_anchor,state_new),(result_anchor,result_new)):
   if s.count(old)!=1:
    print("FAIL: rewarded ad integration anchor missing",old,s.count(old));sys.exit(1)
   s=s.replace(old,new,1)
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

if world_patch_count!=1:
 print("FAIL: expected exactly one world-map JS bundle, got",world_patch_count)
 sys.exit(1)
