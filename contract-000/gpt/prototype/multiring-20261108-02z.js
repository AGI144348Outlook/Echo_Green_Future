// Echo-GPT 02Z independent synthetic prototype; no external effects.
// Run: node contract-000/gpt/prototype/multiring-20261108-02z.js
const seeds=[3301,3302,3303,3304];
const glyphs=[..."אבגדהוזחטיכלמנסעפצקרשת"].concat(["ך","ם","ן","ף","ץ"]);
const base=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];
const coords=Array.from({length:27},(_,i)=>[Math.floor(i/9),Math.floor(i/3)%3,i%3]);
const neighbors=i=>coords.map((p,j)=>[j,p.reduce((a,v,k)=>a+Math.abs(v-coords[i][k]),0)]).filter(x=>x[1]===1).map(x=>x[0]);
const sq=(a,b)=>a.reduce((s,v,i)=>s+(v-b[i])**2,0)/a.length;
function field(seed,opts={}){
 const {rings=2,coupling=.28,shuffle=false,reverse=false,stationary=false,zero=false}=opts;
 const weights=shuffle?[...base].reverse():base;
 const out=Array(27).fill(0);
 const radii=[];
 for(let r=0;r<rings;r++)for(let t=0;t<5;t++){
  const angle=(stationary?0:t)*(.29+.11*r)+(seed%101)*.013+(reverse?-1:1)*r*.7;
  const radius=1+.12*Math.sin(angle+r);radii.push(radius);
  const idx=(seed+7*r+3*t)%27;
  const value=zero?0:(weights[idx]/400)*Math.cos(angle)*radius*(1+coupling*Math.sin(angle+r));
  out[idx]+=value;
 }
 return {out,radii};
}
function diffuse(a,k=.24){return a.map((v,i)=>v+k*neighbors(i).reduce((s,j)=>s+a[j]-v,0));}
function oracle(seed){return coords.map(([x,y,z],i)=>.15*Math.sin(seed*.007+x*.9-y*.4+z*.6)+.07*Math.cos(i*.31));}
const report=[];
for(const seed of seeds){
 const a=field(seed),b=field(seed,{coupling:0}),s=field(seed,{shuffle:true}),tri=field(seed,{rings:3}),rev=field(seed,{reverse:true}),noop=field(seed,{zero:true});
 const target=oracle(seed);
 const intervention=Array(27).fill(0);intervention[13]=1;
 const effect=diffuse(intervention);
 const tests={
 identity:glyphs.length===27&&new Set(glyphs).size===27&&coords.length===27&&new Set(coords.map(x=>x.join(","))).size===27,
 boundary:a.radii.every(r=>r>=.88-1e-12&&r<=1.12+1e-12),
 replay:JSON.stringify(a)===JSON.stringify(field(seed)),
 noop:noop.out.every(x=>x===0),
 uncoupled:b.out.some((v,i)=>v!==a.out[i]),
 shuffle:s.out.some((v,i)=>v!==a.out[i]),
 ring_count:tri.radii.length===15&&a.radii.length===10,
 phase_reversal:rev.out.some((v,i)=>v!==a.out[i]),
 causal_local:neighbors(13).length===6&&effect.every((v,i)=>i===13||neighbors(13).includes(i)||v===0),
 prediction_finite:[a,b,s,tri].every(q=>Number.isFinite(sq(diffuse(q.out),target)))
 };
 const loss={coupled:sq(diffuse(a.out),target),uncoupled:sq(diffuse(b.out),target),shuffled:sq(diffuse(s.out),target),three_ring:sq(diffuse(tri.out),target),noop:sq(Array(27).fill(0),target)};
 report.push({seed,tests,loss,center_effect:effect[13],neighbor_effect:effect[neighbors(13)[0]]});
}
const passed=report.reduce((n,r)=>n+Object.values(r.tests).filter(Boolean).length,0);
console.log(JSON.stringify({schema:"echo-gpt-02z-v1",seeds,passed,total:40,report},null,2));
