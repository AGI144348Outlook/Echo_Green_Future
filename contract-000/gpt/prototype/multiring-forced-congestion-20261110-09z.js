// GPT-only synthetic 27-seat FIFO congestion; Issue #390 prospective registration.
function run(seed,opts={}) {
 const N=27, M=54, cap=3, arrivals=Array.from({length:M},(_,i)=>({id:i,seat:(i*7+seed)%N,mass:1+(i%5)/10}));
 const queue=arrivals.slice(N), active=arrivals.slice(0,N), admitted=active.slice(), released=[];
 const initialQueue=queue.length, initialActive=active.length;
 for(let tick=0;tick<27;tick++){
   for(let j=0;j<cap && active.length;j++) released.push(active.shift());
   while(active.length<N && queue.length) {let e=queue.shift();active.push(e);admitted.push(e);}
 }
 const order=admitted.map(e=>e.id), ids=new Set(order);
 const map=opts.shift? (i)=>(i+1)%N : (i)=>i;
 const field=Array(N).fill(0);
 for(const e of admitted) if(!opts.noop) field[map(e.seat)]+=e.mass*(opts.uncoupled?0:1);
 const mass=admitted.reduce((a,e)=>a+e.mass,0);
 return {seed,initialQueue,initialActive,remainingQueue:queue.length,remainingActive:active.length,released:released.length,order,unique:ids.size,field,mass,fieldMass:field.reduce((a,b)=>a+b,0),phase:27%N};
}
function tests(){
 const seeds=[11,23,47,89], rows=[];
 for(const seed of seeds){
  const a=run(seed),b=run(seed),z=run(seed,{noop:true}),u=run(seed,{uncoupled:true}),s=run(seed,{shift:true});
  const l1=a.field.reduce((x,v,i)=>x+Math.abs(v-s.field[i]),0);
  const checks={T1:a.unique===54,T2:a.initialQueue===27&&a.initialActive===27,T3:a.remainingQueue===0&&a.released===54,T4:a.order.length===54&&a.order.every((x,i)=>x===i),T5:JSON.stringify(a)===JSON.stringify(b),T6:z.field.every(v=>v===0),T7:u.field.every(v=>v===0),T8:l1>0,T9:Math.abs(a.fieldMass-a.mass)<1e-9,T10:a.phase===0};
  rows.push({seed,checks,initialQueue:a.initialQueue,remainingQueue:a.remainingQueue,released:a.released,spatialL1:l1,massError:Math.abs(a.fieldMass-a.mass)});
 }
 return {rows,passed:rows.reduce((n,r)=>n+Object.values(r.checks).filter(Boolean).length,0),total:40};
}
