// Echo-GPT noncanonical synthetic queue experiment #388; Node or isolated V8; no external effects.
const SEEDS=[11,23,37,53];
function run(seed,{coupling=true,reverse=true,shuffle=false,service=9}={}){
 const events=Array.from({length:54},(_,id)=>({id,payload:1+((id*7+seed)%13)/20}));
 if(shuffle){let s=seed>>>0;for(let i=events.length-1;i>0;i--){s=(Math.imul(s,1664525)+1013904223)>>>0;const j=s%(i+1);[events[i].payload,events[j].payload]=[events[j].payload,events[i].payload];}}
 const slots=events.slice(0,27),queue=events.slice(27),served=[],matrix=Array(27).fill(10),warehouse=Array(27).fill(0);
 const initialQueued=queue.length;let maxOccupied=slots.length, maxQueued=queue.length;
 for(let tick=0;tick<9;tick++){
  const count=Math.min(service,slots.length);
  for(let j=0;j<count;j++){const ev=slots.shift();served.push(ev.id);if(coupling){const k=ev.id%27,move=ev.payload/10;matrix[k]-=move;warehouse[k]+=move;if(reverse){const back=move/5;warehouse[k]-=back;matrix[k]+=back;}}}
  while(slots.length<27 && queue.length)slots.push(queue.shift());
  maxOccupied=Math.max(maxOccupied,slots.length);maxQueued=Math.max(maxQueued,queue.length);
 }
 return {seed,initialQueued,maxOccupied,maxQueued,served,pending:slots.map(e=>e.id).concat(queue.map(e=>e.id)),queueRemaining:queue.length,matrix,warehouse,initialMass:270,finalMass:matrix.reduce((a,b)=>a+b,0)+warehouse.reduce((a,b)=>a+b,0)};
}
function check(seed){const a=run(seed),b=run(seed),off=run(seed,{coupling:false}),one=run(seed,{reverse:false}),shuf=run(seed,{shuffle:true}),slow=run(seed,{service:1});const eq=(x,y)=>JSON.stringify(x)===JSON.stringify(y);const l1=(x,y)=>x.reduce((s,v,i)=>s+Math.abs(v-y[i]),0);const tests={capacity:a.maxOccupied===27,contention:a.initialQueued===27&&a.maxQueued===27,fifo:eq(a.served,Array.from({length:54},(_,i)=>i)),identity:a.served.length===54&&new Set(a.served).size===54&&a.pending.length===0,replay:eq(a,b),mass:Math.abs(a.finalMass-a.initialMass)<1e-9,noop:off.warehouse.every(v=>v===0)&&off.matrix.every(v=>v===10),reverse:l1(a.warehouse,one.warehouse)>0,shuffled:l1(a.warehouse,shuf.warehouse)>0&&eq(a.served,shuf.served),slow:slow.pending.length>0&&slow.served.length===9};return {seed,tests,metrics:{initialQueued:a.initialQueued,served:a.served.length,reverseL1:l1(a.warehouse,one.warehouse),shuffleL1:l1(a.warehouse,shuf.warehouse),massError:Math.abs(a.finalMass-a.initialMass),slowPending:slow.pending.length}};}
function main(){return SEEDS.map(check)}
if(typeof module!=='undefined')module.exports={run,check,main,SEEDS};
