// GPT-only bounded 3x3x3 local-intervention portfolio. No external effects.
const SEEDS=[1109,2203,3301,4409];
const xyz=i=>[Math.floor(i/9),Math.floor(i/3)%3,i%3];
const dist=(a,b)=>xyz(a).reduce((s,v,j)=>s+Math.abs(v-xyz(b)[j]),0);
const neighbors=i=>Array.from({length:27},(_,j)=>j).filter(j=>dist(i,j)===1);
const gem=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900];
function step(state,source,amplitude,coupling,phase=1){let out=state.slice();for(let i=0;i<27;i++){let influence=neighbors(i).includes(source)?amplitude*coupling*phase:0;out[i]+=influence;}return out;}
function portfolio(){let rows=[];for(const seed of SEEDS){let state=Array(27).fill(0),center=13,delta=(seed%7+1)/10;
let shuffled=gem.slice();let offset=seed%26+1;shuffled=shuffled.map((_,i)=>gem[(i+offset)%27]);
const cases=[
["T1 identity bijection",new Set(Array.from({length:27},(_,i)=>xyz(i).join(","))).size===27],
["T2 neighbor degree",neighbors(center).length===6&&neighbors(0).length===3],
["T3 center intervention",neighbors(center).every(i=>step(state,center,delta,1)[i]===delta)],
["T4 nonneighbor exclusion",Array.from({length:27},(_,i)=>i).filter(i=>dist(i,center)!==1).every(i=>step(state,center,delta,1)[i]===0)],
["T5 no-op stationary",step(state,center,0,1).every(v=>v===0)],
["T6 deterministic replay",JSON.stringify(step(state,center,delta,1))===JSON.stringify(step(state,center,delta,1))],
["T7 shuffled gematria",shuffled.some((v,i)=>v!==gem[i])&&shuffled.slice().sort((a,b)=>a-b).join(",")===gem.slice().sort((a,b)=>a-b).join(",")],
["T8 phase decoupling",step(state,center,delta,1,0).every(v=>v===0)],
["T9 bounded deformation",Array.from({length:27},(_,i)=>xyz(i).map(v=>v+0.1*Math.sin(seed+i+v)).every(v=>v>=-0.1&&v<=2.1)).every(Boolean)],
["T10 null coupling",step(state,center,delta,0).every(v=>v===0)]
];for(const [type,pass] of cases)rows.push({seed,type,pass});}return rows;}
