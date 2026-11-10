// Echo-GPT independent synthetic ring experiment, 2026-11-10 23Z. Issue #404 preregistration.
(function(){
const seeds=[11,23,37,53], N=27, steps=9;
const sum=a=>a.reduce((x,y)=>x+y,0), l1=(a,b)=>sum(a.map((x,i)=>Math.abs(x-b[i])));
function init(seed){let x=seed>>>0;return Array.from({length:N},()=>{x=(1664525*x+1013904223)>>>0;return 0.5+x/4294967296;});}
function sim(seed,options={}){
 const mass=init(seed), initial=mass.slice(), ringCount=options.rings||2;
 const phase=Array.from({length:N},(_,i)=>(i+seed%7)*0.11);
 const freq=Array.from({length:N},(_,i)=>0.04+(i%5)*0.007);
 for(let t=0;t<steps;t++){
  for(let i=0;i<N;i++)phase[i]+=freq[i]*(options.frequency||1);
  const delta=Array(N).fill(0);
  for(let i=0;i<N;i++){
   let j=(i+ (options.shuffle?7:1)+(ringCount===3?2:0))%N;
   let affinity=1+0.2*Math.cos((i-j)*0.1+(options.phase||0));
   let gate=options.boundary===false?1:(0.75+0.25*Math.sin((i+t)*0.2)**2);
   let flow=(options.gain===undefined?0.035:options.gain)*affinity*gate*mass[i];
   delta[i]-=flow;delta[j]+=flow;
  }
  for(let i=0;i<N;i++)mass[i]+=delta[i];
 }
 return {mass,initial,phase,identity:Array.from({length:N},(_,i)=>'glyph-'+i)};
}
const cases=[];
for(const seed of seeds){
 const a=sim(seed), replay=sim(seed), three=sim(seed,{rings:3}), unc=sim(seed,{gain:0}), noop=sim(seed,{gain:0}), shuf=sim(seed,{shuffle:true}), offset=sim(seed,{phase:1}), freq=sim(seed,{frequency:1.5});
 const tests=[
 ['T1 replay',l1(a.mass,replay.mass)===0],
 ['T2 matched initial mass',l1(a.initial,three.initial)===0],
 ['T3 conservation',Math.abs(sum(a.mass)-sum(a.initial))<1e-10],
 ['T4 nonnegative',a.mass.every(x=>x>=0)],
 ['T5 zero-gain no-op',l1(noop.mass,noop.initial)===0],
 ['T6 evolving uncoupled',l1(unc.mass,unc.initial)===0&&unc.phase[0]!==0.11*(seed%7)],
 ['T7 shuffled routing',l1(a.mass,shuf.mass)>1e-8],
 ['T8 phase offset',l1(a.mass,offset.mass)>1e-8],
 ['T9 frequency mismatch',l1(a.mass,freq.mass)>1e-8],
 ['T10 3 vs 2 matched initial',l1(a.mass,three.mass)>1e-8&&l1(a.initial,three.initial)===0]
 ];
 cases.push({seed,tests,metrics:{initial:sum(a.initial),final:sum(a.mass),shuffled:l1(a.mass,shuf.mass),phase:l1(a.mass,offset.mass),frequency:l1(a.mass,freq.mass),three:l1(a.mass,three.mass),uncoupledPhaseAdvance:unc.phase[0]-0.11*(seed%7)}});
}
return {seeds,steps,tests:cases,passed:cases.flatMap(c=>c.tests).filter(t=>t[1]).length,total:cases.length*10};
})()