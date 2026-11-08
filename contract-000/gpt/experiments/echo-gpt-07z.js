// Echo-GPT synthetic 07Z, preregistered Issue #349. No external effects.
(function(){
"use strict";
const glyphs=Array.from("אבגדהוזחטיכלמנסעפצקרשתךםןףץ");
const values=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];
const seeds=[3301,3302,3303,3304];
function rng(seed){let x=seed>>>0;return ()=>{x=(1664525*x+1013904223)>>>0;return x/4294967296;};}
function occupancy(offset){return glyphs.map((_,i)=>glyphs[(i+offset)%27]);}
function compose(offsets,seat){return offsets.map(o=>glyphs[(seat+o)%27]).join("");}
function radius(t){return 1+0.12*Math.sin(t*0.19);}
function neighbors(i){let x=i%3,y=Math.floor(i/3)%3,z=Math.floor(i/9),a=[];for(const [dx,dy,dz] of [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]]){let X=x+dx,Y=y+dy,Z=z+dz;if(X>=0&&X<3&&Y>=0&&Y<3&&Z>=0&&Z<3)a.push(X+3*Y+9*Z);}return a;}
function influence(cell,perturbed,delta){return neighbors(cell).includes(perturbed)?delta*0.025:0;}
function run(seed){let rand=rng(seed),offs=[Math.floor(rand()*27),Math.floor(rand()*27),Math.floor(rand()*27)],phase=rand()*6.2831853;
const prediction=(mode,t)=>{let ix=(t*7+offs[0])%27,v=values[ix]/400;let base=0.045*Math.sin(t*.13+phase);if(mode==="noop")return 0;if(mode==="uncoupled")return base;if(mode==="reversed")return base+0.025*Math.cos(t*.17-phase)*v;if(mode==="shuffled")return base+0.025*Math.sin(t*.17+phase)*values[(ix+13)%27]/400;return base+0.025*Math.sin(t*.17+phase)*v;};
const target=t=>0.04*Math.cos(t*.11)+0.012*Math.sin(t*.27);
const mse=mode=>{let sum=0;for(let t=0;t<64;t++)sum+=(prediction(mode,t)-target(t))**2;return sum/64;};
return {offs,phase,metrics:Object.fromEntries(["coupled","uncoupled","shuffled","reversed","noop"].map(k=>[k,mse(k)])),composition:compose(offs,13)};}
let out=[];
for(let seed of seeds){let a=run(seed),b=run(seed),o=a.offs,old=occupancy(0),rot=occupancy(1);
const frozen=Object.freeze({id:"A-000",aliases:Object.freeze(["A-000","resh"])});let refused=false;try{frozen.aliases.push("evil");}catch(e){refused=e instanceof TypeError;}
const tests={
T1:glyphs.length===27&&new Set(glyphs).size===27,
T2:JSON.stringify(a)===JSON.stringify(b),
T3:JSON.stringify(old)!==JSON.stringify(rot)&&new Set(rot).size===27&&old.every(g=>rot.includes(g)),
T4:compose(o.slice(0,2),13)===glyphs[(13+o[0])%27]+glyphs[(13+o[1])%27],
T5:a.composition===glyphs[(13+o[0])%27]+glyphs[(13+o[1])%27]+glyphs[(13+o[2])%27],
T6:Array.from({length:32},(_,t)=>radius(t)).every(r=>r>=.88&&r<=1.12),
T7:refused&&frozen.aliases.length===2,
T8:Math.abs(influence(12,13,.4))>0&&influence(0,13,.4)===0,
T9:Number.isFinite(a.metrics.coupled)&&Number.isFinite(a.metrics.uncoupled),
T10:["shuffled","reversed","noop"].every(k=>Number.isFinite(a.metrics[k]))
};out.push({seed,tests,metrics:a.metrics,neighbor_delta:influence(12,13,.4),far_delta:influence(0,13,.4),offs:o});}
return {protocol:349,version:"07z-v1",seeds,results:out};
})()