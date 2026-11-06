// GPT-only noncanonical experiment, 2026-11-06 16Z. Pre-registered Issue #327.
// Node/JS stdlib only; deterministic arithmetic; independent ledger reconstruction.
const seeds=[1106,1116,1124], STEPS=270, DWELL=3, MAXAGE=8;
function run(seed,mode="baseline"){
 let state=seed>>>0;const rand=()=>{state=(Math.imul(1664525,state)+1013904223)>>>0;return state/4294967296};
 const q=[],events=[],arrivals=[];let id=0;
 for(let t=0;t<STEPS;t++){
  for(let draw=0;draw<2;draw++)if(rand()<0.54){
   const a={id:id++,birth:t,seat:(id*7)%27};q.push(a);arrivals.push(a);
  }
  if(mode!=="expiry_off")for(let k=q.length-1;k>=0;k--)if(t-q[k].birth>MAXAGE){events.push({type:"expire",t,id:q[k].id,birth:q[k].birth,seat:q[k].seat});q.splice(k,1)}
  let admitted=0;
  for(let k=0;k<q.length && admitted<(mode==="admit_two"?2:1);){
   const a=q[k],busy=events.some(e=>e.type==="admit"&&e.seat===a.seat&&t-e.t<DWELL&&t>=e.t);
   if(!busy){events.push({type:"admit",t,id:a.id,birth:a.birth,seat:a.seat});q.splice(k,1);admitted++}else k++;
  }
 }
 for(const a of q)events.push({type:"terminal",t:STEPS,id:a.id,birth:a.birth,seat:a.seat});
 return {seed,mode,arrivals,events};
}
function inspect(r){
 const ad=r.events.filter(e=>e.type==="admit"),ex=r.events.filter(e=>e.type==="expire"),terminal=r.events.filter(e=>e.type==="terminal");
 const counts=new Map(), seats=new Map();let overlap=0,maxAge=0;
 for(const e of ad){counts.set(e.t,(counts.get(e.t)||0)+1);maxAge=Math.max(maxAge,e.t-e.birth);const last=seats.get(e.seat);if(last!==undefined&&e.t-last<DWELL)overlap++;seats.set(e.seat,e.t)}
 return {arrivals:r.arrivals.length,accepted:ad.length,expired:ex.length,terminal:terminal.length,waited:ad.filter(e=>e.t>e.birth).length,maxAge,maxPerStep:Math.max(0,...counts.values()),overlap,conserved:r.arrivals.length===ad.length+ex.length+terminal.length};
}
function trajectory(seed,mode){
 let x=seed%27,y=(seed+7)%27;const out=[];
 for(let t=0;t<81;t++){const delta=mode==="coupled"?((x+y+t)%5):mode==="shuffled"?((x*7+t)%5):0;x=(x+1+delta)%27;y=(y+2+(mode==="coupled"?x%3:0))%27;out.push(x)}
 return out;
}
function loss(a){return a.reduce((s,x,i)=>s+Math.min(Math.abs(x-((i*11+3)%27)),27-Math.abs(x-((i*11+3)%27))),0)/a.length}
function portfolio(){
 const base=seeds.map(s=>inspect(run(s))), expiry=inspect(run(1106,"expiry_off")),two=inspect(run(1106,"admit_two"));
 const u=trajectory(1106,"uncoupled"),c=trajectory(1106,"coupled"),sh=trajectory(1106,"shuffled");
 const tests={
 T1:base.every(v=>v.arrivals>STEPS),T2:base.every(v=>v.waited>0),T3:base.every(v=>v.expired>0),
 T4:base.every(v=>v.maxPerStep<=1),T5:base.every(v=>v.maxAge<=MAXAGE),
 T6:expiry.maxAge>MAXAGE,T7:two.maxPerStep>1,T8:base.every(v=>v.overlap===0),
 T9:JSON.stringify(run(1106))===JSON.stringify(run(1106)),
 T10:JSON.stringify(c)!==JSON.stringify(u)&&JSON.stringify(sh)!==JSON.stringify(u)&&[loss(c),loss(u),loss(sh)].every(Number.isFinite)
 };
 return {tests,passed:Object.values(tests).filter(Boolean).length,base,expiry,two,losses:{coupled:loss(c),uncoupled:loss(u),shuffled:loss(sh)}};
}
if(typeof module!=="undefined")module.exports={run,inspect,portfolio};
if(typeof process!=="undefined"&&typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(portfolio(),null,2));
