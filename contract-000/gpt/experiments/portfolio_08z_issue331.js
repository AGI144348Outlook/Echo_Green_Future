// GPT-only noncanonical diagnostic; preregistered Issue #331 before execution.
// Fixed seeds, no external I/O; returns JSON-serializable observations.
(function(){
const seeds=[1106,1107,1108,1109], tau=2*Math.PI;
function rng(s){return ()=>{s=(Math.imul(1664525,s)+1013904223)>>>0;return s/4294967296}}
function input(seed){let r=rng(seed);return Array.from({length:32},(_,t)=>({id:t,at:t,arrive:r()<.73})).filter(x=>x.arrive)}
function ledger(seed,dwell=3){const arrivals=input(seed),events=[],queue=[];let seat=null,release=-1;
for(let t=0;t<45;t++){if(seat!==null&&t>=release){events.push({t,k:"release",id:seat});seat=null}
for(const a of arrivals.filter(a=>a.at===t)){events.push({t,k:"arrival",id:a.id});queue.push(a)}
while(queue.length&&t-queue[0].at>=6){events.push({t,k:"expire",id:queue.shift().id})}
if(seat===null&&queue.length){seat=queue.shift().id;release=t+dwell;events.push({t,k:"admit",id:seat})}}
return {arrivals,events,dwell}}
function inspect(p){let arrived=new Set(),terminal=new Set(),waiting=[],seat=null,at=null,err=[];
for(const e of p.events){if(e.k==="arrival"){if(arrived.has(e.id))err.push("duplicate_arrival");arrived.add(e.id);waiting.push(e.id)}
if(e.k==="expire"){if(terminal.has(e.id))err.push("duplicate_terminal");terminal.add(e.id);waiting=waiting.filter(x=>x!==e.id)}
if(e.k==="admit"){if(seat!==null)err.push("overlap");if(waiting[0]!==e.id)err.push("fifo");waiting=waiting.filter(x=>x!==e.id);seat=e.id;at=e.t}
if(e.k==="release"){if(seat!==e.id)err.push("release_identity");if(e.t-at!==p.dwell)err.push("dwell");if(terminal.has(e.id))err.push("duplicate_terminal");terminal.add(e.id);seat=null}}
const expected=new Set(p.arrivals.map(a=>a.id));if(arrived.size!==expected.size||[...expected].some(x=>!arrived.has(x)))err.push("census");if(terminal.size!==expected.size)err.push("terminal");if(seat!==null)err.push("open_seat");return err}
const values=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];
const cells=Array.from({length:27},(_,i)=>[Math.floor(i/9),Math.floor(i/3)%3,i%3]);
function ring(seed,n,mode){let r=rng(seed),p=Array.from({length:n},()=>r()*tau),initial=p.slice(),loss=0;let vals=values.slice();if(mode==="shuffled"){let q=rng(seed+900);for(let i=26;i>0;i--){let j=Math.floor(q()*(i+1));[vals[i],vals[j]]=[vals[j],vals[i]]}}
for(let t=0;t<32;t++){let ids=p.map(x=>((Math.round(x/tau*27)%27)+27)%27);let pred=Math.atan2(p.reduce((a,x)=>a+Math.sin(x),0),p.reduce((a,x)=>a+Math.cos(x),0));let target=(.137*t+Math.sin(.21*t))%tau;loss+=1-Math.cos(pred-target);let old=p.slice();if(mode!=="noop")p=p.map((x,i)=>{let c=mode==="uncoupled"?0:.08*Math.sin(old[(i+1)%n]-x)*vals[ids[i]]/400;let d=mode==="deformable"?.015*Math.sin(.17*t+i):0;if(mode==="projected"){let [a,b,c2]=cells[ids[i]];d+=.002*(a-b+c2-1)}return (x+.04*Math.sin(.13*t+i)+c+d+tau)%tau})}
return {loss:loss/32,initial,final:p}}
let rows=[];function put(type,seed,pass,observation){rows.push({type,seed,pass,observation})}
for(const seed of seeds){let p=ledger(seed),e=inspect(p),p2=ledger(seed);
put("T1-replay",seed,JSON.stringify(p)===JSON.stringify(p2),{events:p.events.length});
put("T2-conservation",seed,e.length===0,{errors:e,arrivals:p.arrivals.length});
put("T3-fifo",seed,!e.includes("fifo"),{errors:e});
put("T4-exclusion",seed,!e.includes("overlap"),{errors:e});
put("T5-dwell",seed,!e.includes("dwell"),{errors:e});
let q=JSON.parse(JSON.stringify(p));let term=q.events.find(x=>x.k==="release"||x.k==="expire");if(term)q.events.push({...term});put("T6-duplicate-terminal",seed,!!term&&inspect(q).includes("duplicate_terminal"),{activated:!!term,errors:inspect(q)});
let m=JSON.parse(JSON.stringify(p));let ix=m.events.findIndex(x=>x.k==="arrival");if(ix>=0)m.events.splice(ix,1);put("T7-missing-arrival",seed,ix>=0&&inspect(m).includes("census"),{activated:ix>=0,errors:inspect(m)});
let frozen=[2,3,4].every(n=>{let x=ring(seed,n,"noop");return x.initial.every((v,i)=>v===x.final[i])});put("T8-noop-projection",seed,frozen&&new Set(cells.map(x=>x.join(","))).size===27,{frozen,cells:cells.length});
let losses={};for(let n of [2,3,4]){losses[n]={};for(let mode of ["noop","uncoupled","coupled","shuffled","deformable","projected"])losses[n][mode]=ring(seed,n,mode).loss}put("T9-ring-comparison",seed,Object.values(losses).every(x=>Object.values(x).every(Number.isFinite)),{losses});
let alt=ledger(seed,5),n1=p.events.filter(x=>x.k==="admit").length,n2=alt.events.filter(x=>x.k==="admit").length;put("T10-paired-intervention",seed,JSON.stringify(input(seed))===JSON.stringify(input(seed))&&JSON.stringify(p.events)!==JSON.stringify(alt.events),{dwell3_admits:n1,dwell5_admits:n2,delta:n2-n1,causal_scope:"queue throughput only, not learning"})}
let counts={};for(const row of rows){let c=counts[row.type]??={passed:0,total:0};c.total++;if(row.pass)c.passed++}return {schema:"echo-gpt-331-v1",seeds,counts,rows,limitations:["synthetic toy; no semantic intelligence","T9 descriptive, no held-out training","T10 paired intervention only, not predictive causality","oracle and generator co-located; independent review needed"]};
})()