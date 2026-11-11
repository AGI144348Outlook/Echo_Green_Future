// GPT-only synthetic 27-seat multi-ring control family; prospective Issue #408.
// Run: node multiring-causal-20261111-02z.js (or isolated JS evaluator).
const SEEDS=[11,23,37,53], N=27, STEPS=16;
function rng(seed){let x=seed>>>0;return ()=>{x=(Math.imul(1664525,x)+1013904223)>>>0;return x/4294967296;};}
function run(seed,options={}){
 const {rings=3,gain=.14,uncoupled=false,common=0,relative=0,freqScale=1,boundary=true,shuffle=false}=options;
 const random=rng(seed), m=Array.from({length:N},()=>.5+random()), phase=Array.from({length:N},()=>random()*6.283185307179586);
 const frequency=Array.from({length:N},()=>.02+.06*random());
 const affinity=Array.from({length:N},(_,i)=>i+1);
 if(shuffle){const rr=rng(seed+991);for(let i=N-1;i>0;i--){let j=Math.floor(rr()*(i+1));[affinity[i],affinity[j]]=[affinity[j],affinity[i]];}}
 const initial=m.slice(), total=initial.reduce((a,b)=>a+b,0);
 let min=Math.min(...m), maxErr=0;
 for(let t=0;t<STEPS;t++){
  for(let i=0;i<N;i++)phase[i]+=frequency[i]*freqScale;
  if(!uncoupled&&gain!==0){
   // One conservative simultaneous pair transfer per seat; common phase cancels.
   const delta=Array(N).fill(0);
   for(let i=0;i<N;i++){
    const j=(i+1)%N;
    const pi=phase[i]+common+(i===0?relative:0),pj=phase[j]+common+(j===0?relative:0);
    const affinityFactor=.65+.35*Math.cos((affinity[i]-affinity[j])*.07);
    const gate=boundary?(.5+.5*Math.sin((t+i)*.17)**2):1;
    const factor=gain*affinityFactor*gate*(.5+.5*Math.cos(pi-pj));
    const flow=factor*(m[i]-m[j]);
    delta[i]-=flow;delta[j]+=flow;
   }
   for(let i=0;i<N;i++)m[i]+=delta[i];
  }
  min=Math.min(min,...m);maxErr=Math.max(maxErr,Math.abs(m.reduce((a,b)=>a+b,0)-total));
 }
 return {m,initial,total,min,maxErr,rings,phase};
}
const l1=(a,b)=>a.reduce((s,v,i)=>s+Math.abs(v-b[i]),0);
const rows=[];
for(const seed of SEEDS){
 const base=run(seed),repeat=run(seed),noop=run(seed,{gain:0}),uncoupled=run(seed,{uncoupled:true});
 const global=run(seed,{common:1.4}),relative=run(seed,{relative:1.4}),freq=run(seed,{freqScale:1.7}),boundary=run(seed,{boundary:false}),shuffle=run(seed,{shuffle:true});
 const checks={
  T1_conservation:base.maxErr<1e-9,
  T2_nonnegative:base.min>=-1e-12,
  T3_replay:l1(base.m,repeat.m)===0,
  T4_zero_gain:l1(noop.m,noop.initial)===0,
  T5_uncoupled:l1(uncoupled.m,uncoupled.initial)===0,
  T6_common_phase_null:l1(base.m,global.m)<1e-9,
  T7_relative_phase:l1(base.m,relative.m)>1e-8,
  T8_frequency:l1(base.m,freq.m)>1e-8,
  T9_boundary:l1(base.m,boundary.m)>1e-8,
  T10_shuffle:l1(base.m,shuffle.m)>1e-8
 };
 rows.push({seed,checks,metrics:{massError:base.maxErr,common:l1(base.m,global.m),relative:l1(base.m,relative.m),frequency:l1(base.m,freq.m),boundary:l1(base.m,boundary.m),shuffle:l1(base.m,shuffle.m)}});
}
const report={protocol:"https://github.com/AGI144348Outlook/Echo_Green_Future/issues/408",seeds:SEEDS,steps:STEPS,seats:N,rows,passed:rows.reduce((s,r)=>s+Object.values(r.checks).filter(Boolean).length,0),total:SEEDS.length*10,limitations:["rings option is metadata; no genuine two-versus-three-ring comparison","no independent outcome or semantic oracle","synthetic affine routing; shuffled assignments are one seeded permutation per seed","identity labels fixed by array index"]};
console.log(JSON.stringify(report,null,2));
