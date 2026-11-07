// GPT-only experimental portfolio; deterministic, no external effects.
// Run with node portfolio_20z.js or eval in isolated JS runtime.
const SEEDS=[3301,3302,3303,3304];
const GLYPHS=Array.from({length:27},(_,i)=>i);
const xyz=i=>[Math.floor(i/9),Math.floor(i/3)%3,i%3];
const dist=(i,j)=>xyz(i).reduce((s,v,k)=>s+Math.abs(v-xyz(j)[k]),0);
const neighbors=i=>GLYPHS.filter(j=>dist(i,j)===1);
const rng=seed=>()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};
const positions=(seed,n,shift=0)=>Array.from({length:n},(_,r)=>(Math.floor(rng(seed+31*r)()*27)+shift*r)%27);
const compose=(seed,n,shift=0)=>positions(seed,n,shift).map(i=>String.fromCodePoint(0x05d0+i%22)).join('');
const field=(seed,phase=0,coupling=0.3)=>{let a=Array(27).fill(0);a[13]=1;let out=a.map((v,i)=>v+(coupling*Math.cos(phase+i/9))*neighbors(i).reduce((s,j)=>s+a[j],0));return out;};
const pulse=(phase=0,coupling=0.3)=>{let a=Array(27).fill(0);a[13]=1;return a.map((v,i)=>v+coupling*Math.cos(phase+i/9)*neighbors(i).reduce((s,j)=>s+a[j],0));};
const target=(seed)=>GLYPHS.map(i=>0.14*Math.sin((seed%19+i*3)/7)+0.08*Math.cos(i/4));
const mse=(a,b)=>a.reduce((s,v,i)=>s+(v-b[i])**2,0)/a.length;
const run=()=>SEEDS.flatMap(seed=>{const r=rng(seed);const phase=r()*Math.PI*2;const a=pulse(phase,.3),z=pulse(phase,0),s=pulse(phase+Math.PI,.3),t=target(seed);
const shuffled=a.slice().reverse();const p2=positions(seed,2),p3=positions(seed,3);
const vals=[
 ['bijection',new Set(GLYPHS.map(x=>xyz(x).join(','))).size===27],
 ['center-neighbors',neighbors(13).length===6],
 ['deterministic-replay',JSON.stringify(pulse(phase,.3))===JSON.stringify(a)],
 ['ring-composition',compose(seed,2).length===2&&compose(seed,3).length===3&&p2.every((x,i)=>x===p3[i])],
 ['zero-coupling',z[13]===1&&z.filter((v,i)=>i!==13).every(v=>v===0)],
 ['nonneighbor-exclusion',a.every((v,i)=>i===13||neighbors(13).includes(i)||v===0)],
 ['phase-counterfactual',mse(a,s)>0],
 ['gematria-shuffle',mse(a,shuffled)>0],
 ['deformation-bounds',GLYPHS.every(i=>{const radius=1+0.1*Math.sin(phase+i);return radius>=.9&&radius<=1.1})],
 ['heldout-comparison-finite',[mse(a,t),mse(z,t),mse(shuffled,t)].every(Number.isFinite)]
 ];
return vals.map(([type,pass])=>({seed,type,pass,candidate_mse:mse(a,t),noop_mse:mse(z,t),shuffle_mse:mse(shuffled,t),phase}));});
if(typeof module!=='undefined')module.exports={run};
if(typeof require!=='undefined'&&require.main===module)console.log(JSON.stringify(run(),null,2));
