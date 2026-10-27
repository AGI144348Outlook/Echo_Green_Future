"use strict";
/* F-001 Run402 HOLD-only exact-occurrence reviewer grouping.
 * Usage: node f001_review_group_402.js <F-001-COVERAGE-TRIAGE-PACKET-401.json>
 * Output: JSON to stdout. Does not approve, modify source, or publish.
 */
function normalize(s){return s.replace(/\s+/g," ").trim().toLowerCase();}
function validatePacket(p){
 if(!p||p.project!=="F-001"||p.release_authorized!==false||p.status!=="HOLD / NOT LAUNCH-READY")throw Error("project/release guard");
 if(!p.source_pins||Object.keys(p.source_pins).length!==8||!Array.isArray(p.items)||p.items.length!==37||p.human_approved_count!==0)throw Error("source/count guard");
 const ids=new Map();
 for(const x of p.items){
  if(!x||typeof x.id!=="string"||ids.has(x.id))throw Error("duplicate or malformed id");
  const m=x.id.match(/^(.*)#S([1-9]\d*)$/);
  if(!m||m[1]!==x.source_file||p.source_pins[x.source_file]!==x.source_blob_sha||x.source_commit!==p.source_commit)throw Error("source identity mismatch");
  if(typeof x.full_sentence!=="string"||!x.full_sentence.trim()||x.human_review_status!=="UNREVIEWED"||x.editorial_disposition!==null||x.evidence_reference!==null||x.rights_clearance!==null||x.reviewer!==null)throw Error("unauthorized editorial state");
  if(!Array.isArray(x.other_candidate_exact_text_ids))throw Error("bad duplicate links");
  ids.set(x.id,x);
 }
 for(const x of p.items){
  const actual=p.items.filter(y=>y.id!==x.id&&normalize(y.full_sentence)===normalize(x.full_sentence)).map(y=>y.id).sort();
  const listed=x.other_candidate_exact_text_ids.slice().sort();
  if(actual.join("|")!==listed.join("|"))throw Error("duplicate links inconsistent "+x.id);
 }
 return true;
}
function buildReviewMap(p){
 validatePacket(p);
 const groups=[], bySentence=new Map();
 for(const x of p.items){
  const k=normalize(x.full_sentence);
  let g=bySentence.get(k);
  if(!g){
   const s=x.full_sentence;
   const focus=[];
   if(/\b(?:would|could|if|proposes?|in this model|intuition|hypothes)/i.test(s))focus.push("hypothetical-or-conditional-framing");
   if(/\b(?:bronze age|indus|maya|egypt|mesopotamia|levan|ancient|archaeolog|hoard|artifact|historical|forensic|evidence)/i.test(s))focus.push("historical-evidence-required");
   if(/\b(?:gravity|gravimetric|electromagnetic|flow rate|water clock|clock|calibrat|predict|metric friction|latitude|longitude)/i.test(s))focus.push("mechanism-or-measurement-check");
   if(/\b(?:perfect|universal|standard|exact|proves?|demonstrat|ensured|enforced|were keeping|became)/i.test(s))focus.push("certainty-or-attribution-check");
   if(s.includes("\n"))focus.push("heading-or-layout-segmentation-check");
   if(focus.length===0)focus.push("general-claim-context-review");
   g={group_id:"G"+String(groups.length+1).padStart(3,"0"),full_sentence:s,occurrence_ids:[],source_refs:[],review_focus:focus,human_review_status:"UNREVIEWED",editorial_disposition:null,independent_evidence:null,rights_clearance:null,reviewer:null,release_authorized:false};
   groups.push(g);bySentence.set(k,g);
  }
  g.occurrence_ids.push(x.id);
  g.source_refs.push({id:x.id,file:x.source_file,blob_sha:x.source_blob_sha,source_commit:x.source_commit,sentence_no:x.sentence_no});
 }
 const output={format:"f001-exact-occurrence-review-map-v1",project:"F-001",run:402,status:"HOLD / NOT LAUNCH-READY",release_authorized:false,source_packet_blob:"dfa28a6a750967a2bb600e56a6e962117890478b",source_commit:p.source_commit,source_pins:p.source_pins,occurrence_count:p.items.length,distinct_group_count:groups.length,human_approved_count:0,scope:"Structural grouping and heuristic focus only; no evidence, rights or editorial approval",groups};
 validateMap(output,p);return output;
}
function validateMap(o,p){
 validatePacket(p);
 if(o.project!=="F-001"||o.release_authorized!==false||o.status!=="HOLD / NOT LAUNCH-READY"||o.human_approved_count!==0||o.occurrence_count!==37||o.distinct_group_count!==o.groups.length)throw Error("map metadata guard");
 if(o.source_commit!==p.source_commit||JSON.stringify(o.source_pins)!==JSON.stringify(p.source_pins))throw Error("map pin mismatch");
 const idMap=new Map(p.items.map(x=>[x.id,x])),seen=new Set(),sentences=new Set();
 for(const g of o.groups){
  if(g.release_authorized!==false||g.human_review_status!=="UNREVIEWED"||g.editorial_disposition!==null||g.independent_evidence!==null||g.rights_clearance!==null||g.reviewer!==null)throw Error("map approval guard");
  const n=normalize(g.full_sentence);if(sentences.has(n))throw Error("duplicate group");sentences.add(n);
  if(g.occurrence_ids.length!==g.source_refs.length||!g.occurrence_ids.length)throw Error("group refs mismatch");
  for(let i=0;i<g.occurrence_ids.length;i++){
   const id=g.occurrence_ids[i],x=idMap.get(id),ref=g.source_refs[i];
   if(!x||seen.has(id)||normalize(x.full_sentence)!==n||ref.id!==id||ref.blob_sha!==x.source_blob_sha||ref.source_commit!==x.source_commit||ref.file!==x.source_file||ref.sentence_no!==x.sentence_no)throw Error("map occurrence mismatch");
   seen.add(id);
  }
 }
 if(seen.size!==37)throw Error("dropped occurrence");
 return true;
}
if(typeof module!=="undefined")module.exports={normalize,validatePacket,buildReviewMap,validateMap};
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("node:fs");const p=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
 process.stdout.write(JSON.stringify(buildReviewMap(p),null,2)+"\n");
}