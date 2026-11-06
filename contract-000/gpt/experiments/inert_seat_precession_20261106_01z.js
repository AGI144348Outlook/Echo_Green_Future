// Preregistered in Issue #312 BEFORE creation/execution. Pure deterministic stdlib JavaScript.
function experiment(){
 const mod=x=>((x%1)+1)%1, N=27, T=32, seed=1106;
 const seats=Array.from({length:N},(_,i)=>({id:i,occupant:null}));
 const glyphs=Array.from({length:N},(_,i)=>({id:i,seat:null}));
 const xyz=i=>[i%3,Math.floor(i/3)%3,Math.floor(i/9)], inv=p=>p[0]+3*p[1]+9*p[2];
 const ent=Array.from({length:7},(_,i)=>.12+.08*i);
 function run(gain=.15,couple=.07,entropy=ent){
   let phase=Array.from({length:7},(_,i)=>mod((seed+i*17)/997)),radius=Array(7).fill(.8),trace=[];
   for(let t=0;t<T;t++){
     const old=phase.slice();
     phase=old.map((v,i)=>mod(v+.021+.006*i+gain*(entropy[i]-.36)*.012+(i?couple*Math.sin(2*Math.PI*(old[0]-v))*.01:0)));
     radius=radius.map((r,i)=>Math.max(.65,Math.min(.95,.8+gain*(entropy[i]-.36)*.25+.02*Math.sin(2*Math.PI*phase[i]))));
     trace.push({phase:phase.slice(),radius:radius.slice()});
   }
   return {phase,radius,trace};
 }
 const base=run(), noop=run(0,0), altered=run(.15,.07,ent.map((x,i)=>i===3?x+.2:x)), zero=run(0,.07,ent.map((x,i)=>i===3?x+.2:x)), shuffled=run(.15,.07,ent.slice().reverse()),uncoupled=run(.15,0);
 const dist=(a,b)=>a.reduce((s,x,i)=>{const d=Math.abs(x-b[i]);return s+Math.min(d,1-d)},0);
 const diff=(a,b)=>dist(a.phase,b.phase);
 const radiusSeries=base.trace.flatMap(t=>t.radius);
 const checks={
  inert:seats.every(s=>s.occupant===null)&&glyphs.every(g=>g.seat===null),
  cube:glyphs.every(g=>inv(xyz(g.id))===g.id)&&new Set(glyphs.map(g=>g.id)).size===27,
  phase:base.trace.every(t=>t.phase.every(p=>p>=0&&p<1)),
  noop:JSON.stringify(seats)===JSON.stringify(Array.from({length:N},(_,i)=>({id:i,occupant:null}))),
  replay:JSON.stringify(base)===JSON.stringify(run()),
  entropyIntervention:diff(base,altered)>0,
  zeroGain:diff(run(0,.07),zero)===0,
  shuffled:diff(base,shuffled)>0,
  radius:radiusSeries.every(r=>r>=.65&&r<=.95)&&Math.max(...radiusSeries)-Math.min(...radiusSeries)>.001,
  parentCoupling:diff(base,uncoupled)>0
 };
 return {issue:312,seed,steps:T,checks,pass:Object.values(checks).filter(Boolean).length,types:Object.keys(checks).length,metrics:{entropyIntervention:diff(base,altered),zeroGain:diff(run(0,.07),zero),shuffled:diff(base,shuffled),parentCoupling:diff(base,uncoupled),radiusRange:[Math.min(...radiusSeries),Math.max(...radiusSeries)],endPhases:base.phase},limitations:["synthetic entropy inputs not observed warehouse entropy","27 seats empty by construction; not DB constraints","no predictive or semantic task","no external dataset or significance inference"]};
}
