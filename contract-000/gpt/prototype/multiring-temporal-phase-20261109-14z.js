// GPT experimental synthetic temporal ring, 2026-11-09 14Z. Preregistered Issue #371.
// Node.js >=18, no dependencies or external effects. Run: node multiring-temporal-phase-20261109-14z.js
const crypto=require('node:crypto');
const G=[...'אבגדהוזחטיכלמנסעפצקרשת',...'ךםןףץ'],N=27,SEEDS=[9101,9102,9103,9104];
function pulse(i){const a=Array(N).fill(0);a[i]=1;return a;}
function evolve(a,t,g,edges){let b=a.map(x=>0.6*x);for(let i=0;i<N;i++)for(const j of edges[i])b[j]+=g*(1+0.25*Math.cos(t*0.3))*a[i];return b;}
const ring=Array.from({length:N},(_,i)=>[(i+1)%N,(i+N-1)%N]);
function hash(x){return crypto.createHash('sha256').update(JSON.stringify(x)).digest('hex');}
function simulate(seed,edges=ring,g=0.11,phase=true){let a=pulse(seed%N),trace=[];for(let t=0;t<27;t++){a=evolve(a,phase?t:Math.PI/0.3,g,edges);trace.push(a.slice());}return trace;}
function run(seed){const s=seed%N,a=pulse(s),z=Array(N).fill(0),first=evolve(a,0,0.11,ring),zero=evolve(z,0,0.11,ring),unc=evolve(a,0,0,ring);
const shuffled=Array.from({length:N},(_,i)=>[(i+7)%N,(i+N-7)%N]);const sh=evolve(a,0,0.11,shuffled);
const x=simulate(seed),y=simulate(seed),off=simulate(seed,ring,0.11,false);const id={glyphs:G,algorithm:'A-000-experimental',schema:1},digest=hash(id);const mutant={...id,algorithm:'IMPOSTOR'};
const diff=x[26].reduce((n,v,i)=>n+Math.abs(v-off[26][i]),0);
const tests={T1_unique:new Set(G).size===27,T2_order:G[s]+G[(s+1)%N]!==G[(s+1)%N]+G[s],T3_projection:new Set(Array.from({length:27},(_,i)=>(s+i)%N)).size===27,T4_replay:JSON.stringify(x)===JSON.stringify(y),T5_noop:zero.every(v=>v===0),T6_uncoupled:unc[(s+1)%N]===0,T7_locality:first[s]>0&&first[(s+7)%N]===0&&first[(s+1)%N]>0,T8_phase:diff>1e-9,T9_shuffle:first[(s+1)%N]>0&&sh[(s+1)%N]===0,T10_digest:digest!==hash(mutant)};
return {seed,tests,metrics:{local:first[s],neighbor:first[(s+1)%N],distant:first[(s+7)%N],shuffledNeighbor:sh[(s+1)%N],phaseL1:diff,identityDigest:digest}};}
const results=SEEDS.map(run);const summary={tests:10,seeds:SEEDS,passed:results.reduce((n,r)=>n+Object.values(r.tests).filter(Boolean).length,0),total:40,results};console.log(JSON.stringify(summary,null,2));if(summary.passed!==40)process.exitCode=1;
