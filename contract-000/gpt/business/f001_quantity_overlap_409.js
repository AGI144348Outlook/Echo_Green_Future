#!/usr/bin/env node
/* F-001 Run409 HOLD-only quantity-overlap triage. Not fact-checking, not an approval.
 * Usage: node f001_quantity_overlap_409.js <baseline397.html> <supplemental406.html>
 * Requires f001_cross_queue_audit_407.js in the same directory.
 */
"use strict";
const fs=require("fs");
const {extractJSON,audit,gitBlobSha}=require("./f001_cross_queue_audit_407.js");
const PINS=["7da6d43f42618ae915adb9f1fda216890a635674","e3e2942181d5460b631e428096429c9939a6062d"];
function quantities(text){
  if(typeof text!=="string")throw Error("non-string passage");
  const result=[...text.matchAll(/(?<![\\p{L}\\p{N}])(\\d+(?:[.,]\\d+)?)\\s*(kg|km|mm|cm|grams?|g)(?![\\p{L}])/giu)]
    .map(m=>m[1].replace(",",".")+"|"+(m[2].toLowerCase().startsWith("gram")?"g":m[2].toLowerCase()));
  return [...new Set(result)].sort();
}
function review(cards,map){
  const proof=audit(cards,map);
  if(proof.source_id_overlaps.length||proof.exact_text_overlaps.length)throw Error("source overlap: HOLD");
  for(const c of cards)if(c.approved===true||c.release_authorized===true||
    (c.human_review_status&&c.human_review_status!=="UNREVIEWED"))throw Error("baseline approval: HOLD");
  const pairs=[],frequency=new Map();
  for(const c of cards)for(const g of map.groups){
    const a=quantities(c.text),b=new Set(quantities(g.full_sentence));
    const shared=a.filter(x=>b.has(x));
    if(!shared.length)continue;
    pairs.push({c,g,shared});
    for(const x of shared)frequency.set(x,(frequency.get(x)||0)+1);
  }
  const ubiquitous=[...frequency].filter(([token,count])=>count>10).map(([token,count])=>({token,pair_count:count}));
  const selected=pairs.filter(p=>p.shared.some(x=>frequency.get(x)<=10)).map(p=>({
    baseline_id:p.c.id,baseline_priority:p.c.priority,baseline_file:p.c.file,baseline_blob:p.c.blob,
    baseline_sentence:p.c.text,supplemental_group:p.g.group_id,
    supplemental_ids:[...p.g.occurrence_ids],
    supplemental_refs:p.g.source_refs.map(r=>({id:r.id,file:r.file,blob_sha:r.blob_sha,source_commit:r.source_commit})),
    supplemental_sentence:p.g.full_sentence,
    rare_shared_quantities:p.shared.filter(x=>frequency.get(x)<=10),
    ubiquitous_shared_quantities:p.shared.filter(x=>frequency.get(x)>10),
    human_review_status:"UNREVIEWED",editorial_disposition:null,rights_clearance:null,release_authorized:false
  })).sort((a,b)=>a.supplemental_group.localeCompare(b.supplemental_group)||a.baseline_id.localeCompare(b.baseline_id));
  ubiquitous.sort((a,b)=>b.pair_count-a.pair_count||a.token.localeCompare(b.token));
  return {format:"f001-quantity-overlap-v1",project:"F-001",status:"HOLD / NOT LAUNCH-READY",
    release_authorized:false,source_commit:proof.source_commit,editor_blobs:{baseline:PINS[0],supplemental:PINS[1]},
    baseline_count:proof.baseline_count,baseline_p1:proof.baseline_p1,
    supplemental_groups:proof.supplemental_group_count,supplemental_occurrences:proof.supplemental_occurrence_count,
    total_pairs_compared:cards.length*map.groups.length,
    matched_quantity_pairs:pairs.length,ubiquitous_quantity_pairs:pairs.filter(p=>p.shared.every(x=>frequency.get(x)>10)).length,
    rarity_rule:"retain a pair only if it shares a number+mass/length unit seen in <=10 cross-queue pairs",
    ubiquitous_quantities:ubiquitous,rare_candidate_pairs:selected.length,candidates:selected,
    limitations:["Shared 13.7g is background repetition, not independent corroboration or semantic equivalence.",
      "A rare number+unit match is a retrieval clue only; it does not verify geodetic measurements or source rights.",
      "Only g/kg/km/mm/cm units and exact numeric forms are matched; paraphrases, conversions and other units may be missed.",
      "All source review states remain UNREVIEWED; no editing, sale or publication authorized."]};
}
function main(argv){
  if(argv.length!==2)throw Error("usage: node f001_quantity_overlap_409.js <baseline397.html> <supplemental406.html>");
  const texts=argv.map((path,i)=>{const b=fs.readFileSync(path);if(gitBlobSha(b)!==PINS[i])throw Error("source Git blob mismatch: "+path);return b.toString("utf8")});
  process.stdout.write(JSON.stringify(review(extractJSON(texts[0],"CARDS"),extractJSON(texts[1],"MAP")),null,2)+"\\n");
}
if(require.main===module){try{main(process.argv.slice(2))}catch(e){process.stderr.write("HOLD quantity audit failed: "+e.message+"\\n");process.exitCode=1}}
module.exports={quantities,review,PINS};
