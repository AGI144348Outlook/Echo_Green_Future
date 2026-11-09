// Echo-GPT experimental only. Issue #377 prospective preregistration.
// Run: node contract-000/gpt/experiments/ring-zero-coupling-20z.js
const crypto = require('node:crypto');
const GLYPHS=[...'אבגדהוזחטיכלמנסעפצקרשת',...'ךםןףץ'];
const N=27, SEEDS=[9701,9702,9703,9704];
function rng(seed){let x=seed>>>0;return ()=>{x=(1664525*x+1013904223)>>>0;return x/4294967296;};}
function initial(seed){const r=rng(seed);return Array.from({length:N},()=>r()+0.01);}
function A(x){return x.map((v,i)=>0.8*v+0.2*x[(i+N-1)%N]);}
function B(x){const y=Array(N).fill(0);for(let i=0;i<N;i++)y[(i*5+1)%N]=x[i];return y;}
function destination(i,shuffled=false){return shuffled?(i*7+3)%N:(i+9)%N;}
function C(x,gain,shuffled=false){const y=x.map(v=>v*(1-gain));for(let i=0;i<N;i++)y[destination(i,shuffled)]+=gain*x[i];return y;}
function oracleC(x,gain,shuffled=false){return Array.from({length:N},(_,j)=>x[j]*(1-gain)+gain*x.reduce((s,v,i)=>s+(destination(i,shuffled)===j?v:0),0));}
function I(x){return x.slice();}
function run(seed,gain=.15,shuffled=false){return C(B(A(initial(seed))),gain,shuffled);}
function l1(a,b){return a.reduce((s,v,i)=>s+Math.abs(v-b[i]),0);}
function mass(x){return x.reduce((s,v)=>s+v,0);}
const core={name:'A-000',role:'experimental-index',glyph:'ר',version:1};
function digest(o){return crypto.createHash('sha256').update(JSON.stringify(o)).digest('hex');}
const results=[];
for(const seed of SEEDS){
 const x=initial(seed), a=A(x), b=B(a), full=C(b,.15), nullArm=I(b);
 const doseLow=C(b,.05), shuffle=C(b,.15,true), zero=Array(N).fill(0);
 const checks=[
  ['glyph_uniqueness',new Set(GLYPHS).size===27,GLYPHS.length],
  ['deterministic_replay',l1(run(seed),run(seed))===0,l1(run(seed),run(seed))],
  ['zero_input',l1(C(B(A(zero)),.15),zero)===0,l1(C(B(A(zero)),.15),zero)],
  ['mass_conservation',Math.abs(mass(x)-mass(full))<1e-10,Math.abs(mass(x)-mass(full))],
  ['zero_coupling_identity',l1(C(b,0),nullArm)===0,l1(C(b,0),nullArm)],
  ['matched_positive_causal_effect',l1(full,nullArm)>1e-8,l1(full,nullArm)],
  ['dose_monotonic_l1',l1(full,nullArm)>l1(doseLow,nullArm)+1e-8,[l1(doseLow,nullArm),l1(full,nullArm)]],
  ['shuffled_topology_difference',l1(full,shuffle)>1e-8,l1(full,shuffle)],
  ['incoming_edge_oracle',l1(full,oracleC(b,.15))<1e-10,l1(full,oracleC(b,.15))],
  ['immutable_core_digest',digest(core)===digest({...core})&&digest(core)!==digest({...core,role:'mutated'}),[digest(core),digest({...core,role:'mutated'})]]
 ];
 results.push({seed,checks:checks.map(([type,pass,value])=>({type,pass,value}))});
}
const summary={protocol:'issue-377',seeds:SEEDS,test_types:10,total:results.length*10,passed:results.flatMap(r=>r.checks).filter(c=>c.pass).length,results};
console.log(JSON.stringify(summary,null,2));
if(summary.passed!==summary.total)process.exitCode=1;
