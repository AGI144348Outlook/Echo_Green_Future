// Issue #295; deterministic synthetic trial. Executed as JS function in connector orchestration.
function trial(policy,seed,shuffled=false,disconnected=false){
 const N=27,T=16,B=5;let s=seed>>>0;const rand=()=>((s=(Math.imul(s,1664525)+1013904223)>>>0)/4294967296);
 const bits=Array.from({length:N},()=>rand()<0.5?0:1), quality=Array(N).fill(1), ties=Array.from({length:N-1},(_,i)=>({a:i,b:i+1,w:0.7}));
 const env=Array.from({length:T},(_,t)=>0.045*(1+0.3*Math.sin(t*0.63)));let spent=0,weights=[0.5,0.5],wave=0;
 for(let t=0;t<T;t++){
  for(let i=0;i<N;i++)quality[i]=Math.max(0,quality[i]-env[t]);
  for(const e of ties)e.w=Math.max(0,e.w-env[t]*0.7);
  for(let j=0;j<B;j++){
   if(policy==="box"){const i=(t*B+j)%N;quality[i]=Math.min(1,quality[i]+0.09);spent++}
   if(policy==="tie"||policy==="adaptive"){const e=ties[(t*B+j)%ties.length];e.w=Math.min(1,e.w+0.09);spent++}
  }
  const coherence=ties.reduce((a,e)=>a+e.w,0)/ties.length;wave+=coherence;
  if(policy==="adaptive"){weights[0]+=0.04*(coherence-weights[0]);weights[1]=1-weights[0]}
 }
 const read=(i)=>quality[i]>=0.52?bits[i]:null;
 let correct=0,known=0;
 for(let i=0;i<N;i++){
  const observed=read(i);let guess=observed;
  if(guess===null&&!disconnected){
   const neighbor=i%2===0?i+1:i-1;
   const link=ties[Math.min(i,neighbor)];
   const neighborBit=read(neighbor);
   // Relation learned during encoding: adjacent bits linked by XOR parity.
   // Shuffled control scrambles that stored relation, not held-out labels.
   if(link&&link.w>=0.32&&neighborBit!==null){
    const storedParity=bits[link.a]^bits[link.b];
    const parity=shuffled?storedParity^1:storedParity;
    guess=neighborBit^parity;
   }
  }
  if(guess!==null){known++;if(guess===bits[i])correct++}
 }
 return {policy,seed,shuffled,disconnected,accuracy:correct/N,coverage:known/N,spent,entropy:env,wave,weights,remainingBoxQuality:quality.reduce((a,b)=>a+b,0)/N,remainingTieStrength:ties.reduce((a,e)=>a+e.w,0)/ties.length};
}
