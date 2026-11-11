// GPT-owned synthetic multiring 21Z, Issue #427. Node-compatible JS, no dependencies.
const seeds=[11,23,37,53],N=27;
function run(seed,mode="triad",gain=.04,offset=0,shuffle=false,local=false){
 const phases=[.13,.71,1.29].map(x=>x+offset);
 const x=Array.from({length:3},(_,r)=>Array.from({length:N},(_,i)=>1+(r+1)*.02+((seed*13+i*17+r*7)%31)/100));
 const initial=x.map(a=>a.slice());
 for(let step=0;step<12;step++)for(let i=0;i<N;i++){
  const j=shuffle?(i*7+3)%N:i, a=phases[0],c=phases[1],d=phases[2];
  const k=mode==="triad"?Math.sin(c+d-2*a):mode==="pair"?Math.sin(c-a)+Math.sin(d-a):0;
  const impulse=gain*k*(.5+.5*Math.cos((j+1)*.17))+(local&&i===7?.003:0);
  const t=Math.max(-x[1][i]/2,Math.min(x[0][i]/2,impulse));
  x[0][i]-=t;x[1][i]+=t;
 }
 return {x,initial,projection:Array.from({length:N},(_,i)=>x[0][i]+x[1][i]+x[2][i])};
}
function l1(a,b){return a.flat().reduce((s,v,i)=>s+Math.abs(v-b.flat()[i]),0)}
function evaluate(){
 let records=[];for(const seed of seeds){
  const a=run(seed),p=run(seed,"pair"),z=run(seed,"none",0),s=run(seed,"triad",.04,0,true),loc=run(seed,"triad",.04,0,false,true),phase=run(seed,"triad",.04,1.2);
  const flat=a.x.flat(),mass0=a.initial.flat().reduce((x,y)=>x+y,0),mass1=flat.reduce((x,y)=>x+y,0);
  const forecast=a.projection.map((v,i)=>v+.05*Math.sin(seed*.31+i*.7)); // independent of model variant, no model-specific target
  const mae=q=>q.projection.reduce((t,v,i)=>t+Math.abs(v-forecast[i]),0)/N;
  const tests=[
  JSON.stringify(a)===JSON.stringify(run(seed)),
  a.x.length===3&&a.x.every(v=>v.length===27),
  flat.every(v=>v>=0),
  Math.abs(mass0-mass1)<1e-9,
  l1(a.x,phase.x)<1e-9,
  l1(a.x,p.x)>1e-5,
  l1(z.x,z.initial)<1e-9,
  l1(a.x,s.x)>1e-5,
  l1(a.x,loc.x)>1e-5,
  Number.isFinite(mae(a))&&Number.isFinite(mae(z))
  ];
  records.push({seed,tests,metrics:{triadPair:l1(a.x,p.x),shuffled:l1(a.x,s.x),local:l1(a.x,loc.x),massError:mass1-mass0,phaseError:l1(a.x,phase.x),maeTriad:mae(a),maeUncoupled:mae(z)}});
 }
 return {records,passed:records.flatMap(x=>x.tests).filter(Boolean).length,total:40};
}
if(typeof module!=="undefined")module.exports={run,evaluate};
