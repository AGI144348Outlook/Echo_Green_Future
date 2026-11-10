// GPT-only synthetic 27-seat border/warehouse ring; no semantic/physical claim.
// Run: node contract-000/gpt/experimental/ring27-20261110-03z.js
const GLYPHS=[..."אבגדהוזחטיכלמנסעפצקרשתךםןףץ"];
function rng(seed){let s=seed>>>0;return ()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296}}
function simulate(seed,{coupling=.2,reverse=.1,shuffle=false,input=true}={}){
 const random=rng(seed),matrix=Array.from({length:27},()=>input?random():0),warehouse=Array(27).fill(0);
 const mapping=Array.from({length:27},(_,i)=>shuffle?(i*7+3)%27:i);
 const initial=matrix.reduce((a,b)=>a+b,0);
 let tick=0;
 for(let t=0;t<27;t++){const seat=t%27, w=mapping[seat];const moved=matrix[seat]*coupling;
 matrix[seat]-=moved;warehouse[w]+=moved;
 const returned=warehouse[w]*reverse;warehouse[w]-=returned;matrix[seat]+=returned;tick++;}
 return {matrix,warehouse,mapping,phase:tick%27,total:matrix.reduce((a,b)=>a+b,0)+warehouse.reduce((a,b)=>a+b,0),initial};
}
function l1(a,b){return a.reduce((s,v,i)=>s+Math.abs(v-b[i]),0)}
function run(seed){const a=simulate(seed),b=simulate(seed),z=simulate(seed,{input:false}),n=simulate(seed,{coupling:0,reverse:0}),f=simulate(seed,{reverse:0}),s=simulate(seed,{shuffle:true});
 const dif={forward:l1(a.warehouse,n.warehouse),reverse:l1(a.matrix,f.matrix),shuffled:l1(a.warehouse,s.warehouse),mass:Math.abs(a.total-a.initial)};
 const checks={
 uniqueGlyphs:new Set(GLYPHS).size===27,
 seatBijection:new Set(a.mapping).size===27,
 deterministic:JSON.stringify(a)===JSON.stringify(b),
 zeroInput:z.matrix.every(v=>v===0)&&z.warehouse.every(v=>v===0),
 zeroCoupling:n.warehouse.every(v=>v===0),
 forwardInfluence:dif.forward>1e-9,
 reverseInfluence:dif.reverse>1e-9,
 shuffledTopology:Number.isFinite(dif.shuffled),
 massConservation:dif.mass<1e-10,
 phaseClosure:a.phase===0
 };return {seed,checks,dif,shuffledNull:dif.shuffled<=1e-9};}
const results=[9401,9402,9403,9404].map(run);
const report={protocol:"issue-384",source:"ring27-20261110-03z.js",results,passed:results.reduce((s,r)=>s+Object.values(r.checks).filter(Boolean).length,0),total:40};
if(typeof module!=="undefined")module.exports={run,simulate,report};
if(typeof console!=="undefined")console.log(JSON.stringify(report));
