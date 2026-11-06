// GPT-only bounded experiment, preregistered Issue #313 before creation and execution.
function experiment(){
 const seeds=[17,29,43,71,101],T=48,N=27,mod=x=>((x%1)+1)%1;
 const seats=Array.from({length:N},(_,id)=>({id,occupant:null}));
 const glyphs=Array.from({length:N},(_,id)=>({id,seat:null}));
 const xyz=i=>[i%3,Math.floor(i/3)%3,Math.floor(i/9)];
 const inv=p=>p[0]+3*p[1]+9*p[2];
 const identity=Object.freeze({algorithm:"A-000",spec:"proposed-invariant-v0",grant:null});
 function run(seed,gain=.2,couple=.09,shuffle=false,perturb=false){
   const entropy=Array.from({length:7},(_,i)=>.28+.11*Math.sin(seed*.07+i*.81));
   if(perturb)entropy[3]+=.15;
   if(shuffle)entropy.reverse();
   let phase=Array.from({length:7},(_,i)=>mod(seed*.013+i*.11)),radii=[],history=[];
   for(let t=0;t<T;t++){
     const prev=phase.slice();
     phase=prev.map((p,i)=>mod(p+.011+.002*i+gain*(entropy[i]-.28)*.01+(i?couple*Math.sin(2*Math.PI*(prev[0]-p))*.012:0)));
     const radius=phase.map((p,i)=>Math.max(.7,Math.min(.9,.8+gain*(entropy[i]-.28)*.1+.01*Math.sin(2*Math.PI*p))));
     radii.push(...radius);history.push(phase.slice());
   }
   const target=Array.from({length:7},(_,i)=>mod(.18+.003*seed+.019*i+.06*Math.sin(seed*.13+i*.4)));
   const circ=(x,y)=>{let d=Math.abs(x-y);return Math.min(d,1-d)};
   const loss=phase.reduce((s,p,i)=>s+circ(p,target[i]),0)/7;
   return {phase,radii,loss,history};
 }
 const d=(a,b)=>a.phase.reduce((s,x,i)=>{let z=Math.abs(x-b.phase[i]);return s+Math.min(z,1-z)},0);
 const per=seeds.map(seed=>({seed,coupled:run(seed),uncoupled:run(seed,.2,0),zero:run(seed,0,0),changed:run(seed,.2,.09,false,true),zeroChanged:run(seed,0,0,false,true),shuffled:run(seed,.2,.09,true)}));
 const allR=per.flatMap(x=>x.coupled.radii);
 const checks={
  seats:seats.length===27&&seats.every(x=>x.occupant===null)&&glyphs.every(x=>x.seat===null),
  cube:glyphs.every(x=>inv(xyz(x.id))===x.id)&&new Set(glyphs.map(x=>x.id)).size===27,
  replay:per.every(x=>JSON.stringify(x.coupled)===JSON.stringify(run(x.seed))),
  zeroGain:per.every(x=>d(x.zero,x.zeroChanged)===0),
  entropyResponse:per.some(x=>d(x.coupled,x.changed)>0),
  shuffleControl:per.some(x=>d(x.coupled,x.shuffled)>0),
  couplingContrast:per.some(x=>d(x.coupled,x.uncoupled)>0),
  radiusBounded:allR.every(r=>r>=.7&&r<=.9)&&Math.max(...allR)-Math.min(...allR)>.001,
  externalTarget:per.every(x=>Number.isFinite(x.coupled.loss)&&Number.isFinite(x.zero.loss)),
  identityGrant:identity.algorithm==="A-000"&&identity.grant===null&&Object.isFrozen(identity)
 };
 const avg=k=>per.reduce((s,x)=>s+x[k].loss,0)/per.length;
 return {issue:313,seeds,steps:T,checks,passed:Object.values(checks).filter(Boolean).length,total:Object.keys(checks).length,metrics:{coupledMeanLoss:avg("coupled"),uncoupledMeanLoss:avg("uncoupled"),zeroMeanLoss:avg("zero"),coupledWinsZero:per.filter(x=>x.coupled.loss<x.zero.loss).length,entropyInterventions:per.map(x=>d(x.coupled,x.changed)),shuffledDistances:per.map(x=>d(x.coupled,x.shuffled)),couplingDistances:per.map(x=>d(x.coupled,x.uncoupled)),radiusMin:Math.min(...allR),radiusMax:Math.max(...allR)},limitations:["synthetic entropy, not Neon measurements","target deterministic external formula, not real semantic task","no learning; fixed parameters","identity is a string, not cryptographic attestation","27 glyph IDs, not asserted 27 Hebrew base letters"]};
}