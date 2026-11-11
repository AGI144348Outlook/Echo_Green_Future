// Echo-GPT only. Issue #422 preregistered before execution. Node/V8, no dependencies.
"use strict";
const seeds=[11,23,37,53], n=27, budget=0.12, steps=12;
const glyphs=Array.from({length:n},(_,i)=>i+1);
function initial(seed){let a=Array.from({length:3},(_,r)=>Array.from({length:n},(_,i)=>0.5+((seed*17+i*13+r*7)%29)/29));let sum=a.flat().reduce((x,y)=>x+y,0);return a.map(row=>row.map(x=>x/sum));}
function edges(mode){return mode==="path"?[[0,1],[1,2]]:mode==="triangle"?[[0,1],[1,2],[0,2]]:[[0,1],[1,2],[0,2]];}
function simulate(seed,mode="triangle",opt={}) {
 const state=initial(seed), start=initial(seed), phases=[0.1,0.7,1.5], freq=[0.02,0.04,0.07], gain=opt.zero?0:budget;
 const e=edges(mode), each=gain/e.length, affine=Array.from({length:n},(_,i)=>opt.shuffle?glyphs[(i*7+3)%n]:glyphs[i]);
 for(let t=0;t<steps;t++){for(let i=0;i<n;i++){let moves=[];for(let k=0;k<e.length;k++){let [a,b]=e[k];let delta=((opt.commonPhase||0)+phases[b]+(opt.relative&&b===2?0.37:0)+freq[b]*(opt.frequency&&b===2?1.6:1)*t)-((opt.commonPhase||0)+phases[a]+freq[a]*t);
 let c=Math.cos(delta), affinity=0.4+affine[i]/54, deform=opt.boundary?1+0.2*Math.sin(i+t):1;
 let flux=each*c*affinity*deform*(state[a][i]-state[b][i]);
 moves.push([a,b,flux]);}
 for(let [a,b,flux] of moves){state[a][i]-=flux;state[b][i]+=flux;}}}
 return {state,start,projected:Array.from({length:n},(_,i)=>state[0][i]+state[1][i]+state[2][i])};
}
const flat=x=>x.state.flat(), l1=(a,b)=>a.reduce((s,x,i)=>s+Math.abs(x-b[i]),0), mass=x=>x.reduce((a,b)=>a+b,0);
function target(seed){let s=initial(seed);return s.map(row=>row.map((_,i)=>row[(i+1)%n])).flat();}
function mae(a,b){return l1(a,b)/a.length;}
function tests(seed){
 const base=simulate(seed), f=flat(base), replay=flat(simulate(seed)), zero=simulate(seed,"triangle",{zero:true}), init=initial(seed).flat();
 const path=simulate(seed,"path"),triad=simulate(seed,"triad");
 const metrics={
 replay:l1(f,replay), conservation:Math.abs(mass(f)-1), minimum:Math.min(...f),
 commonPhase:l1(f,flat(simulate(seed,"triangle",{commonPhase:0.7}))),
 zero:l1(flat(zero),init),
 shuffle:l1(f,flat(simulate(seed,"triangle",{shuffle:true}))),
 relative:l1(f,flat(simulate(seed,"triangle",{relative:true}))),
 frequency:l1(f,flat(simulate(seed,"triangle",{frequency:true}))),
 boundary:l1(f,flat(simulate(seed,"triangle",{boundary:true}))),
 pathDifference:l1(f,flat(path)),triadDifference:l1(f,flat(triad)),
 heldout:{uncoupled:mae(flat(zero),target(seed)),path:mae(flat(path),target(seed)),triangle:mae(f,target(seed)),triad:mae(flat(triad),target(seed))}
 };
 const predicates={replay:metrics.replay<1e-12,conservation:metrics.conservation<1e-9,nonnegative:metrics.minimum>=0,commonPhase:metrics.commonPhase<1e-9,zero:metrics.zero<1e-12,shuffle:metrics.shuffle>1e-10,relative:metrics.relative>1e-10,frequency:metrics.frequency>1e-10,boundary:metrics.boundary>1e-10,heldout:Number.isFinite(metrics.heldout.triangle)&&Number.isFinite(metrics.heldout.uncoupled)};
 return {seed,metrics,predicates};
}
const result={protocol:"issue-422",source:"Echo-GPT capacity matched v1",seeds,tests:seeds.map(tests)};
result.passed=result.tests.reduce((n,t)=>n+Object.values(t.predicates).filter(Boolean).length,0);
result.total=seeds.length*10;
if(typeof module!=="undefined"&&module.exports)module.exports={simulate,tests,result};
if(typeof process!=="undefined"&&process.stdout)process.stdout.write(JSON.stringify(result,null,2)+"\n");
