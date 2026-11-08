"use strict";
// GPT experimental 22Z; preregistered Issue #365. Synthetic noncanonical labels.
const ids=Array.from({length:27},(_,i)=>"G"+String(i).padStart(2,"0"));
function rng(seed){let s=seed>>>0;return ()=>((s=(Math.imul(s,1664525)+1013904223)>>>0)/4294967296);}
function compose(seed,n,t){return Array.from({length:n},(_,r)=>ids[(seed+7*r+t*(r+1))%27]);}
function project(i){return [Math.floor(i/9),Math.floor(i/3)%3,i%3];}
function base(seed){let f=rng(seed);return Array.from({length:27},()=>f()*.2-.1);}
function predict(x,mode,seed){let out=x.slice();for(let i=0;i<27;i++){let j=(i+1)%27,amp=mode==="uncoupled"||mode==="noop"?0:.025;let phase=mode==="phase"?-1:1, freq=mode==="detune"?1.8:1,gem=mode==="shuffle"?((i*11+7)%27)/27:i/27,radius=mode==="deform"?1+.1*Math.sin(i+seed):1;out[i]+=amp*phase*freq*radius*(x[j]-x[i])*(1+gem*.1);}return out;}
function mse(a,b){return a.reduce((s,v,i)=>s+(v-b[i])**2,0)/a.length;}
function evaluate(seed){let x=base(seed),target=base(seed+900000),modes=["coupled","uncoupled","noop","shuffle","phase","detune","deform"],p=Object.fromEntries(modes.map(m=>[m,predict(x,m,seed)]));
let y=x.slice();y[13]+=.4;let intervention=predict(y,"coupled",seed),delta=intervention[12]-p.coupled[12],expected=.4*.025*(1+(12/27)*.1);
let tests=[
["T1",compose(seed,2,1).length===2&&compose(seed,2,1)[1]===ids[(seed+7+2)%27]],
["T2",compose(seed,3,2).length===3&&compose(seed,3,2)[2]===ids[(seed+14+6)%27]],
["T3",new Set(ids.map((_,i)=>project(i).join(","))).size===27],
["T4",new Set(ids).size===27],
["T5",mse(p.coupled,p.phase)>0],
["T6",mse(p.coupled,p.detune)>0],
["T7",mse(p.coupled,p.shuffle)>0],
["T8",Array.from({length:27},(_,i)=>1+.1*Math.sin(i+seed)).every(v=>v>=.9-1e-12&&v<=1.1+1e-12)],
["T9",Math.abs(delta-expected)<1e-12&&Math.abs(intervention[0]-p.coupled[0])<1e-12&&Math.abs(predict(y,"uncoupled",seed)[12]-p.uncoupled[12])<1e-12],
["T10",modes.every(m=>Number.isFinite(mse(p[m],target)))&&target.every((v,i)=>v===base(seed+900000)[i])]];
return {seed,tests:tests.map(([type,pass])=>({type,pass})),mse:Object.fromEntries(modes.map(m=>[m,mse(p[m],target)])),neighbor_delta:delta};}
const results=[3301,3302,3303,3304].map(evaluate);
return JSON.stringify({protocol:"Issue #365",source:"multiring_22z.js",results});
