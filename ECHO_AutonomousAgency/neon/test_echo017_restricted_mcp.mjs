import test from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {createCardEvidenceRpc} from "./card_evidence_rpc.mjs";

const manifest=JSON.parse(readFileSync(new URL("./echo017_restricted_mcp_tools.json",import.meta.url),"utf8"));
const allowed=[
 "dictionary.lexical_path","catalog.card.get",
 "evidence.edge.trace","evidence.edge.propose"
];
const adapters={
 dictionaryPath:async ({word})=>({word,source:"genesis.wordnet_chain",admitted_new_words:0}),
 getCard:async ({card_id,revision})=>({card_id,revision,review_state:"proposed"}),
 traceEdges:async ({node_id})=>({node_id,edges:[{evidence_state:"proposed"}]}),
 proposeEdge:async ({edge_id})=>({edge_id,evidence_state:"proposed",truth_verified:false})
};
const ctx={authenticated_principal:"echo_study:synthetic",mission_id:"ECHO-017",
 allowed_tools:allowed,may_propose:true,admitted_words:["being","existence"]};
const handle=createCardEvidenceRpc(manifest,adapters,(c,name)=>c.allowed_tools.includes(name));
const req=(name,arguments_)=>({jsonrpc:"2.0",id:1,method:"tools/call",
 params:{name,arguments:arguments_}});

test("exact four-tool restricted discovery, no other capabilities",async()=>{
 assert.deepEqual(manifest.tools.map(t=>t.name),allowed);
 const list=await handle({jsonrpc:"2.0",id:1,method:"tools/list"},ctx);
 assert.deepEqual(list.result.tools.map(t=>t.name),allowed);
 assert.ok(list.result.tools.every(t=>/^(dictionary|catalog|evidence)\./.test(t.name)));
 assert.ok(!list.result.tools.some(t=>/search|browse|deploy|approve|execute|shell/.test(t.name)));
});
test("dictionary declares positive use-for learning rather than use-when",async()=>{
 const list=await handle({jsonrpc:"2.0",id:1,method:"tools/list"},ctx);
 const dictionary=list.result.tools.find(t=>t.name==="dictionary.lexical_path");
 assert.match(dictionary.description,/Use it for gaining additional meaning/);
 assert.doesNotMatch(dictionary.description,/use it when/i);
});
test("only previously admitted dictionary words can be read",async()=>{
 assert.equal((await handle(req("dictionary.lexical_path",{word:"being"}),ctx)).result.isError,false);
 assert.equal((await handle(req("dictionary.lexical_path",{word:"unadmitted"}),ctx)).error.code,-32003);
});
test("can propose relationships, never promote or forge an approval",async()=>{
 const allowedProposal=await handle(req("evidence.edge.propose",{
  edge_id:"study:test",source_node:"word:being",target_node:"word:existence",
  relation_type:"shared_lexical_ancestor",relation_domain:"lexical",
  source_ref:"genesis.wordnet_chain:being"}),ctx);
 assert.equal(allowedProposal.result.isError,false);
 assert.equal(JSON.parse(allowedProposal.result.content[0].text).truth_verified,false);
 const denied=await handle(req("catalog.card.propose",{
  card_id:"fraud",expected_revision:0,card_kind:"authority_stamp",title:"bad",body:{}}),ctx);
 assert.equal(denied.error.code,-32602);
});
test("no administrative tools or unauthorized mutation are discoverable",async()=>{
 for(const name of ["deployment.execute","evidence.edge.approve","shell.run",
                    "catalog.card.propose","dictionary.admit","neon.run_sql"]){
  const out=await handle(req(name,{}),ctx);
  assert.equal(out.error.code,-32602,name);
 }
});
test("no untrusted acting-seat elevation through MCP input",async()=>{
 const o=await handle(req("catalog.card.get",{card_id:"lex:being",revision:1,acting_seat:"01"}),ctx);
 assert.equal(o.error.code,-32602);
});
