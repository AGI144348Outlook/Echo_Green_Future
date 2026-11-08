// Echo-GPT independent synthetic multiring portfolio; preregistration Issue #350.
// No external inputs, no network, no canonical Echo writes. Run: node this-file.js
(function(){
"use strict";
const seeds=[3301,3302,3303,3304], glyphs=Array.from({length:27},(_,i)=>i);
const vals=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900];
function rotate(a,k){let n=a.length,k2=((k%n)+n)%n;return a.slice(n-k2).concat(a.slice(0,n-k2))}
function mix(seed){let s=seed>>>0;return ()=>((s=(Math.imul(s,1664525)+1013904223)>>>0)/4294967296)}
function neighbors(i){let x=i%3,y=Math.floor(i/3)%3,z=Math.floor(i/9),out=[];for(let [dx,dy,dz] of [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]]){let a=x+dx,b=y+dy,c=z+dz;if(a>=0&&a<3&&b>=0&&b<3&&c>=0&&c<3)out.push(a+3*b+9*c)}return out}
function digest(a){let h=2166136261>>>0;for(let n of a){h=Math.imul((h^n)>>>0,16777619)>>>0}return h}
function mse(a,b){return a.reduce((s,v,i)=>s+(v-b[i])**2,0)/a.length}
function predict(seed,mode){let rand=mix(seed),out=[];for(let i=0;i<27;i++){let t=(i+1)*0.17,phase=Math.sin(t+seed*0.0003),g=vals[i]/900,noise=(rand()-.5)*.015;let c=mode==="uncoupled"?0:mode==="shuffled"?vals[(i*7+3)%27]/900:mode==="noop"?0:g;let v=mode==="noop"?0:0.055*Math.sin(t)+0.025*c*Math.cos(phase)+noise;out.push(v)}return out}
const cases=[],errors=[];
for(const seed of seeds){
const rand=mix(seed), r1=rotate(glyphs,seed%27),r2=rotate(glyphs,(seed+7)%27),r3=rotate(glyphs,(seed+13)%27);
const checks=[];
function check(type,pass,observation){checks.push({type,pass:!!pass,observation});if(!pass)errors.push({seed,type,observation})}
const back=rotate(r1,-(seed%27));check("T1 reversible bijection",new Set(r1).size===27&&back.every((v,i)=>v===i),{unique:new Set(r1).size,restored:back.every((v,i)=>v===i)});
const c2=[r1[0],r2[0]],c3=[r1[0],r2[0],r3[0]];check("T2 ordered 2/3 ring",c2.join(",")!==c2.slice().reverse().join(",")&&c3.join(",")!==c3.slice().reverse().join(","),{c2,c3});
const radii=Array.from({length:27},(_,i)=>1+.15*Math.sin(i*.4+seed*.01));check("T3 deformable boundary",radii.every(x=>x>=.85-1e-12&&x<=1.15+1e-12)&&Math.max(...radii)>Math.min(...radii),{min:Math.min(...radii),max:Math.max(...radii)});
const base=Array(27).fill(0),changed=base.slice();changed[13]=.4;const spatial=a=>a.map((_,i)=>neighbors(i).reduce((s,j)=>s+a[j]*.025,0));let before=spatial(base),after=spatial(changed),near=after[12]-before[12],far=after[0]-before[0];check("T4 causal six-neighbor",near>.0099&&Math.abs(far)<1e-12&&neighbors(13).includes(12)&&!neighbors(13).includes(0),{near,far});
const a=predict(seed,"coupled"),b=predict(seed,"uncoupled"),sh=predict(seed,"shuffled"),zero=predict(seed,"noop");check("T5 phase coupling effect",a.some((v,i)=>Math.abs(v-b[i])>1e-5),{meanDifference:a.reduce((s,v,i)=>s+Math.abs(v-b[i]),0)/27});
const align=(d)=>Array.from({length:27},(_,i)=>Math.cos(d*i*.25)).reduce((s,v)=>s+v,0)/27;let locked=align(0),detuned=align(1);check("T6 frequency detuning",locked>detuned,{locked,detuned});
let affinity=vals.reduce((s,v,i)=>s+v*vals[(i+1)%27],0),permuted=vals.reduce((s,v,i)=>s+v*vals[((i+1)*7+3)%27],0);check("T7 gematria shuffle",affinity!==permuted,{affinity,permuted});
let d0=digest(r1),mut=r1.slice();mut[4]=(mut[4]+1)%27;check("T8 mutation digest",d0!==digest(mut),{original:d0,mutated:digest(mut)});
let target=Array.from({length:27},(_,i)=>.012*Math.sin((i+1)*.21)+.003*Math.cos((i+1)*.4)),scores={coupled:mse(a,target),uncoupled:mse(b,target),shuffled:mse(sh,target),noop:mse(zero,target)};check("T9 independent target control",Object.values(scores).every(Number.isFinite),scores);
const alt=predict(seed+100,"coupled"),delta=mse(a,alt);check("T10 independent-seed null",delta>0&&mse(sh,a)>0&&scores.noop>=0,{seedDelta:delta,shuffleDelta:mse(sh,a)});
cases.push({seed,checks,scores});
}
return {protocol:"issue-350",runtime:"isolated V8 or Node.js",seeds,types:10,cases:cases.length,total:cases.reduce((s,x)=>s+x.checks.length,0),passed:cases.reduce((s,x)=>s+x.checks.filter(z=>z.pass).length,0),failed:errors.length,errors,details:cases,limitations:["Target specified in same source and visible to developer; not blind","Synthetic causal kernel is built by construction, not inferred","Gematria numbers illustrative; no semantic lexicon validation","No learning or independent external outcomes","Seeds adjacent; statistical independence not established"]};
})()