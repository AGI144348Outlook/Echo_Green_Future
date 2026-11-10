/* GPT-owned synthetic 27-seat warehouse ring. Issue #389 preregistration.
   Offline, deterministic; no canonical Echo dependencies or external effects. */
(function(global){
"use strict";
const SEEDS=[11,23,37,53], CAP=27;
function makeEvents(seed,shuffle=false){
 const a=[];for(let i=0;i<54;i++)a.push({id:i,arrival:2*Math.floor(i/18),duration:1+((i+seed)%4),payload:1+((shuffle?(i*17)%54:i)+seed)%9});
 return a;
}
function simulate(seed,opt={}){
 const events=makeEvents(seed,!!opt.shuffle),limit=opt.limit??64,forward=opt.forward??0.12,reverse=opt.reverse??0.07;
 const queue=[],active=[],admitted=[],completed=[],history=[];let warehouse=0,returned=0,maxActive=0,maxQueue=0;const spatial=Array(CAP).fill(0);
 for(let t=0;t<limit;t++){
   for(const e of events)if(e.arrival===t)queue.push(e);
   // Discharge first; then admit FIFO. Different service times permit non-FIFO completion.
   for(let k=active.length-1;k>=0;k--)if(active[k].end<=t){const e=active.splice(k,1)[0];completed.push(e.id);warehouse+=e.payload*forward;spatial[e.id%CAP]+=e.payload*forward;returned+=e.payload*forward*reverse;}
   while(active.length<CAP&&queue.length){const e=queue.shift();active.push({id:e.id,end:t+e.duration,payload:e.payload});admitted.push(e.id);}
   maxActive=Math.max(maxActive,active.length);maxQueue=Math.max(maxQueue,queue.length);
   history.push([t,active.length,queue.length,completed.length]);
 }
 return {seed,events,admitted,completed,queued:queue.map(e=>e.id),active:active.map(e=>e.id),warehouse,returned,spatial,maxActive,maxQueue,history};
}
function evaluate(seed){
 const a=simulate(seed),b=simulate(seed),noop=simulate(seed,{forward:0,reverse:0}),one=simulate(seed,{reverse:0}),shuffled=simulate(seed,{shuffle:true}),short=simulate(seed,{limit:5});
 const ids=a.admitted.concat(a.queued,a.active),massExpected=a.completed.reduce((s,id)=>s+a.events[id].payload*0.12,0);
 const tests=[
 ["T1 seat capacity",a.maxActive<=CAP&&a.maxActive>0,{max:a.maxActive}],
 ["T2 staggered arrivals",a.events.filter(e=>e.arrival===0).length===18&&a.events.filter(e=>e.arrival===2).length===18&&a.events.filter(e=>e.arrival===4).length===18,{waves:[0,2,4]}],
 ["T3 FIFO admission",a.admitted.every((id,i)=>id===i),{first:a.admitted.slice(0,5),last:a.admitted.slice(-5)}],
 ["T4 no loss or duplication",ids.length===54&&new Set(ids).size===54&&a.completed.length===54&&a.queued.length===0&&a.active.length===0,{admitted:a.admitted.length,completed:a.completed.length}],
 ["T5 deterministic replay",JSON.stringify(a)===JSON.stringify(b),{same:JSON.stringify(a)===JSON.stringify(b)}],
 ["T6 transfer mass accounting",Math.abs(a.warehouse-massExpected)<1e-9,{expected:massExpected,observed:a.warehouse}],
 ["T7 zero coupling null",noop.warehouse===0&&noop.returned===0,{warehouse:noop.warehouse}],
 ["T8 reverse coupling",a.returned>0&&one.returned===0&&a.admitted.join(",")===one.admitted.join(","),{difference:a.returned-one.returned}],
 ["T9 shuffled payload control",a.spatial.reduce((n,v,i)=>n+Math.abs(v-shuffled.spatial[i]),0)>1e-9&&a.admitted.join(",")===shuffled.admitted.join(","),{spatialL1:a.spatial.reduce((n,v,i)=>n+Math.abs(v-shuffled.spatial[i]),0)}],
 ["T10 short-horizon backlog",short.queued.length>0&&short.completed.length===0,{pending:short.queued.length,active:short.active.length}]
 ];
 return {seed,tests:tests.map(([name,pass,observation])=>({name,pass,observation})),summary:{maxActive:a.maxActive,maxQueue:a.maxQueue,completed:a.completed.length,warehouse:a.warehouse,returned:a.returned}};
}
function run(){const cases=SEEDS.map(evaluate);return {issue:389,seeds:SEEDS,types:10,total:40,passed:cases.reduce((n,c)=>n+c.tests.filter(t=>t.pass).length,0),cases};}
global.ECHO_GPT_08Z={simulate,evaluate,run};
})(globalThis);
