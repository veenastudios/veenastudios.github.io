(()=>{
const root=document.getElementById('root')||document.body;
const layer=document.createElement('div');layer.className='srCollageTrial';
layer.innerHTML='<a class="srCollageTop" href="https://veenastudios.in/" target="_blank" rel="noopener noreferrer" aria-label="Explore SR Gamers"><strong>♛ VEENA STUDIOS</strong><b>🎮 SR GAMERS</b><small class="srCollageCTA">EXPLORE OUR GAMES ❯</small></a><a class="srCollageBottom" href="https://veenastudios.in/" target="_blank" rel="noopener noreferrer" aria-label="Explore SR Kids"><strong>📚 SR KIDS 🚀</strong><small>LEARNING · ACTIVITIES · STORIES</small><b class="srCollageCTA">EXPLORE NOW ❯</b></a>';
document.body.appendChild(layer);
const top=layer.firstElementChild,bottom=layer.lastElementChild;
function layout(){
const art=document.querySelector('.srPremiumHome');
const home=!!art&&!document.querySelector('.worldMap,.game,.result,.srPauseOverlay,.srStoreOverlay,.srExitConfirm');
layer.style.display=home?'block':'none';if(!home)return;
const rect=art.getBoundingClientRect(),premium=document.querySelector('.srStoreButton');
const upperStart=Math.max(46,window.innerHeight*.045),upperHeight=Math.min(175,Math.max(0,rect.top-upperStart-9));
top.style.top=upperStart+'px';top.style.height=upperHeight+'px';top.style.display=upperHeight>=65?'flex':'none';
let lowerEnd=window.innerHeight-95;
if(premium&&!premium.hidden){
premium.style.top=(window.innerHeight-82)+'px';premium.style.bottom='auto';premium.style.left='50%';premium.style.right='auto';premium.style.transform='translateX(-50%)';
lowerEnd=premium.getBoundingClientRect().top-10;
}
const lowerStart=rect.bottom+9,lowerHeight=Math.min(170,Math.max(0,lowerEnd-lowerStart));
bottom.style.top=lowerStart+'px';bottom.style.height=lowerHeight+'px';bottom.style.display=lowerHeight>=65?'flex':'none';
}
new MutationObserver(()=>requestAnimationFrame(layout)).observe(root,{childList:true,subtree:true});
window.addEventListener('resize',layout);window.addEventListener('orientationchange',layout);
document.addEventListener('load',layout,true);requestAnimationFrame(layout);
})();