// GPT-owned bounded synthetic multiring experiment; preregistered Issue #341.
// No canonical claims. Run with node or V8 eval; zero dependencies.
const SEEDS=[3301,3302,3303,3304];
const GLYPHS=[...'אבגדהוזחטיכלמנסעפצקרשתךםןףץ'];
const GEM=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];
function evaluate(seed){
  let x=seed>>>0;const rnd=()=>((x=(1664525*x+1013904223)>>>0)/4294967296);
  const phase=[rnd()*6.283185307179586,rnd()*6.283185307179586,rnd()*6.283185307179586];
  const freq=[0.071,0.113,0.173];
  const ring=(t,k,intervention=0)=>{const a=phase[k]+freq[k]*t+(k===0?intervention:0);const radius=1+0.12*Math.sin(0.13*t+k);return Array.from({length:27},(_,i)=>[radius*Math.cos(a+2*Math.PI*i/27),radius*Math.sin(a+2*Math.PI*i/27)]);};
  const compose=(t,n)=>Array.from({length:n},(_,k)=>GLYPHS[Math.floor(((phase[k]+freq[k]*t)/(2*Math.PI))*27+7*k)%27]).join('');
  const cube=i=>[Math.floor(i/9),Math.floor(i/3)%3,i%3];
  const pred=(t,coupled=1,shuffle=false,intervention=0)=>{
    const weights=shuffle?[...GEM].reverse():GEM;
    let v=0;for(let i=0;i<27;i++)v+=(weights[i]/400)*Math.sin(phase[i%3]+freq[i%3]*t+i*2*Math.PI/27);
    return v/27*(1+coupled*0.25*Math.cos(phase[0]-phase[1]+intervention));
  };
  // External mathematical target: nonlinear time rule, independent of candidate weights and ring formula.
  const target=Array.from({length:16},(_,j)=>Math.tanh(0.4*Math.sin((j+16)*0.29+(seed%19)*0.1)+0.22*Math.cos((j+16)*0.17)));
  const mse=(c,s=false)=>target.reduce((a,y,j)=>a+(pred(j+16,c,s)-y)**2,0)/16;
  const noop=target.reduce((a,y)=>a+y*y,0)/16;
  const checks={
    glyph_census:GLYPHS.length===27&&new Set(GLYPHS).size===27,
    cross_call_replay:JSON.stringify(ring(5,1))===JSON.stringify(ring(5,1)),
    cube_bijection:new Set(Array.from({length:27},(_,i)=>cube(i).join(','))).size===27,
    ordered_two_ring:compose(4,2).length===2&&[...compose(4,2)].every(c=>GLYPHS.includes(c)),
    ordered_three_ring:compose(4,3).length===3&&[...compose(4,3)].every(c=>GLYPHS.includes(c)),
    phase_motion:JSON.stringify(ring(0,0))!==JSON.stringify(ring(1,0)),
    bounded_deformation:[0,1,2].every(k=>[0,1,5,12,31].every(t=>ring(t,k).every(p=>Math.hypot(...p)>0.879&&Math.hypot(...p)<1.121))),
    uncoupled_intervention_inert:pred(8,0,false,0)===pred(8,0,false,1.5),
    gematria_shuffle_changes:Math.abs(pred(8,1,false)-pred(8,1,true))>1e-12,
    heldout_metrics_finite:[mse(1),mse(0),mse(1,true),noop].every(Number.isFinite)
  };
  return {seed,checks,mse:{coupled:mse(1),uncoupled:mse(0),shuffled:mse(1,true),noop},sample2:compose(4,2),sample3:compose(4,3),intervention_delta:pred(8,1,false,1.5)-pred(8,1,false,0)};
}
function run(){const runs=SEEDS.map(evaluate);return {seeds:SEEDS,runs,pass:runs.reduce((n,r)=>n+Object.values(r.checks).filter(Boolean).length,0),fail:runs.reduce((n,r)=>n+Object.values(r.checks).filter(v=>!v).length,0)};}
if(typeof module!=='undefined')module.exports={run,evaluate};
