// Echo-GPT 10Z standalone synthetic experiment. Issue #416 preregistered before test.
(function(){
"use strict";
const seeds=[11,23,37,53], N=27, ticks=12;
const L1=(a,b)=>a.reduce((s,x,i)=>s+Math.abs(x-b[i]),0);
function simulate(seed,opt={}){
 const rings=opt.rings||2, gain=opt.gain===undefined?0.08:opt.gain;
 const phaseShift=opt.phaseShift||0, relative=opt.relative||0, freqShift=opt.freqShift||0;
 const boundary=opt.boundary===undefined?1:opt.boundary;
 const m=Array.from({length:rings},(_,r)=>Array.from({length:N},(_,i)=>{
   let total=1+((seed*7+i*13)%17)/17;
   // exact equal per-seat total in all ring configurations
   let frac=rings===2?(r===0?0.35:0.65):(r===0?0.20:r===1?0.35:0.45);
   return total*frac;
 }));
 const initial=m.map(row=>row.slice());
 const initialMass=m.flat().reduce((a,b)=>a+b,0);
 const phases=Array.from({length:rings},(_,r)=>0.23*r+phaseShift+(r===0?relative:0));
 const freq=Array.from({length:rings},(_,r)=>0.014+0.007*r+(r===0?freqShift:0));
 for(let t=0;t<ticks;t++){
   // local deterministic rotation is independently evolving even when cross-ring coupling disabled
   for(let r=0;r<rings;r++){
     let rotated=m[r].slice();
     for(let i=0;i<N;i++){let f=0.004*(1+((i+seed)%5)/5);rotated[i]-=f*m[r][i];rotated[(i+1)%N]+=f*m[r][i];}
     m[r]=rotated;
   }
   if(gain!==0){
     for(let r=0;r<rings-1;r++)for(let i=0;i<N;i++){
       let angle=(phases[r+1]-phases[r])+(freq[r+1]-freq[r])*t;
       let affinity=0.6+0.4*((((i+1)*((seed%11)+3))%19)/19);
       let coeff=Math.min(0.2,Math.max(0,gain*boundary*affinity*(1+Math.sin(angle))/2));
       let transfer=coeff*(m[r][i]-m[r+1][i]);
       m[r][i]-=transfer;m[r+1][i]+=transfer;
     }
   }
 }
 const projected=Array.from({length:N},(_,i)=>m.reduce((s,row)=>s+row[i],0));
 return {rings,m,initial,projected,initialMass,finalMass:m.flat().reduce((a,b)=>a+b,0)};
}
function evaluate(){
 const rows=[];
 for(const seed of seeds){
 const base=simulate(seed), repeat=simulate(seed), nullGain=simulate(seed,{gain:0}), uncoupled=simulate(seed,{gain:0,phaseShift:1.2});
 const gauge=simulate(seed,{phaseShift:1.2}), relative=simulate(seed,{relative:0.9}), frequency=simulate(seed,{freqShift:0.03}), boundary=simulate(seed,{boundary:0});
 const three=simulate(seed,{rings:3});
 const ringL1=x=>L1(base.m.flat(),x.m.flat());
 const target=Array.from({length:N},(_,i)=>1+((seed*7+i*13)%17)/17+0.06*Math.sin((i+seed)/3));
 const mae=x=>x.projected.reduce((s,v,i)=>s+Math.abs(v-target[i]),0)/N;
 const massErr=Math.abs(base.finalMass-base.initialMass);
 const checks={
  replay:JSON.stringify(base)===JSON.stringify(repeat),
  mass:massErr<1e-10,
  nonnegative:base.m.flat().every(v=>v>=0),
  noop:L1(nullGain.m.flat(),uncoupled.m.flat())<1e-10,
  uncoupledEvolves:L1(nullGain.m.flat(),nullGain.initial.flat())>1e-6,
  gauge:ringL1(gauge)<1e-10,
  relative:ringL1(relative)>1e-8,
  frequency:ringL1(frequency)>1e-8,
  boundary:ringL1(boundary)>1e-8,
  topologyMatched:three.initial.every((_,r)=>true)&&base.initial[0].every((_,i)=>Math.abs(base.initial.reduce((s,row)=>s+row[i],0)-three.initial.reduce((s,row)=>s+row[i],0))<1e-12)
 };
 rows.push({seed,checks,massErr,relativeRingL1:ringL1(relative),relativeProjectedL1:L1(base.projected,relative.projected),frequencyRingL1:ringL1(frequency),boundaryRingL1:ringL1(boundary),gaugeRingL1:ringL1(gauge),twoThreeProjectedL1:L1(base.projected,three.projected),heldoutMAE:{two:mae(base),three:mae(three),uncoupled:mae(nullGain)},twoThreeRingDimension:[base.m.length,three.m.length]});
 }
 return {issue:416,seeds,ticks,rows,passed:rows.reduce((s,r)=>s+Object.values(r.checks).filter(Boolean).length,0),total:rows.length*10};
}
globalThis.echoGPT416={simulate,evaluate};
})();