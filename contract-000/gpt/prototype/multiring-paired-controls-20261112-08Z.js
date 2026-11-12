// Echo-GPT independent 08Z controlled synthetic ring model. Node 18+; no dependencies.
// Seeds fixed, no semantic or physical claims. Pure deterministic computation.
function rng(seed){let x=seed>>>0;return ()=>((x=(Math.imul(x,1664525)+1013904223)>>>0)/4294967296);}
const N=27,SEEDS=[11,23,37,53];
function init(seed){const q=rng(seed);return Array.from({length:3},(_,r)=>Array.from({length:N},(_,i)=>({id:i,m:0.5+q(),p:q()*6.28318530718,w:(i%7-3)*0.017})))}
function affinity(shuffle=false){let a=Array.from({length:N},(_,i)=>(i%22+1)/22);if(shuffle){let q=rng(8128);for(let i=N-1;i>0;i--){let j=Math.floor(q()*(i+1));[a[i],a[j]]=[a[j],a[i]]}}return a}
function evolve(base,{gain=0.14,triad=true,shuffle=false,detune=false,boundary="relative",feedback=true,shift=0}={}){
 const a=affinity(shuffle),s=base.map(r=>r.map(n=>({...n,p:n.p+shift})));
 for(let t=0;t<8;t++){const old=s.map(r=>r.map(n=>({...n})));
 for(let r=0;r<3;r++){let delta=Array(N).fill(0);for(let i=0;i<N;i++){
 const n=old[r][i],j=old[(r+1)%3][i],k=old[(r+2)%3][(i+1)%N];
 const phase=triad?j.p+k.p-2*n.p:j.p-n.p;
 const radius=feedback?(boundary==="relative"?Math.cos(j.p-n.p):Math.cos(n.p)):0;
 const signal=gain*a[i]*(Math.sin(phase)+0.18*radius);
 delta[i]=signal*0.045;
 }for(let i=0;i<N;i++){const next=(i+1)%N;let d=delta[i];s[r][i].m-=d;s[r][next].m+=d}
 for(let i=0;i<N;i++)s[r][i].p+=old[r][i].w*(detune?(1+(i%5)*0.3):1)+0.005*gain*Math.sin(old[(r+1)%3][i].p-old[r][i].p);
 }}
 return s;
}
function dist(a,b){let v=0;for(let r=0;r<3;r++)for(let i=0;i<N;i++)v+=Math.abs(a[r][i].m-b[r][i].m);return v}
function total(a){return a.flat().reduce((v,n)=>v+n.m,0)}
function runAll(){let rows=[],passed=0,failed=0;for(const seed of SEEDS){let base=init(seed),x=evolve(base),same=evolve(init(seed));
 const checks=[
 ["replay",dist(x,same)<1e-12],
 ["identity",base.every(r=>new Set(r.map(n=>n.id)).size===27)],
 ["nonnegative",x.every(r=>r.every(n=>n.m>=0))],
 ["conservation",Math.abs(total(x)-total(base))<1e-9],
 ["zero_gain",dist(evolve(base,{gain:0}),evolve(base,{gain:0,triad:false,shuffle:true,boundary:"absolute"}))<1e-12],
 ["relative_shift",dist(x,evolve(base,{shift:0.71}))<1e-10],
 ["absolute_shift_breaks",dist(evolve(base,{boundary:"absolute"}),evolve(base,{boundary:"absolute",shift:0.71}))>1e-6],
 ["triad_pairwise",dist(x,evolve(base,{triad:false}))>1e-6],
 ["shuffled_affinity",dist(x,evolve(base,{shuffle:true}))>1e-6],
 ["detune_and_feedback",dist(x,evolve(base,{detune:true}))>1e-6&&dist(x,evolve(base,{feedback:false}))>1e-6]
 ];
 for(let [name,ok] of checks){rows.push({seed,test:name,pass:ok});ok?passed++:failed++}
 rows.push({seed,metrics:{triad_pairwise:dist(x,evolve(base,{triad:false})),shuffled:dist(x,evolve(base,{shuffle:true})),detune:dist(x,evolve(base,{detune:true})),boundary:dist(x,evolve(base,{feedback:false})),absolute_shift:dist(evolve(base,{boundary:"absolute"}),evolve(base,{boundary:"absolute",shift:0.71})),mass_error:total(x)-total(base)}})
 }return {passed,failed,rows};}
