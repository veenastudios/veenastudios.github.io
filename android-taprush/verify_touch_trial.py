from pathlib import Path
import re, subprocess
root=Path("app/src/main/assets")
js=(root/"assets/index-B_be548G.js").read_text()
html=(root/"index.html").read_text()
assert ".game.jungleGame .target::after" in html
assert "touch-action:none" in html
assert ".game:has(.srPauseOverlay) .target::after{pointer-events:none!important}" in html
m=re.search(r'onPointerDown:(L=>\{if\(L.button!==0.*?F\(z,L\),dl\(z\)\})',js)
assert m,"Patched handler missing"
code='''let effects=0,scores=0;const z={};const F=()=>effects++,dl=()=>scores++;const handler='''+m.group(1)+''';
const nodes=Array.from({length:100},()=>({dataset:{}}));
for(const node of nodes){const e={button:0,currentTarget:node,preventDefault(){}};handler(e);handler(e);}
handler({button:2,currentTarget:{dataset:{}},preventDefault(){}});
if(scores!==100||effects!==100)throw Error("Touch guard failed");
console.log("PASS: 100 distinct targets, duplicate and secondary button rejection");
'''
subprocess.run(["node","-e",code],check=True)
