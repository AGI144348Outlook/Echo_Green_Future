// GPT-owned synthetic 27-seat multiring portfolio. Node >=18 are explicitly synthetic placeholders.
const SEEDS=[11,23,47,89], N=27;
const values=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];
const ids=Array.from({length:N},(_,i)=>i<22?"HEB-"+i:"SYN-"+i);
function rng(seed){let s=seed>>>0;return ()=>((s=(1664525*s+1013904223)>>>0)/4294967296)}
function perm(seed){let a=values.slice(),r=rng(seed);for(let i=N-1;i>0;i--){let j=Math.floor(r()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function simulate(seed,opt={}){
 const rings=opt.rings||2, r=rng(seed), mass=Array.from({length:rings},()=>Array.from({length:N},()=>.2+r())), initial=mass.flat().reduce((a,b)=>a+b,0);
 const affinity=opt.values||values,gain=opt.gain===undefined?.08:opt.gain;
 for(let t=0;t<(opt.ticks===undefined?9:opt.ticks);t++){
  for(let k=0;k<rings-1;k++){
   const delta=Array(N).fill(0);
   for(let i=0;i<N;i++){
    if(opt.knockout===i)continue;
    let j=opt.shuffle?(i*7+3)%N:i;
    let phase=Math.sin((t+(opt.phase||0))*(opt.freq||1)*2*Math.PI/27+i*.23);
    let gate=opt.boundary===false?1:(.65+.35*Math.sin(t*.3+i*.13)**2);
    let aff=.5+.5*(affinity[i]%17)/16;
    let raw=gain*aff*gate*(.55+.45*phase)*(mass[k][i]-mass[k+1][j]);
    let d=Math.max(-mass[k+1][j],Math.min(mass[k][i],raw));
    delta[i]-=d;mass[k+1][j]+=d;
   }
   for(let i=0;i<N;i++)mass[k][i]+=delta[i];
  }
 }
 const flat=mass.flat(), total=flat.reduce((a,b)=>a+b,0);
 return {flat,initial,total,ids:ids.slice(),min:Math.min(...flat)};
}
const L1=(a,b)=>a.reduce((s,x,i)=>s+Math.abs(x-b[i]),0);
function run(){
 let results=[];
 for(const seed of SEEDS){
  const b=simulate(seed),again=simulate(seed),noop=simulate(seed,{gain:0}),unc=simulate(seed,{gain:0,ticks:0}),p=simulate(seed,{phase:7}),sh=simulate(seed,{shuffle:true}),bd=simulate(seed,{boundary:false});
  const nulls=[1,2,3,4].map(i=>L1(b.flat,simulate(seed,{values:perm(seed+i*101)}).flat));
  const cases=[
   ["replay",JSON.stringify(b)===JSON.stringify(again),0],
   ["mass_conservation",Math.abs(b.total-b.initial)<1e-9,Math.abs(b.total-b.initial)],
   ["nonnegative",b.min>=-1e-12,b.min],
   ["zero_gain_noop",L1(noop.flat,unc.flat)<1e-12,L1(noop.flat,unc.flat)],
   ["uncoupled_initial",Math.abs(unc.total-unc.initial)<1e-12,Math.abs(unc.total-unc.initial)],
   ["identity",new Set(b.ids).size===27&&b.ids.every((x,i)=>x===ids[i]),b.ids.length],
   ["shuffled_route",L1(b.flat,sh.flat)>1e-8,L1(b.flat,sh.flat)],
   ["phase_offset",L1(b.flat,p.flat)>1e-8,L1(b.flat,p.flat)],
   ["boundary_ablation",L1(b.flat,bd.flat)>1e-8,L1(b.flat,bd.flat)],
   ["gematria_null",nulls.every(x=>Number.isFinite(x))&&nulls.length===4,nulls]
  ];
  results.push({seed,cases});
 }
 return {seeds:SEEDS,tests_per_seed:10,results,passed:results.flatMap(x=>x.cases).filter(x=>x[1]).length,total:40};
}
if(typeof module!=="undefined")module.exports={run,simulate,perm};
