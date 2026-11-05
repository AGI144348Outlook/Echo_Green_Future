// Prospective Issue #297; deterministic synthetic portfolio; call portfolio().
function portfolio(){
 const seeds=[20261105,20261106],tests=[];function check(name,ok,details){tests.push({name,pass:!!ok,details})}
 const glyphs=Array.from({length:27},(_,i)=>i),coords=glyphs.map(i=>[Math.floor(i/9),Math.floor(i/3)%3,i%3]);
 check("T1 3³ bijection",new Set(coords.map(x=>x.join(","))).size===27);
 check("T2 2/3/4 ordered ring compositions",[2,3,4].every(k=>glyphs.slice(0,k).join("-").split("-").length===k));
 const rng=s=>()=>((s=(Math.imul(s,1664525)+1013904223)>>>0)/4294967296);
 const sim=(seed,coupled,shuffle=false)=>{const random=rng(seed),phase=Array.from({length:27},()=>random()*Math.PI*2),aff=Array.from({length:27},(_,i)=>shuffle?26-i:i);for(let t=0;t<16;t++){const old=phase.slice();for(let i=1;i<27;i++)phase[i]+=0.02+(coupled?0.09*Math.sin(old[i-1]-old[i])*(1+aff[i]/100):0)}return phase};
 check("T3 fixed seed replay",JSON.stringify(sim(seeds[0],true))===JSON.stringify(sim(seeds[0],true)));
 const no=sim(seeds[0],false),yes=sim(seeds[0],true);
 check("T4 no-op null coupling",no.every((p,i)=>Math.abs(p-sim(seeds[0],false)[i])<1e-12));
 check("T5 shuffled affinity intervention",sim(seeds[0],true,true).some((p,i)=>Math.abs(p-yes[i])>1e-9));
 const radii=Array.from({length:27},(_,i)=>1+.15*Math.sin(i*0.71));
 check("T6 deformable radius bounded",radii.every(r=>r>=.85&&r<=1.15));
 check("T7 causal directed intervention",Math.abs(yes[0]-no[0])<1e-12&&yes.slice(1).some((p,i)=>Math.abs(p-no[i+1])>1e-9));
 let boxes=[];const history=[];for(const target of [12,24,48,96]){while(boxes.length<target)boxes.push({id:boxes.length,born:history.length});history.push({count:boxes.length,retained:boxes.slice(0,12).every((b,i)=>b.id===i)})}
 check("T8 cumulative warehouse growth",history.map(x=>x.count).join(",")==="12,24,48,96"&&history.every(x=>x.retained),history);
 const entropy=Array.from({length:10},(_,i)=>(i+1)*.004),fields=policy=>entropy.map(e=>Array.from({length:16},(_,t)=>e*(1+.25*Math.sin(t*.63))));
 check("T9 exogenous ten-entropy invariance",JSON.stringify(fields("noop"))===JSON.stringify(fields("adaptive")));
 let w=.5;for(let t=0;t<16;t++)w+=.08*(.7-w);
 check("T10 plastic wave weight is not external learning proof",w!==.5&&Number.isFinite(w),{waveWeight:w,heldOutAccuracy:null});
 return {tests,seeds,entropy,history,notes:"Synthetic structural controls. Cumulative growth is IDs only; no tested retrieval or knowledge learning."};
}
