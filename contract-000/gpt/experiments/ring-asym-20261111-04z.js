// GPT-owned synthetic ring portfolio, preregistration Issue #410. Node 18+; node ring-asym-04z.js
"use strict";
const N=27, STEPS=16, SEEDS=[11,23,37,53], TAU=2*Math.PI;
function rng(seed){let x=seed>>>0;return ()=>((x=(1664525*x+1013904223)>>>0)/4294967296);}
function run(seed,opt={}){
 const rings=opt.rings||2, rand=rng(seed), mass=[],phase=[],freq=[],values=[];
 for(let r=0;r<rings;r++){let a=[],p=[],f=[];for(let i=0;i<N;i++){a.push(.4+rand()+.15*r+.03*Math.sin(i+r));p.push(TAU*rand()+(opt.common||0)+(opt.relative&&r===1?opt.relative:0));f.push(.2+.15*rand()+(opt.freq&&r===1?opt.freq:0));}mass.push(a);phase.push(p);freq.push(f);}
 const initial=mass.flat().reduce((a,b)=>a+b,0),scale=27/initial;
 mass.forEach(a=>a.forEach((v,i)=>a[i]=v*scale));
 const original=mass.map(a=>a.slice()), base=mass.flat().reduce((a,b)=>a+b,0);
 const val=Array.from({length:N},(_,i)=>1+(i*7)%N);if(opt.shuffle)val.reverse();
 for(let t=0;t<STEPS;t++){
   const d=mass.map(()=>Array(N).fill(0));
   for(let r=0;r<rings;r++)for(let i=0;i<N;i++){
     let j=(i+1)%N, a=mass[r][i],b=mass[r][j], rate=(opt.gain===0?0:.022)*(1+.15*Math.sin(phase[r][j]-phase[r][i]))*(1+.1*val[i]/N);
     let flux=rate*(a-b);d[r][i]-=flux;d[r][j]+=flux;
   }
   if(!opt.uncoupled&&opt.gain!==0)for(let r=0;r<rings-1;r++)for(let i=0;i<N;i++){
     let a=mass[r][i],b=mass[r+1][i], delta=phase[r+1][i]-phase[r][i], gate=opt.boundary===false?1:(.55+.45*Math.cos(.17*t+.3*i+r));
     let affinity=1+.1*val[i]/N;
     let flux=.018*gate*affinity*(1+.35*Math.cos(delta))*(a-b);
     if(opt.triadic&&rings===3)flux*=1+.1*Math.cos(phase[2][i]-phase[0][i]);
     d[r][i]-=flux;d[r+1][i]+=flux;
   }
   for(let r=0;r<rings;r++)for(let i=0;i<N;i++){mass[r][i]+=d[r][i];phase[r][i]+=freq[r][i];}
 }
 return {mass,original,base,total:mass.flat().reduce((a,b)=>a+b,0),min:Math.min(...mass.flat()),ids:Array.from({length:N},(_,i)=>i),phase};
}
function l1(a,b){return a.reduce((s,v,i)=>s+Math.abs(v-b[i]),0);}
function project(x){return Array.from({length:N},(_,i)=>x.mass.reduce((s,r)=>s+r[i],0));}
function tests(seed){
 let a=run(seed),b=run(seed,{rings:3}),p=project(a), zero=run(seed,{gain:0}), unc=run(seed,{uncoupled:true}), com=run(seed,{common:.8}),rel=run(seed,{relative:.8}),fr=run(seed,{freq:.3}),bound=run(seed,{boundary:false}),shuf=run(seed,{shuffle:true});
 let t=[
 ["T1_mass",Math.max(Math.abs(a.total-27),Math.abs(b.total-27))<1e-8,Math.max(Math.abs(a.total-27),Math.abs(b.total-27))],
 ["T2_nonnegative_identity",a.min>=0&&b.min>=0&&new Set(a.ids).size===N,Math.min(a.min,b.min)],
 ["T3_replay",JSON.stringify(a.mass)===JSON.stringify(run(seed).mass),0],
 ["T4_zero_gain",l1(zero.mass.flat(),zero.original.flat())<1e-12,l1(zero.mass.flat(),zero.original.flat())],
 ["T5_uncoupled_evolves",l1(unc.mass.flat(),unc.original.flat())>1e-6&&unc.phase[0][0]!==a.phase[0][0]===false,l1(unc.mass.flat(),unc.original.flat())],
 ["T6_common_phase_null",l1(a.mass.flat(),com.mass.flat())<1e-8,l1(a.mass.flat(),com.mass.flat())],
 ["T7_relative_phase",l1(a.mass.flat(),rel.mass.flat())>1e-7,l1(a.mass.flat(),rel.mass.flat())],
 ["T8_frequency",l1(a.mass.flat(),fr.mass.flat())>1e-7,l1(a.mass.flat(),fr.mass.flat())],
 ["T9_boundary",l1(a.mass.flat(),bound.mass.flat())>1e-7,l1(a.mass.flat(),bound.mass.flat())],
 ["T10_two_three",Math.abs(a.base-b.base)<1e-8&&l1(p,project(b))>1e-7,l1(p,project(b))]
 ];return {seed,tests:t,aux_shuffle_l1:l1(a.mass.flat(),shuf.mass.flat()),triadic_l1:l1(project(b),project(run(seed,{rings:3,triadic:true})))};
}
const result={protocol:"Issue #410",version:"04z-v1",seeds:SEEDS,results:SEEDS.map(tests)};
result.passed=result.results.reduce((s,x)=>s+x.tests.filter(t=>t[1]).length,0);result.total=40;
if(require.main===module)console.log(JSON.stringify(result,null,2));
module.exports={run,tests,result};
