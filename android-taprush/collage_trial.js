(()=>{
const root=document.getElementById('root')||document.body;
// Deliberately no install-referral coins: native share is not proof of installation.
const layer=document.createElement('div');layer.className='srCollageTrial';
layer.innerHTML='<a class="srCollageTop" href="https://veenastudios.in/" target="_blank" rel="noopener noreferrer" aria-label="Explore SR Gamers"><strong>♛ VEENA STUDIOS</strong><b>🎮 SR GAMERS</b><small class="srCollageCTA">EXPLORE OUR GAMES ❯</small></a><a class="srCollageBottom" href="https://veenastudios.in/" target="_blank" rel="noopener noreferrer" aria-label="Explore SR Kids"><strong>📚 SR KIDS 🚀</strong><small>LEARNING · ACTIVITIES · STORIES</small><b class="srCollageCTA">EXPLORE NOW ❯</b></a>';
document.body.appendChild(layer);
const shareButton=document.createElement('button');
shareButton.className='srCollageShare';shareButton.type='button';shareButton.textContent='↗ SHARE GAME';
shareButton.setAttribute('aria-label','Share Tap Rush');
shareButton.addEventListener('click',async()=>{
 const url='https://veenastudios.in/tap-rush/';
 const data={title:'Tap Rush — SR GAMERS',text:'Play Tap Rush by Veena Studios!',url};
 try{
  if(navigator.share){await navigator.share(data);return}
  if(navigator.clipboard&&navigator.clipboard.writeText){await navigator.clipboard.writeText(url);window.alert('Game link copied');return}
  window.prompt('Copy Tap Rush link',url)
 }catch(err){if(err&&err.name!=='AbortError')window.prompt('Copy Tap Rush link',url)}
});
layer.appendChild(shareButton);
const top=layer.querySelector('.srCollageTop'),bottom=layer.querySelector('.srCollageBottom');
// Task 2: only hide the accessible text once the actual image decodes successfully.
for(const [element,file] of [[top,'sr_gamers_banner.webp'],[bottom,'sr_kids_banner.webp']]){
 const img=new Image();img.onload=()=>{if(img.naturalWidth>0)element.classList.add('hasArtwork')};
 img.onerror=()=>element.classList.remove('hasArtwork');img.src='./'+file;
}

function layout(){
const art=document.querySelector('.srPremiumHome');
const home=!!art&&!document.querySelector('.worldMap,.game,.result,.srPauseOverlay,.srStoreOverlay,.srExitConfirm');
layer.style.display=home?'block':'none';if(!home)return;
const rect=art.getBoundingClientRect(),premium=document.querySelector('.srStoreButton');
const upperStart=Math.max(46,window.innerHeight*.045),upperHeight=Math.min(175,Math.max(0,rect.top-upperStart-9));
top.style.top=upperStart+'px';top.style.height=upperHeight+'px';top.style.display=upperHeight>=65?'flex':'none';
shareButton.style.display='block';
const lowerStart=rect.bottom+8;
const bottomLimit=window.innerHeight-94;
const lowerHeight=Math.max(0,Math.min(158,bottomLimit-lowerStart-8));
bottom.style.top=lowerStart+'px';bottom.style.height=lowerHeight+'px';
bottom.style.display=lowerHeight>=58?'flex':'none';
// Banner artwork remains separate from the approved game image.
// When the available space is too short, hide banners instead of covering game controls.
if(premium&&!premium.hidden){
 premium.style.setProperty('top',(window.innerHeight-77)+'px','important');premium.style.setProperty('bottom','auto','important');
 premium.style.setProperty('left','4%','important');premium.style.setProperty('right','auto','important');premium.style.setProperty('transform','none','important');
 premium.style.setProperty('width','44%','important');premium.style.setProperty('height','59px','important');
 premium.style.setProperty('font-size','clamp(13px,3.5vw,21px)','important');
}
shareButton.style.top=(window.innerHeight-77)+'px';shareButton.style.left='52%';shareButton.style.right='4%';shareButton.style.width='44%';shareButton.style.height='59px';
}
new MutationObserver(()=>requestAnimationFrame(layout)).observe(root,{childList:true,subtree:true});
window.addEventListener('resize',layout);window.addEventListener('orientationchange',layout);
document.addEventListener('load',layout,true);requestAnimationFrame(layout);
})();