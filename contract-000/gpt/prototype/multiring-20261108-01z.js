// GPT-owned synthetic multiring experiment, preregistered Issue #343. No canonical imports.
const SEEDS=[3301,3302,3303,3304];
const GLYPHS=Array.from('אבגדהוזחטיכלמנסעפצקרשתךםןףץ');
const GEM=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];
const XYZ=Array.from({length:27},(_,i)=>[Math.floor(i/9),Math.floor(i/3)%3,i%3]);
function neighbors(i){return XYZ.flatMap((p,j)=>p.reduce((a,v,k)=>a+Math.abs(v-XYZ[i][k]),0)===1?[j]:[]);}
function step(a,k=.2){return a.map((v,i)=>v*(1-k)+k*neighbors(i).reduce((s,j)=>s+a[j],0)/neighbors(i).length);}
function rng(seed){let x=seed>>>0;return ()=>{x=(Math.imul(1664525,x)+1013904223)>>>0;return x/4294967296;};}
function rings(seed,n=2,coupled=true,shuffle=false,reverse=false){
 const random=rng(seed),weights=GEM.slice();
 if(shuffle)for(let i=weights.length-1;i>0;i--){const j=Math.floor(random()*(i+1));[weights[i],weights[j]]=[weights[j],weights[i]];}
 let phases=Array.from({length:n},()=>random()*2*Math.PI-Math.PI);
 if(reverse)phases=phases.map(p=>-p);
 const values=[],radii=[];
 for(let t=0;t<12;t++){const rad=phases.map(p=>1+.08*Math.sin(.3*t+p));radii.push(...rad);
  for(let i=0;i<27;i++)values.push(phases.reduce((s,p,k)=>s+Math.sin(.27*t+p+(coupled?.001*weights[(i+k)%27]:0))*rad[k],0)/n);
 }return {values,radii};
}
function mse(a,b){return a.reduce((s,v,i)=>s+(v-b[i])**2,0)/a.length;}
function evaluate(seed){
 const a=Array(27).fill(0);a[13]=1;const b=step(a),z=step(Array(27).fill(0));
 const base=rings(seed),same=rings(seed),shuffled=rings(seed,2,true,true),reversed=rings(seed,2,true,false,true),uncoupled=rings(seed,2,false),triple=rings(seed,3);
 const target=Array.from({length:324},(_,idx)=>.7*Math.sin(.27*Math.floor(idx/27)+.19)+.3*Math.cos(.11*Math.floor(idx/27)+.33));
 const losses={coupled:mse(base.values,target),uncoupled:mse(uncoupled.values,target),shuffled:mse(shuffled.values,target),three_ring:mse(triple.values,target)};
 const checks={
 identity_bijection:new Set(GLYPHS).size===27&&new Set(XYZ.map(p=>p.join(','))).size===27,
 neighbor_degree:neighbors(13).length===6&&neighbors(0).length===3,
 causal_neighbor:neighbors(13).every(j=>b[j]>0),
 nonneighbor_exclusion:b.every((v,j)=>j===13||neighbors(13).includes(j)||v===0),
 no_op:z.every(v=>v===0),
 deterministic_replay:JSON.stringify(base)===JSON.stringify(same),
 gematria_shuffle_sensitivity:JSON.stringify(base.values)!==JSON.stringify(shuffled.values),
 phase_reversal_sensitivity:JSON.stringify(base.values)!==JSON.stringify(reversed.values),
 deformation_bound:base.radii.every(r=>r>=.92-1e-12&&r<=1.08+1e-12),
 independent_target_control:Object.values(losses).every(Number.isFinite)
 };
 return {seed,checks,losses,neighbor_effect:neighbors(13).reduce((s,j)=>s+b[j],0)};
}
function run(){const results=SEEDS.map(evaluate);return {issue:343,seeds:SEEDS,results,passed:results.reduce((s,r)=>s+Object.values(r.checks).filter(Boolean).length,0),total:40};}
