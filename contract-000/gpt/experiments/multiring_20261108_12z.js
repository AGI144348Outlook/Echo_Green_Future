// GPT-owned bounded experiment, 2026-11-08 12Z. Run with node file.js; no external dependencies.
const seeds=[3301,3302,3303,3304], N=27;
function run(seed,mode='coupled',intervention=0){
 const glyph=Array.from({length:N},(_,i)=>i);
 const val=i=>[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,20,40,50,80][i];
 const shift=(seed%N+3)%N;
 const rings=[glyph.map((_,i)=>glyph[(i+shift)%N]),glyph.map((_,i)=>glyph[(i+2*shift)%N]),glyph.map((_,i)=>glyph[(i+3*shift)%N])];
 const radius=Array.from({length:N},(_,i)=>1+0.04*Math.sin((i+seed)*0.2));
 const phase=(i)=>Math.sin((i+seed)*0.013), freq=(i)=>Math.cos((i+seed)*0.017);
 const values=Array.from({length:N},(_,i)=>{
   const g=rings[0][i], h=rings[1][i];
   const affinity=(mode==='shuffle'?val((g+7)%N):val(g))/500;
   const coupling=mode==='uncoupled'||mode==='noop'?0:(mode==='reverse'?-1:1);
   return coupling*(0.035*phase(i)+0.018*freq(i)+0.004*affinity)+(i===12?0.025*intervention:0);
 });
 const target=Array.from({length:N},(_,i)=>0.015*Math.sin(seed*0.073+i*0.31)+0.009*Math.cos(seed*0.19+i*0.17));
 const mse=values.reduce((s,v,i)=>s+(v-target[i])**2,0)/N;
 return {rings,radius,values,mse,target};
}
function evaluate(){
 const rows=[];
 for(const seed of seeds){
  const a=run(seed),b=run(seed),u=run(seed,'uncoupled'),s=run(seed,'shuffle'),p=run(seed,'reverse'),n=run(seed,'noop'),v=run(seed,'coupled',0.4);
  const checks=[
   new Set(a.rings.flat()).size===27,
   a.rings.slice(0,2).every(r=>r.length===27)&&a.rings[0][0]!==a.rings[1][0],
   a.rings.length===3&&a.rings.every(r=>new Set(r).size===27),
   JSON.stringify(a)===JSON.stringify(b),
   a.radius.every(x=>x>=0.96&&x<=1.04),
   Number.isFinite(p.mse)&&p.values.some((x,i)=>x!==a.values[i]),
   a.values.some((x,i)=>Math.abs(x-(0.035*Math.sin((i+seed)*0.013)+0.004*([1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,20,40,50,80][a.rings[0][i]]/500)))>1e-8),
   Number.isFinite(s.mse)&&s.values.some((x,i)=>x!==a.values[i]),
   Math.abs(v.values[12]-a.values[12]-0.01)<1e-12&&v.values[0]===a.values[0],
   [a,u,n].every(x=>Number.isFinite(x.mse))&&n.values.every(x=>x===0)
  ];
  rows.push({seed,checks,pass:checks.filter(Boolean).length,coupled:a.mse,uncoupled:u.mse,shuffled:s.mse,reversed:p.mse,noop:n.mse,intervention_delta:v.values[12]-a.values[12]});
 }
 return rows;
}
if(typeof module!=='undefined'&&require.main===module)console.log(JSON.stringify(evaluate(),null,2));
