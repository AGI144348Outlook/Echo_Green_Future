// GPT-only synthetic experiment. Preregistered Issue #398. No external effects.
const N=27, SEEDS=[11,23,47,89];
const ids=Object.freeze(Array.from({length:N},(_,i)=>"G"+String(i).padStart(2,"0")));
const initial=(seed,rings)=>Array.from({length:rings},(_,k)=>Array.from({length:N},(_,i)=>({id:ids[i],mass:(0.2+((i*7+seed)%29)/29)/rings})));
const sum=a=>a.flat().reduce((s,x)=>s+x.mass,0);
const l1=(a,b)=>a.flat().reduce((s,x,i)=>s+Math.abs(x.mass-b.flat()[i].mass),0);
function simulate(seed,{rings=2,gain=.14,phase=0,freq=1,shuffle=false,knock=-1,reverse=true}={}){
 let a=initial(seed,rings), before=sum(a), originalIds=a.map(r=>r.map(x=>x.id));
 let permutation=Array.from({length:N},(_,i)=>i);
 if(shuffle){let s=seed;for(let i=N-1;i>0;i--){s=(1664525*s+1013904223)>>>0;let j=s%(i+1);[permutation[i],permutation[j]]=[permutation[j],permutation[i]];}}
 for(let t=0;t<9;t++){
  for(let k=0;k<rings;k++)for(let i=0;i<N;i++){
   if(i===knock)continue;
   let j=(permutation[i]+Math.floor(t*freq+phase))%N, next=(k+1)%rings;
   if(j===knock || (!reverse && k===rings-1))continue;
   let amount=a[k][i].mass*gain*(.6+.4*Math.sin((t+i+phase)*Math.PI/27)**2);
   a[k][i].mass-=amount;a[next][j].mass+=amount;
  }
 }
 return {a,before,after:sum(a),idsOk:a.every((r,k)=>r.every((x,i)=>x.id===originalIds[k][i]))&&new Set(ids).size===N,min:Math.min(...a.flat().map(x=>x.mass))};
}
function run(){
 let results=[];
 for(let seed of SEEDS){
  let b=simulate(seed), replay=simulate(seed),tri=simulate(seed,{rings:3}),noop=simulate(seed,{gain:0}),sh=simulate(seed,{shuffle:true}),ph=simulate(seed,{phase:7}),fr=simulate(seed,{freq:1.17}),ko=simulate(seed,{knock:0}),nr=simulate(seed,{reverse:false});
  let first=a=>a.a[0].reduce((s,x)=>s+x.mass,0);
  let measures={shuffle:l1(b.a,sh.a),phase:l1(b.a,ph.a),frequency:l1(b.a,fr.a),knockout:l1(b.a,ko.a),reverse:l1(b.a,nr.a),matchedRing0:first(tri)-first(b),massError2:b.after-b.before,massError3:tri.after-tri.before};
  let tests=[
   ["T1 replay",JSON.stringify(b.a)===JSON.stringify(replay.a)],
   ["T2 persistent identity",b.idsOk&&tri.idsOk],
   ["T3 two-ring conservation",Math.abs(measures.massError2)<1e-9&&b.min>=0],
   ["T4 matched-mass three-ring conservation",Math.abs(measures.massError3)<1e-9&&Math.abs(tri.before-b.before)<1e-9&&tri.min>=0],
   ["T5 no-op",l1(noop.a,initial(seed,2))<1e-12],
   ["T6 seeded shuffled routing",measures.shuffle>1e-8],
   ["T7 phase offset",measures.phase>1e-8],
   ["T8 frequency contrast",measures.frequency>1e-8],
   ["T9 matched-mass ring0 contrast",Math.abs(measures.matchedRing0)>1e-8],
   ["T10 reverse coupling intervention",measures.reverse>1e-8&&measures.knockout>1e-8]
  ];
  results.push({seed,measures,tests});
 }
 return {protocol:"issue-398",seeds:SEEDS,results,passed:results.flatMap(x=>x.tests).filter(x=>x[1]).length,total:40};
}
if(typeof module!=="undefined")module.exports={run,simulate,initial};