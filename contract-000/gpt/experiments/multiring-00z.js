// GPT-only synthetic multiring experiment; no canonical Echo imports.
// Run: node contract-000/gpt/experiments/multiring-00z.js
const seeds=[11,23,37,51], N=27, R=3;
const glyphs=Array.from({length:N},(_,i)=>i); // stable identity tokens, NOT Hebrew semantics
const gem=Array.from({length:N},(_,i)=>1+(i*7)%31);
const phase=(seed,r,s)=>0.17*seed+0.39*r+0.13*s;
function simulate(seed,{kind="triad",gain=.04,shuffle=false,ablate=false,shift=0}={}){
 let x=Array.from({length:R},(_,r)=>Array.from({length:N},(_,s)=>1+((seed+r*7+s*3)%11)/10));
 const initial=x.map(a=>a.slice());
 for(let t=0;t<5;t++)for(let s=0;s<N;s++){
  const a=phase(seed,0,s)+shift,b=phase(seed,1,s)+shift,c=phase(seed,2,s)+shift;
  const affinity=(shuffle?gem[(s*11)%N]:gem[s])/32;
  let f=kind==="triad"?Math.sin(b+c-2*a):Math.sin(b-a);
  let q=gain*affinity*f*(ablate&&s===7?0:1);
  // conservative bounded transfer, no negative masses
  q=Math.max(-x[1][s]/2,Math.min(x[0][s]/2,q));
  x[0][s]-=q;x[1][s]+=q;
 }
 return {x,initial,ids:glyphs.slice()};
}
const flat=x=>x.flat(),l1=(a,b)=>a.reduce((v,z,i)=>v+Math.abs(z-b[i]),0);
const sum=x=>flat(x).reduce((a,b)=>a+b,0);
const proj=x=>Array.from({length:N},(_,s)=>x.reduce((a,r)=>a+r[s],0));
const results=[];
for(const seed of seeds){
 const base=simulate(seed), replay=simulate(seed), zero=simulate(seed,{gain:0}), shifted=simulate(seed,{shift:2.3}),pair=simulate(seed,{kind:"pair"}),shuf=simulate(seed,{shuffle:true}),abl=simulate(seed,{ablate:true});
 const tests=[
 ["replay",l1(flat(base.x),flat(replay.x))===0],
 ["identity",new Set(base.ids).size===27&&base.ids.length===27],
 ["conservation",Math.abs(sum(base.x)-sum(base.initial))<1e-9],
 ["nonnegative",flat(base.x).every(z=>z>=0)],
 ["zero_gain",l1(flat(zero.x),flat(zero.initial))===0],
 ["common_phase",l1(flat(base.x),flat(shifted.x))<1e-9],
 ["triad_vs_pair",l1(flat(base.x),flat(pair.x))>1e-8],
 ["shuffled_affinity",l1(flat(base.x),flat(shuf.x))>1e-8],
 ["local_ablation",l1(flat(base.x),flat(abl.x))>1e-8],
 ["projection",l1(proj(base.x),proj(pair.x))<1e-9]
 ];
 results.push({seed,tests:Object.fromEntries(tests),metrics:{pair_l1:l1(flat(base.x),flat(pair.x)),shuffle_l1:l1(flat(base.x),flat(shuf.x)),ablation_l1:l1(flat(base.x),flat(abl.x)),projection_l1:l1(proj(base.x),proj(pair.x)),mass_error:Math.abs(sum(base.x)-sum(base.initial))}});
}
console.log(JSON.stringify({protocol:"issue-430",results},null,2));
if(results.some(r=>Object.values(r.tests).some(v=>!v)))process.exitCode=1;
