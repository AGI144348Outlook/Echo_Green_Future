// Echo-GPT synthetic multiring portfolio; seed 20261105; ES2020; no external effects.
// The 27 positions are labels, NOT learned glyph semantics.
const glyphs=[..."אבגדהוזחטיכלמנסעפצקרשתךםןףץ"];
const mod=x=>((x%(2*Math.PI))+2*Math.PI)%(2*Math.PI);
const dist=(a,b)=>Math.abs(Math.atan2(Math.sin(a-b),Math.cos(a-b)));
function run({rings=2,coupling=.18,lag=0,deform=false,shuffle=false,perturb=0,common=0,steps=16,seed=20261105}={}){
 let s=seed>>>0; const rnd=()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296};
 let p=Array.from({length:27},(_,i)=>rnd()*2*Math.PI), w=Array.from({length:27},(_,i)=>.04+i*.001);
 let a=Array.from({length:27},(_,i)=>shuffle?((i*7)%27)+1:i+1);
 let radius=1;const initial=p.slice();
 for(let t=0;t<steps;t++){
  let next=p.slice();const scale=deform?radius:1;
  for(let i=0;i<27;i++){
   const prev=i===0?null:i-1;
   const input=prev===null?0:coupling*(a[prev]/27)*Math.sin(p[prev]-p[i]-lag)*scale;
   next[i]=mod(p[i]+w[i]+input+common*Math.sin(.2*t)+(i===1?perturb:0)+(rings-2)*.001*(i%3));
  }
  p=next;if(deform)radius=Math.max(.8,Math.min(1.2,radius+.015*Math.sin(p[1]-p[0])));
 }
 return {p,initial,radius};
}
function identity(x){return x.digest==="pinned-A000"&&x.origin==="EXTERNAL"&&x.permission==="EXECUTE"&&x.active===true}
function portfolio(){
 const base={steps:16,seed:20261105},a=run(base),again=run(base);
 const no=run({...base,steps:0}),unc=run({...base,coupling:0}),uncP=run({...base,coupling:0,perturb:.03});
 const two=run({...base,rings:2}),three=run({...base,rings:3});
 const chain=run({...base,perturb:.03}),shuf=run({...base,shuffle:true}),lag=run({...base,lag:.4}),deform=run({...base,deform:true});
 const shared=run({...base,common:.1,coupling:0});
 const metrics={positions:new Set(glyphs).size,replay:Math.max(...a.p.map((v,i)=>dist(v,again.p[i]))),noop:Math.max(...no.p.map((v,i)=>dist(v,no.initial[i]))),uncoupled_downstream:dist(unc.p[2],uncP.p[2]),ring_contrast:dist(two.p[2],three.p[2]),downstream:dist(a.p[2],chain.p[2]),upstream:dist(a.p[0],chain.p[0]),common_cause_joint_shift:dist(unc.p[2],shared.p[2]),shuffle:dist(a.p[2],shuf.p[2]),lag:dist(a.p[2],lag.p[2]),deform:dist(a.p[2],deform.p[2]),forged_accepted:identity({digest:"pinned-A000",origin:"SELF-DEPLOYED",permission:"EXECUTE",active:true}),unauthorized_accepted:identity({digest:"pinned-A000",origin:"EXTERNAL",permission:"READ",active:true}),valid_accepted:identity({digest:"pinned-A000",origin:"EXTERNAL",permission:"EXECUTE",active:true})};
 const tests={T1:metrics.positions===27,T2:metrics.replay===0,T3:metrics.noop===0,T4:metrics.uncoupled_downstream===0,T5:metrics.ring_contrast>0,T6:metrics.downstream>0&&metrics.upstream===0,T7:metrics.common_cause_joint_shift>0&&metrics.uncoupled_downstream===0,T8:metrics.shuffle>0,T9:metrics.lag>0&&metrics.deform>0,T10:!metrics.forged_accepted&&!metrics.unauthorized_accepted&&metrics.valid_accepted};
 return {seed:base.seed,steps:base.steps,metrics,tests,passed:Object.values(tests).filter(Boolean).length,total:10,limitations:["synthetic numerical model","common-cause test is illustrative, not statistical inference","identity is hard-coded, not cryptographic","ring arity uses a synthetic additive term"]};
}
return portfolio();
