// Pre-test Issue #296; exact deterministic trial function, executed in JS tool orchestration.
function experiment({n,entropy,seed,policy,shuffled=false,disconnected=false}){
 let s=seed>>>0;const rand=()=>((s=(Math.imul(s,1664525)+1013904223)>>>0)/4294967296);
 const bits=Array.from({length:n},()=>rand()<.5?0:1),quality=Array(n).fill(1),ties=Array.from({length:n-1},(_,i)=>({a:i,b:i+1,w:.8,parity:0}));
 for(const e of ties)e.parity=bits[e.a]^bits[e.b]; // encoded relation, NOT learned
 let spent=0,weight=.5;const fields=[];
 for(let t=0;t<16;t++){
  const field=entropy*(1+.25*Math.sin(t*.63));fields.push(field);
  for(let i=0;i<n;i++)quality[i]=Math.max(0,quality[i]-field);
  for(const e of ties)e.w=Math.max(0,e.w-field*.8);
  const coherence=ties.reduce((v,e)=>v+e.w,0)/ties.length;
  if(policy==="adaptive")weight+=.08*(coherence-weight);
  for(let j=0;j<5;j++){
   const boxChoice=policy==="box"||(policy==="adaptive"&&weight<.64);
   if(policy==="noop")break;
   if(boxChoice){const i=(t*5+j)%n;quality[i]=Math.min(1,quality[i]+.10)}
   else{const e=ties[(t*5+j)%ties.length];e.w=Math.min(1,e.w+.10)}
   spent++;
  }
 }
 // Fixed observable anchor cues at every 4th box, with others deliberately hidden.
 const observed=Array.from({length:n},(_,i)=>i%4===0&&quality[i]>=.38?bits[i]:null);
 const guesses=observed.slice();
 if(!disconnected)for(let pass=0;pass<3;pass++){
  for(let i=0;i<n-1;i++){
   const e=ties[i];if(e.w<.38)continue;
   const parity=shuffled?e.parity^1:e.parity;
   if(guesses[i]!==null&&guesses[i+1]===null)guesses[i+1]=guesses[i]^parity;
   else if(guesses[i]===null&&guesses[i+1]!==null)guesses[i]=guesses[i+1]^parity;
  }
 }
 let correct=0,known=0,hiddenCorrect=0,hiddenKnown=0,hiddenCount=0;
 for(let i=0;i<n;i++){if(i%4!==0)hiddenCount++;if(guesses[i]!==null){known++;if(guesses[i]===bits[i])correct++;if(i%4!==0){hiddenKnown++;if(guesses[i]===bits[i])hiddenCorrect++}}}
 return {n,entropy,seed,policy,spent,fieldChecksum:fields.reduce((a,b)=>a+b,0),weight,boxQuality:quality.reduce((a,b)=>a+b,0)/n,tieStrength:ties.reduce((a,e)=>a+e.w,0)/ties.length,coverage:known/n,accuracy:correct/n,hiddenCoverage:hiddenKnown/hiddenCount,hiddenAccuracy:hiddenCorrect/hiddenCount,shuffled,disconnected};
}
