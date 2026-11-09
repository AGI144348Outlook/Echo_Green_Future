// GPT-only synthetic 27-seat temporal ring experiment; no external effects.
// Reproduce in JavaScript: node contract-000/gpt/experiments/ring17.js
const glyphs = [..."אבגדהוזחטיכלמנסעפצקרשת", ..."ךםןףץ"];
const seeds = [9401,9402,9403,9404];
const n=27, eps=1e-11;
function l1(a,b){return a.reduce((s,v,i)=>s+Math.abs(v-b[i]),0)}
function sum(a){return a.reduce((s,v)=>s+v,0)}
function impulse(k){let a=Array(n).fill(0);a[k]=1;return a}
function zero(){return Array(n).fill(0)}
function step(x,op,origin=0){
  let y=Array(n).fill(0);
  for(let i=0;i<n;i++){
    y[i]+=0.6*x[i];
    const j=op==="A"?(i+1)%n:(i+2+origin)%n;
    y[j]+=0.4*x[i];
  }
  return y;
}
function oracle(x,op,origin=0){return Array.from({length:n},(_,j)=>0.6*x[j]+0.4*x[(j-(op==="A"?1:2+origin)+n*3)%n])}
function run(seed){
  const k=seed%n, x=impulse(k), a=step(x,"A"), b=step(x,"B"), un=x.slice();
  let ab=x.slice(),ba=x.slice();
  for(let t=0;t<26;t++){ab=step(ab,t%2===0?"A":"B");ba=step(ba,t%2===0?"B":"A")}
  // Noncommuting topology: A/B are cyclic shifts, so they commute. Record null honestly.
  const results={
    glyph_identity: glyphs.length===27&&new Set(glyphs).size===27,
    replay: l1(step(x,"A"),step(x,"A"))===0,
    zero: l1(step(zero(),"A"),zero())===0,
    local: Math.abs(a[k]-0.6)<eps,
    neighbor: Math.abs(a[(k+1)%n]-0.4)<eps,
    distant: Math.abs(a[(k+8)%n])<eps,
    uncoupled: l1(un,x)===0,
    topology: l1(a,b)>0,
    phase_order: l1(ab,ba)>eps,
    conservation_oracle: Math.abs(sum(a)-1)<eps&&l1(a,oracle(x,"A"))<eps
  };
  return {seed,tests:results,phase_l1:l1(ab,ba),topology_l1:l1(a,b),mass:sum(a)};
}
const report={version:"ring17-v1",seeds,results:seeds.map(run)};
if(typeof module!=="undefined")module.exports={report,run};
if(typeof console!=="undefined"&&typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(report,null,2));
