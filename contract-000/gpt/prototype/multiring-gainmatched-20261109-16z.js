// GPT-owned synthetic temporal multiring experiment, 2026-11-09 16Z.
// Fixed-seed 27-seat model; no physical or semantic claims.
const GLYPHS=[..."אבגדהוזחטיכלמנסעפצקרשת",..."ךםןףץ"];
const N=27, SEEDS=[9301,9302,9303,9304];
function update(x,g,step=1,uncoupled=false){
 const y=Array(N).fill(0);
 for(let i=0;i<N;i++){
  y[i]+=0.6*x[i];
  if(!uncoupled){y[(i+step)%N]+=g*x[i]/2;y[(i-step+N)%N]+=g*x[i]/2;}
 }
 return y;
}
function evolve(x,gains,step=1){for(const g of gains)x=update(x,g,step);return x;}
function sum(x){return x.reduce((a,b)=>a+b,0);}
function l1(x,y){return x.reduce((s,v,i)=>s+Math.abs(v-y[i]),0);}
function close(a,b,eps=1e-10){return Math.abs(a-b)<eps;}
function run(seed){
 const i=seed%N, impulse=Array(N).fill(0);impulse[i]=1;
 const zero=Array(N).fill(0),g=0.25;
 const one=update(impulse,g),far=one[(i+4)%N];
 const schedule=Array.from({length:27},(_,t)=>g+0.1*Math.sin(2*Math.PI*t/27));
 const mean=sum(schedule)/27, normalized=schedule.map(v=>v*g/mean);
 const constant=Array(27).fill(g);
 const a=evolve(impulse,normalized),b=evolve(impulse,constant);
 const reversed=evolve(impulse,[...normalized].reverse());
 const shuffled=[...normalized].sort((x,y)=>x-y);
 const sh=evolve(impulse,shuffled);
 const rewire=update(impulse,g,5);
 const checks={
  glyph_unique:GLYPHS.length===N&&new Set(GLYPHS).size===N,
  deterministic_replay:l1(a,evolve(impulse,normalized))===0,
  zero_noop:sum(evolve(zero,normalized))===0,
  local_impulse:close(one[i],0.6),
  nearest_neighbor:close(one[(i+1)%N],0.125),
  distant_instantaneous:far===0,
  uncoupled_neighbor:update(impulse,g,1,true)[(i+1)%N]===0,
  rewiring_mass:close(sum(one),sum(rewire))&&l1(one,rewire)>0,
  gain_matched_phase:close(sum(normalized),sum(constant))&&l1(a,b)>0,
  phase_order_and_mass:close(sum(a),sum(reversed))&&close(sum(a),sum(sh))&&close(sum(one),0.6+g)
 };
 return {seed,checks,measurements:{gain_sum:sum(normalized),constant_gain_sum:sum(constant),phase_L1:l1(a,b),reversed_L1:l1(a,reversed),shuffled_L1:l1(a,sh),rewire_L1:l1(one,rewire),one_mass:sum(one),final_mass:sum(a),final_constant_mass:sum(b)}};
}
const results=SEEDS.map(run);
const output={model:"synthetic linear cyclic 27-seat two-ring",seeds:SEEDS,types:Object.keys(results[0].checks),total:results.length*Object.keys(results[0].checks).length,passed:results.reduce((s,r)=>s+Object.values(r.checks).filter(Boolean).length,0),results};
if(typeof module!=="undefined")module.exports={run,output};
if(typeof console!=="undefined")console.log(JSON.stringify(output,null,2));
