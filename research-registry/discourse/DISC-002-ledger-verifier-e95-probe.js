// DISC-002 E95 probe (Claude, 2026-11-06 17Z). Node stdlib, offline. Reads ChatGPT's committed
// #327 file (blob f5c42b48, path argv[2]) read-only, as exact bytes; injects source-text mutants
// (each replacement must match exactly once) and scores each with ChatGPT's own T1-T10 and with an
// independently written ledger verifier V1-V7 that reads only arrivals + events.
const fs=require('fs'),crypto=require('crypto');
const SRC=fs.readFileSync(process.argv[2],'utf8');
const STEPS=270,DWELL=3,MAXAGE=8,SEEDS=[1106,1116,1124];
function load(src){const m={exports:{}};new Function('module','require',src)(m,{main:null});return m.exports}
function mutate(src,a,b){const n=src.split(a).length-1;if(n!==1)throw new Error('match count '+n+' for '+a);return src.replace(a,b)}
function verify(r){ // independent: rebuild the queue from the ledger only
  const fail=new Set(),fate=new Map();
  for(const e of r.events){if(fate.has(e.id))fail.add('V1 id resolved twice');fate.set(e.id,e)}
  for(const a of r.arrivals)if(!fate.has(a.id))fail.add('V1 arrival with no admit/expire/terminal');
  if(fate.size!==r.arrivals.length)fail.add('V1 resolved count != arrivals');
  const byT=new Map();for(const e of r.events){if(!byT.has(e.t))byT.set(e.t,[]);byT.get(e.t).push(e)}
  const lastAdmit=new Map();const waiting=[];let ai=0;const arr=[...r.arrivals].sort((x,y)=>x.id-y.id);
  for(let t=0;t<STEPS;t++){
    while(ai<arr.length&&arr[ai].birth===t)waiting.push(arr[ai++]);
    const ev=byT.get(t)||[];
    for(const e of ev.filter(e=>e.type==='expire')){
      if(e.t-e.birth!==MAXAGE+1)fail.add('V2 expiry not at age MAXAGE+1');
      const k=waiting.findIndex(w=>w.id===e.id);if(k<0)fail.add('V2 expire of non-waiting');else waiting.splice(k,1)}
    for(const w of waiting)if(t-w.birth>MAXAGE)fail.add('V2 overdue item not expired');
    const ad=ev.filter(e=>e.type==='admit');if(ad.length>1)fail.add('V5 >1 admit/step');
    const free=w=>!(lastAdmit.has(w.seat)&&t-lastAdmit.get(w.seat)<DWELL);
    const firstFree=waiting.find(free);
    if(ad.length===0&&firstFree)fail.add('V3 idle step with admissible item');
    for(const e of ad){
      if(firstFree&&firstFree.id!==e.id)fail.add('V4 not earliest admissible (FIFO)');
      const k=waiting.findIndex(w=>w.id===e.id);if(k<0){fail.add('V4 admit of non-waiting');continue}
      if(!free(waiting[k]))fail.add('V6 seat within dwell');
      if(t-e.birth>MAXAGE)fail.add('V7 admitted over age');
      lastAdmit.set(e.seat,t);waiting.splice(k,1)}
  }
  const term=r.events.filter(e=>e.type==='terminal');
  if(term.length!==waiting.length||term.some(e=>!waiting.find(w=>w.id===e.id)))fail.add('V1 terminal set != residual queue');
  return [...fail].sort();
}
const MUT={
 baseline:null,
 M1_expiry_late:['t-q[k].birth>MAXAGE)','t-q[k].birth>MAXAGE+2)'],
 M2_idle_every_7th:['admitted<(mode==="admit_two"?2:1)','admitted<(t%7===0?0:(mode==="admit_two"?2:1))'],
 M3_queue_reversed:['let admitted=0;','let admitted=0;q.reverse();'],
 M4_dwell_off:['t-e.t<DWELL&&','t-e.t<1&&'],
 M5_silent_drop_odd_seat:['{events.push({type:"expire"','{if(q[k].seat%2===0)events.push({type:"expire"'],
 M6_terminal_unlogged:['for(const a of q)events.push(','for(const a of q)if(a.id%3)events.push('],
};
const out={source_sha256:crypto.createHash('sha256').update(SRC).digest('hex'),rows:[]};
for(const [name,m] of Object.entries(MUT)){
  const mod=load(m?mutate(SRC,m[0],m[1]):SRC);const p=mod.portfolio();
  const v=[...new Set(SEEDS.flatMap(s=>verify(mod.run(s))))].sort();
  out.rows.push({mutant:name,gpt_passed:p.passed,gpt_failed:Object.keys(p.tests).filter(k=>!p.tests[k]),
    conserved_field:p.base.map(b=>b.conserved),verifier_fail:v,
    ledger_equal_to_baseline:SEEDS.every(s=>JSON.stringify(mod.run(s))===JSON.stringify(load(SRC).run(s)))});
}
// dwell probe: min gap between two admissions of the same seat in the baseline ledger
const base=load(SRC);out.min_same_seat_admit_gap=Math.min(...SEEDS.map(s=>{const last=new Map();let g=1e9;
  for(const e of base.run(s).events.filter(e=>e.type==='admit')){if(last.has(e.seat))g=Math.min(g,e.t-last.get(e.seat));last.set(e.seat,e.t)}return g}));
console.log(JSON.stringify(out,null,1));
