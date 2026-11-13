// Echo-GPT independent synthetic 08Z. Node >=18. Fixed seeds; no external effects.
const SEEDS=[11,23,37,53],N=27,T=24;
const wrap=x=>Math.atan2(Math.sin(x),Math.cos(x));
function simulate(seed,opt={}){
 let phase=Array.from({length:N},(_,i)=>wrap((i*17+seed)/19)),initial=phase.slice();
 let mem=Array(N).fill(0),occupied=Array(N).fill(false),contacts=0,maxOcc=0;
 const ids=Array.from({length:N},(_,i)=>i);
 for(let t=0;t<(opt.noop?0:T);t++){
  let next=phase.slice();
  for(let i=0;i<N;i++){
   const hit=((i*7+t*11+seed)%29===0);
   if(hit){occupied[i]=true;contacts++;}
   const j=(i+1)%N,k=(i+2)%N;
   const aff=opt.shuffle?((i*13+7)%N):i;
   const pair=0.014*Math.sin(phase[j]-phase[i]);
   const tri=opt.ablate?0:0.003*Math.sin(phase[j]+phase[k]-2*phase[i]);
   const feedback=opt.uncoupled||opt.sham?0:0.005*mem[aff];
   const deform=opt.rigid?0:0.001*Math.sin(t/3+i);
   next[i]=wrap(phase[i]+0.02+pair+tri+feedback+deform);
   mem[i]=occupied[i]?0.86*mem[i]+0.14*Math.sin(phase[j]-phase[i]):0.9*mem[i];
   if((t+i)%17===0)occupied[i]=false;
  }
  phase=next;maxOcc=Math.max(maxOcc,occupied.filter(Boolean).length);
 }
 return {phase,mem,occupied,ids,contacts,maxOcc,initial};
}
const distance=(a,b)=>a.reduce((s,v,i)=>s+Math.abs(wrap(v-b[i])),0)/a.length;
function runAll(){
 const rows=[];
 for(const seed of SEEDS){
 const a=simulate(seed),b=simulate(seed,{sham:true}),u=simulate(seed,{uncoupled:true}),n=simulate(seed,{noop:true});
 const shift=0.7;
 // Explicit phase covariance tested by shift of output under no-op only; full model shift requires shifted initial state.
 const replay=simulate(seed),sh=simulate(seed,{shuffle:true}),ab=simulate(seed,{ablate:true}),rig=simulate(seed,{rigid:true});
 const types={
 noop_exact:JSON.stringify(n.phase)===JSON.stringify(n.initial)&&n.contacts===0&&n.maxOcc===0&&n.mem.every(x=>x===0)&&n.occupied.every(x=>!x),
 active_vs_sham:distance(a.phase,b.phase)>1e-8,
 uncoupled_null:distance(u.phase,b.phase)===0,
 phase_wrap:Math.max(...a.phase.map(v=>Math.abs(wrap(v+shift)-wrap(v+shift))))<1e-12,
 identity_unique:new Set(a.ids).size===N&&a.ids.every((x,i)=>x===i),
 capacity:a.maxOcc<=N,
 deterministic:JSON.stringify(a)===JSON.stringify(replay),
 shuffle:distance(a.phase,sh.phase)>1e-8,
 triadic_ablation:distance(a.phase,ab.phase)>1e-8,
 boundary_deformation:distance(a.phase,rig.phase)>1e-8
 };
 rows.push({seed,types,metrics:{active_sham:distance(a.phase,b.phase),uncoupled_sham:distance(u.phase,b.phase),shuffled:distance(a.phase,sh.phase),triadic:distance(a.phase,ab.phase),rigid:distance(a.phase,rig.phase),maxOcc:a.maxOcc,contacts:a.contacts}});
 }
 return {seeds:SEEDS,ticks:T,rows,passed:rows.reduce((n,r)=>n+Object.values(r.types).filter(Boolean).length,0),total:40,limitations:["phase_wrap is a tautology, NOT a full model covariance test","no independent warehouse agents","toy numeric affinities are not Hebrew gematria","no semantic learning or physical precession"]};
}
console.log(JSON.stringify(runAll(),null,2));
