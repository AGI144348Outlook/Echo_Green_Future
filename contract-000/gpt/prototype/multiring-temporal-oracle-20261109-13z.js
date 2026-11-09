// GPT-only synthetic temporal 27-seat ring, fixed seeds. No external effects.
const GLYPHS=[..."אבגדהוזחטיכלמנסעפצקרשת",..."ךםןףץ"];
const N=27, seeds=[8801,8802,8803,8804];
function step(v,g){const out=Array(N).fill(0);for(let i=0;i<N;i++){out[i]+=0.6*v[i];out[(i+1)%N]+=g*v[i];out[(i+N-1)%N]+=g*v[i];}return out;}
function oracle(v,g){return Array.from({length:N},(_,j)=>0.6*v[j]+g*(v[(j+N-1)%N]+v[(j+1)%N]));}
function pulse(i){let a=Array(N).fill(0);a[i]=1;return a;}
function close(a,b){return a.every((v,i)=>Math.abs(v-b[i])<1e-12);}
function run(seed){let s=seed%N,g=0.1+(seed%5)*0.01;let base=pulse(s),n=Array(N).fill(0),a=step(base,g),b=oracle(base,g),d=step(n,g);
let trace=base,or=base,traceOK=true;for(let t=0;t<27;t++){trace=step(trace,g);or=oracle(or,g);traceOK=traceOK&&close(trace,or);}
const shuffled=(s+7)%N;let shifted=pulse(shuffled),sh=step(shifted,g);let phase=Math.cos((seed%9)*0.11),freq=1+(seed%7)*0.02,radius=1+0.05*Math.sin(seed);let identity=JSON.stringify(GLYPHS);
return {seed,source:s,g,tests:{
T1:new Set(GLYPHS).size===27,
T2:GLYPHS[s]+GLYPHS[(s+1)%N]===GLYPHS.slice(s).concat(GLYPHS.slice(0,s)).slice(0,2).join(""),
T3:[0,1,2].map(k=>GLYPHS[(s+k)%N]).join("").length===3,
T4:new Set(Array.from({length:27},(_,t)=>(s+t)%27)).size===27,
T5:Math.abs(a[s]-d[s])>0.5,
T6:close(a,b)&&traceOK,
T7:a[(s+7)%N]===0,
T8:step(base,0)[(s+1)%N]===0,
T9:a[(s+1)%N]!==sh[(s+1)%N],
T10:Math.abs(phase)<=1&&freq>0&&radius>=0.95&&radius<=1.05&&identity===JSON.stringify(GLYPHS)},
observed:{local:a[s],neighbor:a[(s+1)%N],distant:a[(s+7)%N],uncoupled:step(base,0)[(s+1)%N],shuffleReceiver:sh[(s+1)%N],phase,freq,radius,traceOracleMatch:traceOK}};}
JSON.stringify({runtime:"JavaScript ES2020",seeds,results:seeds.map(run)});
