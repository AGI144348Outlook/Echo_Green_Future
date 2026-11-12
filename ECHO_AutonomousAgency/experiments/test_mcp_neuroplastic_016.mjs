import test from "node:test";
import assert from "node:assert/strict";
import {
  WORDS,PROJECTION_COUNTS,PROJECTION,makeEnvironment,metadataScores,a120Score,
  negativeControls,run016,PURPOSE_FAMILIES,createReadOnlySqlProjection
} from "./mcp_neuroplastic_016.mjs";

test("A-000 Algorithm Matrix trial uses exact frozen Neon projection inventory",()=>{
  assert.equal(WORDS.length,22);
  assert.deepEqual(PROJECTION_COUNTS,{
    dictionary_words:22,lexical_cards:22,evidence_nodes:73,lexical_edges:124
  });
  const card=PROJECTION.cards.get("lex:being");
  assert.equal(card.revision,1);
  assert.equal(card.provenance.source_table,"genesis.wordnet_chain");
  assert.equal(card.review_state,"proposed");
});
test("new Dictionary description advertises positive contextual expansion, no conditional mandate",async()=>{
  const env=makeEnvironment();
  const out=await env.invoke("tools/list");
  assert.equal(out.result.tools.length,6);
  const dictionary=out.result.tools.find(t=>t.name==="dictionary.lexical_path");
  assert.match(dictionary.description,/Use it for gaining additional meaning/);
  assert.match(dictionary.description,/evidence|semantic relationships/);
  assert.doesNotMatch(dictionary.description,/use it when/i);
  assert.equal(out.result.tools.filter(t=>t.name.endsWith(".propose")).length,0);
});
test("schema-derived arguments and real Echo RPC invoke existing Neon-shaped adapter",async()=>{
  const env=makeEnvironment();
  const path=await env.invoke("tools/call",{
    name:"dictionary.lexical_path",arguments:{word:"being"}});
  const lexical=JSON.parse(path.result.content[0].text);
  assert.equal(lexical.synset,"being.n.01");
  assert.equal(lexical.admitted_new_words,0);
  const c=await env.invoke("tools/call",{
    name:"catalog.card.get",arguments:{card_id:"lex:being",revision:1}});
  const card=JSON.parse(c.result.content[0].text);
  assert.equal(card.card_id,"lex:being");
  assert.equal(card.provenance.source_word,"being");
  const trace=await env.invoke("tools/call",{
    name:"evidence.edge.trace",arguments:{node_id:"word:being",max_edges:10}});
  const result=JSON.parse(trace.result.content[0].text);
  assert.ok(result.edges.length>0);
  assert.equal(result.edges[0].supporting_card_id,"lex:being");
  assert.equal(result.edges[0].source_ref,"genesis.wordnet_chain:being");
  assert.equal(result.edges[0].evidence_state,"proposed");
});
test("evidence comparison remains provisional and exact-card dependent",async()=>{
  const env=makeEnvironment();
  const r=await env.invoke("tools/call",{
    name:"dictionary.network.compare",
    arguments:{left:"being",right:"existence",max_hops:12}});
  const d=JSON.parse(r.result.content[0].text);
  assert.equal(d.decision,"supported_provisional");
  assert.equal(d.independent_verification,false);
  assert.equal(d.pinned_cards.length,2);
  const missing=makeEnvironment({omitCards:new Set(["lex:existence"])});
  const fail=await missing.invoke("tools/call",{
    name:"dictionary.network.compare",
    arguments:{left:"being",right:"existence",max_hops:12}});
  assert.equal(JSON.parse(fail.result.content[0].text).decision,"abstain");
});
test("source projection does not allow writes and caller scope blocks proposal",async()=>{
  const projection=createReadOnlySqlProjection();
  await assert.rejects(projection.query("INSERT INTO evidence_net.edges VALUES ($1)",["x"]),/strictly read only/);
  const env=makeEnvironment({allowed_tools:["evidence.node.get"]});
  const list=await env.invoke("tools/list");
  assert.deepEqual(list.result.tools.map(t=>t.name),["evidence.node.get"]);
  const denied=await env.invoke("tools/call",{
    name:"dictionary.lexical_path",arguments:{word:"being"}});
  assert.equal(denied.error.code,-32003);
});
test("five context families have controlled training and heldout task sets",()=>{
  assert.equal(PURPOSE_FAMILIES.length,5);
  assert.equal(new Set(PURPOSE_FAMILIES.map(f=>f.tool)).size,5);
  for(const f of PURPOSE_FAMILIES){
    assert.equal(f.training.length,4);
    assert.equal(f.holdout.length,3);
  }
});
test("A-120 reward refuses irrelevant tool success despite syntactically valid result",()=>{
  assert.equal(a120Score({relevance:false,sourceWitness:true,provisionalTruthHandling:true}),0);
  assert.equal(a120Score({relevance:true,sourceWitness:true,provisionalTruthHandling:true}),1);
  assert.ok(Math.abs(a120Score({relevance:true,sourceWitness:false,provisionalTruthHandling:true})-0.65)<1e-12);
});
test("tool descriptions contribute to metadata ranking",async()=>{
  const env=makeEnvironment();
  const tools=(await env.invoke("tools/list")).result.tools;
  const goal=PURPOSE_FAMILIES[0].training[0][1];
  const regular=metadataScores(tools,goal);
  const blind=metadataScores(tools,goal,{blindDescriptions:true});
  assert.ok(regular.some(x=>x.score>0));
  assert.ok(blind.every(x=>x.score===0));
});
test("negative privilege, admission, version and missing evidence guards hold",async()=>{
  const controls=await negativeControls();
  assert.ok(Object.keys(controls).length>=6);
  assert.ok(Object.values(controls).every(Boolean),JSON.stringify(controls));
});
test("pre-registered arms evaluate equal budgets without heldout feedback",async()=>{
  const report=await run016();
  assert.deepEqual(report.arms.map(x=>x.mode),["fixed","blinded","metadata","adaptive"]);
  for(const arm of report.arms){
    assert.equal(arm.training.cases,20);
    assert.equal(arm.heldout.cases,15);
    assert.equal(arm.discovered_tools,6);
    assert.ok(arm.heldout.correct_tool>=0 && arm.heldout.correct_tool<=15);
    assert.ok(arm.heldout.completed>=0 && arm.heldout.completed<=15);
  }
  const adaptive=report.arms.find(x=>x.mode==="adaptive");
  assert.equal(adaptive.neuroplastic_state.actions,20);
  assert.ok(adaptive.neuroplastic_state.ema_contexts>0);
  assert.equal(report.design.no_llm,true);
  assert.equal(report.design.no_actual_vocabulary_admission,true);
  assert.ok(report.interpretation_limitations.some(s=>s.includes("NOT")||s.includes("not")));
});
