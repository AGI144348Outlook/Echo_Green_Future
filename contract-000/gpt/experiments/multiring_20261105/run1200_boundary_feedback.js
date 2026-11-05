// Echo-GPT run1200. Synthetic offline controls, not canonical Echo.
const SEED=20261105, GLYPHS=[..."אבגדהוזחטיכלמנסעפצקרשתךםןףץ"];
const wrap=x=>((x%(2*Math.PI))+2*Math.PI)%(2*Math.PI);
const delta=(a,b)=>Math.abs(Math.atan2(Math.sin(a-b),Math.cos(a-b)));
function sim({rings=3,steps=16,coupling=.16,boundary=true,shuffle=false,perturb=0}={}){
 const p=Array.from({length:27},(_,i)=>wrap((i*17+SEED%101)*.037));
 const b=Array.from({length:27},(_,i)=>1+.15*Math.sin(i+SEED%17));
 p[0]+=perturb;
 for(let t=0;t<steps;t++){
   const old=p.slice();
   for(let i=0;i<27;i++){
     const prev=(i+26)%27, next=(i+1)%27;
     const affinity=shuffle?((i*7+3)%11+1)/12:((i*3+5)%11+1)/12;
     const feedback=boundary?b[i]:1;
     let force=0;
     for(let k=1;k<rings;k++)force+=Math.sin(old[(i+27-k)%27]-old[i])/(rings-1);
     p[i]=wrap(old[i]+.025+.004*(i%3)+coupling*affinity*feedback*force);
     if(boundary)b[i]=Math.max(.4,Math.min(1.6,b[i]+.015*Math.sin(old[next]-old[i])));
   }
 }
 return {phase:p,boundaries:b};
}
function gates(){
 const active=new Set(), components=new Map();
 const register=(origin,host,id)=>{const key=origin+":"+id;if(components.has(key))throw Error("duplicate");components.set(key,{origin,host,id})};
 const dispatch=(origin,id)=>{const c=components.get(origin+":"+id);return !!c&&active.has(origin)};
 register("פ",0,"grammar");register("ע",0,"classify");
 return {active,dispatch,components};
}
function run(){
 const base=sim(), again=sim(), two=sim({rings:2}), unc=sim({coupling:0}), uncPert=sim({coupling:0,perturb:.7});
 const pert=sim({steps:1,perturb:.7}), unpert=sim({steps:1});
 const frozen=sim({boundary:false}), shuffled=sim({shuffle:true}), g=gates();
 const inactive=!g.dispatch("פ","grammar");g.active.add("פ");
 const active=g.dispatch("פ","grammar"), isolated=!g.dispatch("ע","classify");
 const downstream=delta(pert.phase[1],unpert.phase[1]);
 const upstream=delta(pert.phase[26],unpert.phase[26]);
 const boundaryDelta=delta(base.phase[6],frozen.phase[6]);
 const shuffledDelta=delta(base.phase[6],shuffled.phase[6]);
 const checks=[
 ["27-addresses",GLYPHS.length===27&&new Set(GLYPHS).size===27],
 ["deterministic-replay",JSON.stringify(base)===JSON.stringify(again)],
 ["two-v-three-ring",delta(two.phase[6],base.phase[6])>1e-9],
 ["inactive-gate",inactive],
 ["active-gate",active],
 ["cross-origin-isolation",isolated],
 ["uncoupled-perturbation-null",delta(unc.phase[1],uncPert.phase[1])<1e-12],
 ["directed-one-step",downstream>1e-7&&upstream<1e-12],
 ["boundary-feedback-operative",boundaryDelta>1e-7],
 ["shuffled-affinity-measured",Number.isFinite(shuffledDelta)]
 ];
 return {seed:SEED,steps:16,tests:checks.map(([name,pass])=>({name,pass})),metrics:{downstream,upstream,boundaryDelta,shuffledDelta,uncoupled:delta(unc.phase[1],uncPert.phase[1])},passCount:checks.filter(x=>x[1]).length,total:checks.length,interpretation:"Synthetic programmed checks; not autonomous learning, semantic validation or authenticated A-000."};
}
if(typeof module!=="undefined")module.exports={run,sim,gates};
