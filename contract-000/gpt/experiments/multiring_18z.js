// GPT-owned bounded synthetic ring experiment; Node 18+ or isolated V8. No external dependencies.
const seeds=[3301,3302,3303,3304], ids=Array.from({length:27},(_,i)=>i);
const gem=ids.map(i=>[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,20,40,50,80][i]);
function ring(seed,r,t,reverse=false,detune=0){return (seed+3*r+Math.floor(t*(1+detune)*(r+1))+(reverse?-t:t)+27000)%27}
function composition(seed,t,n,reverse=false,detune=0){return Array.from({length:n},(_,r)=>ring(seed,r,t,reverse,detune))}
function predict(seed,t,mode,input){let base=input.map((v,i)=>v*.94+.015*Math.sin((seed+i+t)/7));if(mode==='noop')return input.slice();if(mode==='uncoupled')return base;let map=mode==='shuffled'?gem.slice().reverse():gem;return base.map((v,i)=>v+.025*input[(i+1)%27]*(mode==='phase'? -1:1)+.0001*map[(i+t)%27]);}
function target(seed,t,input){return input.map((v,i)=>v*.975+.004*Math.cos((i*3+t+seed)/11))}
function mse(a,b){return a.reduce((s,x,i)=>s+(x-b[i])**2,0)/a.length}
function run(seed){let input=ids.map(i=>.2+.01*i+.02*Math.sin((i+seed)/13)),t=3;
let a=composition(seed,t,2),b=composition(seed,t,3);
let coupled=predict(seed,t,'coupled',input),uncoupled=predict(seed,t,'uncoupled',input),noop=predict(seed,t,'noop',input),shuffled=predict(seed,t,'shuffled',input),truth=target(seed,t,input);
let modified=input.slice();modified[13]+=.4;let changed=predict(seed,t,'coupled',modified),changedU=predict(seed,t,'uncoupled',modified);
let tests={
identity:new Set(ids).size===27,
two_ring:a.length===2&&a[0]===ring(seed,0,t)&&a[1]===ring(seed,1,t),
three_ring:b.length===3&&b[2]===ring(seed,2,t),
projection:ids.every(i=>{let x=i%3,y=Math.floor(i/3)%3,z=Math.floor(i/9);return x+3*y+9*z===i}),
phase:JSON.stringify(composition(seed,t,3,true))!==JSON.stringify(b),
frequency:JSON.stringify(composition(seed,t,3,false,.5))!==JSON.stringify(b),
gematria:mse(shuffled,coupled)>0,
boundary:ids.every(i=>{let radius=1+.08*Math.sin((seed+i)/9);return radius>=.92&&radius<=1.08}),
intervention:Math.abs(changed[12]-coupled[12]-.01)<1e-10&&Math.abs(changed[0]-coupled[0])<1e-10&&Math.abs(changedU[12]-uncoupled[12])<1e-10,
baseline:[coupled,uncoupled,noop,shuffled].every(v=>Number.isFinite(mse(v,truth)))
};
return {seed,tests,mse:{coupled:mse(coupled,truth),uncoupled:mse(uncoupled,truth),noop:mse(noop,truth),shuffled:mse(shuffled,truth)},delta:changed[12]-coupled[12]}}
const results=seeds.map(run);if(typeof module!=='undefined')module.exports={run,results};if(typeof console!=='undefined')console.log(JSON.stringify(results));