// GPT-only synthetic model. Prospective Issue #407. No external effects.
function run(seed,opts={}) {
 const N=27,R=opts.rings||2,ids=Array.from({length:N},(_,i)=>"glyph-"+i);
 let masses=Array.from({length:R},()=>Array.from({length:N},(_,i)=>(1+((i*7+seed)%11))/R));
 let phases=Array.from({length:R},(_,r)=>Array.from({length:N},(_,i)=>i*.11+r*.29+seed*.001+(opts.common||0)+(r===0&&i%3===0?(opts.relative||0):0)));
 const initial=masses.map(a=>a.slice()),start=masses.flat().reduce((a,b)=>a+b,0);
 for(let t=0;t<9;t++){
  for(let r=0;r<R;r++)for(let i=0;i<N;i++)phases[r][i]+=.06*(1+r*.1)+(opts.frequency||0)*(i+1)/N;
  if(opts.gain===0)continue;
  for(let r=0;r<R;r++)for(let i=0;i<N;i++){
   const j=(i+(opts.shuffle?7:1))%N,rr=(r+1)%R,a=masses[r][i];
   const coupling=.012*(opts.gain??1)*(1+.8*Math.sin(phases[r][i]-phases[rr][j]));
   const flow=Math.min(a,Math.max(0,coupling*a));masses[r][i]-=flow;masses[rr][j]+=flow;
  }
 }
 return {ids,masses,phases,initial,start,total:masses.flat().reduce((a,b)=>a+b,0)};
}
function tests(seed){
 const b=run(seed),replay=run(seed),noop=run(seed,{gain:0}),unc=run(seed,{gain:0,frequency:.2}),freq=run(seed,{frequency:.2}),relative=run(seed,{relative:.7}),common=run(seed,{common:.7}),shuf=run(seed,{shuffle:true}),three=run(seed,{rings:3});
 const flat=x=>x.masses.flat(),diff=(a,c)=>flat(a).reduce((s,v,i)=>s+Math.abs(v-flat(c)[i]),0);
 const initNode=x=>Array.from({length:27},(_,i)=>x.initial.reduce((s,r)=>s+r[i],0));
 const matched=initNode(b).every((v,i)=>Math.abs(v-initNode(three)[i])<1e-10);
 const metrics={frequency:diff(b,freq),relative:diff(b,relative),common:diff(b,common),shuffle:diff(b,shuf),massError:b.total-b.start,matched};
 return {seed,T1:JSON.stringify(b)===JSON.stringify(replay),T2:Math.abs(metrics.massError)<1e-8,T3:flat(b).every(v=>v>=0),T4:new Set(b.ids).size===27,T5:JSON.stringify(noop.masses)===JSON.stringify(noop.initial),T6:JSON.stringify(unc.masses)===JSON.stringify(unc.initial)&&JSON.stringify(unc.phases)!==JSON.stringify(noop.phases),T7:metrics.frequency>1e-7,T8:metrics.relative>1e-7&&metrics.common<1e-8,T9:metrics.shuffle>1e-7,T10:matched&&Math.abs(b.total-three.total)<1e-8,metrics};
}
console.log(JSON.stringify([11,23,37,53].map(tests),null,2));
