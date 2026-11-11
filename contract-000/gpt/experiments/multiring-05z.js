// GPT-only experimental model; preregistered Issue #411 before execution.
// Run with Node: node contract-000/gpt/experiments/multiring-05z.js
const SEEDS=[11,23,37,53], N=27, TICKS=12;
const glyphs=[..."אבגדהוזחטיכלמנסעפצקרשתךםןףץ"];
const gem=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];
function simulate(seed,opts={}){
 const rings=opts.rings||3, gain=opts.gain===undefined?0.035:opts.gain;
 const mass=Array.from({length:rings},(_,r)=>Array.from({length:N},(_,i)=>r===0?0.7+((i*7+seed)%11)/40:r===1?0.3+((i*5+seed)%7)/50:0));
 const init=mass.flat();let phase=Array.from({length:rings},(_,r)=>Array.from({length:N},(_,i)=>((i*13+r*19+seed)%67)/67*6.283185307179586+(opts.common||0)+(opts.relative&&r===1?0.7:0)));
 const values=opts.shuffle?gem.map((_,i)=>gem[(i*7+3)%27]):gem;
 const freq=(r,i)=>0.01+0.001*(values[i]%17)+(opts.freq&&r===1?0.02:0);
 const total0=init.reduce((a,b)=>a+b,0);let maxErr=0,min=Infinity;
 for(let t=0;t<TICKS;t++){
  phase=phase.map((row,r)=>row.map((p,i)=>p+freq(r,i)));
  if(gain!==0){
   const delta=mass.map(row=>row.map(()=>0));
   for(let r=0;r<rings;r++)for(let i=0;i<N;i++){
    const j=(i+1)%N;
    const flux=gain*0.05*(mass[r][i]-mass[r][j])*(1+0.15*Math.cos(phase[r][i]-phase[r][j]));
    delta[r][i]-=flux;delta[r][j]+=flux;
   }
   for(let r=0;r<rings-1;r++)for(let i=0;i<N;i++){
    const gate=opts.boundary===false?1:0.5+0.5*Math.sin((i+t)/27*6.283185307179586)**2;
    const affinity=0.5+0.5*((values[i]%13)/13);
    const flux=gain*0.14*(mass[r][i]-mass[r+1][i])*gate*affinity*(1+0.3*Math.cos(phase[r][i]-phase[r+1][i]));
    delta[r][i]-=flux;delta[r+1][i]+=flux;
   }
   for(let r=0;r<rings;r++)for(let i=0;i<N;i++)mass[r][i]+=delta[r][i];
  }
  const all=mass.flat();min=Math.min(min,...all);maxErr=Math.max(maxErr,Math.abs(all.reduce((a,b)=>a+b,0)-total0));
 }
 return {projected:Array.from({length:N},(_,i)=>mass.reduce((a,row)=>a+row[i],0)),mass:mass.flat(),init,total0,maxErr,min,phase,ids:glyphs.join("")};
}
const l1=(a,b)=>a.reduce((s,x,i)=>s+Math.abs(x-b[i]),0);
function evaluate(seed){
 const base=simulate(seed), replay=simulate(seed), zero=simulate(seed,{gain:0}), unc=simulate(seed,{gain:0,freq:true}),common=simulate(seed,{common:1.234}),relative=simulate(seed,{relative:true}),freq=simulate(seed,{freq:true}),boundary=simulate(seed,{boundary:false}),two=simulate(seed,{rings:2}),shuffled=simulate(seed,{shuffle:true});
 const metrics={mass_error:base.maxErr,minimum_mass:base.min,replay_l1:l1(base.mass,replay.mass),zero_mass_l1:l1(zero.mass,zero.init),uncoupled_mass_l1:l1(unc.mass,unc.init),uncoupled_phase_difference:l1(unc.phase.flat(),zero.phase.flat()),common_l1:l1(base.projected,common.projected),relative_l1:l1(base.projected,relative.projected),frequency_l1:l1(base.projected,freq.projected),boundary_l1:l1(base.projected,boundary.projected),topology_l1:l1(base.projected,two.projected),shuffle_l1:l1(base.projected,shuffled.projected),matched_initial_mass:l1(two.init,base.init.slice(0,54)),identity_preserved:base.ids===glyphs.join("")};
 const checks={T1:base.maxErr<1e-8,T2:base.min>=-1e-10,T3:metrics.replay_l1===0&&metrics.identity_preserved,T4:metrics.zero_mass_l1===0,T5:metrics.uncoupled_mass_l1===0&&metrics.uncoupled_phase_difference>0,T6:metrics.common_l1<1e-8,T7:metrics.relative_l1>1e-8,T8:metrics.frequency_l1>1e-8,T9:metrics.boundary_l1>1e-8,T10:metrics.matched_initial_mass===0&&metrics.topology_l1>1e-8};
 return {seed,checks,metrics};
}
const results=SEEDS.map(evaluate);const pass=results.reduce((n,r)=>n+Object.values(r.checks).filter(Boolean).length,0);
const output={protocol:"https://github.com/AGI144348Outlook/Echo_Green_Future/issues/411",seeds:SEEDS,types:10,passed:pass,total:40,results};
if(typeof module!=="undefined")module.exports={simulate,evaluate,output};
if(typeof process!=="undefined"&&require.main===module)console.log(JSON.stringify(output,null,2));