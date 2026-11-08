// GPT-only 17Z independent diagnostic extension; preregistered Issue #360.
// Reuses 16Z model equations but adds independent mutation and identity controls.
const G=[..."אבגדהוזחטיכלמנסעפצקרשתךםןףץ"];
const idx=(s,t,r,delta=0)=>((s%27+Math.floor(t*(r+1+delta))+r*5)%27+27)%27;
const ring=(s,t,n,delta=0)=>Array.from({length:n},(_,r)=>G[idx(s,t,r,r===1?delta:0)]).join("");
const field=(s,t,couple,gem,shuffle=false)=>{const a=Array.from({length:27},(_,i)=>Math.sin((s%101+i*3+t)*.031)*.06);return a.map((v,i)=>v+(couple?.025*a[(i+1)%27]:0)+(gem?.008*Math.sin(idx(s,t,1)+(shuffle?(i*7+3)%27:i)):0));};
const mse=(a,b)=>a.reduce((v,x,i)=>v+(x-b[i])**2,0)/a.length;
function run(seed){const t=7,checks={};
checks.T1=G.length===27&&new Set(G).size===27;
checks.T2=ring(seed,t,2).length===2&&ring(seed,t,2)[0]===G[idx(seed,t,0)];
checks.T3=ring(seed,t,3).length===3&&ring(seed,t,3)[2]===G[idx(seed,t,2)];
checks.T4=ring(seed,t,3)!==ring(seed,0,3);
checks.T5=[0,1,2].every(r=>Math.abs(.04*Math.sin((seed+t+r)*.23))<=.04);
checks.T6=idx(seed,t,1)!==((seed%27+Math.floor(-t*2)+5)%27+27)%27;
checks.T7=ring(seed,t,3,.37)!==ring(seed,t,3);
const base=field(seed,t,true,true),unc=field(seed,t,false,true),shuf=field(seed,t,true,true,true),noop=field(seed,t,false,false);
checks.T8=base.some((v,i)=>Math.abs(v-shuf[i])>1e-9);
const a=Array.from({length:27},(_,i)=>Math.sin((seed%101+i*3+t)*.031)*.06), b=a.slice();b[13]+=.4;
const coupled=x=>x.map((v,i)=>v+.025*x[(i+1)%27]);
checks.T9=Math.abs(coupled(b)[12]-coupled(a)[12]-.01)<1e-12&&coupled(b)[0]===coupled(a)[0]&&b[12]===a[12];
const target=Array.from({length:27},(_,i)=>Math.sin((seed*17+i*7+19)*.019)*.012);
const scores={coupled:mse(base,target),uncoupled:mse(unc,target),shuffled:mse(shuf,target),noop:mse(noop,target)};
checks.T10=Object.values(scores).every(x=>Number.isFinite(x)&&x>=0);
return {seed,checks,passed:Object.values(checks).filter(Boolean).length,scores};}
const results=[3301,3302,3303,3304].map(run);
if(typeof module!=="undefined")module.exports={run,results};
if(typeof console!=="undefined")console.log(JSON.stringify(results));
