// GPT-only synthetic multiring experiment; #345 preregistered before execution.
// Run: node multiring-20261108-03z.js ; no dependencies, no network.
const seeds=[3301,3302,3303,3304];
const glyphs=[...'אבגדהוזחטיכלמנסעפצקרשתךםןףץ'];
const xyz=i=>[Math.floor(i/9),Math.floor(i/3)%3,i%3];
const neighbors=i=>Array.from({length:27},(_,j)=>j).filter(j=>xyz(i).reduce((s,v,k)=>s+Math.abs(v-xyz(j)[k]),0)===1);
const gem=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];
const ring=(s,t,k,reverse=false)=>({phase:(s%97)*.019+t*.27*(reverse?-1:1)+k*.61,radius:1+.12*Math.sin(t*.3+k+s*.001)});
const field=(s,mode='coupled',rings=2,reverse=false)=>Array.from({length:27},(_,i)=>{let z=0;for(let k=0;k<rings;k++){let r=ring(s,3,k,reverse),g=gem[(i+k)%27];if(mode==='shuffle')g=gem[(i*7+k)%27];z+=Math.sin(r.phase+i*.13+g*.001)*r.radius;}return mode==='noop'?0:mode==='uncoupled'?Math.sin(i*.17+s*.001)*.12:z*.12/rings});
const target=(s)=>Array.from({length:27},(_,i)=>Math.tanh((neighbors(i).reduce((v,j)=>v+Math.cos(j*.21+s*.001),0)/Math.max(1,neighbors(i).length))*.23));
const mse=(a,b)=>a.reduce((v,x,i)=>v+(x-b[i])**2,0)/a.length;
function run(){let rows=[];for(const seed of seeds){const a=field(seed),b=field(seed,'uncoupled'),sh=field(seed,'shuffle'),n=field(seed,'noop'),three=field(seed,'coupled',3),rev=field(seed,'coupled',2,true),t=target(seed);
const tests=[
['identity_27',glyphs.length===27&&new Set(glyphs).size===27],
['neighbor_geometry',neighbors(13).length===6&&neighbors(0).length===3],
['deterministic_replay',JSON.stringify(a)===JSON.stringify(field(seed))],
['noop_zero',n.every(x=>x===0)],
['uncoupled_distinct',b.some((x,i)=>x!==a[i])],
['shuffle_perturbation',sh.some((x,i)=>x!==a[i])],
['two_vs_three_rings',three.some((x,i)=>x!==a[i])],
['phase_reversal',rev.some((x,i)=>x!==a[i])],
['deformation_bounds',Array.from({length:4},(_,k)=>ring(seed,k,0).radius).every(r=>r>=.88-1e-12&&r<=1.12+1e-12)],
['causal_locality',neighbors(13).length===6&&neighbors(13).every(i=>i!==13)]
];rows.push({seed,tests:Object.fromEntries(tests),mse:{coupled:mse(a,t),uncoupled:mse(b,t),shuffled:mse(sh,t),noop:mse(n,t),three:mse(three,t),reverse:mse(rev,t)},center_neighbors:neighbors(13)});}return {protocol:'issue-345',seeds,rows};}
if(typeof module!=='undefined'&&require.main===module)console.log(JSON.stringify(run(),null,2));
