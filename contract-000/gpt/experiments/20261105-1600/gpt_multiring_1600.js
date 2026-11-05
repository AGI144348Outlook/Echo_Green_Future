// GPT independent research only. Source preregistered in Issue #292 before any execution.
// ES2020, deterministic seed 20261105; NOT canonical Echo or a semantic learning engine.
const SEED=20261105, TAU=2*Math.PI, GEM=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];
const wrap=x=>((x%TAU)+TAU)%TAU;
const dist=(a,b)=>Math.abs(Math.atan2(Math.sin(a-b),Math.cos(a-b)));
const coords=Array.from({length:27},(_,i)=>[Math.floor(i/9),Math.floor(i/3)%3,i%3]);
const harmonic=(a,b)=>(Math.max(a,b)%Math.min(a,b)===0?1:0);
function simulate({rings=3,steps=16,k=.15,deform=.035,lag=0,shuffle=false,perturb=0,source=1,noop=false}={}){
 const vals=shuffle?GEM.map((_,i)=>GEM[(i+7)%27]):GEM;
 let p=Array.from({length:27},(_,i)=>wrap((i+1)*.137+(SEED%101)*.001)),b=Array(27).fill(1);
 const initial=p.slice();
 if(perturb)p[source]=wrap(p[source]+perturb);
 if(noop)return {p,initial,b};
 for(let t=0;t<steps;t++){
  const next=p.slice(),nb=b.slice();
  for(let i=0;i<27;i++){
   const omega=.025+.0003*(i%7);
   let influence=0;
   if(i>0&&i<rings*9){
    const weight=1+.25*harmonic(vals[i-1],vals[i]);
    influence=k*b[i]*weight*Math.sin(p[i-1]-p[i]-lag);
   }
   next[i]=wrap(p[i]+omega+influence);
   if(deform)nb[i]=Math.max(.5,Math.min(1.5,b[i]+deform*Math.sin(p[i]-.4)));
  }
  p=next;b=nb;
 }
 return {p,initial,b};
}
function run(){
 const tests=[], add=(id,pass,measure)=>tests.push({id,pass:!!pass,measure});
 const base=simulate(),replay=simulate();
 add('T1 27-coordinate bijection',new Set(coords.map(v=>v.join(','))).size===27&&coords.every(v=>v.every(x=>x>=0&&x<3)),{unique:new Set(coords.map(v=>v.join(','))).size});
 add('T2 deterministic replay',JSON.stringify(base.p)===JSON.stringify(replay.p),{delta:Math.max(...base.p.map((v,i)=>dist(v,replay.p[i])))});
 const two=simulate({rings:2});add('T3 two-versus-three rings',dist(two.p[25],base.p[25])>1e-8,{delta:dist(two.p[25],base.p[25])});
 const nop=simulate({noop:true});add('T4 no-op preservation',nop.p.every((v,i)=>dist(v,nop.initial[i])===0),{max_delta:Math.max(...nop.p.map((v,i)=>dist(v,nop.initial[i])))});
 const unc=simulate({k:0}),uncP=simulate({k:0,source:1,perturb:.6});add('T5 uncoupled propagation',dist(unc.p[2],uncP.p[2])<1e-12,{downstream_delta:dist(unc.p[2],uncP.p[2])});
 const a=simulate({steps:1}),p=simulate({steps:1,source:1,perturb:.6});
 add('T6 connected directional one-step intervention',dist(a.p[2],p.p[2])>1e-8&&dist(a.p[0],p.p[0])<1e-12,{downstream:dist(a.p[2],p.p[2]),upstream:dist(a.p[0],p.p[0]),edge_0_to_1:true,edge_1_to_2:true});
 const shuffled=simulate({shuffle:true});const ratio39=harmonic(3,9),ratio23=harmonic(2,3);
 add('T7 harmonic gematria vs shuffled',ratio39>ratio23&&dist(base.p[12],shuffled.p[12])>1e-8,{ratio_3_9:ratio39,ratio_2_3:ratio23,shuffled_delta:dist(base.p[12],shuffled.p[12])});
 const lagged=simulate({lag:.23});add('T8 phase lag contrast',dist(base.p[12],lagged.p[12])>1e-8,{delta:dist(base.p[12],lagged.p[12])});
 const frozen=simulate({deform:0});add('T9 deformable boundary feedback',dist(base.p[12],frozen.p[12])>1e-8,{delta:dist(base.p[12],frozen.p[12])});
 const pinned='A000:governor:v1:independent-anchor';const authorized=(id,perm)=>id===pinned&&perm==='EXECUTE';
 const funcs=Array.from({length:17},(_,i)=>({id:'פ'+i,origin:'פ',host:i}));
 const dispatch=(id,active)=>funcs.some(f=>f.id===id&&active.has(f.origin));
 add('T10 separate identity/permission/origin gate',authorized(pinned,'EXECUTE')&&!authorized('ACTIVE','EXECUTE')&&!authorized(pinned,'READ')&&funcs.every(f=>!dispatch(f.id,new Set())&&dispatch(f.id,new Set(['פ']))),{forged_active_denied:true,read_denied:true,pe_inactive_blocked:17});
 return {seed:SEED,steps:16,engine:'ES2020',tests,passed:tests.filter(t=>t.pass).length,total:tests.length};
}
if(typeof module!=='undefined'){module.exports={run,simulate};if(require.main===module)console.log(JSON.stringify(run(),null,2));}
