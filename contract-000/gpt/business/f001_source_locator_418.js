#!/usr/bin/env node
/* F-001 HOLD-only locator: node f001_source_locator_418.js <handoff.json> <TAM-source-dir>.
 * Requires exact original TAM commit d46456a; never approves editorial claims or release.
 * Sentence splitter transcribes claim_scan.py into JS; no original Python parity claimed. */
'use strict';
const FILES=["README.md","Article 1 Hacksilber","Article 2 Water Weight Computes","The Color Dyed and Dental Records","Article 5","Article 6","Article 10","Collective information"];
const COMMIT="d46456a18fe412398d0ae37ec5a8c4eebb44e0c9";
const sentences=s=>s.split(/(?<=[.!?])\s+|\n{2,}/).map(x=>x.trim()).filter(Boolean);
function audit(p,sources) {
 const errors=[],rows=[],seen=new Set(),groups=new Set();
 const bad=(code,id)=>errors.push({code,id});
 if(p.project!=="F-001"||p.source_commit!==COMMIT)bad("PROJECT_OR_COMMIT","packet");
 if(p.status!=="HOLD / NOT LAUNCH-READY"||p.release_authorized!==false||p.human_reviewed_count!==0)bad("HOLD_REQUIRED","packet");
 if(!Array.isArray(p.rows))return {ok:false,errors:[{code:"ROWS_MISSING",id:"packet"}]};
 const n={baseline:0,supplemental:0,p1:0,baseline_exact:0,baseline_partial:0,supplemental_exact:0};
 for(const r of p.rows) {
  const id=r.id;
  if(!["baseline","supplemental"].includes(r.queue)){bad("QUEUE",id);continue}
  n[r.queue]++;
  if(r.queue==="baseline"&&r.review_priority==="P1")n.p1++;
  if(r.queue==="supplemental"&&r.group_id)groups.add(r.group_id);
  if(seen.has(id))bad("DUPLICATE_ID",id);seen.add(id);
  if(!FILES.includes(r.file)||id!==r.file+"#S"+r.sentence_no){bad("LOCATION_ID",id);continue}
  if(r.review_status!=="UNREVIEWED"||r.editorial_disposition!==null||r.evidence_ref!==null||r.rights_clearance!==null||r.reviewer!==null||r.release_authorized!==false)bad("UNAUTHORIZED_DISPOSITION",id);
  if(r.source_commit!==COMMIT)bad("ROW_COMMIT",id);
  const source=sources[r.file];
  if(!source){bad("SOURCE_MISSING",id);continue}
  if(source.sha!==r.source_blob_sha){bad("SOURCE_PIN",id);continue}
  const actual=sentences(source.text)[r.sentence_no-1];
  if(!Number.isInteger(r.sentence_no)||!actual){bad("SENTENCE_INDEX",id);continue}
  if(typeof r.source_excerpt!=="string"||!actual.includes(r.source_excerpt)){bad("EXCERPT_MISMATCH",id);continue}
  const exact=actual===r.source_excerpt;
  if(r.excerpt_is_full_sentence===true&&!exact)bad("FALSE_FULL_SENTENCE",id);
  if(r.queue==="baseline")n[exact?"baseline_exact":"baseline_partial"]++;
  else if(exact)n.supplemental_exact++;
  rows.push({id,queue:r.queue,source_sha:source.sha,source_chars:actual.length,excerpt_chars:r.source_excerpt.length,excerpt_exact:exact,group_id:r.group_id});
 }
 if(p.rows.length!==82||n.baseline!==45||n.supplemental!==37||n.p1!==18||groups.size!==34)bad("COVERAGE_COUNTS","packet");
 for(let i=1;i<=34;i++)if(!groups.has("G"+String(i).padStart(3,"0")))bad("GROUP_ID","G"+i);
 if(rows.length!==82)bad("LOCATIONS_UNRESOLVED","packet");
 return {ok:errors.length===0,project:"F-001",release:"HOLD",source_commit:COMMIT,counts:{...n,supplemental_groups:groups.size,resolved:rows.length},errors,rows};
}
if(typeof module!=="undefined")module.exports={audit,sentences,FILES,COMMIT};
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
 const args=process.argv.slice(2);
 if(args.length!==2){process.stderr.write("Usage: node f001_source_locator_418.js <handoff.json> <TAM-dir>\n");process.exit(2)}
 try {
  const packet=JSON.parse(fs.readFileSync(args[0],"utf8")),sources={};
  for(const name of FILES){
   const file=path.join(args[1],name),st=fs.lstatSync(file);
   if(!st.isFile()||st.isSymbolicLink()||st.size>2000000)throw Error("unsafe source: "+name);
   const bytes=fs.readFileSync(file);
   const sha=crypto.createHash("sha1").update(Buffer.from("blob "+bytes.length+"\0")).update(bytes).digest("hex");
   sources[name]={sha,text:new TextDecoder("utf-8",{fatal:true}).decode(bytes)};
  }
  const report=audit(packet,sources);process.stdout.write(JSON.stringify(report,null,2)+"\n");process.exit(report.ok?0:1);
 }catch(e){process.stderr.write(String(e)+"\n");process.exit(2)}
}