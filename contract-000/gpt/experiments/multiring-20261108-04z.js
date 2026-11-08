// Echo-GPT independent synthetic prototype, #346. Not canonical Echo.
const seeds=[3301,3302,3303,3304];
const glyphs=Array.from({length:27},(_,i)=>"G"+String(i).padStart(2,"0"));
const xyz=i=>[Math.floor(i/9),Math.floor(i/3)%3,i%3];
const neighbors=i=>Array.from({length:27},(_,j)=>j).filter(j=>xyz(i).reduce((s,v,k)=>s+Math.abs(v-xyz(j)[k]),0)===1);
function rng(seed){let s=seed>>>0;return()=>((s=(Math.imul(1664525,s)+1013904223)>>>0)/4294967296)}
function inputs(seed){let r=rng(seed);return Array.from({length:27},()=>r()*2-1)}
const weight=i=>[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900][i];
function model(x,{coupling=.12,phase=.3,shuffle=false,rings=2}={}){
 return x.map((v,i)=>{
 const nb=neighbors(i),m=nb.reduce((s,j)=>s+x[j],0)/nb.length;
 const w=weight(shuffle?26-i:i);
 const ring=(rings===3?Math.cos(phase*2+i*.3):Math.sin(phase+i*.3));
 return .7*v+coupling*m*(1+.05*Math.sin(w*.01+phase))+.025*ring;
 });
}
function target(x){return x.map((v,i)=>.65*v+.07*Math.tanh(neighbors(i).reduce((s,j)=>s+x[j],0)));}
function mse(a,b){return a.reduce((s,v,i)=>s+(v-b[i])**2,0)/a.length}
function evaluate(seed){
 const x=inputs(seed),base=model(x),unc=model(x,{coupling:0}),sh=model(x,{shuffle:true}),rev=model(x,{phase:-.3}),tri=model(x,{rings:3}),y=target(x),zero=Array(27).fill(0);
 const intervene=x.slice();intervene[13]+=.4;
 const a=model(x),b=model(intervene),same=model(x.slice());
 const rad=Array.from({length:27},(_,i)=>1+.1*Math.sin(i*.2+seed*.001));
 const tests={
 T1:new Set(glyphs).size===27,
 T2:neighbors(13).length===6&&neighbors(0).length===3,
 T3:JSON.stringify(base)===JSON.stringify(model(inputs(seed))),
 T4:JSON.stringify(unc)===JSON.stringify(model(x,{coupling:0})),
 T5:Math.abs(b[12]-a[12])>1e-9&&Math.abs(b[0]-a[0])<1e-12,
 T6:JSON.stringify(a)===JSON.stringify(same),
 T7:mse(base,sh)>1e-15,
 T8:mse(base,rev)>1e-15,
 T9:rad.every(v=>v>=.9-1e-12&&v<=1.1+1e-12),
 T10:[base,unc,sh,rev,tri,zero].every(z=>Number.isFinite(mse(z,y)))
 };
 return {seed,tests,mse:{coupled:mse(base,y),uncoupled:mse(unc,y),shuffled:mse(sh,y),phase_reversed:mse(rev,y),three_ring:mse(tri,y),noop:mse(zero,y)},intervention:{neighbor_delta:b[12]-a[12],far_delta:b[0]-a[0]}};
}
const results=seeds.map(evaluate);
JSON.stringify({issue:346,seeds,results});
