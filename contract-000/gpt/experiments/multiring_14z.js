// GPT-only 14Z ring experiment. Preregistered Issue #357. V8 standalone, no I/O.
const seeds=[3301,3302,3303,3304], glyphs=[...'אבגדהוזחטיכלמנסעפצקרשתךםןףץ'], gem=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];
const mod=(a,n)=>(a%n+n)%n;
function rng(seed){let x=seed>>>0;return ()=>((x=(Math.imul(x,1664525)+1013904223)>>>0)/4294967296)}
function calc(seed,opt={}){const rand=rng(seed),starts=[0,9,18],fre=[.12,.19*(opt.detune?1.41:1),.27],g=[...gem];if(opt.shuffle){let rr=rng(seed+17);for(let i=26;i>0;i--){let j=Math.floor(rr()*(i+1));[g[i],g[j]]=[g[j],g[i]]}}
let vals=[],words=[],positions=[],radii=[];
for(let t=0;t<12;t++){let offs=starts.map((v,k)=>opt.frozen?v:mod(v+(t+1)*(k+1),27));let rad=starts.map((_,k)=>opt.rigid?1:1+.11*Math.sin(.21*t+.7*k));radii.push(...rad);positions.push([...Array(27)].map((_,j)=>mod(j+offs[0],27)));words.push(offs.map(x=>glyphs[x]).join(''));
for(let i=0;i<27;i++){let a=mod(i+offs[0],27),bb=mod(i+offs[1],27),c=mod(i+offs[2],27),phase=(opt.reverse?-1:1)*fre.reduce((x,y)=>x+y,0)*t;let signal=.014*Math.sin(phase+.13*g[a]+.07*g[bb]+.04*g[c])*rad.reduce((x,y)=>x*y,1);let base=.003*Math.cos(.31*i+.09*t);vals.push(base+(opt.uncoupled?0:signal));}}
if(opt.intervention){for(let t=0;t<12;t++)vals[t*27+12]+=.01}return {vals,words,positions,radii};}
const mse=(a,b)=>a.reduce((s,x,i)=>s+(x-b[i])**2,0)/a.length;
function run(){let rows=[];for(let seed of seeds){let base=calc(seed),frozen=calc(seed,{frozen:true}),rigid=calc(seed,{rigid:true}),reverse=calc(seed,{reverse:true}),detune=calc(seed,{detune:true}),shuffle=calc(seed,{shuffle:true}),unc=calc(seed,{uncoupled:true}),inter=calc(seed,{intervention:true});let rr=rng(seed+100000),target=base.vals.map((_,i)=>.004*Math.cos(.23*(i%27)+.17*Math.floor(i/27))+.002*(rr()-.5));let no=target.map(()=>0);let checks={
T1_27_unique:base.positions.every(p=>new Set(p).size===27),
T2_two_order:base.words.every((w,t)=>w.slice(0,2)===[glyphs[mod(0+t+1,27)],glyphs[mod(9+2*(t+1),27)]].join('')),
T3_three_order:base.words.every((w,t)=>w===[glyphs[mod(t+1,27)],glyphs[mod(9+2*(t+1),27)],glyphs[mod(18+3*(t+1),27)]].join('')),
T4_motion:mse(base.vals,frozen.vals)>1e-9,
T5_boundary:mse(base.vals,rigid.vals)>1e-10&&base.radii.every(x=>x>=.89&&x<=1.11),
T6_phase:mse(base.vals,reverse.vals)>1e-9,
T7_detune:mse(base.vals,detune.vals)>1e-9,
T8_shuffle:mse(base.vals,shuffle.vals)>1e-9,
T9_intervention:Math.abs(inter.vals[12]-base.vals[12]-.01)<1e-12&&inter.vals[0]===base.vals[0],
T10_target:target.length===324&&mse(base.vals,target)>0};
rows.push({seed,checks,mse:{coupled:mse(base.vals,target),uncoupled:mse(unc.vals,target),no_op:mse(no,target),shuffled:mse(shuffle.vals,target)},delta12:inter.vals[12]-base.vals[12]});}
return {rows,passed:rows.reduce((s,r)=>s+Object.values(r.checks).filter(Boolean).length,0),total:40};}
