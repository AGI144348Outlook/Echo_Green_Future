// T97 GPT-only synthetic multiring: run with Node.js: node gpt_experiments/T97_seat_occupancy.js
const glyphs=[..."אבגדהוזחטיכלמנסעפצקרשת",..."ךםןףץ"];
const vals=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];
const seeds=[11,23,37,53], tau=2*Math.PI;
const dist=(a,b)=>Math.abs(Math.atan2(Math.sin(a-b),Math.cos(a-b)));
const effect=(a,b)=>a.reduce((s,x,i)=>s+dist(x,b[i]),0)/a.length;
const unique=a=>a.length===27&&new Set(a).size===27;
const validCoords=a=>a.length===27&&new Set(a.map(x=>x.join(","))).size===27&&a.every(x=>x.length===3&&x.every(v=>Number.isInteger(v)&&v>=0&&v<3));
function simulate(seed,o={}){
 let s=seed>>>0;const rand=()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296};
 let p=Array.from({length:27},()=>rand()*tau),v=o.shuffle?vals.map((_,i)=>vals[(i*11)%27]):vals;
 const steps=o.steps??24;
 for(let t=0;t<steps;t++){
  const old=p.slice(),radius=1+(o.boundary?.2*Math.sin(t*.2):0);
  // Quantized ring-seat occupation: 27 positions, collisions resolved by glyph-index order.
  const seats=old.map(x=>Math.floor(((x%tau)+tau)%tau/tau*27));
  const counts=Array(27).fill(0);seats.forEach(x=>counts[x]++);
  const occupied=seats.map(x=>counts[x]>1?1:0);
  const occupancy=o.shuffleSeats?occupied.map((_,i)=>occupied[(i*11)%27]):occupied;
  p=old.map((x,i)=>{
   const j=(i+1)%27,k=(i+2)%27;
   const pair=(o.pair||0)*Math.sin(old[j]-x)/(1+Math.abs(v[i]-v[j])/100);
   const tri=(o.tri||0)*Math.sin(old[j]+old[k]-2*x);
   const geom=(o.geometry||0)*occupancy[i]*.012*Math.cos(old[(i+3)%27]-x);
   const edge=(o.feedback||0)*(radius-1)*Math.sin(old[(i+9)%27]-x);
   return (x+(o.detune===false?.02:.02+(i%7)*.003)+pair+tri+geom+edge+tau)%tau;
  });
 }
 return p;
}
function experiment(){
 const coords=Array.from({length:27},(_,i)=>[Math.floor(i/9),Math.floor(i/3)%3,i%3]);
 const rows=seeds.map(seed=>{
 const b=simulate(seed),same=simulate(seed);
 const pair=effect(b,simulate(seed,{pair:.12})),tri=effect(b,simulate(seed,{tri:.08}));
 const gem=effect(simulate(seed,{pair:.12}),simulate(seed,{pair:.12,shuffle:true}));
 const gemOff=effect(b,simulate(seed,{shuffle:true}));
 const freq=effect(b,simulate(seed,{detune:false}));
 const occ=effect(b,simulate(seed,{geometry:1})),occShuffled=effect(simulate(seed,{geometry:1}),simulate(seed,{geometry:1,shuffleSeats:true}));
 const occOff=effect(b,simulate(seed,{geometry:0,shuffleSeats:true}));
 const edge=effect(b,simulate(seed,{boundary:true,feedback:.3})),edgeOff=effect(b,simulate(seed,{boundary:true,feedback:0}));
 const checks={identity:unique(glyphs)&&!unique([...glyphs.slice(0,26),glyphs[0]]),projection:validCoords(coords)&&!validCoords([...coords.slice(0,26),coords[0]]),replay:effect(b,same)===0,noop:effect(simulate(seed,{steps:0}),simulate(seed,{steps:0,pair:.1}))===0,pair:pair>0,tri:tri>0,gematria:gem>0&&gemOff===0,frequency:freq>0,occupancy:occ>0&&occOff===0,boundary:edge>0&&edgeOff===0};
 return {seed,checks,metrics:{pair,tri,gem,gemOff,freq,occ,occShuffled,occOff,edge,edgeOff}};
 });
 return {version:"T97",seeds,tests:Object.keys(rows[0].checks),passed:rows.reduce((n,r)=>n+Object.values(r.checks).filter(Boolean).length,0),total:rows.length*Object.keys(rows[0].checks).length,rows};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(experiment(),null,2));
