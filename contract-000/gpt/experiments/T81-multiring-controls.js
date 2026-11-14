// GPT-only T81 bounded offline synthetic experiment; no external effects.
// Execute runT81() in a JavaScript runtime; fixed seeds and no network.
function runT81(){
 const seeds=[7,19,43,101], rows=[];
 const glyphs=Array.from({length:27},(_,i)=>"g"+String(i).padStart(2,"0"));
 function step(seed){return (Math.imul(seed,1664525)+1013904223)>>>0}
 function phase(seed){return (step(seed)%100000)/100000*2*Math.PI}
 function couple(a,b,w){return a+w*Math.sin(b-a)}
 function record(type,seed,pass,observation){rows.push({type,seed,pass,observation})}
 for(const seed of seeds){
  const a=step(seed)%27,b=step(a+seed)%27,c=step(b+seed)%27,d=step(c+seed)%27;
  record("01 unique glyph IDs",seed,new Set(glyphs).size===27,{count:new Set(glyphs).size});
  const coords=glyphs.map((_,i)=>[Math.floor(i/9),Math.floor(i/3)%3,i%3].join(":"));
  record("02 3x3x3 bijection",seed,new Set(coords).size===27&&coords.every(x=>x.split(":").every(n=>Number(n)<3)),{count:new Set(coords).size});
  const two=[glyphs[a],glyphs[b]].join("|");
  record("03 ordered 2-ring",seed,two===`${glyphs[a]}|${glyphs[b]}`,{two});
  const three=[glyphs[a],glyphs[b],glyphs[c]].join("|");
  record("04 ordered 3-ring",seed,three.split("|").length===3&&three.split("|")[0]===glyphs[a],{three});
  const four=[glyphs[a],glyphs[b],glyphs[c],glyphs[d]].join("|");
  record("05 ordered 4-ring",seed,four.split("|").length===4&&four.split("|")[3]===glyphs[d],{four});
  const p=phase(seed),q=phase(seed+1);
  record("06 no-op",seed,Object.is(couple(p,q,0),p),{delta:couple(p,q,0)-p});
  const uncoupled=couple(p,q,0);
  record("07 uncoupled sham",seed,uncoupled===p,{delta:uncoupled-p});
  const coupled=couple(p,q,0.2),delta=coupled-p;
  record("08 phase coupling",seed,Math.abs(delta)>1e-12,{delta});
  const affinity=((a+1)*(b+3)%17)/17,shuffled=((b+1)*(a+3)%17)/17;
  const effect=couple(p,q,0.2*affinity)-couple(p,q,0.2*shuffled);
  record("09 shuffled affinity",seed,Number.isFinite(effect),{effect,affinity,shuffled});
  const radius=1+0.1*Math.sin(p), bounded=radius>=0.9-1e-12&&radius<=1.1+1e-12;
  record("10 deformable boundary",seed,bounded,{radius});
 }
 return {seeds,types:10,checks:rows.length,passed:rows.filter(x=>x.pass).length,rows,limitations:"Synthetic deterministic structural and numerical checks only; no semantic or causal learning claims."}
}
