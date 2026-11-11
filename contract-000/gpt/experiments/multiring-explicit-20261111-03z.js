// GPT-owned synthetic multiring controls, preregistered Issue #409; Node >=18.
// 27 distinct seat IDs per ring; no Hebrew semantic inference.
const SEEDS=[11,23,37,53], N=27, STEPS=16, TAU=2*Math.PI;
function rng(seed){let x=seed>>>0;return ()=>((x=(Math.imul(x,1664525)+1013904223)>>>0)/4294967296);}
function init(seed,rings){
 const rand=rng(seed), base=Array.from({length:N},()=>0.2+rand());
 const phases=Array.from({length:N},()=>TAU*rand());
 // same base per-seat mass for every ring, divided by ring count to match TOTAL mass.
 return {rings:Array.from({length:rings},(_,r)=>({id:r,m:base.map(x=>x/rings),p:phases.slice()})),
 baseMass:base.reduce((a,b)=>a+b,0)};
}
function run(seed,opt={}){
 const rings=opt.rings||2, state=init(seed,rings), initial=state.rings.map(z=>z.m.slice());
 const gain=opt.gain===undefined?0.035:opt.gain, freq=opt.freq===undefined?0.17:opt.freq;
 const rel=opt.rel||0, common=opt.common||0, boundary=opt.boundary!==false, coupled=opt.coupled!==false;
 const perm=opt.shuffle?Array.from({length:N},(_,i)=>(i*11+7)%N):Array.from({length:N},(_,i)=>i);
 const ids=state.rings.map(z=>Array.from({length:N},(_,i)=>'g'+String(i).padStart(2,'0')));
 for(let t=0;t<STEPS;t++){
   // deterministic phase evolution, including uncoupled control.
   state.rings.forEach((z,r)=>z.p.forEach((p,i)=>{z.p[i]=p+freq*(1+0.01*i)+common+(r===1?rel:0);}));
   if(!coupled||gain===0)continue;
   // intra-ring conservative adjacent-seat transfers.
   for(const z of state.rings){
     for(let i=0;i<N;i++){let j=(i+1)%N;
       let d=(z.m[i]-z.m[j])*gain*0.15*(1+0.2*Math.cos(z.p[i]-z.p[j]));
       z.m[i]-=d;z.m[j]+=d;
     }
   }
   // cross-ring conservative transfer: 2-ring and 3-ring topologies differ genuinely.
   for(let r=0;r<rings;r++){
     const a=state.rings[r], b=state.rings[(r+1)%rings];
     for(let i=0;i<N;i++){
       let j=perm[i], gate=boundary?(0.6+0.4*Math.sin((t+i+r)*0.27)**2):1;
       let phase=1+0.3*Math.cos(a.p[i]-b.p[j]);
       let d=(a.m[i]-b.m[j])*gain*gate*phase;
       a.m[i]-=d;b.m[j]+=d;
     }
   }
 }
 const projected=Array.from({length:N},(_,i)=>state.rings.reduce((s,z)=>s+z.m[i],0));
 return {rings, projected, mass:state.rings.reduce((s,z)=>s+z.m.reduce((a,b)=>a+b,0),0), initialMass:state.baseMass,
 min:Math.min(...state.rings.flatMap(z=>z.m)),ids,initial,final:state.rings.map(z=>z.m)};
}
const l1=(a,b)=>a.reduce((s,x,i)=>s+Math.abs(x-b[i]),0);
const results=[];
for(const seed of SEEDS){
 const base=run(seed), replay=run(seed), zero=run(seed,{gain:0}), unc=run(seed,{coupled:false});
 const shift=run(seed,{common:0.5}), rel=run(seed,{rel:0.4}), freq=run(seed,{freq:0.23});
 const gate=run(seed,{boundary:false}), three=run(seed,{rings:3}), shuffle=run(seed,{shuffle:true});
 const tests={
  T1_mass:Math.abs(base.mass-base.initialMass)<1e-9&&Math.abs(three.mass-three.initialMass)<1e-9,
  T2_nonnegative:base.min>=-1e-12&&three.min>=-1e-12,
  T3_replay:JSON.stringify(base)===JSON.stringify(replay),
  T4_zero_gain:l1(zero.projected,zero.initial[0].map((_,i)=>zero.initial.reduce((s,z)=>s+z[i],0)))<1e-9,
  T5_uncoupled:l1(unc.projected,unc.initial[0].map((_,i)=>unc.initial.reduce((s,z)=>s+z[i],0)))<1e-9,
  T6_common_phase:l1(base.projected,shift.projected)<1e-9,
  T7_relative_phase:l1(base.projected,rel.projected)>1e-10,
  T8_frequency:l1(base.projected,freq.projected)>1e-10,
  T9_boundary:l1(base.projected,gate.projected)>1e-10,
  T10_topology:l1(base.projected,three.projected)>1e-10
 };
 results.push({seed,tests,metrics:{massError:Math.abs(base.mass-base.initialMass),threeMassError:Math.abs(three.mass-three.initialMass),common:l1(base.projected,shift.projected),relative:l1(base.projected,rel.projected),frequency:l1(base.projected,freq.projected),boundary:l1(base.projected,gate.projected),topology:l1(base.projected,three.projected),shuffle:l1(base.projected,shuffle.projected),initial2:base.initialMass,initial3:three.initialMass},uniqueIds:base.ids.every(row=>new Set(row).size===N)});
}
console.log(JSON.stringify({issue:409,seeds:SEEDS,results},null,2));
