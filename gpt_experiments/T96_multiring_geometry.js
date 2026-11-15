// T96 GPT-only synthetic multiring test runner; source for V8 replay.
// Run: invoke experiment() and JSON.stringify result in an ECMAScript runtime.
const experiment = function experiment(){
const glyphs=[..."אבגדהוזחטיכלמנסעפצקרשת"].concat([..."ךםןףץ"]);
const vals=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];
const seeds=[11,23,37,53], TAU=2*Math.PI,dist=(a,b)=>Math.abs(Math.atan2(Math.sin(a-b),Math.cos(a-b)));
const unique=a=>a.length===27&&new Set(a).size===27;
const project=a=>a.length===27&&new Set(a.map(x=>x.join(","))).size===27&&a.every(x=>x.length===3&&x.every(v=>v>=0&&v<3));
function sim(seed,o={}){
let rng=seed>>>0; const rand=()=>{rng=(Math.imul(1664525,rng)+1013904223)>>>0;return rng/4294967296};
let p=Array.from({length:27},()=>rand()*TAU), f=Array.from({length:27},(_,i)=>.02+(i%7)*.003);
let v=o.shuffle?vals.map((_,i)=>vals[(i*11)%27]):vals;
let n=o.steps??24;
for(let t=0;t<n;t++){
const old=p.slice(),rad=1+(o.boundary?0.2*Math.sin(t*.2):0);
p=p.map((x,i)=>{
const j=(i+1)%27,k=(i+2)%27;
const affinity=1/(1+Math.abs(v[i]-v[j])/100);
const pair=(o.pair||0)*affinity*Math.sin(old[j]-x);
const tri=(o.tri||0)*Math.sin(old[j]+old[k]-2*x);
const occupancy=o.occupancy?((i%3===0?1:-1)*.012*Math.cos(old[(i+3)%27]-x)):0;
const geom=o.geometry?o.geometry*occupancy:0;
const boundary=o.feedback?o.feedback*(rad-1)*Math.sin(old[(i+9)%27]-x):0;
return (x+(o.detune===false?.02:f[i])+pair+tri+geom+boundary+TAU)%TAU;
});
}
return p;
}
const effect=(a,b)=>a.reduce((s,x,i)=>s+dist(x,b[i]),0)/a.length;
const rows=[];
for(const seed of seeds){
const base=sim(seed),same=sim(seed),no=sim(seed,{steps:0}),no2=sim(seed,{steps:0,pair:0,tri:0});
const pair=effect(base,sim(seed,{pair:.12})),tri=effect(base,sim(seed,{tri:.08}));
const shuffled=effect(sim(seed,{pair:.12}),sim(seed,{pair:.12,shuffle:true}));
const shuffledNull=effect(sim(seed,{pair:0}),sim(seed,{pair:0,shuffle:true}));
const frequency=effect(base,sim(seed,{detune:false}));
const geometry=effect(base,sim(seed,{occupancy:true,geometry:1}));
const geometryOff=effect(base,sim(seed,{occupancy:true,geometry:0}));
const boundary=effect(base,sim(seed,{boundary:true,feedback:.3}));
const boundaryOff=effect(base,sim(seed,{boundary:true,feedback:0}));
const coords=Array.from({length:27},(_,i)=>[Math.floor(i/9),Math.floor(i/3)%3,i%3]);
const checks={identity:unique(glyphs)&&!unique([...glyphs.slice(0,26),glyphs[0]]),projection:project(coords)&&!project([...coords.slice(0,26),coords[0]]),replay:effect(base,same)===0,noop:effect(no,no2)===0,pair:pair>0,tri:tri>0,gematria:shuffled>0&&shuffledNull===0,frequency:frequency>0,occupancy:geometry>0&&geometryOff===0,boundary:boundary>0&&boundaryOff===0};
rows.push({seed,checks,measurements:{pair,tri,shuffled,shuffledNull,frequency,geometry,geometryOff,boundary,boundaryOff}});
}
return {version:"T96",runtime:"ECMAScript V8",seeds,steps:24,tests:Object.keys(rows[0].checks),total:rows.length*Object.keys(rows[0].checks).length,passed:rows.reduce((n,r)=>n+Object.values(r.checks).filter(Boolean).length,0),rows,limitations:["synthetic equations, no lexicon or semantics","geometry occupancy term is imposed by a predefined i%3 pattern","boundary effect is specified coupling, not emergent physics","gematria final glyphs use base-letter values"]};
};
const result = experiment();
JSON.stringify(result,null,2);
