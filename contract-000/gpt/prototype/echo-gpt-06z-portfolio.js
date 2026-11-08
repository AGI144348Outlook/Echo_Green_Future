// Echo-GPT 06Z bounded synthetic portfolio. Run: evaluate as JS expression; returns JSON object.
(()=>{
const seeds=[3301,3302,3303,3304], glyphs=[..."אבגדהוזחטיכלמנסעפצקרשתךםןףץ"], gem=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];
function model(seed){
 let rng=seed>>>0;const rand=()=>{rng=(Math.imul(1664525,rng)+1013904223)>>>0;return rng/4294967296};
 const rings=[0,1,2].map((k)=>({offset:Math.floor(rand()*27),speed:k+1,phase:rand()*Math.PI*2,rad:1}));
 const positions=(t)=>rings.map(r=>Array.from({length:27},(_,i)=>glyphs[(i+r.offset+r.speed*t)%27]));
 const radius=(t,k)=>1+0.12*Math.sin(t*0.3+rings[k].phase);
 const neighbor=(a,b)=>{let p=i=>[Math.floor(i/9),Math.floor(i/3)%3,i%3];let x=p(a),y=p(b);return x.reduce((s,v,j)=>s+Math.abs(v-y[j]),0)===1};
 const field=(t,variant)=>Array.from({length:27},(_,i)=>{let ids=rings.map((r,k)=>(i+r.offset+r.speed*t)%27);let g=ids.map(j=>gem[j]);if(variant==="shuffle")g=g.slice().reverse();let phase=variant==="reverse"?-1:1;let coupling=variant==="uncoupled"?0:0.13;return 0.06*Math.sin(t*0.19+i*0.11+phase*rings[0].phase)+coupling*Math.cos(phase*(rings[1].phase+t*0.07)+g[0]/40)*Math.sin(g[1]/50);});
 const project=(f,intervention=0)=>f.map((v,i)=>v+0.025*Array.from({length:27},(_,j)=>neighbor(i,j)?f[j]+(j===13?intervention:0):0).reduce((a,b)=>a+b,0));
 const target=Array.from({length:27},(_,i)=>0.05*Math.sin(i*0.12)+0.02*Math.cos(i*0.31));
 const mse=x=>x.reduce((a,v,i)=>a+(v-target[i])**2,0)/27;
 const metric=v=>mse(project(field(7,v)));
 const first=positions(0),next=positions(1),identity=Object.freeze({name:"A-000",aliases:Object.freeze(["A-000","resh","governor"])});
 const before=identity.aliases[0];try{identity.aliases[0]="BAD"}catch(e){}
 const f=field(7,"coupled"),base=project(f),changed=project(f,0.4);
 const results=[
 ["T1",glyphs.length===27&&new Set(glyphs).size===27&&first.every(x=>new Set(x).size===27)],
 ["T2",JSON.stringify(positions(7))===JSON.stringify(positions(7))&&JSON.stringify(field(7,"coupled"))===JSON.stringify(field(7,"coupled"))],
 ["T3",first.every((a,k)=>a.some((v,i)=>v!==next[k][i])&&new Set(next[k]).size===27)],
 ["T4",first[0][0]+first[1][0]===first.slice(0,2).map(x=>x[0]).join("")],
 ["T5",first.slice(0,3).map(x=>x[0]).join("").length===3],
 ["T6",Array.from({length:32},(_,t)=>rings.every((_,k)=>radius(t,k)>=0.88-1e-12&&radius(t,k)<=1.12+1e-12)).every(Boolean)],
 ["T7",identity.aliases[0]===before&&Object.isFrozen(identity.aliases)],
 ["T8",changed[12]!==base[12]&&changed[0]===base[0]],
 ["T9",Number.isFinite(metric("coupled"))&&Number.isFinite(metric("uncoupled"))],
 ["T10",["shuffle","reverse","noop"].every(v=>Number.isFinite(v==="noop"?mse(Array(27).fill(0)):metric(v)))]
 ];
 return {seed,checks:results,neighbor_delta:changed[12]-base[12],far_delta:changed[0]-base[0],mse:{coupled:metric("coupled"),uncoupled:metric("uncoupled"),shuffled:metric("shuffle"),reversed:metric("reverse"),noop:mse(Array(27).fill(0))},compositions:{two:first.slice(0,2).map(x=>x[0]).join(""),three:first.slice(0,3).map(x=>x[0]).join("")}};
}
return {protocol:"issue-348",source:"Echo-GPT 06Z",results:seeds.map(model)};
})()