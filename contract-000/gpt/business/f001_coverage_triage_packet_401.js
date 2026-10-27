#!/usr/bin/env node
"use strict";
/** F-001 HOLD-only 37-candidate reviewer packet builder (Run401).
 * Inputs: exact pinned TAM source directory, Run400 coverage JSON, Run388 45-card queue JSON.
 * Usage: node f001_coverage_triage_packet_401.js <tam-dir> <coverage.json> <queue.json>
 * stdout: JSON. Never writes source files or authorizes release.
 */
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
const gitBlobSha=s=>{const b=Buffer.from(s,"utf8");return crypto.createHash("sha1").update(Buffer.from("blob "+b.length+"\0")).update(b).digest("hex")};
const buildPacket=function buildPacket(sources,coverage,queue,shas){
 if(coverage.project!=="F-001"||queue.project!=="F-001"||coverage.source_commit!==queue.source_commit)throw Error("project/commit mismatch");
 const names=Object.keys(coverage.source_pins),existing=new Map(queue.cards.map(c=>[c.id,c]));
 if(queue.cards.length!==45||existing.size!==45)throw Error("existing queue invalid");
 if(names.length!==8||names.some(n=>!Object.prototype.hasOwnProperty.call(sources,n)||shas[n]!==coverage.source_pins[n]))throw Error("source pin or presence mismatch");
 const ss=Object.fromEntries(names.map(n=>[n,sources[n].split(/(?<=[.!?])\s+|\n{2,}/).map(s=>s.trim()).filter(Boolean)]));
 const items=coverage.observations.unit_assertion_triage;
 if(!Array.isArray(items)||items.length!==37)throw Error("triage candidate count mismatch");
 const ids=new Set();
 const norm=s=>s.replace(/\s+/g," ").trim().toLowerCase();
 const result=[];
 for(const x of items){
  if(ids.has(x.id)||existing.has(x.id))throw Error("duplicate or existing queue ID "+x.id);
  ids.add(x.id);
  const m=x.id.match(/^(.*)#S([1-9]\d*)$/);if(!m)throw Error("bad ID");
  const [_,file,ns]=m;const idx=Number(ns)-1,segments=ss[file];if(!segments||!segments[idx])throw Error("missing source occurrence");
  const full=segments[idx];if(full.slice(0,220)!==x.excerpt)throw Error("excerpt mismatch "+x.id);
  const flags=[];
  if(full.includes("\n"))flags.push("multi-line-or-heading-mixed");
  if(/\b\d+(?:\.\d+)?\s*(?:g|grams?|kg|cm|mm)\b/i.test(full))flags.push("unit-bearing");
  if(/\b(?:perfect|exact|standard|universal|forensic|calibrat|enforc|predict|proved|trade|archaeolog|histor)\w*/i.test(full))flags.push("historical-or-empirical-assertion-cue");
  if(/\b(?:if|then|equals|equivalent|fraction|ratio|units?)\b/i.test(full))flags.push("derived-arithmetic-cue");
  const sameQueue=queue.cards.filter(c=>norm(c.full_sentence||"")===norm(full)).map(c=>c.id);
  result.push({id:x.id,source_file:file,source_commit:coverage.source_commit,source_blob_sha:coverage.source_pins[file],sentence_no:idx+1,full_sentence:full,previous_sentence:idx?segments[idx-1]:null,next_sentence:idx+1<segments.length?segments[idx+1]:null,run400_preview:x.excerpt,provisional_flags:flags,existing_queue_exact_text_ids:sameQueue,other_candidate_exact_text_ids:[],human_review_status:"UNREVIEWED",editorial_disposition:null,evidence_reference:null,rights_clearance:null,reviewer:null,reviewer_question:"Is this an empirical/historical claim, a heading, a derivation or a quotation? Verify independent primary evidence and rights; decide add/covered/not-claim with reasons. Do not assume the metric claim is true."});
 }
 for(const item of result)item.other_candidate_exact_text_ids=result.filter(x=>x.id!==item.id&&norm(x.full_sentence)===norm(item.full_sentence)).map(x=>x.id);
 return {format:"f001-coverage-triage-packet-v1",project:"F-001",run:401,status:"HOLD / NOT LAUNCH-READY",release_authorized:false,source_repo:coverage.source_repo,source_commit:coverage.source_commit,source_pins:coverage.source_pins,source_coverage_blob:"50fe65a1c17fcc3f7270e4128881634b72eacf39",existing_queue_blob:"06530d6729c3af39feebce9a6999650270008bf5",existing_queue_count:45,coverage_candidate_count:37,human_approved_count:0,scope:"Supplemental heuristic triage; 37 potential candidates outside existing queue; no claims admitted or approved.",review_decision_options:["ADD_TO_QUEUE","ALREADY_COVERED","NOT_AN_EDITORIAL_CLAIM","DEFER_MORE_EVIDENCE"],instructions:"Claude independently reviews source, independent evidence, rights and duplicates. Any proposed decision remains unapproved until attributable human authorization; publication stays HOLD.",items:result};
};
if(require.main===module){
 if(process.argv.length!==5){console.error("usage: node f001_coverage_triage_packet_401.js <tam-dir> <coverage.json> <queue.json>");process.exit(2)}
 const [dir,cfile,qfile]=process.argv.slice(2),coverage=JSON.parse(fs.readFileSync(cfile,"utf8")),queue=JSON.parse(fs.readFileSync(qfile,"utf8"));
 const sources=Object.fromEntries(Object.keys(coverage.source_pins).map(n=>[n,fs.readFileSync(path.join(dir,n),"utf8")]));
 const shas=Object.fromEntries(Object.entries(sources).map(([n,s])=>[n,gitBlobSha(s)]));
 try{console.log(JSON.stringify(buildPacket(sources,coverage,queue,shas),null,2))}catch(e){console.error("HOLD / FAIL CLOSED:",e.message);process.exit(1)}
}
module.exports={buildPacket,gitBlobSha};
