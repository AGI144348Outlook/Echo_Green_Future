// GPT-only offline experiment #310. Node/JS stdlib; no network, no mutation.
const mod=x=>((x%1)+1)%1;
const init=s=>Array.from({length:4},(_,i)=>mod(Math.sin(s*0.17+i*1.31)*10000));
const step=(a,c,shuffle=false)=>a.map((v,i)=>mod(v+0.07+c*(a[(i+1)%a.length]-v)*(shuffle?-1:1)));
function run(s,n=3,c=.13,shuffle=false){let a=init(s).slice(0,n);for(let k=0;k<32;k++)a=step(a,c,shuffle);return a;}
const linear=(a,b)=>a.reduce((s,x,i)=>s+Math.abs(x-b[i]),0);
const circular=(a,b)=>a.reduce((s,x,i)=>{let d=Math.abs(x-b[i]);return s+Math.min(d,1-d)},0);
const target=(s,n)=>Array.from({length:n},(_,i)=>mod(Math.sin(s*0.037+i*2.7)*0.5+0.5)); // different rule, independent of update
const seeds=Array.from({length:200},(_,i)=>1000+i);
const summary={};for(const metric of [['linear',linear],['circular',circular]]){let wins=0,shuffleWins=0,mean={coupled:0,null:0,shuffled:0};for(const s of seeds){const t=target(s,3),c=metric[1](run(s,3,.13),t),n=metric[1](run(s,3,0),t),sh=metric[1](run(s,3,.13,true),t);wins+=c<n;shuffleWins+=sh<c;mean.coupled+=c/200;mean.null+=n/200;mean.shuffled+=sh/200;}summary[metric[0]]={coupledBeatsNull:wins,shuffledBeatsCoupled:shuffleWins,mean};}
const glyph=Array.from({length:27},(_,i)=>i);
const xyz=i=>[i%3,Math.floor(i/3)%3,Math.floor(i/9)];
const inverse=([x,y,z])=>x+3*y+9*z;
const radii=Array.from({length:200},(_,i)=>0.8+0.15*Math.sin(i*.2));
const checks={
wrap:circular([.98],[.02])<.041 && linear([.98],[.02])>.95,
replay:JSON.stringify(run(1011))===JSON.stringify(run(1011)),
unique:new Set(glyph).size===27,
projection:glyph.every(i=>inverse(xyz(i))===i),
noop:JSON.stringify(init(1011).slice(0,3))===JSON.stringify(init(1011).slice(0,3)),
zeroIntervention:circular(run(1011,3,0),run(1011,3,0,true))===0,
shuffled:circular(run(1011,3,.13),run(1011,3,.13,true))>0,
radius:radii.every(x=>x>=.65&&x<=.95),
externalComparison:Number.isFinite(summary.circular.mean.coupled)&&Number.isFinite(summary.circular.mean.null),
identitySensitivity:JSON.stringify({version:1,glyph})!==JSON.stringify({version:2,glyph})
};
const output={issue:310,seeds:[1000,1199],types:Object.keys(checks).length,pass:Object.values(checks).filter(Boolean).length,checks,summary,limitations:['no external semantic target','no statistical superiority claim','radius checks bound only, not interaction dynamics','identity sensitivity is serialization check, not cryptographic digest','no-op checks deterministic input preservation only']};
console.log(JSON.stringify(output));