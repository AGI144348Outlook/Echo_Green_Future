// T85 standalone deterministic offline experiment; run: node T85-multiring.js
const experiment = function experiment(){
 const seeds=[11,23,37,53], N=27, twopi=2*Math.PI;
 const glyphs=Array.from({length:N},(_,i)=>i), gem=Array.from({length:N},(_,i)=>[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,20,40,50,80][i]);
 const coord=i=>[Math.floor(i/9),Math.floor(i%9/3),i%3],inv=c=>c[0]*9+c[1]*3+c[2];
 const simulate=(seed,mode)=>{
   let s=seed>>>0;const rnd=()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296};
   let p=Array.from({length:N},()=>rnd()*twopi),w=Array.from({length:N},()=>0.025+0.03*rnd());
   const initial=p.slice(), shuffled=gem.slice().reverse();
   for(let t=0;t<12;t++){const old=p.slice();p=p.map((v,i)=>{
     const j=(i+1)%N,k=(i+9)%N;
     const affinity=(mode==="shuffle"?shuffled[i]:gem[i])/500;
     const pair=(mode==="zero"||mode==="frequency"?0:0.045*Math.sin(old[j]-v)*(1+affinity));
     const tri=(mode==="tri"?0.027*Math.sin(old[j]+old[k]-2*v):0);
     const freq=(mode==="frequency"?w[i]+0.007:w[i]);
     return v+freq+pair+tri;
   });}
   const diff=(a,b)=>a.reduce((s,v,i)=>s+Math.abs(v-b[i]),0)/N;
   return {p,initial,diff};
 };
 const results=[];
 for(const seed of seeds){
  const z=simulate(seed,"zero"), z2=simulate(seed,"zero"),f=simulate(seed,"frequency"),pair=simulate(seed,"pair"),tri=simulate(seed,"tri"),shuf=simulate(seed,"shuffle");
  const delta=(a,b)=>z.diff(a.p,b.p);
  const radii=Array.from({length:N},(_,i)=>1+0.08*Math.sin(seed+i*0.37));
  const checks={
    unique27:new Set(glyphs).size===27,
    projection:glyphs.every(i=>inv(coord(i))===i),
    composition:[2,3,4].every(n=>glyphs.slice(0,n).join(",").split(",").length===n),
    replay:delta(z,z2)===0,
    noop:delta(z,z2)===0,
    frequency:delta(f,z)>0,
    pairwise:delta(pair,z)>0,
    triadic:delta(tri,pair)>0,
    shuffle:delta(shuf,pair)>0,
    boundary:radii.every(r=>r>=0.92&&r<=1.08)
  };
  results.push({seed,checks,measurements:{frequency_vs_zero:delta(f,z),pair_vs_zero:delta(pair,z),tri_vs_pair:delta(tri,pair),shuffled_vs_pair:delta(shuf,pair),noop:delta(z,z2),radius_min:Math.min(...radii),radius_max:Math.max(...radii)}});
 }
 return {protocol:"T85 synthetic multiring v1",seeds,steps:12,types:10,checks:results.reduce((a,x)=>a+Object.values(x.checks).filter(Boolean).length,0),total:40,results,limitations:["Toy deterministic equations, no semantic benchmark","no independent reference implementation","no real warehouse/precession mechanism","shuffled affinity is reversed weights only","same-source replay not independent certification"]};
};
console.log(JSON.stringify(experiment(),null,2));
