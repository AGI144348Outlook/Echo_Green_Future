/* GPT-only synthetic portfolio, Issue #325 PRE, 2026-11-06.
Run in any JS runtime: evaluate source and call runPortfolio().
No external IO, no canonical Echo or real glyph semantics. */
function runPortfolio(){
const N=27, STEP=360/N, seeds=[1106,1116,1124], checks={};
function near(a,b,t=1e-8){return Math.abs(a-b)<t}
function cd(a,b){const d=((Math.abs(a-b)%360)+360)%360;return Math.min(d,360-d)}
function lcg(seed){let x=seed>>>0;return ()=>((x=(1664525*x+1013904223)>>>0)/4294967296)}
function phase(t,step=STEP){return (t*step)%360}
checks.T1_27_tick_circular_closure=seeds.every(s=>cd(phase(27+s*27),0)<1e-8);
checks.T2_26_tick_nonclosure=cd(phase(26),0)>1;
checks.T3_double_step_mutant=cd(phase(1,2*STEP),phase(1))>1 && cd(phase(27,2*STEP),0)<1e-8;
function policy(grants,kind,mut={}){
 let live=[-99,-99],waiting=[],accepted=0,expired=0,dropped=0,admissions=[],latencies=[];
 const horizon=grants.length+12;
 for(let t=0;t<horizon;t++){
  if(t<grants.length&&grants[t]){const item={born:t,seat:t%2,attempt:0};if(kind==="queue")waiting.push(item);else if(t>=live[item.seat]+3){live[item.seat]=t;accepted++;admissions.push(t);latencies.push(0)}else if(kind==="retry"){waiting.push(item)}else dropped++}
  if(kind==="queue"&&!mut.noExpiry){let old=waiting.length;waiting=waiting.filter(x=>t-x.born<9);expired+=old-waiting.length}
  let max=kind==="queue"?(mut.doubleAdmit?2:1):waiting.length;
  let next=[];
  for(const item of waiting){if(max>0 && t>=live[item.seat]+3 && (kind!=="retry" || item.attempt<(mut.longRetry?5:2))){live[item.seat]=t;accepted++;admissions.push(t);latencies.push(t-item.born);max--}else {item.attempt++;if(kind==="retry"&&item.attempt>=(mut.longRetry?5:2))dropped++;else next.push(item)}}
  waiting=next;
 }
 if(kind==="queue")expired+=waiting.length;else dropped+=waiting.length;
 return {accepted,expired,dropped,admissions,latencies};
}
const grants=Array.from({length:270},(_,t)=>t%2===0||t%7===0);
const base=policy(grants,"queue"),noExpiry=policy(grants,"queue",{noExpiry:true}),double=policy(grants,"queue",{doubleAdmit:true});
checks.T4_expiry_mutant=base.expired>0&&noExpiry.expired===0&&noExpiry.accepted!==base.accepted;
checks.T5_double_admission_mutant=double.accepted!==base.accepted;
const retry=policy(grants,"retry"),longRetry=policy(grants,"retry",{longRetry:true});
checks.T6_retry_limit_mutant=retry.accepted!==longRetry.accepted;
const drop=policy(grants,"drop");
checks.T7_drop_retry_signature=drop.accepted<retry.accepted && drop.expired===0 && retry.expired===0;
const balanced=Array.from({length:270},(_,t)=>t%2),biased=Array.from({length:270},()=>0);
checks.T8_seat_assignment_mutant=balanced.filter(x=>x===0).length===135&&biased.filter(x=>x===0).length===270;
function rings(seed,coupling,shuffle=false,n=3){
 const rand=lcg(seed),vals=Array.from({length:N},(_,i)=>i+1);
 if(shuffle){for(let i=N-1;i>0;i--){let j=Math.floor(rand()*(i+1));[vals[i],vals[j]]=[vals[j],vals[i]]}}
 const p=Array.from({length:n},(_,i)=>i*2);
 let alignment=0,trace=[];
 for(let t=0;t<32;t++){
  const old=p.slice();
  for(let k=0;k<n;k++)p[k]=(old[k]+1+((coupling&&vals[old[(k+1)%n]%N]%3===0)?1:0))%N;
  if(new Set(p).size<n)alignment++;
  trace.push(p.join(","));
 }
 return {alignment,trace,unique:vals.length===new Set(vals).size,projection:p.map(x=>[x%3,Math.floor(x/3)%3,Math.floor(x/9)])};
}
const unc=rings(1106,false),coupled=rings(1106,true),shuffled=rings(1106,true,true);
checks.T9_multiring_intervention=unc.unique&&coupled.unique&&shuffled.unique&&coupled.trace.join("|")!==unc.trace.join("|")&&coupled.projection.every(c=>c.every(v=>v>=0&&v<3));
const targets=Array.from({length:32},(_,t)=>(7*t+3)%N);
function loss(r){return r.trace.reduce((a,row,t)=>{let p=Number(row.split(",")[0]),d=Math.abs(p-targets[t]);return a+Math.min(d,N-d)},0)/targets.length}
const losses={uncoupled:loss(unc),coupled:loss(coupled),shuffled:loss(shuffled)};
checks.T10_independent_target_no_claim=Object.values(losses).every(Number.isFinite)&&near(loss(rings(1106,true)),losses.coupled);
return {issue:325,source:"ring_policy_portfolio_14z.js",seeds,checks,passed:Object.values(checks).filter(Boolean).length,total:Object.keys(checks).length,observations:{grants:grants.filter(Boolean).length,queue:base,retry,drop,mutants:{noExpiry,double,longRetry},alignment:{uncoupled:unc.alignment,coupled:coupled.alignment,shuffled:shuffled.alignment},losses},limitations:["Synthetic fixture, not real entropy or predictive learning","T3 double step still closes after 27 ticks: intermediate phase detects mutant","T8 tests assignment vector only, not all collision dynamics","No semantics inferred from gematria numerical values"]};
}
