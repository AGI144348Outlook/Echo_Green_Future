// T99 GPT-only synthetic experiment; Node: node gpt_experiments/T99_topologies.js
const glyphs=[..."אבגדהוזחטיכלמנסעפצקרשת",..."ךםןףץ"], vals=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];
const seeds=[11,23,37,53], tau=2*Math.PI;
function rng(seed){let s=seed>>>0;return ()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296;};}
function permutation(n,seed){const a=Array.from({length:n},(_,i)=>i),r=rng(seed);for(let i=n-1;i>0;i--){const j=Math.floor(r()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
function dist(a,b){return Math.abs(Math.atan2(Math.sin(a-b),Math.cos(a-b)));}
function effect(a,b){return a.reduce((s,x,i)=>s+dist(x,b[i]),0)/a.length;}
function unique(a){return a.length===27&&new Set(a).size===27;}
function validCoords(a){return a.length===27&&new Set(a.map(x=>x.join(","))).size===27&&a.every(x=>x.length===3&&x.every(v=>Number.isInteger(v)&&v>=0&&v<3));}
function simulate(seed,o={}){
 const r=rng(seed);let p=Array.from({length:27},()=>r()*tau);
 const v=o.shuffle?vals.map((_,i)=>vals[(i*11)%27]):vals;
 const perm=permutation(27,seed+997);
 for(let t=0;t<(o.steps??24);t++){
  const old=p.slice(),seats=old.map(x=>Math.floor(x/tau*27)%27);
  const counts=Array(27).fill(0);seats.forEach(x=>counts[x]++);
  const occupancy=seats.map(x=>counts[x]>1?1:0);
  const occ=o.permuteOccupancy?perm.map(i=>occupancy[i]):occupancy;
  const radius=1+(o.boundary?.2*Math.sin(t*.2):0);
  p=old.map((x,i)=>{
   const j=(i+(o.topology==="opposite"?13:1))%27,k=(i+2)%27;
   const pair=(o.pair||0)*Math.sin(old[j]-x)/(1+Math.abs(v[i]-v[j])/100);
   const tri=(o.tri||0)*Math.sin(old[j]+old[k]-2*x);
   const geom=(o.geometry||0)*occ[i]*.012*Math.cos(old[(i+3)%27]-x);
   const edge=(o.feedback||0)*(radius-1)*Math.sin(old[(i+9)%27]-x);
   return (x+.02+(o.detune===false?0:(i%7)*.003)+pair+tri+geom+edge+tau)%tau;
  });
 }
 return p;
}
function experiment(){
 const coords=Array.from({length:27},(_,i)=>[Math.floor(i/9),Math.floor(i/3)%3,i%3]);
 const rows=seeds.map(seed=>{
  const b=simulate(seed),pair=simulate(seed,{pair:.12}),tri=simulate(seed,{tri:.08});
  const near=simulate(seed,{pair:.12,topology:"nearest"}),opp=simulate(seed,{pair:.12,topology:"opposite"});
  const geom=simulate(seed,{geometry:1}),shuffled=simulate(seed,{geometry:1,permuteOccupancy:true});
  const metrics={topology:effect(near,opp),pair:effect(b,pair),tri:effect(b,tri),gematria:effect(pair,simulate(seed,{pair:.12,shuffle:true})),gemOff:effect(b,simulate(seed,{shuffle:true})),occupancy:effect(geom,shuffled),occupancyOff:effect(b,simulate(seed,{permuteOccupancy:true})),boundary:effect(b,simulate(seed,{boundary:true,feedback:.3})),boundaryOff:effect(b,simulate(seed,{boundary:true,feedback:0})),frequency:effect(b,simulate(seed,{detune:false})),topologyOff:effect(b,simulate(seed,{topology:"opposite"}))};
  const a=permutation(27,seed+997),sameMultiset=a.slice().sort((x,y)=>x-y).every((x,i)=>x===i);
  const checks={identity:unique(glyphs)&&!unique([...glyphs.slice(0,26),glyphs[0]]),projection:validCoords(coords)&&!validCoords([...coords.slice(0,26),coords[0]]),replay:effect(b,simulate(seed))===0,noop:effect(simulate(seed,{steps:0}),simulate(seed,{steps:0,pair:.12}))===0,topology:metrics.topology>0&&metrics.topologyOff===0,pair:metrics.pair>0,tri:metrics.tri>0,gematria:metrics.gematria>0&&metrics.gemOff===0,occupancy:sameMultiset&&metrics.occupancy>0&&metrics.occupancyOff===0,boundary:metrics.boundary>0&&metrics.boundaryOff===0};
  return {seed,checks,metrics};
 });
 return {version:"T99",seeds,tests:Object.keys(rows[0].checks),passed:rows.reduce((n,r)=>n+Object.values(r.checks).filter(Boolean).length,0),total:rows.length*Object.keys(rows[0].checks).length,rows};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(experiment(),null,2));
