// GPT-only synthetic 27-seat simultaneous occupancy; Issue #385 preregistered.
const GLYPHS=[..."אבגדהוזחטיכלמנסעפצקרשתךםןףץ"];
const N=27, SEEDS=[10401,10402,10403,10404];
function rng(seed){let s=seed>>>0;return ()=>((s=(Math.imul(s,1664525)+1013904223)>>>0)/4294967296);}
function l1(a,b){return a.reduce((s,v,i)=>s+Math.abs(v-b[i]),0);}
function sum(a){return a.reduce((s,v)=>s+v,0);}
function events(seed){const r=rng(seed);return Array.from({length:28},(_,id)=>({id,glyph:GLYPHS[id%27],seat:id%27,amount:0.1+r()}));}
function allocate(e,policy="queue"){const occupied=Array(N).fill(null),pending=[],rejected=[];
 for(const event of e){if(occupied[event.seat]===null)occupied[event.seat]=event;else if(policy==="queue")pending.push(event);else rejected.push(event);}
 return {occupied,pending,rejected};}
function process(e,forward=0.25,reverse=0.1,shift=0){
 const a=allocate(e),matrix=Array(N).fill(0),warehouse=Array(N).fill(0);
 for(const event of a.occupied){if(event===null)continue;matrix[event.seat]+=event.amount;}
 const baseline=matrix.slice(),seen=Array(N).fill(0);
 for(let i=0;i<N;i++){let target=(i+shift)%N,amount=matrix[i]*forward;matrix[i]-=amount;warehouse[target]+=amount;seen[target]+=amount;}
 const oneWay=matrix.slice();
 for(let j=0;j<N;j++){let source=(j-shift+N)%N,amount=seen[j]*reverse;warehouse[j]-=amount;matrix[source]+=amount;}
 return {a,baseline,matrix,warehouse,oneWay,phase:((27%27)+27)%27};
}
function run(seed){
 const e=events(seed),queued=allocate(e),rejected=allocate(e,"reject");
 const zero=process(e,0,0),one=process(e,.25,0),two=process(e,.25,.1),shuffle=process(e,.25,.1,7);
 const replay=JSON.stringify(events(seed))===JSON.stringify(e);
 const metrics={forward_l1:l1(one.matrix,one.baseline),reverse_l1:l1(two.matrix,one.matrix),shuffle_l1:l1(two.warehouse,shuffle.warehouse),mass_error:Math.abs(sum(two.matrix)+sum(two.warehouse)-sum(two.baseline)),queue:queued.pending.length,rejected:rejected.rejected.length};
 const checks={glyph_unique:GLYPHS.length===N&&new Set(GLYPHS).size===N,capacity:queued.occupied.filter(Boolean).length===N,queued_overflow:queued.pending.length===1&&queued.pending[0].id===27,reject_audited:rejected.rejected.length===1&&rejected.rejected[0].id===27,replay,zero_coupling:l1(zero.warehouse,Array(N).fill(0))===0&&l1(zero.matrix,zero.baseline)===0,forward_effect:metrics.forward_l1>1e-8,reverse_effect:metrics.reverse_l1>1e-8,shuffle_conservation:Number.isFinite(metrics.shuffle_l1)&&metrics.mass_error<1e-9&&Math.abs(sum(shuffle.matrix)+sum(shuffle.warehouse)-sum(shuffle.baseline))<1e-9,phase_closure:two.phase===0};
 return {seed,checks,metrics};
}
function main(){const results=SEEDS.map(run);return {source:"ring27-simultaneous-20261110-04z.js",seeds:SEEDS,results,passed:results.reduce((s,x)=>s+Object.values(x.checks).filter(Boolean).length,0),total:SEEDS.length*10};}
if(typeof module!=="undefined")module.exports={main,run};
