// GPT-owned noncanonical synthetic prototype. Prospective Issue #457, 2026-11-13 07Z.
function simulate(seed,mode="active",shift=0){
 const n=27,twopi=2*Math.PI,phase=Array.from({length:n},(_,i)=>((seed*0.017+i*0.231+shift)%twopi)),freq=Array.from({length:n},(_,i)=>0.016+(i%7)*0.001),warehouse=Array(n).fill(null),identities=Array.from({length:n},(_,i)=>i),contacts=[],occupancy=[];
 const affinity=Array.from({length:n},(_,i)=>mode==="shuffled"?((i*11)%27)+1:i+1);
 for(let t=0;t<24;t++){
  const arrivals=[];for(let i=0;i<n;i++)if((i*7+t*3+seed)%19===0)arrivals.push(i);
  contacts.push(arrivals.join(","));
  for(let i=0;i<n;i++)if(warehouse[i]!==null){warehouse[i]=warehouse[i]*0.92+0.08*Math.sin(phase[(i+1)%n]-phase[i]);}
  const next=phase.map((p,i)=>{
   const pair=Math.sin(phase[(i+1)%n]-p)*0.007;
   const triad=mode==="no-triad"?0:0.002*Math.sin(phase[(i+1)%n]+phase[(i+2)%n]-2*p);
   const w=mode==="active"||mode==="shuffled"||mode==="no-triad"?warehouse[i]:null;
   const fb=w===null?0:0.003*w*(1+affinity[i]/100);
   return p+freq[i]+(mode==="noop"?0:pair+triad+fb);
  });
  for(let i=0;i<n;i++)phase[i]=next[i];
  for(const i of arrivals)if(warehouse[i]===null)warehouse[i]=Math.sin(phase[(i+1)%n]-phase[i]);
  if(t%9===8)for(let i=0;i<n;i++)if((i+t)%3===0)warehouse[i]=null;
  occupancy.push(warehouse.filter(x=>x!==null).length);
 }
 return {phase,identities,contacts,occupancy,cube:identities.map(i=>[Math.floor(i/9),Math.floor(i/3)%3,i%3])};
}
function distance(a,b){return a.reduce((s,x,i)=>s+Math.abs(Math.atan2(Math.sin(x-b[i]),Math.cos(x-b[i]))),0)/a.length}
// Run seeds [11,23,37,53], modes active/sham/uncoupled/shuffled/no-triad/noop, global phase shift 0.7.
