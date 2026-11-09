// GPT-only synthetic 27-seat ring experiment v21; Issue #378 preregistered.
const GLYPHS=[..."אבגדהוזחטיכלמנסעפצקרשת","ך","ם","ן","ף","ץ"];
const seeds=[9801,9802,9803,9804], N=27;
function input(seed){let x=seed>>>0;return Array.from({length:N},()=>{x=(Math.imul(x,1664525)+1013904223)>>>0;return (x%1000+1)/1000;});}
function A(v){let o=Array(N).fill(0);for(let i=0;i<N;i++){o[i]+=.8*v[i];o[(i+1)%N]+=.1*v[i];o[(i+N-1)%N]+=.1*v[i];}return o;}
function B(v){let o=Array(N).fill(0);for(let i=0;i<N;i++)o[(i*2)%N]=v[i];return o;}
function C(v,gain=.15,rewire=false){let o=Array(N).fill(0);for(let i=0;i<N;i++){o[i]+=(1-gain)*v[i];o[(i+(rewire?7:3))%N]+=gain*v[i];}return o;}
function oracleC(v,g=.15,rewire=false){return Array.from({length:N},(_,j)=>(1-g)*v[j]+g*v[(j+N-(rewire?7:3))%N]);}
const L1=(a,b)=>a.reduce((s,x,i)=>s+Math.abs(x-b[i]),0);
const sum=v=>v.reduce((s,x)=>s+x,0);
function run(seed){let x=input(seed),ab=B(A(x)),abc=C(ab),abi=C(ab,0),low=C(ab,.05),high=C(ab,.15),rew=C(ab,.15,true);
let tests={
glyphs:GLYPHS.length===27&&new Set(GLYPHS).size===27,
replay:JSON.stringify(input(seed))===JSON.stringify(input(seed)),
zero:L1(C(B(A(Array(N).fill(0)))),Array(N).fill(0))===0,
mass:Math.abs(sum(abc)-sum(x))<1e-10,
zero_coupling:L1(C(ab,0),ab)===0,
matched_effect:L1(abc,abi)>1e-8,
dose_order:L1(high,abi)>L1(low,abi)>0,
rewired_topology:L1(rew,abc)>1e-8&&Math.abs(sum(rew)-sum(abc))<1e-10,
incoming_oracle:L1(abc,oracleC(ab))<1e-10
};return {seed,tests,metrics:{matched:L1(abc,abi),dose_low:L1(low,abi),dose_high:L1(high,abi),rewired:L1(rew,abc),oracle:L1(abc,oracleC(ab)),mass_error:Math.abs(sum(abc)-sum(x))}};}
function evaluate(){return seeds.map(run);}
