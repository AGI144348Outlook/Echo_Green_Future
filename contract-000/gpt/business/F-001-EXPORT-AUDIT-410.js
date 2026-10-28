#!/usr/bin/env node
"use strict";
/* F-001 HOLD-only independent exported-draft audit, Run410.
 * Usage: node F-001-EXPORT-AUDIT-410.js <pinned-editor-406.html> <export.json>
 * No network, no writes. Refuses altered editor bytes and untrusted release flags.
 * This is an editorial draft-integrity check, not approval of evidence or rights.
 */
const PINNED_EDITOR_BLOB="e3e2942181d5460b631e428096429c9939a6062d";
function auditDraft(o,map){
 const fail=s=>{throw Error(s)};
 const exact=(obj,required)=>obj&&typeof obj==="object"&&!Array.isArray(obj)&&Object.keys(obj).length===required.length&&required.every(k=>Object.prototype.hasOwnProperty.call(obj,k));
 const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const keys=["format","project","status","release_authorized","source_commit","source_map_blob","source_pins","group_count","occurrence_count","baseline_queue_count","source_groups","drafts","created_at"];
 if(!exact(o,keys))fail("export keys");
 if(!map||map.project!=="F-001"||!Array.isArray(map.groups)||map.groups.length!==34||map.groups.reduce((n,g)=>n+g.occurrence_ids.length,0)!==37)fail("trusted map structure");
 if(o.format!=="f001-supplemental-review-draft-v1"||o.project!=="F-001"||o.status!=="HOLD / NOT LAUNCH-READY"||o.release_authorized!==false)fail("HOLD status");
 if(o.source_commit!==map.source_commit||o.source_map_blob!=="32dfe75589a031de46c28145fe993122ee2ca0f2"||!eq(o.source_pins,map.source_pins))fail("source pins");
 if(o.group_count!==34||o.occurrence_count!==37||o.baseline_queue_count!==45||!eq(o.source_groups,map.groups))fail("source group integrity");
 if(typeof o.created_at!=="string"||o.created_at.length>32||! /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(o.created_at)||!Number.isFinite(Date.parse(o.created_at))||new Date(o.created_at).toISOString()!==o.created_at)fail("timestamp");
 if(!o.drafts||typeof o.drafts!=="object"||Array.isArray(o.drafts)||Object.getPrototypeOf(o.drafts)!==Object.prototype)fail("draft collection");
 const ids=new Set(map.groups.map(g=>g.group_id));
 const fields=["decision","evidence","rights_notes","editorial_note","reviewer"];
 const limits={decision:50,evidence:2500,rights_notes:1500,editorial_note:2500,reviewer:150};
 const decisions=new Set(["","ADD_TO_QUEUE","ALREADY_COVERED","NOT_AN_EDITORIAL_CLAIM","DEFER_MORE_EVIDENCE"]);
 for(const [id,d] of Object.entries(o.drafts)){
  if(!ids.has(id)||!d||typeof d!=="object"||Array.isArray(d)||Object.getPrototypeOf(d)!==Object.prototype||Object.keys(d).some(k=>!fields.includes(k)))fail("draft identity/shape");
  for(const k of fields){const v=d[k]===undefined?"":d[k];if(typeof v!=="string"||v.length>limits[k])fail("draft value "+k);if(k==="decision"&&!decisions.has(v))fail("decision");}
 }
 return {project:"F-001",status:"HOLD / NOT LAUNCH-READY",trusted_source_commit:map.source_commit,group_count:34,occurrence_count:37,draft_count:Object.keys(o.drafts).length,release_authorized:false};
}
if(typeof require==="function" && typeof module==="object" && require.main===module){
 const fs=require("node:fs"),crypto=require("node:crypto");
 try{
  if(process.argv.length!==4)throw Error("usage: node F-001-EXPORT-AUDIT-410.js <pinned-editor-406.html> <export.json>");
  function readBounded(path){const s=fs.statSync(path);if(!s.isFile()||s.size>2097152)throw Error("not a bounded regular file: "+path);return fs.readFileSync(path);}
  const editor=readBounded(process.argv[2]), exported=readBounded(process.argv[3]);
  const blob=crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+editor.length+"\0"),editor])).digest("hex");
  if(blob!==PINNED_EDITOR_BLOB)throw Error("editor Git blob mismatch");
  const match=editor.toString("utf8").match(/const MAP = ([^\n]+);\s*;\s*const FORMAT=/);
  if(!match)throw Error("trusted source map missing");
  const trustedMap=JSON.parse(match[1]);
  const result=auditDraft(JSON.parse(exported.toString("utf8")),trustedMap);
  console.log(JSON.stringify({audit:"PASS",...result,editor_git_blob:blob}));
 }catch(e){console.error(JSON.stringify({audit:"FAIL",reason:String(e.message)}));process.exitCode=1;}
}
