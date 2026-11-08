// GPT noncanonical multiring 21Z, preregistration Issue #364. Synthetic IDs, deterministic no external effects.
"use strict";
const ids=Array.from({length:27},(_,i)=>"G"+String(i).padStart(2,"0"));
function rng(seed){let s=seed>>>0;return ()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296;};}
function idx(seed,ring,step){return (seed+ring*7+step*(ring+1))%27;}
function compose(seed,n,step){return Array.from({length:n},(_,r)=>ids[idx(seed,r,step)]);}
function project(i){return [Math.floor(i/9),Math.floor(i/3)%3,i%3];}
function base(seed){const rand=rng(seed);return Array.from({length:27},()=>rand()*.2-.1);}
function predict(input,mode,seed){const out=input.slice();const shuf=Array.from({length:27},(_,i)=>(i*11+7)%27);for(let i=0;i<27;i++){let j=(i+1)%27;let a=mode==="uncoupled"||mode==="noop"?0:.025;let phase=mode==="phase"?-1:1;let freq=mode==="detune"?1.8:1;let gem=mode==="shuffle"?shuf[i]/27:i/27;let radius=mode==="deform"?1+.1*Math.sin(i+seed):1;out[i]+=a*phase*freq*radius*(input[j]-input[i])*(1+gem*.1);}return out;}
function mse(a,b){return a.reduce((s,v,i)=>s+(v-b[i])**2,0)/a.length;}
function evaluate(seed){const x=base(seed),target=base(seed+900000);const modes=["coupled","uncoupled","noop","shuffle","phase","detune","deform"];const p={};for(const m of modes)p[m]=predict(x,m,seed);const test=[
["T1",compose(seed,2,1).length===2&&compose(seed,2,1).every((v,r)=>v===ids[idx(seed,r,1)])],
["T2",compose(seed,3,2).length===3&&compose(seed,3,2).every((v,r)=>v===ids[idx(seed,r,2)])],
["T3",new Set(ids.map((_,i)=>project(i).join(","))).size===27],
["T4",new Set(ids).size===27],
["T5",mse(p.coupled,p.phase)>0],
["T6",mse(p.coupled,p.detune)>0],
["T7",mse(p.coupled,p.shuffle)>0],
["T8",Array.from({length:27},(_,i)=>1+.1*Math.sin(i+seed)).every(r=>r>=.9-1e-12&&r<=1.1+1e-12)],
["T9",(()=>{let y=x.slice();y[13]+=.4;let a=predict(y,"coupled",seed),b=predict(y,"uncoupled",seed);return Math.abs(a[12]-p.coupled[12]-(0.4*0.025*(1+(12/27)*0.1)))<1e-9&&Math.abs(a[0]-p.coupled[0])<1e-12&&Math.abs(b[12]-p.uncoupled[12])<1e-12;})()],
["T10",modes.every(m=>Number.isFinite(mse(p[m],target)))]];return {seed,tests:test.map(([name,pass])=>({name,pass})),mse:Object.fromEntries(modes.map(m=>[m,mse(p[m],target)])),neighbor_delta:0.4*0.025*(1+(12/27)*0.1)};}
const results=[3301,3302,3303,3304].map(evaluate);
return JSON.stringify({protocol:"Issue #364",source:"multiring_21z.js",results});
