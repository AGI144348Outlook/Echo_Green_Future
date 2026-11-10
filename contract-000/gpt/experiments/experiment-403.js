// GPT-only synthetic experiment 403; node: node experiment-403.js
const seeds=[11,23,47,89], n=27;
const gem=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,20,40,50,80];
function run(seed,rings=2,opt={}){
 let state=Array.from({length:rings},(_,r)=>Array.from({length:n},(_,i)=>((seed*17+i*13+r*7)%23+1)/rings));
 let initial=state.map(a=>a.slice()), ids=Array.from({length:n},(_,i)=>i);
 for(let t=0;t<(opt.ticks??9);t++){
  for(let r=0;r<rings-1;r++){
   for(let i=0;i<n;i++){
    let j=(i+((opt.shuffle)?7:0))%n;
    let a=state[r][i],b=state[r+1][j];
    let phase=Math.sin((t+i+(opt.phase??0))*0.37+(opt.freq??0)*t);
    let value=(opt.permute?gem[(i+7)%n]:gem[i]);
    let gate=opt.boundary===false?1:(0.5+0.5*Math.sin((t+i)*0.21));
    let transfer=(opt.gain??0.1)*gate*(0.5+0.5*phase)*(0.5+value/1000)*Math.min(a,b+1);
    transfer=Math.max(0,Math.min(a,transfer));
    state[r][i]-=transfer;state[r+1][j]+=transfer;
   }
  }
 }
 return {state,initial,ids,mass:state.flat().reduce((a,b)=>a+b,0),initialMass:initial.flat().reduce((a,b)=>a+b,0)};
}
function l1(a,b){return a.flat().reduce((s,x,i)=>s+Math.abs(x-b.flat()[i]),0)}
function check(seed){
 const b=run(seed), replay=run(seed), zero=run(seed,2,{gain:0}),uncoupled=run(seed,2,{ticks:0});
 const three=run(seed,3); const phase=run(seed,2,{phase:7}),permute=run(seed,2,{permute:true}),boundary=run(seed,2,{boundary:false});
 const twoMass=b.initialMass,threeMass=three.initialMass;
 // Normalize three-ring initial conditions to same total mass for comparable outcome shape (not per-ring capacity).
 const normalized=three.state.map(row=>row.map(x=>x*twoMass/threeMass));
 const checks={
 T1_replay:JSON.stringify(b.state)===JSON.stringify(replay.state),
 T2_mass:Math.abs(b.mass-b.initialMass)<1e-9,
 T3_nonnegative:b.state.flat().every(x=>x>=-1e-12),
 T4_noop:JSON.stringify(zero.state)===JSON.stringify(zero.initial),
 T5_uncoupled:JSON.stringify(uncoupled.state)===JSON.stringify(uncoupled.initial),
 T6_identity:b.ids.length===27&&new Set(b.ids).size===27&&b.ids.every((x,i)=>x===i),
 T7_matched_mass:Math.abs(normalized.flat().reduce((a,b)=>a+b,0)-b.mass)<1e-9,
 T8_phase:l1(b.state,phase.state)>1e-9,
 T9_permutation:l1(b.state,permute.state)>1e-9,
 T10_boundary:l1(b.state,boundary.state)>1e-9
 };
 return {seed,checks,metrics:{massError:b.mass-b.initialMass,phaseL1:l1(b.state,phase.state),permutationL1:l1(b.state,permute.state),boundaryL1:l1(b.state,boundary.state),twoMass,threeMass,matchedThreeMass:normalized.flat().reduce((a,b)=>a+b,0)}};
}
const results=seeds.map(check);
if(typeof module!=='undefined')module.exports={results,run,check};
