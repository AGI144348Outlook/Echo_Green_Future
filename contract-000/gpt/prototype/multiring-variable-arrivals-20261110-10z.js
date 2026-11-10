// GPT-only synthetic experiment. Prospective Issue #391. No canonical Echo semantics.
function run(seed, opt={}) {
 const N=27,M=54, events=Array.from({length:M},(_,i)=>({id:i,seat:(i*7+seed)%N,mass:1+(i%5)/10,arrival:i<27?0:2}));
 let perm=Array.from({length:N},(_,i)=>i), state=(seed>>>0)||1;
 function rng(){state=(Math.imul(1664525,state)+1013904223)>>>0;return state/4294967296;}
 if(opt.shuffle)for(let i=N-1;i>0;i--){const j=Math.floor(rng()*(i+1));[perm[i],perm[j]]=[perm[j],perm[i]];}
 let pending=[],active=[],admitted=[],released=[],maxQ=0,firstQ=0;
 for(let t=0;t<100;t++){
   for(const e of events)if(e.arrival===t)pending.push(e);
   if(t>0){let service=1+((t+seed)%3);while(service-- && active.length)released.push(active.shift());}
   while(active.length<N && pending.length){let e=pending.shift();active.push(e);admitted.push(e);}
   maxQ=Math.max(maxQ,pending.length);if(t===2)firstQ=pending.length;
 }
 let field=Array(N).fill(0),warehouse=Array(N).fill(0);
 for(const e of admitted){if(opt.noop||opt.uncoupled)continue;let k=perm[e.seat],v=e.mass;field[k]+=v;warehouse[k]+=v;if(opt.reverse)field[(k+3)%N]+=v*.2;}
 let mass=admitted.reduce((s,e)=>s+e.mass,0),fieldMass=field.reduce((s,e)=>s+e,0);
 return {seed,admitted:admitted.map(e=>e.id),released:released.map(e=>e.id),pending:pending.length,active:active.length,maxQ,firstQ,field,warehouse,mass,fieldMass,phase:27%N};
}
function tests(){
 let rows=[];for(const seed of [11,23,47,89]){
 const a=run(seed),b=run(seed),n=run(seed,{noop:true}),u=run(seed,{uncoupled:true}),s=run(seed,{shuffle:true}),r=run(seed,{reverse:true});
 const l1=(x,y)=>x.reduce((v,e,i)=>v+Math.abs(e-y[i]),0);
 const checks={T1:new Set(a.admitted).size===54,T2:a.maxQ>0,T3:a.pending===0&&a.active===0&&a.released.length===54,T4:a.admitted.every((x,i)=>x===i)&&a.released.every((x,i)=>x===i),T5:JSON.stringify(a)===JSON.stringify(b),T6:n.field.every(x=>x===0),T7:u.field.every(x=>x===0),T8:l1(a.field,s.field)>0,T9:l1(a.field,r.field)>0,T10:Math.abs(a.fieldMass-a.mass)<1e-9&&a.phase===0};
 rows.push({seed,checks,maxQ:a.maxQ,shuffleL1:l1(a.field,s.field),reverseL1:l1(a.field,r.field),massError:Math.abs(a.fieldMass-a.mass)});
 }return {rows,passed:rows.reduce((n,r)=>n+Object.values(r.checks).filter(Boolean).length,0),total:40};
}
