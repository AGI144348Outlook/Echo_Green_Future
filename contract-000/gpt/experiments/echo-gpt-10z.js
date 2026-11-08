// Echo-GPT 10Z bounded synthetic experiment. Node: node echo-gpt-10z.js
"use strict";
const seeds=[3301,3302,3303,3304], glyphs=Array.from({length:27},(_,i)=>i);
function ring(n,offset){return Array.from({length:n},(_,i)=>glyphs[(i+offset)%27]);}
function neighbors(i){let x=i%3,y=Math.floor(i/3)%3,z=Math.floor(i/9);return [i-1,i+1,i-3,i+3,i-9,i+9].filter(j=>j>=0&&j<27&&Math.abs(j%3-x)+Math.abs(Math.floor(j/3)%3-y)+Math.abs(Math.floor(j/9)-z)===1);}
function signal(i,seed,kind,delta=0){let ns=neighbors(i), phase=(seed%101)/101, affinity=k=>((kind==="shuffle"?(k*17+5)%27:k)%9)/9;let base=.1*Math.sin(i*1.7+phase), coupled=ns.reduce((s,k)=>s+.015*Math.cos(k*0.4+phase)*affinity(k),0);let scale=kind==="uncoupled"||kind==="noop"?0:kind==="reverse"?-1:1;return kind==="noop"?0:base+scale*coupled+(ns.includes(13)?delta*.025:0);}
function target(i,seed){return .07*Math.sin(i*.8+seed*.003)+.02*Math.cos(i*.17);}
function mse(seed,kind){let s=0;for(let i=0;i<27;i++){let e=signal(i,seed,kind)-target(i,seed);s+=e*e;}return s/27;}
function run(seed){let a=ring(27,seed%27), b=ring(27,(seed+1)%27), c=ring(27,(seed+2)%27), i=12;let checks=[
new Set(glyphs).size===27,
[a[0],b[0]].length===2&&a[0]!==b[0],
[a[0],b[0],c[0]].length===3&&new Set([a[0],b[0],c[0]]).size===3,
new Set(ring(27,(seed+1)%27)).size===27,
Array.from({length:27},(_,j)=>1+.08*Math.sin(j+seed)).every(v=>v>=.92-1e-9&&v<=1.08+1e-9),
signal(i,seed,"coupled")!==signal(i,seed,"reverse"),
signal(i,seed+31,"coupled")!==signal(i,seed,"coupled"),
signal(i,seed,"shuffle")!==signal(i,seed,"coupled"),
Math.abs(signal(i,seed,"coupled",.4)-signal(i,seed,"coupled")-.01)<1e-9 && signal(0,seed,"coupled",.4)===signal(0,seed,"coupled"),
["coupled","uncoupled","shuffle","noop"].every(k=>Number.isFinite(mse(seed,k)))
];return {seed,checks,mse:Object.fromEntries(["coupled","uncoupled","shuffle","noop","reverse"].map(k=>[k,mse(seed,k)])),intervention:signal(i,seed,"coupled",.4)-signal(i,seed,"coupled")};}
const results=seeds.map(run);if(typeof module!=="undefined")module.exports={results,run};if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(results,null,2));
