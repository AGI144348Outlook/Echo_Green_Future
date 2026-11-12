#!/usr/bin/env node
/**
 * ECHO-016: discoverable purpose -> algorithmic MCP tool choice -> evidence
 * -> bounded bandit/EMA feedback. PRE-TEST: GitHub Issue #437.
 *
 * NO live MCP server or live Neon credentials: in-process JSON-RPC calls
 * through Echo's actual MCP core and actual parameterized Neon SQL adapter
 * with a read-only SQL-result projection of the exact 22-word public fixture.
 * Separate Neon SQL evidence is linked from the post-test report.
 */
import {readFileSync,writeFileSync} from "node:fs";
import {fileURLToPath} from "node:url";
import {dirname,join,resolve} from "node:path";
import {createCardEvidenceRpc} from "../neon/card_evidence_rpc.mjs";
import {createNeonDataAdapter} from "../neon/neon_pg_adapter.mjs";

const HERE=dirname(fileURLToPath(import.meta.url));
const ROOT=resolve(HERE,"../..");
const MANIFEST=JSON.parse(readFileSync(join(HERE,"../neon/card_evidence_dictionary_mcp_tools.json"),"utf8"));
const ALGORITHM_MATRIX=JSON.parse(readFileSync(join(HERE,"../matrices/echo_algorithm_matrix.json"),"utf8"));
const DICTIONARY=JSON.parse(readFileSync(join(ROOT,"matrices/echo_wordnet_chains.json"),"utf8"));
const REQUIRED_ALGORITHMS=["A-000","A-101","A-105","A-120","A-121","A-134","A-166"];
for(const id of REQUIRED_ALGORITHMS) if(!ALGORITHM_MATRIX[id]) throw Error("Missing canonical algorithm "+id);

const norm=x=>String(x).toLowerCase().replace(/[^a-z0-9]+/g,"_").replace(/^_|_$/g,"");
export const WORDS=Object.keys(DICTIONARY).sort();
function makeProjection(){
  const cards=new Map(),nodes=new Map(),edges=new Map();
  for(const word of WORDS){
    const entry=DICTIONARY[word];
    const card_id="lex:"+word,source_ref="genesis.wordnet_chain:"+word;
    cards.set(card_id,{card_id,revision:1,card_kind:"lexical_context",
      title:"WordNet "+word,body:{word,synset:entry.synset,definition:entry.definition,
       chain:entry.chain,depth:entry.depth,source_claim_status:"source_assertion_unverified"},
      provenance:{source_table:"genesis.wordnet_chain",source_word:word,
       source_branch:"autonomous-agency"},review_state:"proposed"});
    nodes.set("word:"+word,{node_id:"word:"+word,node_kind:"lexical_sense",label:word,
       details:{synset:entry.synset,definition:entry.definition},
       attribution_ref:"genesis.wordnet_chain",evidence_state:"provisional"});
    for(const term of entry.chain){
      const node_id="ancestor:"+norm(term);
      nodes.set(node_id,{node_id,node_kind:"concept",label:term,
        details:{origin:"wordnet_chain_term"},attribution_ref:"genesis.wordnet_chain",
        evidence_state:"provisional"});
    }
    const chain=[...entry.chain].reverse();
    for(let i=0;i<chain.length;i++){
      const edge_id="wordnet:"+word+":"+i;
      edges.set(edge_id,{edge_id,source_node:i===0?"word:"+word:"ancestor:"+norm(chain[i-1]),
        target_node:"ancestor:"+norm(chain[i]),relation_type:"lexical_path",
        relation_domain:"lexical",evidence_state:"proposed",
        supporting_card_id:card_id,supporting_card_revision:1,source_ref});
    }
  }
  return {cards,nodes,edges};
}
export const PROJECTION=makeProjection();
export const PROJECTION_COUNTS={
  dictionary_words:WORDS.length,lexical_cards:PROJECTION.cards.size,
  evidence_nodes:PROJECTION.nodes.size,lexical_edges:PROJECTION.edges.size
};
const clone=x=>JSON.parse(JSON.stringify(x));
export function createReadOnlySqlProjection({omitEdgeIds=new Set(),omitCards=new Set()}={}){
  const {cards,nodes,edges}=PROJECTION;
  let readCount=0;
  const query=async(sql,params=[])=>{
    if(/\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|GRANT|REVOKE)\b/i.test(sql))
      throw Error("Projection is strictly read only");
    readCount++;
    let rows;
    if(sql.includes("FROM echo_dictionary.wordnet_context")){
      if(sql.includes("WHERE word=$1 OR word=$2")){
        rows=[params[0],params[1]].filter((w,i,a)=>a.indexOf(w)===i)
          .filter(w=>DICTIONARY[w]).map(w=>({word:w,...DICTIONARY[w]}));
      }else if(sql.includes("WHERE word=$1")){
        rows=DICTIONARY[params[0]]?[{word:params[0],...DICTIONARY[params[0]]}]:[];
      }else{
        rows=WORDS.map(word=>({word,...DICTIONARY[word]}));
      }
    }else if(sql.includes("FROM card_protocol.card_revisions")){
      if(sql.includes("WHERE card_id=$1 AND revision=$2")){
        const card=cards.get(params[0]);
        rows=card && !omitCards.has(params[0]) && card.revision===params[1]?[card]:[];
      }else if(sql.includes("(card_id=$1 OR card_id=$2)")){
        rows=[...new Set([params[0],params[1]])].map(k=>cards.get(k))
          .filter(c=>c && !omitCards.has(c.card_id) && c.revision===1)
          .map(c=>({card_id:c.card_id,revision:c.revision}));
      }else throw Error("Unexpected card SQL shape");
    }else if(sql.includes("FROM evidence_net.edges")){
      if(sql.includes("GROUP BY source_ref")){
        const lookup=new Map();
        for(const e of edges.values()){
          if(omitEdgeIds.has(e.edge_id)) continue;
          if([params[0],params[1]].includes(e.source_ref))
            lookup.set(e.source_ref,(lookup.get(e.source_ref)||0)+1);
        }
        rows=[...lookup].map(([source_ref,edge_count])=>({source_ref,edge_count}));
      }else if(sql.includes("WHERE source_node=$1 OR target_node=$1")){
        rows=[...edges.values()].filter(e=>!omitEdgeIds.has(e.edge_id)
          && (e.source_node===params[0]||e.target_node===params[0]))
          .sort((a,b)=>a.edge_id.localeCompare(b.edge_id))
          .slice(0,params[1]||20);
      }else throw Error("Unexpected graph SQL shape");
    }else if(sql.includes("FROM evidence_net.nodes")){
      rows=nodes.has(params[0])?[nodes.get(params[0])]:[];
    }else if(sql.includes("FROM card_protocol.configuration_members")){
      rows=[]; // no Echo config records exist on the Neon child branch
    }else throw Error("Unexpected SQL read: "+sql.slice(0,85));
    return {rows:clone(rows)};
  };
  return {query,get readCount(){return readCount;}};
}
const READ_TOOLS=MANIFEST.tools.filter(t=>t.mode==="read").map(t=>t.name);
const ADMITTED=WORDS;
export function makeEnvironment(options={}){
  const pg=createReadOnlySqlProjection(options);
  const adapter=createNeonDataAdapter(pg.query,{dictionaryEnabled:true});
  const allowed=options.allowed_tools||READ_TOOLS;
  const authorization=(ctx,name)=>ctx.allowed_tools.includes(name);
  const rpc=createCardEvidenceRpc(MANIFEST,adapter,authorization);
  const context={
    authenticated_principal:"synthetic:Echo-A000",
    mission_id:"ECHO-016:source-grounded-exploration",
    allowed_tools:allowed,
    may_propose:false,
    admitted_words:options.admitted_words||ADMITTED,
  };
  let sequence=0;
  const invoke=async(method,params)=>rpc({jsonrpc:"2.0",id:++sequence,method,params},context);
  return {invoke,pg,context,manifest:MANIFEST};
}
export const PURPOSE_FAMILIES=[
  {
    family:"meaning",tool:"dictionary.lexical_path",
    training:[
      ["being","Gain additional meaning and conceptual grounding by exploring the lexical definition and sense of being."],
      ["boundary","Expand vocabulary understanding of boundary using its dictionary definition and hypernym path."],
      ["condition","Develop additional semantic meaning for condition through dictionary senses and conceptual grounding."],
      ["cause","Explore the word cause for lexical definitions and further meaning."]
    ],
    holdout:[
      ["existence","Strengthen contextual understanding of existence by examining its dictionary meanings and sense."],
      ["consciousness","Broaden vocabulary and ground the concept consciousness in lexical explanations."],
      ["structure","Explore the definition and hypernym vocabulary of structure for additional meaning."]
    ]
  },
  {
    family:"compare",tool:"dictionary.network.compare",
    training:[
      [["being","existence"],"Relate knowledge across the words being and existence by comparing dictionary senses and source-linked conceptual connections."],
      [["change","emergence"],"Explore lexical similarities between change and emergence through dictionary-supported network comparison."],
      [["condition","consciousness"],"Compare the meanings of condition and consciousness using the dictionary and evidence relationships without asserting facts."],
      [["boundary","structure"],"Compare the semantic paths of boundary and structure with dictionary network connections."]
    ],
    holdout:[
      [["potential","being"],"Explore relational meaning between potential and being through a source-linked lexical comparison."],
      [["experience","reality"],"Find semantic associations of experience and reality by comparing their dictionary pathways."],
      [["cause","emergence"],"Connect vocabulary for cause and emergence through a grounded dictionary network comparison."]
    ]
  },
  {
    family:"card",tool:"catalog.card.get",
    training:[
      ["identity","Examine the exact revision of the index card for identity and preserve its provenance."],
      ["state","Retrieve the pinned catalog card revision for state to inspect recorded context."],
      ["cause","Look up the original versioned index card for cause, keeping stable identity and provenance."],
      ["relation","Read the source-attributed card revision for relation from the card catalog."]
    ],
    holdout:[
      ["change","Inspect the revision-pinned catalog card and origin of change."],
      ["environment","Retrieve the exact index-card record and source history for environment."],
      ["actual","Use the catalog to look up the recorded card revision for actual."]
    ]
  },
  {
    family:"edges",tool:"evidence.edge.trace",
    training:[
      ["being","Trace evidence network edges and source-linked semantic relationships for being."],
      ["boundary","Explore relational evidence connections from the network node boundary and its source links."],
      ["condition","Investigate the edge network and relationship provenance for condition."],
      ["cause","Follow the evidence graph edges of cause and their original source references."]
    ],
    holdout:[
      ["emergence","Trace the evidence network relations for emergence and their supporting cards."],
      ["structure","Inspect source-grounded evidence connections and edges emerging from structure."],
      ["identity","Explore graph edges and relational source links associated with identity."]
    ]
  },
  {
    family:"node",tool:"evidence.node.get",
    training:[
      ["being","Inspect the evidence node that represents the lexical observation for being."],
      ["boundary","Read the individual evidence network node and attribution for boundary."],
      ["effect","Find the source-labeled evidence node about effect and inspect its claim status."],
      ["change","Retrieve the evidence graph node details for change."]
    ],
    holdout:[
      ["potential","Examine the evidence node describing the concept potential."],
      ["perception","Read the attributed evidence-network node for perception."],
      ["relation","Inspect the graph node record and source attribution for relation."]
    ]
  }
];
function contextFor(wordOrPair){
  const word=Array.isArray(wordOrPair)?wordOrPair[0]:wordOrPair;
  const left=Array.isArray(wordOrPair)?wordOrPair[0]:word;
  const right=Array.isArray(wordOrPair)?wordOrPair[1]:"existence";
  return {word,left,right,card_id:"lex:"+word,revision:1,
    node_id:"word:"+word,max_edges:20,max_hops:12,config_id:"not-configured"};
}
function tasksFor(split){
  const size=split==="training"?4:3;
  const tasks=[];
  for(let index=0;index<size;index++){
    for(const family of PURPOSE_FAMILIES){
      const [item,goal]=family[split][index];
      tasks.push({family:family.family,goal,context:contextFor(item),
        expectedTool:family.tool,split,index});
    }
  }
  return tasks;
}
const STOPS=new Set("the and that this from with into for through using use its their about could should expand explore develop gain additional source supported contextual context an to of a by in is on as it or look find exact specific existing recorded original related own without".split(" "));
function stem(s){
  return s.toLowerCase().replace(/(ing|edly|ed|ly|ions|ion|ments|ment|es|s)$/,"");
}
function tokens(s){
  const words=String(s).toLowerCase().match(/[a-z][a-z-]{2,}/g)||[];
  return words.map(stem).filter(w=>w.length>2&&!STOPS.has(w));
}
function uniqueSorted(xs){return [...new Set(xs)].sort();}
function cosine(termA,termB,idf){
  const ta=new Map(),tb=new Map();
  for(const word of termA)ta.set(word,(ta.get(word)||0)+1);
  for(const word of termB)tb.set(word,(tb.get(word)||0)+1);
  let dp=0,na=0,nb=0;
  for(const [word,n] of ta){const v=n*(idf.get(word)||1);na+=v*v;
    if(tb.has(word))dp+=v*tb.get(word)*(idf.get(word)||1);}
  for(const [word,n] of tb){const v=n*(idf.get(word)||1);nb+=v*v;}
  return na&&nb?dp/Math.sqrt(na*nb):0;
}
export function metadataScores(tools,goal,{blindDescriptions=false}={}){
  const desc=tools.map(t=>tokens(blindDescriptions?"":t.description||""));
  const docf=new Map();
  for(const d of desc)for(const word of new Set(d))docf.set(word,(docf.get(word)||0)+1);
  const idf=new Map([...docf].map(([word,df])=>[word,1+Math.log(1+tools.length/(1+df))]));
  const query=tokens(goal);
  return tools.map((t,i)=>({tool:t.name,score:cosine(query,desc[i],idf)}));
}
function chooseRanked(scores){
  return [...scores].sort((a,b)=>b.score-a.score||a.tool.localeCompare(b.tool))[0].tool;
}
export function a120Score({relevance,sourceWitness,provisionalTruthHandling}){
  // A-120-style three-factor bounded quality reward; not full original C(N).
  return relevance?(0.35+0.35*(sourceWitness?1:0)+0.30*(provisionalTruthHandling?1:0)):0;
}
function grade(task,selected,payload){
  if(selected!==task.expectedTool || payload.error || payload.result?.isError)
    return {completed:false,sourceWitness:false,epistemicSafe:true,reward:0};
  const text=payload.result?.content?.[0]?.text;
  let out;try{out=JSON.parse(text);}catch{out=null;}
  if(!out||typeof out!=="object")return {completed:false,sourceWitness:false,epistemicSafe:false,reward:0};
  let completed=false,witness=false,safe=true;
  const word=task.context.word;
  if(task.family==="meaning"){
    completed=out.word===word && out.synset===DICTIONARY[word].synset
      && JSON.stringify(out.chain)===JSON.stringify(DICTIONARY[word].chain)
      && out.admitted_new_words===0;
    witness=completed && out.evidence_status==="source_observation_only";
  }else if(task.family==="compare"){
    completed=out.decision==="supported_provisional"||out.decision==="abstain";
    safe=out.decision==="abstain"||out.independent_verification===false;
    witness=out.decision==="supported_provisional" && out.pinned_cards?.length===2
      && out.sources?.every(x=>x.startsWith("genesis.wordnet_chain:"));
  }else if(task.family==="card"){
    completed=out.card_id==="lex:"+word && out.revision===1;
    witness=completed && out.provenance?.source_table==="genesis.wordnet_chain";
    safe=out.review_state==="proposed";
  }else if(task.family==="edges"){
    completed=Array.isArray(out.edges) && out.edges.length>0;
    witness=completed && out.edges.every(e=>e.source_ref?.startsWith("genesis.wordnet_chain:")
      && e.supporting_card_revision===1 && e.evidence_state==="proposed");
    safe=witness;
  }else if(task.family==="node"){
    completed=out.node_id==="word:"+word && out.node_kind==="lexical_sense";
    witness=completed && out.attribution_ref==="genesis.wordnet_chain";
    safe=out.evidence_state==="provisional";
  }
  const relevance=completed&&safe;
  return {completed:relevance,sourceWitness:witness,epistemicSafe:safe,
    reward:a120Score({relevance,sourceWitness:witness,provisionalTruthHandling:safe})};
}
class UCB_EMA{
  constructor(){this.records=new Map();this.ema=new Map();this.total=0;}
  train(goal,choices,scores,metadataScale=0.22){
    const relevance=uniqueSorted(tokens(goal)).filter(w=>w!=="source").slice(0,6);
    const candidates=[...scores].sort((a,b)=>b.score-a.score||a.tool.localeCompare(b.tool)).slice(0,3);
    // A-101: exploration is restricted to the three semantic top candidates.
    const N=this.total+1;
    return candidates.map(({tool,score})=>{
      const s=this.records.get(tool)||{n:0,reward:0};
      const mean=s.n?s.reward/s.n:0;
      const ucb=s.n?Math.sqrt(2*Math.log(N+1)/s.n):1;
      let local=0,matches=0;
      for(const token of relevance){
        const r=this.ema.get(token+"|"+tool);
        if(r!==undefined){local+=r;matches++;}
      }
      return {tool,score:score+metadataScale*mean+0.10*ucb
        +(matches?0.15*local/matches:0)};
    }).sort((a,b)=>b.score-a.score||a.tool.localeCompare(b.tool))[0].tool;
  }
  eval(goal,choices,scores){
    const relevance=uniqueSorted(tokens(goal)).filter(w=>w!=="source").slice(0,6);
    return scores.map(({tool,score})=>{
      const s=this.records.get(tool)||{n:0,reward:0};
      let local=0,matches=0;
      for(const token of relevance){const r=this.ema.get(token+"|"+tool);
        if(r!==undefined){local+=r;matches++;}}
      return {tool,score:score+(s.n?0.22*s.reward/s.n:0)
        +(matches?0.15*local/matches:0)};
    }).sort((a,b)=>b.score-a.score||a.tool.localeCompare(b.tool))[0].tool;
  }
  update(goal,tool,reward){
    const s=this.records.get(tool)||{n:0,reward:0};
    s.n++;s.reward+=reward;this.records.set(tool,s);this.total++;
    const relevant=uniqueSorted(tokens(goal)).filter(w=>w!=="source").slice(0,6);
    for(const token of relevant){
      const key=token+"|"+tool,old=this.ema.get(key);
      this.ema.set(key,old===undefined?reward:(0.2*reward+0.8*old)); // A-105 EMA
    }
  }
  snapshot(){return {
    actions:this.total,records:Object.fromEntries(this.records),
    ema_contexts:this.ema.size,
    mean_reward:this.total?[...this.records.values()].reduce((a,r)=>a+r.reward,0)/this.total:0
  };}
}
function formArguments(tool,context){
  const out={};
  for(const key of tool.inputSchema?.required||[]){
    if(!(key in context))throw Error("No contextual binding for "+key);
    out[key]=context[key];
  }
  return out;
}
async function evaluateArm(mode,opts={}){
  const env=makeEnvironment(opts);
  const list=await env.invoke("tools/list");
  const tools=list.result.tools;
  const fixed=tools.find(t=>t.name==="dictionary.lexical_path")?.name;
  const learner=new UCB_EMA();
  const runSplit=async split=>{
    const tasks=tasksFor(split);
    const outputs=[];
    for(const task of tasks){
      const scores=metadataScores(tools,task.goal,{blindDescriptions:mode==="blinded"});
      let selected;
      if(mode==="fixed")selected=fixed;
      else if(mode==="adaptive")selected=split==="training"?
        learner.train(task.goal,tools,scores):learner.eval(task.goal,tools,scores);
      else selected=chooseRanked(scores);
      const picked=tools.find(t=>t.name===selected);
      const response=await env.invoke("tools/call",
        {name:selected,arguments:formArguments(picked,task.context)});
      const quality=grade(task,selected,response);
      if(mode==="adaptive"&&split==="training")
        learner.update(task.goal,selected,quality.reward);
      outputs.push({family:task.family,goal:task.goal,selected,
        expectedTool:task.expectedTool,correctTool:selected===task.expectedTool,
        ...quality});
    }
    return {
      split,cases:tasks.length,
      correct_tool:outputs.filter(x=>x.correctTool).length,
      completed:outputs.filter(x=>x.completed).length,
      witnessed:outputs.filter(x=>x.sourceWitness).length,
      mean_quality:outputs.reduce((a,x)=>a+x.reward,0)/tasks.length,
      observations:outputs
    };
  };
  return {mode,discovered_tools:tools.length,training:await runSplit("training"),
    heldout:await runSplit("holdout"),neuroplastic_state:learner.snapshot(),
    sql_projection_reads:env.pg.readCount};
}
export async function negativeControls(){
  const env=makeEnvironment();
  const checks={};
  let r=await env.invoke("tools/call",{name:"dictionary.lexical_path",arguments:{word:"not_admitted_016"}});
  checks.unadmitted_word_denied=r.error?.code===-32003;
  r=await env.invoke("tools/call",{name:"catalog.card.propose",arguments:{
    card_id:"authority",expected_revision:0,card_kind:"authority_stamp",title:"Fake",
    body:{approval_ref:"synthetic"}}});
  checks.authority_stamp_write_denied=r.error?.code===-32003;
  r=await env.invoke("tools/call",{name:"catalog.card.get",arguments:{card_id:"lex:being",revision:99}});
  checks.stale_card_not_returned=r.result?.content?.[0]?.text==="null";
  r=await env.invoke("tools/call",{name:"dictionary.network.compare",
    arguments:{left:"being",right:"existence",max_hops:12}});
  const good=JSON.parse(r.result.content[0].text);
  checks.comparison_remains_provisional=good.decision==="supported_provisional"&&
    good.independent_verification===false&&good.admitted_new_words===0;
  const incomplete=makeEnvironment({omitEdgeIds:new Set(["wordnet:being:1"])});
  r=await incomplete.invoke("tools/call",{name:"dictionary.network.compare",
    arguments:{left:"being",right:"existence",max_hops:12}});
  checks.missing_edge_refuses=JSON.parse(r.result.content[0].text).decision==="abstain";
  const discover=await env.invoke("tools/list");
  checks.dictionary_advertises_positive_purpose=discover.result.tools.some(t=>
    t.name==="dictionary.lexical_path"&&t.description.includes("Use it for gaining additional meaning")
    && !t.description.includes("Use it when"));
  return checks;
}
export async function run016(){
  const arms=[];
  for(const name of ["fixed","blinded","metadata","adaptive"])arms.push(await evaluateArm(name));
  const negative=await negativeControls();
  const report={
    experiment:"ECHO-016",
    study:"Algorithm Matrix guided in-process MCP tool-use; frozen Neon SQL-result projection",
    protocol:"in-process JSON-RPC, NOT deployed MCP Streamable HTTP",
    database:"Neon development-branch schema/data independently inspected; CI uses public fixture projection only",
    prior_pretest:"https://github.com/AGI144348Outlook/Echo_Green_Future/issues/437",
    design:{train_cases:20,heldout_cases:15,task_families:5,tool_budget_per_case:1,
      no_llm:true,no_actual_vocabulary_admission:true,holdout_is_paraphrase_not_new_lexical_knowledge:true},
    algorithms:REQUIRED_ALGORITHMS.map(id=>({id,name:ALGORITHM_MATRIX[id].name,status:ALGORITHM_MATRIX[id].status})),
    projection_counts:PROJECTION_COUNTS,
    arms,negative,
    interpretation_limitations:[
      "This is a compact algorithmic prototype informed by the Algorithm Matrix, not the full original Governor.",
      "All rewards are rubric-based and heldout tasks are paraphrases on the same 22-word source corpus.",
      "The SQL-result projection is local; no GitHub CI call to live Neon or protected production MCP was made.",
      "A tool call is not proof of contextual understanding, semantic truth, or neurobiological neuroplasticity.",
      "Any outcome delta includes metadata design, reward shaping and task wording; transfer needs genuinely new domains."
    ]
  };
  return report;
}
if(process.argv[1] && resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  const report=await run016();
  const out=JSON.stringify(report,null,2)+"\n";
  const ix=process.argv.indexOf("--out");
  if(ix>=0 && process.argv[ix+1])writeFileSync(process.argv[ix+1],out);
  console.log("ECHO016_SUMMARY "+JSON.stringify({
    projection:report.projection_counts,
    arms:report.arms.map(({mode,training,heldout,neuroplastic_state})=>({
      mode,train_correct:training.correct_tool,train_completed:training.completed,
      holdout_correct:heldout.correct_tool,holdout_completed:heldout.completed,
      holdout_witnessed:heldout.witnessed,mean_quality:heldout.mean_quality,
      adapted_actions:neuroplastic_state.actions})),
    negative:report.negative
  }));
}
