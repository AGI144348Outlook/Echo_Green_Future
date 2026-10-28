#!/usr/bin/env node
/* Contract-000 Run419: static Pe/demo persistence boundary, not Genesis runtime.
 * Source Git blob pins: genesis 63eb982989b4f3478d649430b555c8f4ba755c27;
 * demo 64a171a6791f2356006683596b56cbe289cbbdc0.
 * Usage: node test_a000_pe_persistence_419.js <full-genesis.py> <demo.py>.
 * Static tests cannot prove absence of dynamic imports, reflection or external callers. */
'use strict';
const fs=require('node:fs'),crypto=require('node:crypto');
const expected=['63eb982989b4f3478d649430b555c8f4ba755c27','64a171a6791f2356006683596b56cbe289cbbdc0'];
const sha=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
function inspect(g,d){
 const checks=[],put=(label,ok)=>checks.push({label,pass:!!ok});
 const pe=g.slice(g.indexOf("class PeCommunicator:"),g.indexOf("\nclass CrossLobbyBridge:"));
 const ex=pe.slice(pe.indexOf("    def exchange("),pe.indexOf("    def open_exchanges("));
 const post=d.slice(d.indexOf("    all_exchanges = pe.open_exchanges("));
 put("pe-class-found",pe.startsWith("class PeCommunicator:")&&pe.includes("    def exchange("));
 put("resh-validate-gate",ex.includes("if not self.resh.validate():"));
 put("resh-knowledge-new-dict",pe.includes("    def _resh_knows(")&&pe.includes('return {\n            "word":'));
 put("exchange-process-local-log",ex.includes('self.exchanges.append({"entity": entity_word, "log": log})'));
 put("exchange-retrieves-not-indexes",ex.includes("next_k = self._resh_knows(next_seed)")&&!/\b(?:matrix\.index_|matrix\.record\(|self\.matrix\.known\[|self\.lobby\.commit\(|self\.matrix\.index_)/.test(ex));
 put("demo-external-pe-wiring",d.includes("pe = PeCommunicator(matrix, lobby, resh, ayin)")&&post.length>0);
 put("demo-post-no-indexing",!/\b(?:matrix\.index_|matrix\.record\(|lobby\.commit\(|lobby\.populate\()/.test(post));
 put("demo-post-no-qualification",!/\b(?:greenAdmission|vocabulary_promoted|qualify\(|teacher_verdict)/.test(post));
 put("demo-post-no-identity-revalidate",!post.includes("resh.validate("));
 put("demo-counts-lobby-agents",d.includes("known_already = {w for w in encountered if w in lobby.agents}")&&d.includes("new_pointers  = {w for w in encountered if w not in lobby.agents}"));
 put("demo-matrix-wording-mismatch",d.includes("Already in Resh's matrix:")&&d.includes("if w in lobby.agents"));
 put("demo-explicit-not-indexed",d.includes("New pointers (not yet indexed):"));
 const synthetic=[];
 const encountered=new Set(["indexed_but_not_agent","agent","unindexed"]);
 const matrixKnown=new Set(["indexed_but_not_agent","agent"]),lobbyAgents=new Set(["agent"]);
 const candidates=[...encountered].filter(w=>!lobbyAgents.has(w));
 synthetic.push({label:"source-transcribed demo counts indexed-but-not-agent as new pointer",pass:candidates.includes("indexed_but_not_agent")&&matrixKnown.has("indexed_but_not_agent")});
 synthetic.push({label:"lobby agent and matrix entries are different membership predicates",pass:[...encountered].filter(w=>lobbyAgents.has(w)).length===1&&[...encountered].filter(w=>matrixKnown.has(w)).length===2});
 return {checks,synthetic,pass:checks.filter(x=>x.pass).length,synthetic_pass:synthetic.filter(x=>x.pass).length};
}
if(require.main===module){
 if(process.argv.length!==4){console.error('Usage: node test_a000_pe_persistence_419.js <genesis.py> <demo.py>');process.exit(2)}
 const bytes=process.argv.slice(2).map(p=>fs.readFileSync(p));
 if(bytes.some((b,i)=>sha(b)!==expected[i])){console.error('SOURCE_PIN_MISMATCH');process.exit(2)}
 const result=inspect(...bytes.map(b=>new TextDecoder('utf-8',{fatal:true}).decode(b)));
 console.log(JSON.stringify(result,null,2));
 process.exit(result.pass===12&&result.synthetic_pass===2?0:1);
}
module.exports={inspect};
