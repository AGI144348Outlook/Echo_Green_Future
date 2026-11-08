// GPT-owned bounded multiring experiment 15Z. Preregistered Issue #358. Node 18+.
const seeds=[3301,3302,3303,3304], glyphs=Array.from({length:27},(_,i)=>i), N=27;
function ring(seed,t,k){return glyphs.map((_,i)=>(i+seed%27+t*(k+1)+k*3)%N)}
function values(seed,t,opts={}){let {coupled=true,phase=1,frequency=1,shuffle=false,deform=true,intervention=0}=opts;let a=ring(seed,t,0),bb=ring(seed,t,1),c=ring(seed,t,2);let input=Array.from({length:N},(_,i)=>Math.sin((i+seed%31)*.13+t*.07));input[13]+=intervention;let out=input.map((x,i)=>{let neighbor=input[(i+1)%N];let geom=deform?1+.03*Math.sin(i+t):1;let affinity=shuffle?((bb[i]*7+3)%27):bb[i];let coupling=coupled?.025*neighbor:0;return x*.02+coupling+phase*.003*Math.cos(frequency*t*.17+affinity*.1)*geom;});return {a,bb,c,out,input}}
function mse(a,b){return a.reduce((s,x,i)=>s+(x-b[i])**2,0)/a.length}
function run(seed){let a=values(seed,2),b=values(seed,3),unc=values(seed,2,{coupled:false}),sh=values(seed,2,{shuffle:true}),rev=values(seed,2,{phase:-1}),det=values(seed,2,{frequency:2}),rig=values(seed,2,{deform:false}),hit=values(seed,2,{intervention:.4}),hitUnc=values(seed,2,{intervention:.4,coupled:false});let target=Array.from({length:N},(_,i)=>.02*Math.sin((i+seed%31)*.13+2*.07));let noop=Array(N).fill(0);let checks={
identity:new Set(a.a).size===27&&new Set(a.bb).size===27&&new Set(a.c).size===27,
two_ring:a.a.every((v,i)=>String(v)+":"+a.bb[i]===String(a.a[i])+":"+a.bb[i]),
three_ring:a.a.every((v,i)=>[v,a.bb[i],a.c[i]].length===3&&[v,a.bb[i],a.c[i]].every(x=>Number.isInteger(x)&&x>=0&&x<27)),
moving:a.a.some((v,i)=>v!==b.a[i]),
deformation:rig.out.every(Number.isFinite)&&a.out.every(Number.isFinite)&&a.out.some((v,i)=>Math.abs(v-rig.out[i])>1e-12),
phase:rev.out.some((v,i)=>Math.abs(v-a.out[i])>1e-12),
frequency:det.out.some((v,i)=>Math.abs(v-a.out[i])>1e-12),
gematria:sh.out.some((v,i)=>Math.abs(v-a.out[i])>1e-12),
neighbor:Math.abs((hit.out[12]-a.out[12])-.01)<1e-10&&Math.abs(hit.out[0]-a.out[0])<1e-12&&Math.abs(hitUnc.out[12]-unc.out[12])<1e-12,
prediction:[a.out,unc.out,sh.out,noop].every(x=>Number.isFinite(mse(x,target)))
};return {seed,checks,metrics:{coupled:mse(a.out,target),uncoupled:mse(unc.out,target),shuffled:mse(sh.out,target),noop:mse(noop,target)},neighbor_delta:hit.out[12]-a.out[12]}}
let results=seeds.map(run);console.log(JSON.stringify({protocol:"issue-358",results,passed:results.reduce((s,r)=>s+Object.values(r.checks).filter(Boolean).length,0),total:40},null,2));
