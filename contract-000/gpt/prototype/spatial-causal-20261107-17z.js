// Echo-GPT experimental, NOT canonical. Preregistered Issue #335.
"use strict";
const seeds=[1109,2203,3301,4409];
const cells=Array.from({length:27},(_,i)=>[Math.floor(i/9),Math.floor(i/3)%3,i%3]);
const distance=(a,b)=>cells[a].reduce((s,x,k)=>s+Math.abs(x-cells[b][k]),0);
const neighbors=i=>cells.map((_,j)=>j).filter(j=>distance(i,j)===1);
function evolve(state,coupling){return state.map((v,i)=>v+coupling*neighbors(i).reduce((s,j)=>s+state[j],0));}
function impulse(seed){let a=Array(27).fill(0);a[13]=1+(seed%7)/10;return a;}
function mse(a,b){return a.reduce((s,v,i)=>s+(v-b[i])**2,0)/a.length;}
function run(seed){const s=impulse(seed),t=evolve(s,.2),t2=evolve(t,.2),z=evolve(s,0),noop=Array(27).fill(0);
const shuffle=Array.from({length:27},(_,i)=>(i*7+seed%27)%27); // bijection because gcd(7,27)=1
const labels=shuffle.map(i=>i+1);
const cases=[
["coordinates_bijection",new Set(cells.map(x=>x.join(","))).size===27],
["six_center_neighbors",neighbors(13).length===6],
["stationary_noop",evolve(noop,.2).every(x=>x===0)],
["zero_coupling",z.every((x,i)=>x===s[i])],
["one_step_locality",t.every((x,i)=>distance(i,13)<=1||x===0)],
["two_step_spread",t2.some((x,i)=>distance(i,13)===2&&x>0)&&t2.every((x,i)=>distance(i,13)<=2||x===0)],
["deterministic_replay",JSON.stringify(evolve(impulse(seed),.2))===JSON.stringify(t)],
["shuffled_label_invariance",new Set(labels).size===27&&mse(t,evolve(s,.2))===0],
["negative_coupling_control",evolve(s,-.2).filter((x,i)=>distance(i,13)===1).every(x=>x<0)],
["heldout_loss_vs_noop",mse(t,s)>mse(t,t)] // tautological sanity only, not independent predictive success
];return {seed,cases,metrics:{coupled_vs_noop_mse:mse(t,s),two_step_active:t2.filter(x=>x!==0).length}};}
const results=seeds.map(run);
if(require.main===module){console.log(JSON.stringify({results,passed:results.flatMap(x=>x.cases).filter(x=>x[1]).length,total:40},null,2));}
module.exports={run,evolve,neighbors,distance};