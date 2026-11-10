// GPT-only synthetic multiring, preregistered #405. No external effects.
function run(seed, opts={}) {
 const N=27,R=opts.rings||2, ids=Array.from({length:N},(_,i)=>"glyph-"+i);
 let masses=Array.from({length:R},(_,r)=>Array.from({length:N},(_,i)=>(1+((i*7+seed)%11))/R));
 let phases=Array.from({length:R},(_,r)=>Array.from({length:N},(_,i)=>(i*0.11+r*0.29+seed*0.001+(opts.offset||0))));
 const start=masses.flat().reduce((a,b)=>a+b,0),initial=masses.map(a=>a.slice());
 for(let t=0;t<9;t++){
   for(let r=0;r<R;r++) for(let i=0;i<N;i++) phases[r][i]+=0.06*(1+r*0.1)+(opts.frequency||0)*(i+1)/N;
   if(opts.gain===0)continue;
   for(let r=0;r<R;r++)for(let i=0;i<N;i++){
     const j=(i+(opts.shuffle?7:1))%N, rr=(r+1)%R;
     const a=masses[r][i], b=masses[rr][j];
     const coupling=0.012*(opts.gain??1)*(1+0.8*Math.sin(phases[r][i]-phases[rr][j]));
     const flow=Math.min(a,Math.max(0,coupling*a));
     masses[r][i]-=flow;masses[rr][j]+=flow;
   }
 }
 return {ids,masses,phases,initial,start,total:masses.flat().reduce((a,b)=>a+b,0)};
}
function L1(a,b){return a.masses.flat().reduce((s,v,i)=>s+Math.abs(v-b.masses.flat()[i]||0),0)}
function tests(seed){
 const b=run(seed), replay=run(seed), noop=run(seed,{gain:0}),unc=run(seed,{gain:0,frequency:0.2}),freq=run(seed,{frequency:0.2}),phase=run(seed,{offset:0.7}),shuf=run(seed,{shuffle:true}),three=run(seed,{rings:3});
 const flat=x=>x.masses.flat();
 const diff=(a,c)=>flat(a).reduce((s,v,i)=>s+Math.abs(v-flat(c)[i]),0);
 const initialNode=x=>Array.from({length:27},(_,i)=>x.initial.reduce((s,r)=>s+r[i],0));
 const matched=initialNode(b).every((v,i)=>Math.abs(v-initialNode(three)[i])<1e-10);
 const out={seed,T1:JSON.stringify(b)===JSON.stringify(replay),T2:Math.abs(b.total-b.start)<1e-8,T3:flat(b).every(v=>v>=0),T4:new Set(b.ids).size===27,T5:JSON.stringify(noop.masses)===JSON.stringify(noop.initial),T6:JSON.stringify(unc.masses)===JSON.stringify(unc.initial)&&JSON.stringify(unc.phases)!==JSON.stringify(noop.phases),T7:diff(b,freq)>1e-7,T8:diff(b,phase)>1e-7,T9:diff(b,shuf)>1e-7,T10:matched&&Math.abs(b.total-three.total)<1e-8,metrics:{frequency:diff(b,freq),phase:diff(b,phase),shuffle:diff(b,shuf),massError:b.total-b.start,matched,threeTotal:three.total}};
 return out;
}
JSON.stringify([11,23,37,53].map(tests));