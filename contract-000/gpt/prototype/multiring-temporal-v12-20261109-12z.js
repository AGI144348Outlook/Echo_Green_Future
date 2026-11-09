// GPT-owned offline temporal 27-seat ring prototype v12. No canonical Echo behavior.
'use strict';
const N=27, SEEDS=[7701,7702,7703,7704];
const GLYPHS=Array.from({length:N},(_,i)=>i<22?String.fromCharCode(0x05d0+i):['ך','ם','ן','ף','ץ'][i-22]);
function step(s, coupling=0.2, mapping=null, phase=0, freq=1, deformation=0){
 const out=new Array(N).fill(0);
 for(let i=0;i<N;i++){
   const left=mapping?mapping[(i+N-1)%N]:(i+N-1)%N;
   const right=mapping?mapping[(i+1)%N]:(i+1)%N;
   const gain=1+0.1*Math.sin(phase+freq*i/N);
   out[i]=0.6*s[i]+coupling*gain*(s[left]+s[right])/2;
   out[i]*=(1+deformation*Math.cos(2*Math.PI*i/N));
 }
 return out;
}
function simulate(seed,shuffle=false,coupling=0.2){
 const source=seed%N, s=new Array(N).fill(0);s[source]=1;
 const mapping=shuffle?Array.from({length:N},(_,i)=>(i*5+3)%N):null;
 return {source,mapping,initial:s,t1:step(s,coupling,mapping),t2:step(step(s,coupling,mapping),coupling,mapping)};
}
function run(){
 return SEEDS.map(seed=>{
  const a=simulate(seed), b=simulate(seed,true), z=simulate(seed,false,0);
  const near=(a.source+1)%N, far=(a.source+8)%N;
  const visits=Array.from({length:N},(_,tick)=>(a.source+tick)%N);
  const phase=step(a.initial,0.2,null,Math.PI,1);
  const freq=step(a.initial,0.2,null,0,3);
  const deform=step(a.initial,0.2,null,0,1,0.15);
  const word2=[GLYPHS[a.source],GLYPHS[near]].join('');
  const word3=word2+GLYPHS[(a.source+2)%N];
  const identity=JSON.stringify(GLYPHS);
  const mutation=GLYPHS.slice();mutation[0]='CHANGED';
  const metrics={
   T1_uniqueGlyphs:new Set(GLYPHS).size===N,
   T2_word2:word2,
   T3_word3:word3,
   T4_uniqueVisits:new Set(visits).size,
   T5_local:a.t1[a.source],
   T6_neighborDelayed:a.t2[near],
   T7_distantImmediate:a.t1[far],
   T8_uncoupledNeighbor:z.t1[near],
   T9_shuffledReceiverDelta:b.t2[near]-a.t2[near],
   T10_phaseDelta:phase[near]-a.t1[near],
   T10_freqDelta:freq[near]-a.t1[near],
   T10_deformationMax:Math.max(...deform.map(Math.abs)),
   T10_identityMutationDetected:JSON.stringify(mutation)!==identity
  };
  return {seed,source:a.source,metrics};
 });
}
module.exports={run,step,simulate,SEEDS};
if(typeof require!=='undefined'&&require.main===module)console.log(JSON.stringify(run(),null,2));
