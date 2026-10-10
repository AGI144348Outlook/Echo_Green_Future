"use strict";
// NVE-D 047 finite DVE reproducibility runner. Requires sanitized_corpus.json (upstream Git blob 6b9c3424e6c6d6f64ca5ac47837bf350248953db).
const fs=require("fs");
function run047(rows){
  const src=rows.filter(r=>Array.isArray(r.symbols)&&r.symbols.some(s=>s!=="000")).map(r=>({...r,symbols:r.symbols.filter(s=>s!=="000").map(String)}));
  const seeds=[23,41,83,167],budgets=[250,1000,2500,5000,10000],tau=64;
  const hash=(s)=>{let h=2166136261>>>0;for(let i=0;i<s.length;i++){h=Math.imul(h^s.charCodeAt(i),16777619)>>>0}return h>>>0};
  const rng=(seed)=>()=>{seed=(seed+0x6D2B79F5)>>>0;let t=seed;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return ((t^(t>>>14))>>>0)/4294967296};
  const key=r=>r.symbols.join("|");
  const regimes=["sequence_group","site_block","tablet_block","direction_block"];
  const split=(regime,seed)=>{
    let test,train;
    if(regime==="sequence_group"){
      test=src.filter(r=>hash(key(r)+":"+seed)%5===0);
      train=src.filter(r=>hash(key(r)+":"+seed)%5!==0);
    }else if(regime==="site_block"){
      test=src.filter(r=>["Dholavira","Kalibangan","Lothal"].includes(r.site));
      train=src.filter(r=>!["Dholavira","Kalibangan","Lothal"].includes(r.site));
    }else if(regime==="tablet_block"){
      test=src.filter(r=>String(r.artefact_type).startsWith("TAB"));
      train=src.filter(r=>!String(r.artefact_type).startsWith("TAB"));
    }else{
      test=src.filter(r=>r.direction==="L/R");
      train=src.filter(r=>r.direction==="R/L");
    }
    const testKeys=new Set(test.map(key));train=train.filter(r=>!testKeys.has(key(r)));
    return {test,train,removed_overlap:src.length-test.length-train.length};
  };
  function fit(draws,transform){
    const counts=Array.from({length:7},()=>new Map()),context=Array.from({length:7},()=>new Map());
    const dCounts=new Map(),dContext=new Map(),vocab=new Set();let total=0;
    for(const r of draws){
      let a=r.symbols.slice();
      if(transform==="reverse")a.reverse();
      if(transform==="shuffle"){
        let random=rng(hash(r.id+"|"+total));
        for(let i=a.length-1;i>0;i--){let j=Math.floor(random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}
      }
      for(let i=0;i<a.length;i++){
        const token=a[i];vocab.add(token);total++;
        for(let d=0;d<=6;d++){
          if(d>i)break;
          const c=d?a.slice(i-d,i).join("\u0001"):"";
          const k=c+"\u0002"+token;
          counts[d].set(k,(counts[d].get(k)||0)+1);
          context[d].set(c,(context[d].get(c)||0)+1);
        }
        if(i>0){let c=r.direction+"\u0001"+a[i-1],k=c+"\u0002"+token;dCounts.set(k,(dCounts.get(k)||0)+1);dContext.set(c,(dContext.get(c)||0)+1)}
      }
    }
    return {counts,context,dCounts,dContext,vocab,total};
  }
  function loss(model,test,depth,variant){
    let bits=0,n=0,unknown=0;const V=model.vocab.size+1;
    for(const r of test){
      let a=variant==="reverse"?r.symbols.slice().reverse():r.symbols;
      for(let i=0;i<a.length;i++){
        let token=model.vocab.has(a[i])?a[i]:"<UNSEEN>";
        if(token==="<UNSEEN>")unknown++;
        let p=((model.counts[0].get("\u0002"+token)||0)+1)/(model.total+V);
        for(let d=1;d<=depth;d++){
          if(d>i)break;
          const c=a.slice(i-d,i).join("\u0001");
          p=((model.counts[d].get(c+"\u0002"+token)||0)+tau*p)/((model.context[d].get(c)||0)+tau);
        }
        if(variant==="direction"&&i>0){
          const c=r.direction+"\u0001"+a[i-1];
          p=((model.dCounts.get(c+"\u0002"+token)||0)+tau*p)/((model.dContext.get(c)||0)+tau);
        }
        bits-=Math.log2(p);n++;
      }
    }
    return {loss:n?bits/n:null,n,unknown};
  }
  const cmp=(a,b)=>a==null||b==null?"0":Math.abs(a-b)<1e-12?"=":a<b?">":"<";
  let records=[],checkpoints=[],elapsedStart=Date.now(),trainingDraws=0,trainingTokens=0;
  for(const regime of regimes)for(const seed of seeds){
    const {test,train,removed_overlap}=split(regime,seed);
    if(!test.length||!train.length)continue;
    const random=rng(hash("047|"+regime+"|"+seed));
    let draws=[];
    for(const budget of budgets){
      while(draws.length<budget){const r=train[Math.floor(random()*train.length)];draws.push(r);trainingDraws++;trainingTokens+=r.symbols.length}
      const f=fit(draws,"forward"),rev=fit(draws,"reverse"),sh=fit(draws,"shuffle");
      const uni=loss(f,test,0,"forward"),adj=loss(f,test,1,"forward"),
        d3=loss(f,test,3,"forward"),d6=loss(f,test,6,"forward"),
        direction=loss(f,test,1,"direction"),reverse=loss(rev,test,1,"reverse"),
        shuffle=loss(sh,test,1,"forward");
      const vals={unigram:uni.loss,adjacent:adj.loss,depth3:d3.loss,depth6:d6.loss,direction:direction.loss,matched_reverse:reverse.loss,shuffle_training:shuffle.loss};
      const evaluations={adjacent_vs_unigram:cmp(vals.adjacent,vals.unigram),depth3_vs_adjacent:cmp(vals.depth3,vals.adjacent),depth6_vs_adjacent:cmp(vals.depth6,vals.adjacent),direction_vs_adjacent:cmp(vals.direction,vals.adjacent),forward_vs_matched_reverse:cmp(vals.adjacent,vals.matched_reverse),forward_vs_shuffle:cmp(vals.adjacent,vals.shuffle_training)};
      records.push({regime,seed,budget,train_rows:train.length,test_rows:test.length,removed_overlap,test_tokens:uni.n,unknown_tokens:uni.unknown,losses:vals,evaluation:evaluations});
      if(records.length%20===0)checkpoints.push({records:records.length,rolling_fnv32:hash(records.map(r=>JSON.stringify(r)).join("\n")).toString(16),elapsed_ms:Date.now()-elapsedStart});
    }
  }
  const comparison={};
  for(const r of records)for(const [k,v] of Object.entries(r.evaluation)){if(!comparison[k])comparison[k]={"<":0,">":0,"=":0,"0":0};comparison[k][v]++}
  return {summary:{cycle:"NVE-D-HOURLY-047",source:"ShaktiOSindia/indus-sign-regimes-deposit",source_blob:"6b9c3424e6c6d6f64ca5ac47837bf350248953db",original_rows:rows.length,analyzable_rows:src.length,regimes,seeds,budgets,depths:[0,1,3,6],configurations:records.length,model_evaluations:records.length*7,training_draws:trainingDraws,training_tokens:trainingTokens,comparisons:comparison,elapsed_ms:Date.now()-elapsedStart,checkpoints:checkpoints.length,checkpoint_hash_kind:"FNV32 diagnostic only; Git blob provides content integrity after commit",source_semantics:"opaque sign IDs; no cross-corpus ID mapping"},records,checkpoints};
}
const r=run047(JSON.parse(fs.readFileSync(process.argv[2]||"sanitized_corpus.json","utf8")));
fs.writeFileSync("NVE-D-HOURLY-047-shakti-ledger.jsonl",r.records.map(x=>JSON.stringify(x)).join("\n")+"\n");
fs.writeFileSync("NVE-D-HOURLY-047-shakti-summary.json",JSON.stringify(r.summary,null,2)+"\n");
fs.writeFileSync("NVE-D-HOURLY-047-shakti-checkpoints.json",JSON.stringify(r.checkpoints,null,2)+"\n");
console.log(JSON.stringify(r.summary,null,2));
