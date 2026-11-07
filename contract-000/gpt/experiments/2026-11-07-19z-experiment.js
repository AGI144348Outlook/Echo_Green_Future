// GPT-only 19Z bounded synthetic experiment. Run: node experiment.js
const seeds=[3301,3302,3303,3304], glyphs="אבגדהוזחטיכלמנסעפצקרשתךםןףץ".split("");
const xyz=Array.from({length:27},(_,i)=>[Math.floor(i/9),Math.floor(i/3)%3,i%3]);
const adj=(a,b)=>xyz[a].reduce((s,v,k)=>s+Math.abs(v-xyz[b][k]),0)===1;
function rng(seed){let s=seed>>>0;return ()=>((s=(1664525*s+1013904223)>>>0)/4294967296)}
function step(v,k){return v.map((x,i)=>x+k*xyz.reduce((s,_,j)=>s+(adj(i,j)?v[j]:0),0))}
function target(v){return v.map((x,i)=>0.8*x+0.17*xyz.reduce((s,_,j)=>s+(adj(i,j)?Math.tanh(v[j]):0),0)+0.03*Math.sin(i+x))}
function loss(a,b){return a.reduce((s,x,i)=>s+(x-b[i])**2,0)/27}
function run(seed){const random=rng(seed),v=Array.from({length:27},()=>random()*2-1), impulse=Array(27).fill(0);impulse[13]=1;
 const checks=[];
 checks.push(["bijection",new Set(xyz.map(x=>x.join(","))).size===27]);
 checks.push(["center_degree",xyz.filter((_,i)=>adj(13,i)).length===6]);
 checks.push(["replay",JSON.stringify(Array.from({length:5},()=>rng(seed)()))===JSON.stringify(Array.from({length:5},()=>rng(seed)()))]); // PRNG fresh per element, weak check; separate below
 checks[2]=["replay",JSON.stringify(step(v,.2))===JSON.stringify(step(v,.2))];
 checks.push(["noop",step(impulse,0)[13]===1&&step(impulse,0).filter(Boolean).length===1]);
 checks.push(["zero_coupling",loss(step(v,0),v)===0]);
 checks.push(["locality",step(impulse,.2).every((x,i)=>i===13?x===1:adj(i,13)?x===.2:x===0)]);
 const compose=n=>Array.from({length:n},(_,j)=>glyphs[Math.floor(random()*glyphs.length)]).join("");
 checks.push(["ring_arity",compose(2).length===2&&compose(3).length===3]);
 const gem=glyphs.map((_,i)=>i+1),shuffled=gem.slice().reverse();
 checks.push(["gematria_shuffle",gem.some((x,i)=>x!==shuffled[i])&&gem.reduce((a,b)=>a+b,0)===shuffled.reduce((a,b)=>a+b,0)]);
 const phases=[0,Math.PI/3,Math.PI/2], score=c=>phases.reduce((s,p,i)=>s+Math.cos(p+(c?phases[(i+1)%3]*.5:0)),0);
 checks.push(["phase_ablation",score(true)!==score(false)]);
 const truth=target(v),candidate=step(v,.17),noop=v,shuffle=step(v.slice().reverse(),.17);
 const scores={candidate:loss(candidate,truth),noop:loss(noop,truth),shuffled:loss(shuffle,truth)};
 checks.push(["heldout_oracle",Object.values(scores).every(Number.isFinite)]);
 return {seed,checks,scores,candidate_beats_noop:scores.candidate<scores.noop,candidate_beats_shuffle:scores.candidate<scores.shuffled};
}
console.log(JSON.stringify({version:"19z-v1",seeds,results:seeds.map(run)},null,2));
