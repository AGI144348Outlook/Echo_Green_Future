// GPT-only noncanonical multiring experiment. Node 18+ or isolated V8: evaluate runPortfolio().
function runPortfolio(){
 const glyphs=Array.from({length:27},(_,i)=>String.fromCodePoint(0x05d0+(i%22))+(i>=22?'*'+(i-22):'')); // synthetic 27 distinct labels, NOT Hebrew final-form registry
 const seeds=[3301,3302,3303,3304], results=[];
 const near=(a,b)=>Math.abs(a-b)<1e-12;
 function rng(seed){let s=seed>>>0;return ()=>((s=(1664525*s+1013904223)>>>0)/4294967296);}
 function model(seed,opts={},input=null){
  const r=rng(seed),x=input||Array.from({length:27},()=>r()*.2-.1), out=[];
  const freq=opts.detune?1.31:1, phase=opts.reverse?-1:1;
  for(let i=0;i<27;i++){
   const theta=(i+1)*.17*freq+(opts.frozen?0:((seed%13)+1)*.003)*phase;
   const weight=(opts.shuffle?((i*7+3)%27):i)/27;
   const deform=opts.rigid?0:.02*Math.sin(theta);
   const neighbor=opts.uncoupled?0:.025*x[(i+1)%27];
   out.push(x[i]+neighbor+.012*Math.sin(theta)*(.5+weight)+deform*.05);
  }
  return {out,x,radii:Array.from({length:27},(_,i)=>1+(opts.rigid?0:.02*Math.sin((i+1)*.17*freq)))};
 }
 function compose(indices){return indices.map(i=>glyphs[i]).join('|');}
 for(const seed of seeds){
  const base=model(seed),unc=model(seed,{uncoupled:true}),noop=base.x;
  const frozen=model(seed,{frozen:true}),rev=model(seed,{reverse:true}),det=model(seed,{detune:true}),shuffle=model(seed,{shuffle:true}),rigid=model(seed,{rigid:true});
  const changed=base.x.slice();changed[13]+=.4;
  const intervention=model(seed,{},changed),interventionUnc=model(seed,{uncoupled:true},changed);
  const targetRng=rng(seed+900000);const target=base.x.map(x=>x+.002*(targetRng()-.5));
  const mse=a=>a.reduce((s,v,i)=>s+(v-target[i])**2,0)/27;
  const checks=[
   new Set(glyphs).size===27 && glyphs.length===27,
   compose([2,4])===glyphs[2]+'|'+glyphs[4]&&compose([2,4])!==compose([4,2]),
   compose([3,9,3])===glyphs[3]+'|'+glyphs[9]+'|'+glyphs[3],
   base.out.some((v,i)=>!near(v,frozen.out[i])),
   base.out.some((v,i)=>!near(v,rev.out[i])),
   base.out.some((v,i)=>!near(v,det.out[i])),
   base.out.some((v,i)=>!near(v,shuffle.out[i])),
   base.radii.every(v=>v>=.98-1e-12&&v<=1.02+1e-12)&&rigid.radii.every(v=>v===1),
   near(intervention.out[12]-base.out[12],.01)&&near(intervention.out[0],base.out[0])&&near(interventionUnc.out[12],unc.out[12]),
   JSON.stringify(model(seed).out)===JSON.stringify(base.out)&&Number.isFinite(mse(base.out))&&Number.isFinite(mse(unc.out))&&Number.isFinite(mse(noop))
  ];
  results.push({seed,checks,passed:checks.filter(Boolean).length,mse:{coupled:mse(base.out),uncoupled:mse(unc.out),noop:mse(noop),shuffled:mse(shuffle.out)},intervention:intervention.out[12]-base.out[12]});
 }
 return {protocol:"issue-362",source:"gpt-19z",seeds,types:10,results,passed:results.reduce((a,r)=>a+r.passed,0),total:40,limitations:["synthetic 27 labels not canonical glyph registry","evaluation target independently seeded but input visible","structural tests not evidence of intelligence","no parameter learning"]};
}
if(typeof module!=='undefined'&&require.main===module)console.log(JSON.stringify(runPortfolio(),null,2));
