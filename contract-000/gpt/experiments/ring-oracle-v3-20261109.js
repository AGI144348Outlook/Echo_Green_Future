// Echo-GPT v3: bounded synthetic 27-seat ring oracle; seeds 9501-9504.
const GLYPHS=[..."אבגדהוזחטיכלמנסעפצקרשת",..."ךםןףץ"];
const N=27, seeds=[9501,9502,9503,9504];
function rng(seed){let s=seed>>>0;return ()=>((s=(1664525*s+1013904223)>>>0)/4294967296)}
function vec(seed){const r=rng(seed),v=Array.from({length:N},()=>r());const z=v.reduce((a,b)=>a+b,0);return v.map(x=>x/z)}
function zeros(){return Array(N).fill(0)}
function A(x){const y=zeros();for(let i=0;i<N;i++){y[i]+=.6*x[i];y[(i+1)%N]+=.4*x[i]}return y}
function dest(i){return (i+(i%2===0?2:-2)+N)%N}
function B(x){const y=zeros();for(let i=0;i<N;i++){y[i]+=.6*x[i];y[dest(i)]+=.4*x[i]}return y}
function BOracle(x){return Array.from({length:N},(_,j)=>.6*x[j]+.4*x.reduce((s,v,i)=>s+(dest(i)===j?v:0),0))}
function C(x){const y=zeros();for(let i=0;i<N;i++){y[i]+=.6*x[i];y[(i+3)%N]+=.4*x[i]}return y}
function shuffleB(x){const y=zeros();for(let i=0;i<N;i++){y[i]+=.6*x[i];y[(dest(i)+7)%N]+=.4*x[i]}return y}
function sum(x){return x.reduce((a,b)=>a+b,0)}
function l1(a,b){return a.reduce((s,v,i)=>s+Math.abs(v-b[i]),0)}
function run(){return seeds.map(seed=>{const x=vec(seed),z=zeros(),a=A(x),b=B(x),ab=B(a),ba=A(b),sb=shuffleB(a),third=C(ab);const checks={glyph_unique:GLYPHS.length===N&&new Set(GLYPHS).size===N,zero_noop:l1(A(z),z)===0&&l1(B(z),z)===0,replay:l1(vec(seed),x)===0,A_mass:Math.abs(sum(a)-1)<1e-12,B_mass:Math.abs(sum(b)-1)<1e-12,B_oracle:l1(b,BOracle(x))<1e-12,phase_order:l1(ab,ba)>1e-8,uncoupled:l1(x,x)===0,shuffle_topology:l1(ab,sb)>1e-8,ring_count:l1(ab,third)>1e-8};return {seed,checks,metrics:{phase_l1:l1(ab,ba),oracle_l1:l1(b,BOracle(x)),shuffle_l1:l1(ab,sb),third_l1:l1(ab,third),massB:sum(b)}}})}
if(typeof module!=="undefined")module.exports={run,GLYPHS,A,B,BOracle};
