#!/usr/bin/env node
/* F-001 Run408 HOLD-only lexical cross-queue candidate retrieval.
 * Usage: node f001_semantic_candidates_408.js F-001-OFFLINE-EDITOR-397.html F-001-SUPPLEMENTAL-OFFLINE-EDITOR-406.html
 * No ML or semantic entailment: this is transparent lexical retrieval for human review.
 * Inputs are pinned Git blob bytes. Never edits source, drafts, or release state.
 */
"use strict";
const fs=require("fs");
const {extractJSON,audit,gitBlobSha}=require("./f001_cross_queue_audit_407.js");
const PINS=["7da6d43f42618ae915adb9f1fda216890a635674","e3e2942181d5460b631e428096429c9939a6062d"];
const STOP=new Set(("the a an and or of to for in on with from that this these those is are was were be been being as by it its at into out over under not no so if than then which who has have had do does did will would can could may might shall should we our their there they you your what where when how one two three more less same any all each every both only also about according based because through between after before across during some such very now just here them").split(" "));
function tokens(s){
  if(typeof s!=="string")throw Error("non-string sentence");
  return [...new Set((s.normalize("NFKC").toLowerCase().match(/[\p{L}\p{N}]+(?:\.\d+)?/gu)||[])
    .filter(t=>(t.length>=3||/^\d+$/.test(t))&&!STOP.has(t)))].sort();
}
function similarity(a,b){
  const A=tokens(a),B=tokens(b),bs=new Set(B),shared=A.filter(t=>bs.has(t));
  const union=new Set([...A,...B]).size;
  return {score:union?Number((shared.length/union).toFixed(6)):0,shared};
}
function review(cards,map){
  const base=audit(cards,map);
  if(base.source_id_overlaps.length||base.exact_text_overlaps.length)throw Error("exact overlap: review source queues before lexical triage");
  for(const c of cards){
    if(c.release_authorized===true||c.approved===true||c.human_review_status&&c.human_review_status!=="UNREVIEWED")throw Error("baseline contains approval");
  }
  const candidates=[];
  for(const c of cards)for(const g of map.groups){
    const sim=similarity(c.text,g.full_sentence);
    if(sim.shared.length<3||sim.score<0.20)continue;
    candidates.push({
      baseline_id:c.id,baseline_priority:c.priority,baseline_file:c.file,baseline_blob:c.blob,baseline_sentence:c.text,
      supplemental_group:g.group_id,supplemental_ids:[...g.occurrence_ids],
      supplemental_refs:g.source_refs.map(r=>({id:r.id,file:r.file,blob_sha:r.blob_sha,source_commit:r.source_commit})),
      supplemental_sentence:g.full_sentence,
      lexical_jaccard:sim.score,shared_tokens:sim.shared,
      human_review_status:"UNREVIEWED",editorial_disposition:null,rights_clearance:null,release_authorized:false
    });
  }
  candidates.sort((a,b)=>b.lexical_jaccard-a.lexical_jaccard||a.baseline_id.localeCompare(b.baseline_id,"en")||a.supplemental_group.localeCompare(b.supplemental_group,"en"));
  return {format:"f001-lexical-review-candidates-v1",project:"F-001",source_commit:base.source_commit,
    editor_blobs:{baseline:PINS[0],supplemental:PINS[1]},
    status:"HOLD / NOT LAUNCH-READY",release_authorized:false,
    baseline_count:base.baseline_count,baseline_p1:base.baseline_p1,
    supplemental_group_count:base.supplemental_group_count,supplemental_occurrence_count:base.supplemental_occurrence_count,
    total_compared:cards.length*map.groups.length,threshold:{min_shared_tokens:3,min_jaccard:0.20},
    candidate_pair_count:candidates.length,candidates,
    limitations:["Lexical overlap is not semantic equivalence, contradiction, evidence or editorial approval.","A paraphrase with few shared tokens can be missed; unrelated text can share tokens.","No draft, right, credit, sale or release is authorized; all source review statuses remain UNREVIEWED."]};
}
function main(argv){
  if(argv.length!==2)throw Error("usage: node f001_semantic_candidates_408.js <baseline397.html> <supplemental406.html>");
  const contents=argv.map((p,i)=>{const b=fs.readFileSync(p);if(gitBlobSha(b)!==PINS[i])throw Error("input Git blob mismatch: "+p);return b.toString("utf8")});
  const result=review(extractJSON(contents[0],"CARDS"),extractJSON(contents[1],"MAP"));
  process.stdout.write(JSON.stringify(result,null,2)+"\n");
}
if(require.main===module){try{main(process.argv.slice(2))}catch(e){process.stderr.write("HOLD lexical review failure: "+e.message+"\n");process.exitCode=1}}
module.exports={tokens,similarity,review,PINS};
