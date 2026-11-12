import test from "node:test";
import assert from "node:assert/strict";
import {study} from "./echo017_timed_300s.mjs";
test("clock-bounded Echo study uses four named tools, no hidden provider",async()=>{
  const r=await study({durationMs:280,pacingMs:40,logEvery:0});
  assert.ok(r.elapsed_seconds>=0.280);
  assert.ok(r.study_steps>=4);
  assert.equal(r.no_tools_outside_allowlist,true);
  assert.equal(r.no_vocab_admission,true);
  assert.equal(r.knowledge_promotion,false);
  assert.equal(r.no_live_mcp_http,true);
  assert.deepEqual(r.allowed_tools,[
    "dictionary.lexical_path","catalog.card.get","evidence.edge.trace","evidence.edge.propose"]);
  assert.equal(r.resumed_neon_policy,true);
  assert.equal(r.baseline_neon_global_step,192);
});
test("disallow requests beyond 300 seconds",async()=>{
  await assert.rejects(study({durationMs:300001,pacingMs:1}),/ceiling/);
});
test("candidate relations are proposed and source-card pinned",async()=>{
  const r=await study({durationMs:200,pacingMs:35,logEvery:0});
  for(const e of r.candidate_relations){
    assert.equal(e.epistemic_state,"proposed");
    assert.deepEqual(e.pinned_revisions,[1,1]);
    assert.ok(e.source_ref.startsWith("genesis.wordnet_chain:"));
  }
});
