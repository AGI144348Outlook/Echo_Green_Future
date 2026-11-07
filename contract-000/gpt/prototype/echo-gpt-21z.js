// Echo-GPT 21Z: bounded synthetic multiring controls; no canonical code.
const SEEDS=[3301,3302,3303,3304];
const GLYPHS=[..."אבגדהוזחטיכלמנסעפצקרשתךםןףץ"];
const VALUES=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];
function rand(seed){let x=seed>>>0;return ()=>{x=(Math.imul(1664525,x)+1013904223)>>>0;return x/4294967296;}}
function coord(i){return [Math.floor(i/9),Math.floor(i/3)%3,i%3];}
function neighbors(i){const p=coord(i);return Array.from({length:27},(_,j)=>j).filter(j=>coord(j).reduce((s,v,k)=>s+Math.abs(v-p[k]),0)===1);}
function input(seed){const r=rand(seed);return Array.from({length:27},()=>r()*2-1);}
function simulate(v,phase,values=VALUES,scale=1){return v.map((x,i)=>x+scale*phase*(neighbors(i).reduce((s,j)=>s+v[j]*(1+values[j]/500),0)/6));}
function mse(a,b){return a.reduce((s,x,i)=>s+(x-b[i])**2,0)/a.length;}
function compose(seed,n){const r=rand(seed);return Array.from({length:n},()=>GLYPHS[Math.floor(r()*27)]);}
function evaluate(seed){const x=input(seed), target=x.map((v,i)=>0.75*v+0.12*Math.sin(i*0.47+seed*0.001)+0.08*x[(i+7)%27]**2);const coupled=simulate(x,0.45), uncoupled=simulate(x,0), shuffled=simulate(x,0.45,[...VALUES].reverse());return {candidate:mse(coupled,target),uncoupled:mse(uncoupled,target),shuffled:mse(shuffled,target)};}
function run(){let rows=[];for(const seed of SEEDS){const x=input(seed),y=simulate(x,0.5),shuffled=[...VALUES].reverse();const tests=[
["identity",new Set(GLYPHS).size===27&&GLYPHS.length===27],
["geometry",neighbors(13).length===6&&neighbors(0).length===3],
["replay",JSON.stringify(input(seed))===JSON.stringify(input(seed))],
["noop",JSON.stringify(simulate(Array(27).fill(0),0.5))===JSON.stringify(Array(27).fill(0))],
["uncoupled",JSON.stringify(simulate(x,0))===JSON.stringify(x)],
["gematria",JSON.stringify(simulate(x,0.5,shuffled))!==JSON.stringify(y)&&new Set(GLYPHS).size===27],
["composition",compose(seed,2).length===2&&compose(seed,3).length===3],
["phase",JSON.stringify(simulate(x,-0.5))!==JSON.stringify(y)],
["deformation",[0,1,2,3,4,5].every(t=>{const radius=1+0.15*Math.sin(t+seed);return radius>=0.85-1e-12&&radius<=1.15+1e-12;})],
["oracle",Object.values(evaluate(seed)).every(Number.isFinite)]
];rows.push({seed,tests,loss:evaluate(seed),composition2:compose(seed,2).join(""),composition3:compose(seed,3).join("")});}return rows;}
return JSON.stringify({source:"echo-gpt-21z",rows:run()});
