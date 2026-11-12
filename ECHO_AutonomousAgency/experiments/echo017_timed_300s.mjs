#!/usr/bin/env node
/**
 * ECHO-017-T300 - real 300-second paced reinforcement session.
 * Pre-registered before execution in GitHub Issue #438, comment 6819972092.
 * Uses the real Echo scoped application-level MCP JSON-RPC handler, NOT HTTP;
 * its four data handlers are a faithful local model of pinned Neon child-branch
 * source cards and provisional evidence links. NO live PostgreSQL credentials.
 * No model/LLM calls. No network/search/shell/SQL tool exposed to Echo.
 */
import {readFileSync,writeFileSync} from "node:fs";
import {fileURLToPath} from "node:url";
import {dirname,resolve,join} from "node:path";
import {performance} from "node:perf_hooks";
import {setTimeout as sleep} from "node:timers/promises";
import {createCardEvidenceRpc} from "../neon/card_evidence_rpc.mjs";
const HERE=dirname(fileURLToPath(import.meta.url));
const ROOT=resolve(HERE,"../..");
const source=JSON.parse(readFileSync(join(ROOT,"matrices/echo_wordnet_chains.json"),"utf8"));
const manifest=JSON.parse(readFileSync(join(HERE,"../neon/echo017_restricted_mcp_tools.json"),"utf8"));
const seed=JSON.parse(readFileSync(join(HERE,"echo017_neon_study_seed.json"),"utf8"));
const tools=["dictionary.lexical_path","catalog.card.get","evidence.edge.trace","evidence.edge.propose"];
const keys=Object.keys(source).sort();
const pairs=keys.flatMap((a,i)=>keys.slice(i+1).map(b=>[a,b]));
const unique=x=>[...new Set(x)];
function guard(cond,msg){if(!cond)throw Error(msg);}
guard(JSON.stringify(manifest.tools.map(t=>t.name))===JSON.stringify(tools),"Tool discovery changed");
guard(manifest.dictionaryIntegrated===true,"Echo dictionary disabled");
guard(keys.length===22&&pairs.length===231,"Unexpected frozen source population");
guard(seed.policy.length===4,"Missing Neon reinforcement seed");
const state=Object.fromEntries(seed.policy.map(r=>[r.action_name,{
  attempts:Number(r.attempts),total_reward:Number(r.total_reward),ema_reward:Number(r.ema_reward)}]));
const visit=new Set(seed.observations.map(r=>r.action_name+"|"+r.word));
let globalStep=Number(seed.progress.global_step),pairCursor=Number(seed.progress.pair_cursor);
let seq=0;
const links=new Map();
links.set("being|existence",{a:"being",b:"existence",
    ancestor:"being",source_card_ids:["lex:being","lex:existence"],
    source_ref:"genesis.wordnet_chain:being|existence",epistemic_state:"proposed",
    relation_type:"shared_lexical_ancestor",origin:"existing-Neon-development-branch"});
const edgeSourceCounts=Object.fromEntries(keys.map(word=>[word,source[word].chain.length]));
const allowedContext={
 authenticated_principal:"synthetic:Echo-A000",
 mission_id:"ECHO-017-T300",
 allowed_tools:tools,
 admitted_words:keys,
 may_propose:true
};
function ancestralCandidate(a,b){
 if(a===b)return null;
 const ea=source[a],eb=source[b];
 if(!ea||!eb)return null;
 const common=unique(ea.chain).filter(ancestor=>
  eb.chain.includes(ancestor) && ancestor!=="entity" &&
  (ea.synset===eb.synset || (ancestor!==a && ancestor!==b)));
 const rank=common.map(term=>({term,df:keys.filter(word=>source[word].chain.includes(term)).length}))
  .filter(x=>ea.synset===eb.synset||x.df<=Math.ceil(keys.length*0.25))
  .sort((x,y)=>x.df-y.df || y.term.length-x.term.length || x.term.localeCompare(y.term));
 return rank[0]||null;
}
function sourceEvidence(a,b){
 const left=source[a],right=source[b];
 return Boolean(left&&right&&left.synset&&right.synset&&
   left.chain.length===edgeSourceCounts[a] &&
   right.chain.length===edgeSourceCounts[b]);
}
const serverAdapter={
 async dictionaryPath({word}){
  const v=source[word];
  return v?{word,...v,source_ref:"genesis.wordnet_chain:"+word,admitted_new_words:0,
      evidence_status:"source_observation_only"}:null;
 },
 async getCard({card_id,revision}){
  const word=card_id.replace(/^lex:/,"");
  if(card_id!=="lex:"+word||!source[word]||revision!==1)return null;
  return {card_id,revision,title:"WordNet "+word,body:source[word],
    review_state:"proposed",provenance:{source_table:"genesis.wordnet_chain",
    source_word:word}};
 },
 async traceEdges({node_id,max_edges=50}){
  const word=node_id.replace(/^word:/,"");
  if(node_id!=="word:"+word||!source[word])return {node_id,edges:[]};
  const chain=[...source[word].chain].reverse();
  return {node_id,edges:chain.slice(0,max_edges).map((to,i)=>({
    edge_id:"wordnet:"+word+":"+i,source_node:i?"ancestor:"+chain[i-1]:"word:"+word,
    target_node:"ancestor:"+to,relation_type:"lexical_path",
    relation_domain:"lexical",evidence_state:"proposed",
    supporting_card_id:"lex:"+word,supporting_card_revision:1,
    source_ref:"genesis.wordnet_chain:"+word
  }))};
 },
 async proposeEdge(args){
  guard(args.relation_type==="shared_lexical_ancestor"&&args.relation_domain==="lexical",
    "Unexpected proposal shape");
  const a=args.source_node.replace(/^word:/,""),b=args.target_node.replace(/^word:/,"");
  guard(sourceEvidence(a,b),"Missing source witness");
  const witness=ancestralCandidate(a,b);
  guard(Boolean(witness),"Unsupported generic-only relation");
  const k=a+"|"+b;guard(!links.has(k),"Duplicate proposed relation");
  const edge={a,b,ancestor:witness.term,ancestor_frequency:witness.df,
    source_ref:"genesis.wordnet_chain:"+a+"|"+b,
    source_card_ids:["lex:"+a,"lex:"+b],pinned_revisions:[1,1],
    epistemic_state:"proposed",relation_type:"shared_lexical_ancestor",
    origin:"simulated_MCP_not_live_Neon"};
  links.set(k,edge);
  return {edge_id:args.edge_id,evidence_state:"proposed",authority_granted:false,
    fact_verified:false,source_card_ids:edge.source_card_ids};
 }
};
const handle=createCardEvidenceRpc(manifest,serverAdapter,(c,name)=>c.allowed_tools.includes(name));
const rpc=(method,params)=>handle({jsonrpc:"2.0",id:++seq,method,params},allowedContext);
function chooseAction(){
 const total=Object.values(state).reduce((n,x)=>n+x.attempts,0);
 return tools.map(name=>{
  const arm=state[name];
  return {name,score:arm.attempts===0?1e6:
    arm.total_reward/arm.attempts+0.8*Math.sqrt(2*Math.log(total+2)/arm.attempts)};
 }).sort((a,b)=>b.score-a.score||a.name.localeCompare(b.name))[0].name;
}
function decode(response){
 if(!response||response.error||response.result?.isError)return null;
 try{return JSON.parse(response.result.content[0].text);}
 catch{return null;}
}
async function step(){
 const action=chooseAction(),word=keys[globalStep%keys.length];
 let reward=0,outcome="unobserved",pair=null,witness=null;
 if(action==="evidence.edge.propose"){
  if(pairCursor>=pairs.length){reward=0;outcome="pair_space_exhausted";}
  else{
    const [a,b]=pairs[pairCursor++];
    pair=[a,b];
    witness=ancestralCandidate(a,b);
    if(!sourceEvidence(a,b)){outcome="missing_source_witness";reward=-0.3;}
    else if(!witness){outcome="generic_or_unrelated_abstention";reward=0.06;}
    else if(links.has(a+"|"+b)){outcome="existing_relation";reward=-0.08;}
    else{
      const r=decode(await rpc("tools/call",{name:action,arguments:{
        edge_id:"echo017:t300:wordpair:"+a+":"+b,
        source_node:"word:"+a,target_node:"word:"+b,
        relation_type:"shared_lexical_ancestor",relation_domain:"lexical",
        source_ref:"genesis.wordnet_chain:"+a+"|"+b,
        supporting_card_id:"lex:"+a,supporting_card_revision:1
      }}));
      if(!r||r.evidence_state!=="proposed"||r.fact_verified!==false)
        throw Error("Failed provisional evidence proposal or denied MCP tool");
      outcome="new_provisional_relation";reward=0.5+0.4*(1-witness.df/keys.length);
    }
  }
 }else{
  const args=action==="dictionary.lexical_path"?{word}:
    action==="catalog.card.get"?{card_id:"lex:"+word,revision:1}:
      {node_id:"word:"+word,max_edges:50};
  const r=decode(await rpc("tools/call",{name:action,arguments:args}));
  if(!r){outcome="missing_source_record";reward=-0.3;}
  else{
    const key=action+"|"+word;
    const supported=action==="dictionary.lexical_path"?
      r.synset===source[word].synset&&r.admitted_new_words===0:
      action==="catalog.card.get"?
        r.revision===1&&r.provenance.source_table==="genesis.wordnet_chain":
        r.edges?.length===source[word].chain.length &&
         r.edges?.every(e=>e.evidence_state==="proposed" &&
           e.supporting_card_id==="lex:"+word&&e.supporting_card_revision===1);
    if(!supported){outcome="missing_or_unpinned_evidence";reward=-0.3;}
    else if(visit.has(key)){outcome="revisited_sourced_material";reward=0;}
    else{visit.add(key);outcome="first_sourced_exposure";
      reward={"dictionary.lexical_path":0.22,"catalog.card.get":0.24,"evidence.edge.trace":0.28}[action];}
  }
 }
 const arm=state[action];
 arm.ema_reward=0.2*reward+0.8*arm.ema_reward;
 arm.attempts++;arm.total_reward+=reward;globalStep++;
 return {step:globalStep,action,word,pair,outcome,reward,
   ancestor:witness?.term||null,epistemic_state:"provisional"};
}
export async function study({durationMs=300000,pacingMs=1000,logEvery=30}={}){
 guard(durationMs>=1&&durationMs<=300000,"Duration outside authorized 300-second ceiling");
 const allow=decode; // server RPC must be actually called for discovery.
 const list=await rpc("tools/list");
 guard(!list.error&&JSON.stringify(list.result.tools.map(t=>t.name))===JSON.stringify(tools),
   "Server advertised unauthorized tool");
 const started=performance.now(),transcript=[]; let next=started;
 while(performance.now()-started<durationMs){
   const entry=await step();transcript.push(entry);
   if(logEvery>0&&transcript.length%logEvery===0)
     console.log("ECHO017_PROGRESS "+JSON.stringify({steps:transcript.length,
       elapsed_seconds:Number(((performance.now()-started)/1000).toFixed(2)),
       new_relations:[...links.values()].filter(x=>x.origin.startsWith("simulated")).length,
       pair_cursor:pairCursor,global_step:globalStep}));
   next+=pacingMs;
   const remaining=durationMs-(performance.now()-started);
   if(remaining>0)await sleep(Math.max(0,Math.min(remaining,next-performance.now())));
 }
 const elapsed=performance.now()-started;
 const summaries={};
 for(const action of tools){
   const relevant=transcript.filter(t=>t.action===action);
   const counts={};
   for(const v of relevant)counts[v.outcome]=(counts[v.outcome]||0)+1;
   summaries[action]={steps:relevant.length,counts,
    attempts_total:state[action].attempts,total_reward:state[action].total_reward,
    ema_reward:state[action].ema_reward};
 }
 const candidates=[...links.values()].filter(x=>x.origin==="simulated_MCP_not_live_Neon");
 const result={
   id:"ECHO-017-T300",
   method:"real elapsed wall-clock, paced in-process Echo JSON-RPC; not live Neon MCP HTTP",
   requested_seconds:durationMs/1000,elapsed_seconds:elapsed/1000,study_steps:transcript.length,
   pace_target_ms:pacingMs,baseline_neon_global_step:Number(seed.progress.global_step),
   resumed_neon_policy:true,
   eventual_global_step:globalStep,pair_cursor:pairCursor,
   allowed_tools:tools,source_words:keys.length,total_possible_wordpairs:pairs.length,
   source_projection:"existing 22 WordNet words, 22 source cards, 124 proposed lexical edges",
   old_proposed_link_count:1,new_provisional_links:candidates.length,
   candidate_relations:candidates,per_action:summaries,
   refusals:transcript.filter(t=>t.outcome.includes("abstention")||t.outcome.startsWith("missing")).length,
   duplicate_relations:transcript.filter(t=>t.outcome==="existing_relation").length,
   no_tools_outside_allowlist:true,no_vocab_admission:true,
   knowledge_promotion:false,no_live_mcp_http:true,
   source_episode_summary:transcript.reduce((memo,t)=>
      (memo[t.outcome]=(memo[t.outcome]||0)+1,memo),{}),
   interpretation_caution:"Intrinsic UCB1 reward and wall time alone do not establish improved semantic understanding.",
   last_episodes:transcript.slice(-15)
 };
 return result;
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  const short=process.argv.includes("--smoke-test");
  const seconds=short?0.4:300;
  const result=await study({durationMs:seconds*1000,pacingMs:short?80:1000,logEvery:short?0:30});
  const output=process.argv.includes("--out")?
     process.argv[process.argv.indexOf("--out")+1]:null;
  if(output)writeFileSync(output,JSON.stringify(result,null,2)+"\n");
  console.log("ECHO017_RESULT "+JSON.stringify({...result,candidate_relations:result.candidate_relations.slice(0,4),
    last_episodes:result.last_episodes.slice(-2)}));
  if(!short&&result.elapsed_seconds<300)process.exitCode=1;
}
