// GPT-only synthetic 27-seat conservative multi-ring study. Node.js stdlib-free.
const SEEDS=[11,23,47,89], N=27;
function init(seed,rings){return Array.from({length:rings},(_,k)=>Array.from({length:N},(_,i)=>0.1+((i*7+k*11+seed)%29)/29));}
function mass(a){return a.flat().reduce((s,v)=>s+v,0)}
function dist(a,b){return a.flat().reduce((s,v,i)=>s+Math.abs(v-b.flat()[i]),0)}
function evolve(seed,{rings=2,gain=.18,phase=0,freq=1,shuffle=false,knock=-1,steps=9}={}){
 const a=init(seed,rings), before=mass(a);
 for(let t=0;t<steps;t++){
  for(let k=0;k<rings;k++)for(let i=0;i<N;i++){
   if(i===knock)continue;
   const target=(i+(shuffle?((seed%13)+1):0)+Math.floor((t*freq+phase)%N))%N;
   if(target===knock)continue;
   const next=(k+1)%rings;
   const delta=a[k][i]*gain*(.5+.5*Math.sin((t+i+phase)*Math.PI/27)**2);
   a[k][i]-=delta;a[next][target]+=delta;
  }
 }
 return {a,before,after:mass(a),min:Math.min(...a.flat())};
}
function run(){
 const out=[];
 for(const seed of SEEDS){
 const base=evolve(seed,{}), tri=evolve(seed,{rings:3}), no=evolve(seed,{gain:0,steps:9}), init2=init(seed,2);
 const replay=evolve(seed,{}), shuffled=evolve(seed,{shuffle:true}), phase=evolve(seed,{phase:7}),freq=evolve(seed,{freq:1.17}),knock=evolve(seed,{knock:0});
 const tests=[
 ["T1 deterministic replay",JSON.stringify(base.a)===JSON.stringify(replay.a),0],
 ["T2 27-seat identity projection",base.a.length===2&&base.a.every(x=>x.length===27)&&new Set(Array.from({length:27},(_,i)=>i)).size===27,27],
 ["T3 two-ring mass conservation",Math.abs(base.after-base.before)<1e-9,base.after-base.before],
 ["T4 three-ring mass conservation",Math.abs(tri.after-tri.before)<1e-9,tri.after-tri.before],
 ["T5 zero-gain no-op",dist(no.a,init2)<1e-12,dist(no.a,init2)],
 ["T6 shuffled routing contrast",dist(base.a,shuffled.a)>1e-8,dist(base.a,shuffled.a)],
 ["T7 phase-offset contrast",dist(base.a,phase.a)>1e-8,dist(base.a,phase.a)],
 ["T8 frequency mismatch contrast",dist(base.a,freq.a)>1e-8,dist(base.a,freq.a)],
 ["T9 three vs two rings contrast",Math.abs(tri.a[0].reduce((s,v)=>s+v,0)-base.a[0].reduce((s,v)=>s+v,0))>1e-8,tri.a[0].reduce((s,v)=>s+v,0)-base.a[0].reduce((s,v)=>s+v,0)],
 ["T10 knockout contrast",dist(base.a,knock.a)>1e-8,dist(base.a,knock.a)]
 ];
 out.push({seed,tests,min:Math.min(base.min,tri.min,shuffled.min,phase.min,freq.min,knock.min),massErrorMax:Math.max(...[base,tri,shuffled,phase,freq,knock].map(x=>Math.abs(x.after-x.before)))});
 }
 return out;
}
if(typeof module!=="undefined")module.exports={run,evolve,init};
