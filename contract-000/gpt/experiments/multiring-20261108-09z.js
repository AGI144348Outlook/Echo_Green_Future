// GPT-owned Echo multiring synthetic test, #352; deterministic, no external effects.
const seeds=[3301,3302,3303,3304];
function run(seed){
 const glyph=Array.from({length:27},(_,i)=>i);
 const rotate=(a,n)=>a.map((_,i)=>a[(i+n+a.length)%a.length]);
 const r=rotate(glyph,seed%27), back=rotate(r,27-seed%27);
 const orderA=[r[0],r[9]].join('-'),orderB=[r[9],r[0]].join('-');
 const triple=[r[0],r[9],r[18]];
 const rad=Array.from({length:27},(_,i)=>1+.08*Math.sin(i+seed));
 const grid=(i)=>[Math.floor(i/9),Math.floor(i/3)%3,i%3];
 const adjacent=(a,b)=>grid(a).reduce((s,v,i)=>s+Math.abs(v-grid(b)[i]),0)===1;
 const field=(delta,index)=>adjacent(index,13)?delta*.025:0;
 const phase=Math.sin(seed*.01), reverse=Math.sin(seed*.01+Math.PI),detune=Math.sin(seed*.01+.4);
 const affinity=(x,y)=>Math.abs((x+1)*7-(y+1)*7);
 const shuffled=(x,y)=>Math.abs((26-x+1)*7-(y+1)*7);
 const target=Array.from({length:27},(_,i)=>.05*Math.sin(i*.7)+.01*Math.cos(i*.13));
 const pred=(mode,i)=>{let base=.025*Math.sin(i*.7+seed*.001);if(mode==='noop')return 0;if(mode==='uncoupled')return base;if(mode==='shuffled')return base+.007*Math.sin(i*1.1);return base+.012*Math.sin(i*.4+phase)};
 const mse=mode=>target.reduce((s,t,i)=>s+(pred(mode,i)-t)**2,0)/27;
 const metrics={coupled:mse('coupled'),uncoupled:mse('uncoupled'),shuffled:mse('shuffled'),noop:mse('noop')};
 const checks={
 identity_unique:new Set(r).size===27,
 rotation_inverse:back.every((v,i)=>v===i),
 ordered_pair:orderA!==orderB,
 triple_length:triple.length===3&&new Set(triple).size===3,
 bounded_deformation:rad.every(x=>x>=.92-1e-12&&x<=1.08+1e-12),
 local_intervention:field(.4,12)>.009&&field(.4,0)===0,
 phase_reversal:Math.abs(phase-reverse)>1e-5,
 detuning:Math.abs(phase-detune)>1e-5,
 gematria_shuffle:affinity(0,5)!==shuffled(0,5),
 control_comparison:Object.values(metrics).every(Number.isFinite)&&new Set(Object.values(metrics).map(x=>x.toFixed(12))).size>=3
 };
 return {seed,checks,metrics,intervention:{neighbor:field(.4,12),distant:field(.4,0)}};
}
JSON.stringify(seeds.map(run));