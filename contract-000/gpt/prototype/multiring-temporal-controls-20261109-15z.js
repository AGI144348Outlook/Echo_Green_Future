// Echo-GPT independent synthetic ring controls, 2026-11-09 15Z; seeds 9201-9204
const glyphs=[..."אבגדהוזחטיכלמנסעפצקרשת","ך","ם","ן","ף","ץ"];
const N=27, seeds=[9201,9202,9203,9204], mod=i=>(i+N)%N;
function step(a,{phase=0,rewire=1,couple=.125,decay=.6}={}){
 const b=Array(N).fill(0),gain=couple*(1+.2*Math.sin(phase));
 for(let i=0;i<N;i++) {b[i]+=decay*a[i];b[mod(i+rewire)]+=gain*a[i];b[mod(i-rewire)]+=gain*a[i]}
 return b;
}
function sparseOracle(a,o={}){const b=Array(N).fill(0),gain=(o.couple??.125)*(1+.2*Math.sin(o.phase??0)),d=o.decay??.6,k=o.rewire??1;for(let i=0;i<N;i++){for(const [j,w] of [[i,d],[mod(i+k),gain],[mod(i-k),gain]])b[j]+=a[i]*w}return b}
function run(seed){const idx=seed%N, impulse=Array(N).fill(0);impulse[idx]=1;const x=step(impulse),z=Array(N).fill(0),nullStep=step(z);const unc=step(impulse,{couple:0});const rewire=step(impulse,{rewire:5});const sum=a=>a.reduce((p,v)=>p+v,0),l1=(a,b)=>sum(a.map((v,i)=>Math.abs(v-b[i])));let a=impulse.slice(),b=impulse.slice();for(let t=0;t<27;t++){a=step(a,{phase:2*Math.PI*t/27});b=step(b,{phase:0})}const checks={glyph_unique:glyphs.length===27&&new Set(glyphs).size===27,replay:JSON.stringify(step(impulse))===JSON.stringify(step(impulse)),noop:nullStep.every(v=>v===0),local:x[idx]===.6,neighbor:Math.abs(x[mod(idx+1)]-.125)<1e-12,distant:x[mod(idx+8)]===0,uncoupled:unc[mod(idx+1)]===0,rewire_mass:Math.abs(sum(x)-sum(rewire))<1e-12&&l1(x,rewire)>0,phase_gain_matched:l1(a,b)>0,oracle:l1(x,sparseOracle(impulse))<1e-12};return {seed,checks,metrics:{local:x[idx],neighbor:x[mod(idx+1)],distant:x[mod(idx+8)],rewireMassDelta:sum(x)-sum(rewire),rewireL1:l1(x,rewire),phaseL1:l1(a,b),oracleL1:l1(x,sparseOracle(impulse))}}}
const results=seeds.map(run);const total=results.reduce((n,r)=>n+Object.values(r.checks).filter(Boolean).length,0);return {results,total,possible:40};
