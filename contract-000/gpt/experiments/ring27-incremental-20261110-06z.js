// GPT-only incremental ring queue. Prospective Issue #387. Pure JS, no effects.
const N=27, GLYPHS=[..."אבגדהוזחטיכלמנסעפצקרשתךםןףץ"], SEEDS=[10601,10602,10603,10604];
function rng(seed){let x=seed>>>0;return ()=>((x=(Math.imul(x,1664525)+1013904223)>>>0)/4294967296);}
function events(seed){let rand=rng(seed);return Array.from({length:54},(_,id)=>({id,seat:id%N,glyph:GLYPHS[id%N],amount:.1+rand(),arrival:id<18?0:id<36?2:5}));}
function service(seed){let es=events(seed), queues=Array.from({length:N},()=>[]),done=[],max=0,trace=[];for(let t=0;t<12;t++){for(let e of es.filter(e=>e.arrival===t))queues[e.seat].push(e);let active=queues.filter(q=>q.length).length;max=Math.max(max,active);trace.push({t,active,pending:queues.reduce((n,q)=>n+q.length,0)});for(let q of queues)if(q.length)done.push(q.shift());}return {es,done,queues,max,trace};}
function transfer(items,fwd,rev,shift){let m=Array(N).fill(0),w=Array(N).fill(0);for(let e of items)m[e.seat]+=e.amount;let before=m.slice();for(let i=0;i<N;i++){let v=m[i]*fwd;m[i]-=v;w[(i+shift)%N]+=v;}let oneWay=m.slice();for(let i=0;i<N;i++){let j=(i+shift)%N,v=w[j]*rev;w[j]-=v;m[i]+=v;}return {m,w,before,oneWay};}
function sum(a){return a.reduce((x,y)=>x+y,0);}function l1(a,b){return sum(a.map((v,i)=>Math.abs(v-b[i])));}
function run(seed){let s=service(seed), t=transfer(s.done,.25,.1,7),zero=transfer(s.done,0,0,7),one=transfer(s.done,.25,0,7);let ids=s.done.map(x=>x.id),pending=s.queues.flat();let perSeat=Array.from({length:N},(_,i)=>s.done.filter(e=>e.seat===i).map(e=>e.id));let checks=[
GLYPHS.length===27&&new Set(GLYPHS).size===27,
s.max<=27,
new Set(ids.concat(pending.map(e=>e.id))).size===54,
perSeat.every(a=>a.every((v,i)=>i===0||a[i-1]<v)),
s.done.length===54&&pending.length===0,
JSON.stringify(service(seed))===JSON.stringify(s),
l1(zero.m,zero.before)===0&&sum(zero.w)===0,
l1(t.m,zero.m)>0,
l1(t.m,one.m)>0,
Math.abs(sum(t.m)+sum(t.w)+sum(pending.map(e=>e.amount))-sum(s.es.map(e=>e.amount)))<1e-9&&Math.min(...t.m,...t.w)>=-1e-12
];return {seed,checks,metrics:{served:s.done.length,max:s.max,remaining:pending.length,forward_l1:l1(t.m,zero.m),reverse_l1:l1(t.m,one.m),mass_error:Math.abs(sum(t.m)+sum(t.w)-sum(s.es.map(e=>e.amount))),trace:s.trace}};}
const results=SEEDS.map(run); const report={protocol:"Issue #387",results,passed:results.reduce((n,r)=>n+r.checks.filter(Boolean).length,0),total:results.length*10};
if(typeof globalThis!=="undefined")globalThis.ECHO_GPT_REPORT=report;
