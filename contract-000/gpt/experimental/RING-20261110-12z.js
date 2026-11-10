// GPT-owned synthetic two/three-ring conservative experiment. No external effects.
const SEEDS=[11,23,47,89], N=27, STEPS=32;
function rng(seed){let s=seed>>>0;return ()=>{s=(1664525*s+1013904223)>>>0;return s/4294967296}}
function run(seed,mode="base"){
 const random=rng(seed), glyphs=Array.from({length:N},(_,i)=>i);
 let a=Array.from({length:N},()=>0.5+random()),b=Array.from({length:N},()=>0.5+random()),c=Array.from({length:N},()=>0.5+random());
 if(mode==="zero"){a.fill(0);b.fill(0);c.fill(0)}
 const init=a.concat(b,c), initial=init.reduce((x,y)=>x+y,0);
 const map=Array.from({length:N},(_,i)=>i);
 if(mode==="shuffle"){for(let i=N-1;i>0;i--){let j=Math.floor(random()*(i+1));[map[i],map[j]]=[map[j],map[i]]}}
 const k=mode==="uncoupled"||mode==="zero"?0:0.07;
 for(let t=0;t<STEPS;t++){
  for(let i=0;i<N;i++){if(mode==="knockout"&&i===0)continue;
   let j=map[i], d=k*(a[i]-b[j]);if(mode==="forward")d=Math.max(0,d);
   a[i]-=d;b[j]+=d;
  }
  if(mode==="three"||mode==="phase"){for(let i=0;i<N;i++){
   let j=(i+(mode==="phase"?1:0))%N;
   let d=0.035*(b[i]-c[j]);b[i]-=d;c[j]+=d;
  }}
 }
 const all=a.concat(b,c);
 return {glyphs,initial,total:all.reduce((x,y)=>x+y,0),min:Math.min(...all),state:all};
}
function l1(x,y){return x.reduce((s,v,i)=>s+Math.abs(v-y[i]),0)}
function tests(){
 let rows=[];
 for(const seed of SEEDS){
 const base=run(seed), replay=run(seed), unc=run(seed,"uncoupled"),zero=run(seed,"zero"),fwd=run(seed,"forward"),shuffle=run(seed,"shuffle"),knock=run(seed,"knockout"),three=run(seed,"three"),phase=run(seed,"phase");
 const checks=[
 ["T1",new Set(base.glyphs).size===N],
 ["T2",Math.max(...[base,unc,zero,fwd,shuffle,knock,three,phase].map(x=>Math.abs(x.total-x.initial)))<1e-9],
 ["T3",Math.min(...[base,unc,zero,fwd,shuffle,knock,three,phase].map(x=>x.min))>=-1e-12],
 ["T4",l1(base.state,replay.state)===0],
 ["T5",l1(unc.state,run(seed,"uncoupled").state)===0],
 ["T6",zero.total===0],
 ["T7",l1(base.state,fwd.state)>1e-8],
 ["T8",l1(base.state,shuffle.state)>1e-8],
 ["T9",l1(base.state,knock.state)>1e-8],
 ["T10",l1(three.state,phase.state)>1e-8]
 ];
 rows.push({seed,checks,differences:{forward:l1(base.state,fwd.state),shuffle:l1(base.state,shuffle.state),knockout:l1(base.state,knock.state),phase:l1(three.state,phase.state)},massError:Math.abs(base.total-base.initial)});
 }
 return rows;
}
return {run,tests};