// GPT-only synthetic multiring experiment 16Z; issue #359 preregistered before execution.
// Run: node contract-000/gpt/experiments/multiring_16z.js
const glyphs=[..."אבגדהוזחטיכלמנסעפצקרשתךםןףץ"];
function indices(seed,t,ring,detune=false,reverse=false){let f=ring+1+(detune&&ring===1?0.37:0);return ((seed%27+Math.floor(t*f*(reverse&&ring===1?-1:1))+ring*5)%27+27)%27}
function word(seed,t,n,opt={}){return Array.from({length:n},(_,r)=>glyphs[indices(seed,t,r,!!opt.detune,!!opt.reverse)]).join("")}
function radius(seed,t,r,flex){return 1+r*.15+(flex?.04*Math.sin((seed+t+r)*.23):0)}
function vals(seed,t,opt={}){let a=Array.from({length:27},(_,i)=>Math.sin((seed%101+i*3+t)*.031)*.06);let out=a.map((v,i)=>v+(opt.coupled?0.025*a[(i+1)%27]:0)+(opt.gem?0.008*Math.sin(indices(seed,t,1,!!opt.detune,!!opt.reverse)+i):0));return out}
function mse(a,b){return a.reduce((s,v,i)=>s+(v-b[i])**2,0)/a.length}
function run(seed){let t=7,checks={};let w2=word(seed,t,2),w3=word(seed,t,3);let ref=(r)=>glyphs[((seed%27+Math.floor(t*(r+1))+5*r)%27+27)%27];
checks.T1=new Set(glyphs).size===27&&glyphs.length===27;
checks.T2=w2===ref(0)+ref(1);
checks.T3=w3===ref(0)+ref(1)+ref(2);
checks.T4=word(seed,t,3)!==word(seed,0,3);
checks.T5=[0,1,2].every(r=>radius(seed,t,r,true)>0.95+r*.15&&radius(seed,t,r,true)<1.05+r*.15);
checks.T6=word(seed,t,3,{reverse:true})!==w3;
checks.T7=word(seed,t,3,{detune:true})!==w3;
let base=vals(seed,t,{coupled:true,gem:true}),unc=vals(seed,t,{coupled:false,gem:true}),shuf=vals(seed,t,{coupled:true,gem:false}),noop=vals(seed,t,{coupled:false,gem:false});
checks.T8=base.some((v,i)=>Math.abs(v-shuf[i])>1e-8);
let perturb=(coupled)=>{let a=Array.from({length:27},(_,i)=>Math.sin((seed%101+i*3+t)*.031)*.06);a[13]+=.4;return a.map((v,i)=>v+(coupled?.025*a[(i+1)%27]:0))};
let p=perturb(true),q=perturb(false),a=vals(seed,t,{coupled:true,gem:false}),b=vals(seed,t,{coupled:false,gem:false});
checks.T9=Math.abs((p[12]-a[12])-.01)<1e-10&&Math.abs(p[0]-a[0])<1e-10&&Math.abs(q[12]-b[12])<1e-10;
let target=Array.from({length:27},(_,i)=>Math.sin((seed*17+i*7+19)*.019)*.012);
let scores={coupled:mse(base,target),uncoupled:mse(unc,target),shuffled:mse(shuf,target),noop:mse(noop,target)};
checks.T10=Object.values(scores).every(v=>Number.isFinite(v)&&v>=0);
return {seed,checks,passes:Object.values(checks).filter(Boolean).length,scores,neighbor_delta:p[12]-a[12],distant_delta:p[0]-a[0],uncoupled_neighbor_delta:q[12]-b[12]};
}
const results=[3301,3302,3303,3304].map(run);
if(typeof module!=="undefined")module.exports={run,results};
if(typeof console!=="undefined")console.log(JSON.stringify(results));
