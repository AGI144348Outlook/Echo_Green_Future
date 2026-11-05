// GPT-owned offline multiring controls. No network or external effects. Seed 20261105.
const SEED=20261105, N=27, TAU=2*Math.PI;
const glyphs=[...'אבגדהוזחטיכלמנסעפצקרשתךםןףץ'];
const vals=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];
function rng(seed){let s=seed>>>0;return ()=>((s=(Math.imul(1664525,s)+1013904223)>>>0)/4294967296)}
function dist(a,b){return Math.abs(Math.atan2(Math.sin(a-b),Math.cos(a-b)))}
function run({coupling=.07,shuffle=false,perturb=0,rings=3,deform=false,steps=32}={}){
 const rand=rng(SEED), values=vals.slice();
 if(shuffle)for(let i=N-1;i>0;i--){let j=Math.floor(rand()*(i+1));[values[i],values[j]]=[values[j],values[i]]}
 let phases=Array.from({length:N},()=>rand()*TAU),radii=Array(N).fill(1);
 for(let t=0;t<steps;t++){
  const old=phases;phases=old.map((p,i)=>{const j=(i+1)%N, a=Math.max(values[i],values[j])%Math.min(values[i],values[j])===0?1:.2;
   const next=(p+.03*(i%5+1)+coupling*a*Math.sin(old[j]-p)+(t===0&&i===0?perturb:0)+TAU)%TAU;
   if(deform)radii[i]=Math.min(1.2,Math.max(.8,radii[i]+.005*Math.sin(next)));
   return next;});
 }
 const chosen=Array.from({length:rings},(_,k)=>glyphs[phases.reduce((best,p,i)=>dist(p,TAU*k/rings)<dist(phases[best],TAU*k/rings)?i:best,0)]);
 return {phases,radii,chosen};
}
function digest(s){let h=2166136261>>>0;for(const c of s){h=Math.imul(h^c.charCodeAt(0),16777619)>>>0}return h.toString(16).padStart(8,'0')}
const base=run(),noop=run({perturb:0}),unc=run({coupling:0}),uncDo=run({coupling:0,perturb:.4}),coupled=run({perturb:.4}),shuffled=run({shuffle:true}),deform=run({deform:true});
const deltas=base.phases.map((p,i)=>dist(p,coupled.phases[i]));
const cubes=Array.from({length:N},(_,i)=>[Math.floor(i/9),Math.floor(i/3)%3,i%3].join(','));
const oneBase=run({steps:1}),oneDo=run({steps:1,perturb:.4});
const definition={id:'A-000',schema:'v1',formula:'Alg-000=Alg-000+Alg-???'};
const canon=o=>JSON.stringify([o.schema,o.id,o.formula]);
const pin=digest(canon(definition)),tampered={...definition,formula:'modified'};
const checks={
 T1_deterministic_replay:JSON.stringify(base)===JSON.stringify(run()),
 T2_cube_bijection:new Set(cubes).size===27&&new Set(glyphs).size===27,
 T3_ring_arity:[2,3,4].every(n=>run({rings:n}).chosen.length===n),
 T4_noop_replay:JSON.stringify(base)===JSON.stringify(noop),
 T5_uncoupled_negative:unc.phases.slice(1).every((p,i)=>dist(p,uncDo.phases[i+1])<1e-10),
 T6_directed_downstream:deltas[26]>1e-8,
 T7_single_step_reverse_control:dist(oneBase.phases[1],oneDo.phases[1])<1e-10,
 T8_shuffle_measured:base.phases.reduce((s,p,i)=>s+dist(p,shuffled.phases[i]),0)>1e-8,
 T9_deformable_bounded:deform.radii.every(r=>r>=.8&&r<=1.2),
 T10_external_identity_pin:pin!==digest(canon(tampered))&&pin===digest(canon(definition))&&pin===digest(canon({...definition,unrelated:'new index'}))
};
return {seed:SEED,language:'JavaScript ES2020',steps:32,checks,pass:Object.values(checks).filter(Boolean).length,total:10,metrics:{directed_neighbor_delta:deltas[26],reverse_single_step_delta:dist(oneBase.phases[1],oneDo.phases[1]),shuffled_circular_L1:base.phases.reduce((s,p,i)=>s+dist(p,shuffled.phases[i]),0),external_pin_fnv1a32:pin,chosen:{independent:unc.chosen,coupled:base.chosen,shuffled:shuffled.chosen,deformable:deform.chosen}},limitations:['FNV1a32 is noncryptographic illustrative digest, not authorization','single-step reverse check cannot generalize to long horizons','shuffled difference not a performance metric','synthetic directed graph not causal discovery','27 glyph labels do not imply semantic competence']};
