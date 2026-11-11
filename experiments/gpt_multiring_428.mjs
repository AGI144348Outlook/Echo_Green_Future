// GPT-only synthetic multiring experiment, issue #428. Run with node experiments/gpt_multiring_428.mjs
const seeds=[11,23,37,53], N=27;
function sim(seed, mode="triad", opts={}){
 const mass=Array.from({length:3},(_,r)=>Array.from({length:N},(_,i)=>1+0.1*Math.sin(seed+i*1.7+r)));
 const phase=Array.from({length:3},(_,r)=>Array.from({length:N},(_,i)=>seed*.013+i*.19+r*.37+(opts.offset||0)));
 const original=mass.flat().reduce((a,b)=>a+b,0);
 for(let t=0;t<12;t++)for(let i=0;i<N;i++){
  const a=phase[0][i],b=phase[1][i],c=phase[2][i];
  const aff=opts.shuffle?1+((i*7+3)%N)/N:1+(i%9)/9;
  let delta=mode==="uncoupled"?0:mode==="pairwise"?.004*aff*Math.sin(b-a):.004*aff*Math.sin(b+c-2*a);
  if(opts.gain===0)delta=0;
  if(opts.ablate===i)delta=0;
  const boundary=opts.boundary?1+0.1*Math.sin(i*.5+t*.2):1;
  delta*=boundary;
  mass[0][i]+=delta;mass[1][i]-=delta;
 }
 return {mass,original};
}
function l1(a,b){return a.flat().reduce((s,v,i)=>s+Math.abs(v-b.flat()[i]),0)}
function agg(x){return Array.from({length:N},(_,i)=>x.mass.reduce((s,row)=>s+row[i],0))}
function run(seed){
 const x=sim(seed),y=sim(seed),base=sim(seed,"uncoupled"),pair=sim(seed,"pairwise");
 const shift=sim(seed,"triad",{offset:1.4}),nullgain=sim(seed,"triad",{gain:0});
 const shuffle=sim(seed,"triad",{shuffle:true}),ablate=sim(seed,"triad",{ablate:7}),boundary=sim(seed,"triad",{boundary:true});
 const external=Array.from({length:N},(_,i)=>1+0.05*Math.sin(919+i*.77)); // fixed exogenous seed, independent of model
 const mae=m=>agg(m).reduce((s,v,i)=>s+Math.abs(v/3-external[i]),0)/N;
 const metrics={seed,replay:l1(x.mass,y.mass),identity:x.mass.length===3&&x.mass.every(row=>row.length===27),mass_error:Math.abs(x.mass.flat().reduce((a,b)=>a+b,0)-x.original),zero_gain:l1(nullgain.mass,base.mass),common_phase:l1(shift.mass,x.mass),local:l1(ablate.mass,x.mass),shuffle:l1(shuffle.mass,x.mass),triad_pair:l1(x.mass,pair.mass),aggregate:agg(x).reduce((s,v,i)=>s+Math.abs(v-agg(base)[i]),0),boundary:l1(boundary.mass,x.mass),mae_triad:mae(x),mae_pair:mae(pair),mae_uncoupled:mae(base)};
 const predicates={replay:metrics.replay<1e-12,identity:metrics.identity,mass:metrics.mass_error<1e-10,null:metrics.zero_gain<1e-12,common_phase:metrics.common_phase<1e-10,local:metrics.local>1e-5,shuffle:metrics.shuffle>1e-5,triad_pair:metrics.triad_pair>1e-5,aggregate:metrics.aggregate<1e-10,independent_target:Number.isFinite(metrics.mae_triad)&&Number.isFinite(metrics.mae_uncoupled)};
 return {metrics,predicates};
}
const results=seeds.map(run);
if(typeof console!=="undefined")console.log(JSON.stringify({issue:428,seeds,results},null,2));
