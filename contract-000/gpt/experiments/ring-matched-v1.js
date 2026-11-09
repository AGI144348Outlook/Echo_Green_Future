// GPT-owned synthetic 27-seat temporal ring experiment. No external effects.
const GLYPHS = [..."אבגדהוזחטיכלמנסעפצקרשת",..."ךםןףץ"];
const SEEDS = [9601,9602,9603,9604];
const N=27;
function initial(seed){let x=seed>>>0;return Array.from({length:N},()=>{x=(1664525*x+1013904223)>>>0;return 1+(x%997)/997;});}
function A(v){return v.map((_,i)=>0.6*v[i]+0.4*v[(i+N-1)%N]);}
function perm(i){return (i*5+3)%N;}
function B(v){let out=Array(N).fill(0);for(let i=0;i<N;i++){out[i]+=0.7*v[i];out[perm(i)]+=0.3*v[i];}return out;}
function C(v,shift=7){let out=Array(N).fill(0);for(let i=0;i<N;i++){out[i]+=0.8*v[i];out[(i+shift)%N]+=0.2*v[i];}return out;}
function COracle(v,shift=7){return v.map((_,j)=>0.8*v[j]+0.2*v[(j-shift+N)%N]);}
function chain(v,ops){return ops.reduce((s,f)=>f(s),v);}
function sum(v){return v.reduce((a,b)=>a+b,0);}
function l1(a,b){return a.reduce((s,x,i)=>s+Math.abs(x-b[i]),0);}
function evaluate(seed){const v=initial(seed),z=Array(N).fill(0),aba=chain(v,[A,B,A]),abc=chain(v,[A,B,C]),abcShuffled=chain(v,[A,B,w=>C(w,11)]),cOracle=chain(v,[A,B,w=>COracle(w)]),cba=chain(v,[C,B,A]);const tests={
glyph_identity:new Set(GLYPHS).size===27&&GLYPHS.length===27,
replay:l1(abc,chain(initial(seed),[A,B,C]))===0,
zero_input:l1(chain(z,[A,B,C]),z)===0,
mass_conservation:Math.abs(sum(abc)-sum(v))<1e-9,
matched_duration:Number.isFinite(l1(abc,aba))&&l1(abc,aba)>1e-8,
noop_control:l1(aba,chain(v,[A,B,A]))===0,
uncoupled_control:l1(chain(v,[A,B,w=>A(w)]),aba)===0,
shuffled_topology:Number.isFinite(l1(abc,abcShuffled)),
independent_C_oracle:l1(abc,cOracle)<1e-10,
reverse_order:Number.isFinite(l1(abc,cba))
};return {seed,tests,metrics:{matched_l1:l1(abc,aba),shuffled_l1:l1(abc,abcShuffled),order_l1:l1(abc,cba),oracle_l1:l1(abc,cOracle),mass_error:Math.abs(sum(abc)-sum(v))}};}
return {GLYPHS,SEEDS,evaluate};
