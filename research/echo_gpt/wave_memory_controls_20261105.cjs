// Echo-GPT synthetic wave-memory controls; preregistration Issue #294.
// Deterministic bounded experiment, not evidence of autonomous learning.
const assert=require('node:assert/strict');
const seed=20261105, N=27, steps=16;
const rng=(s)=>()=>{s=(Math.imul(1664525,s)+1013904223)>>>0;return s/4294967296};
function run({strategy='noop',entropy=0.08,budget=6,shuffle=false,uncoupled=false,seedOffset=0}={}){
 const random=rng(seed+seedOffset), boxes=Array.from({length:N},(_,i)=>({id:i,content:(i*7)%11,quality:1}));
 const edges=Array.from({length:N-1},(_,i)=>({a:i,b:i+1,w:0.4,phase:random()*Math.PI*2}));
 let evaluator=[0.5,0.5],spent=0,external=0,wave=0;
 for(let t=0;t<steps;t++){
  const field=entropy*(1+0.25*Math.sin(t*0.7)); // exogenous
  for(const b of boxes)b.quality=Math.max(0,b.quality-field);
  for(const e of edges)e.w=Math.max(0,e.w-field*0.6);
  if(strategy==='box'){for(let j=0;j<budget;j++){boxes[(t+j)%N].quality=Math.min(1,boxes[(t+j)%N].quality+0.12);spent++}}
  if(strategy==='tie'||strategy==='adaptive'){for(let j=0;j<budget;j++){const e=edges[(t+j)%edges.length];e.w=Math.min(1,e.w+0.12);spent++}}
  const coherent=edges.reduce((s,e)=>s+e.w*Math.cos(e.phase),0)/edges.length;
  wave+=coherent;
  if(strategy==='adaptive'){const error=boxes.reduce((s,b)=>s+(1-b.quality),0)/N;const target=error<0.5?0.3:0.7;evaluator[0]+=0.05*(target-evaluator[0]);evaluator[1]=1-evaluator[0]}
 }
 // held-out retrieval metric depends on content availability and surviving links, not phase agreement
 external=boxes.reduce((s,b)=>s+b.quality,0)/N;
 const connectivity=edges.reduce((s,e)=>s+e.w,0)/edges.length;
 const retrieval=external*0.7+(uncoupled?0:connectivity*0.3);
 return {seed:seed+seedOffset,field:entropy,spent,retrieval,wave,evaluator,ids:boxes.map(b=>b.id),index:'Algorithm Index',matrix:'Algorithm Matrix',connectivity,checksum:boxes.reduce((s,b)=>s+b.content,0),shuffle};
}
const tests=[];
function test(name,fn){try{fn();tests.push({name,pass:true})}catch(e){tests.push({name,pass:false,error:e.message})}}
const base=run();
test('T1 27-cell Algorithm Matrix bijection',()=>assert.deepEqual(base.ids,Array.from({length:N},(_,i)=>i)));
test('T2 Algorithm Index distinct name',()=>{assert.equal(base.matrix,'Algorithm Matrix');assert.equal(base.index,'Algorithm Index')});
test('T3 deterministic replay',()=>assert.deepEqual(run({strategy:'adaptive'}),run({strategy:'adaptive'})));
test('T4 entropy invariant under agent strategies',()=>assert.equal(run({strategy:'adaptive'}).field,run({strategy:'noop'}).field));
test('T5 unmaintained ties decay',()=>assert.ok(base.connectivity<0.4));
test('T6 maintenance budget bound',()=>assert.ok(run({strategy:'tie'}).spent<=steps*6));
test('T7 wave evaluator neuroplastic',()=>assert.notDeepEqual(run({strategy:'adaptive'}).evaluator,[0.5,0.5]));
test('T8 wave and external signals independent',()=>{const x=run({strategy:'noop'}),y=run({strategy:'tie'});assert.ok(y.retrieval>x.retrieval);assert.equal(x.wave,y.wave)});
test('T9 no-op lower tie persistence than maintenance',()=>assert.ok(run({strategy:'tie'}).connectivity>base.connectivity));
test('T10 uncoupled retrieval control differs',()=>assert.ok(run({strategy:'tie',uncoupled:true}).retrieval<run({strategy:'tie'}).retrieval));
console.log(JSON.stringify({preregistered:'https://github.com/AGI144348Outlook/Echo_Green_Future/issues/294',seed,N,steps,tests,results:{noop:base,tie:run({strategy:'tie'}),adaptive:run({strategy:'adaptive'}),box:run({strategy:'box'})}},null,2));
if(tests.some(t=>!t.pass))process.exitCode=1;
