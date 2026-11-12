import test from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {fileURLToPath} from "node:url";
import {dirname,join} from "node:path";
import {createCardEvidenceRpc} from "./card_evidence_rpc.mjs";
import {createNeonDataAdapter} from "./neon_pg_adapter.mjs";

const directory=dirname(fileURLToPath(import.meta.url));
const filename=join(directory, "card_evidence_mcp_tools.json");
let manifest;
try {manifest=JSON.parse(readFileSync(filename,"utf8"));}
catch {manifest=JSON.parse(readFileSync(join(directory, "card_evidence_dictionary_mcp_tools.json"),"utf8"));}
const echo=manifest.dictionaryIntegrated===true;
const seen=[];
const adapter={
 getCard:async a=>({card_id:a.card_id,revision:a.revision,authority_granted:false}),
 resolveConfiguration:async a=>({config:a,may_execute:false}),
 proposeCard:async a=>({proposed:a.card_id,review_state:"proposed",approved:false}),
 getNode:async a=>({node_id:a.node_id}),
 traceEdges:async a=>({node_id:a.node_id,edges:[]}),
 proposeEdge:async a=>({edge_id:a.edge_id,evidence_state:"proposed"}),
 dictionaryPath:async a=>({word:a.word,admitted_new_words:0}),
 compareWords:async a=>({left:a.left,right:a.right,decision:"provisional"}),
};
const authorize=(ctx,name,kind)=>{
 seen.push({name,kind});
 return ctx.allowed_tools.includes(name);
};
const handle=createCardEvidenceRpc(manifest,adapter,authorize);
const ctx={authenticated_principal:"Seat08",mission_id:"synthetic001",
           allowed_tools:["catalog.card.get","evidence.node.get"],may_propose:false,
           admitted_words:["being","existence"]};
const rpc=(id,method,params)=>({jsonrpc:"2.0",id,method,params});

test("two-system Nexus and three-system Echo registry boundaries",()=>{
 assert.equal(manifest.dictionaryIntegrated,echo);
 assert.equal(manifest.tools.length,echo?8:6);
 assert.equal(manifest.neon_schemas.join(","),"card_protocol,evidence_net");
 assert.equal(manifest.forbiddenToolClasses.includes("deployment execution"),true);
});
test("unauthenticated context is rejected",async()=>{
 const r=await handle(rpc(1,"tools/list"),{});
 assert.equal(r.error.code,-32001);
});
test("only assigned tools are discoverable",async()=>{
 const r=await handle(rpc(2,"tools/list"),ctx);
 assert.deepEqual(r.result.tools.map(x=>x.name),
     ["catalog.card.get","evidence.node.get"]);
 assert.equal(r.result.tools.some(x=>x.name.startsWith("dictionary.")),false);
});
test("authorized read never creates authority",async()=>{
 const r=await handle(rpc(3,"tools/call",{name:"catalog.card.get",
     arguments:{card_id:"stamp001",revision:1}}),ctx);
 assert.equal(r.result.isError,false);
 const item=JSON.parse(r.result.content[0].text);
 assert.equal(item.authority_granted,false);
});
test("unlisted execution and unscoped proposal forbidden",async()=>{
 const r=await handle(rpc(4,"tools/call",{name:"deployment.execute",
      arguments:{target:"production"}}),ctx);
 assert.equal(r.error.code,-32602);
 const p=await handle(rpc(5,"tools/call",{name:"catalog.card.propose",
      arguments:{card_id:"a",expected_revision:0,card_kind:"evidence",
                 title:"a",body:{}}}),ctx);
 assert.equal(p.error.code,-32003);
});
test("the client cannot spoof acting seat or mission in tool fields",async()=>{
 const r=await handle(rpc(6,"tools/call",{name:"catalog.card.get",
      arguments:{card_id:"x",revision:1,acting_seat:"02"}}),ctx);
 assert.equal(r.error.code,-32602);
});
test("dictionary availability is repo-specific and gated by admitted lobby",async()=>{
 const scope={...ctx,allowed_tools:["dictionary.lexical_path"]};
 const a=await handle(rpc(7,"tools/list"),scope);
 assert.equal(a.result.tools.length,echo?1:0);
 if(echo){
   const yes=await handle(rpc(8,"tools/call",{name:"dictionary.lexical_path",
       arguments:{word:"being"}}),scope);
   assert.equal(yes.result.isError,false);
   const no=await handle(rpc(9,"tools/call",{name:"dictionary.lexical_path",
       arguments:{word:"secret"}}),scope);
   assert.equal(no.error.code,-32003);
 }
});
test("Neon SQL adapter uses parameters and proposal-only write",async()=>{
 const statements=[];
 const mockQuery=async(sql,params)=>{
   statements.push({sql,params});
   if(sql.includes("INSERT INTO card_protocol.card_revisions"))
     return {rows:[{card_id:"proposalA",revision:1,review_state:"proposed"}]};
   return {rows:[{card_id:"proposalA",revision:1,card_kind:"evidence"}]};
 };
 const db=createNeonDataAdapter(mockQuery,{dictionaryEnabled:echo});
 const card=await db.getCard({card_id:"proposalA' OR 1=1 --",revision:1});
 assert.equal(card.card_id,"proposalA");
 assert.equal(statements[0].params[0],"proposalA' OR 1=1 --");
 assert.equal(statements[0].sql.includes("1=1"),false);
 const proposal=await db.proposeCard({card_id:"proposalA",expected_revision:0,
    card_kind:"evidence",title:"Proposal",body:{source:"sourceA"}},ctx);
 assert.equal(proposal.authority_granted,false);
 assert.equal(proposal.review_state,"proposed");
 assert.equal(statements[1].sql.includes("'proposed'"),true);
 assert.equal(statements[1].params[1],0);
});
