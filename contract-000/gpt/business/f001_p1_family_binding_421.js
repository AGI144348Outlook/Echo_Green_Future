"use strict";
/* F-001 HOLD-only P1 review-family binding gate, Run421.
 * Source: contract-000/gpt/business/F-001-P1-TRIAGE-420.json
 * Git blob eb139defefba0e86ac23879e753e892ee654aca5.
 * No editorial decisions, publication, payment, network, or source mutation.
 * Pre-test: Echo_Green_Future Issue #94.
 */
const PACKET_BLOB = "eb139defefba0e86ac23879e753e892ee654aca5";
const SOURCE_COMMIT = "d46456a18fe412398d0ae37ec5a8c4eebb44e0c9";
const SOURCE_PACKET_BLOB = "998ca10ccb31ff991041051b9e8d4862751737c3";
const PINS = Object.freeze({
  "README.md":"213bcfaf560dcc54fbb7ae79fad932e86b660357",
  "Article 1 Hacksilber":"237bd3335abdcc0f0465817dffe01ad6eaa86055",
  "Article 2 Water Weight Computes":"ec657c3fa0f70da9686fb1ae52983d28f77c6c4c",
  "The Color Dyed and Dental Records":"b525ad60ab37cb2d72ea43c40ba687b0fe2a348d",
  "Article 5":"c8c1bf617c0d81389f6c2408ed975131695857ff",
  "Article 6":"662d745f0b9b41236d1053cdbaa9351f7c020dd0",
  "Article 10":"e82be564872f636662652d34dcb8d3437559f84f",
  "Collective information":"710ad3cd4feeae7bafa329d7437a78df4c40cfa8"
});
const EXPECT = Object.freeze({parent_occurrences:82,baseline_occurrences:45,supplemental_occurrences:37,p1_occurrences:18,p1_distinct_exact_sentences:14,p1_exact_duplicate_pairs:4});
function validateP1(p) {
  const errors=[];
  const fail=(m)=>errors.push(m);
  if (!p || typeof p!=="object") return {ok:false,errors:["packet object missing"]};
  if (p.format!=="f001-p1-hold-triage-v1") fail("format mismatch");
  if (p.project!=="F-001") fail("project mismatch");
  if (p.status!=="HOLD / NOT LAUNCH-READY") fail("status not HOLD");
  if (p.source_commit!==SOURCE_COMMIT || p.source_packet_blob_sha!==SOURCE_PACKET_BLOB) fail("parent source pin mismatch");
  if (p.human_reviewed_count!==0) fail("human review count not zero");
  if (p.release_authorized!==false) fail("release flag not false");
  for (const [k,v] of Object.entries(EXPECT)) if (p.counts?.[k]!==v) fail("count mismatch "+k);
  if (!p.source_pins || Object.keys(p.source_pins).length!==Object.keys(PINS).length) fail("source pin set mismatch");
  for (const [k,v] of Object.entries(PINS)) if (p.source_pins?.[k]!==v) fail("source pin mismatch "+k);
  if (!Array.isArray(p.families)||!Array.isArray(p.occurrences)) return {ok:false,errors:errors.concat(["families/occurrences not arrays"])};
  if (p.families.length!==14) fail("family length mismatch");
  if (p.occurrences.length!==18) fail("occurrence length mismatch");
  const byFamily=new Map(), ids=new Set(), claimed=new Map(), sentences=new Set();
  for (const f of p.families) {
    if (!f || typeof f!=="object") {fail("invalid family object");continue;}
    if (byFamily.has(f.family_id)) fail("duplicate family "+f.family_id);
    byFamily.set(f.family_id,f);
    if (!/^P1-F(0[1-9]|1[0-4])$/.test(f.family_id||"")) fail("invalid family ID");
    if (typeof f.source_sentence!=="string" || !f.source_sentence.trim()) fail("missing family sentence");
    else sentences.add(f.source_sentence);
    if (!f.reviewer_question || typeof f.reviewer_question!=="string") fail("missing reviewer question");
    if (f.human_disposition!=="UNREVIEWED") fail("family status not UNREVIEWED "+f.family_id);
    if (f.evidence_assessed!==false || f.rights_assessed!==false || f.release_authorized!==false) fail("family flags not HOLD "+f.family_id);
    if (!Array.isArray(f.occurrence_ids) || f.occurrence_ids.length<1 || f.occurrence_ids.length>2) fail("invalid family occurrence IDs "+f.family_id);
    else {
      if (new Set(f.occurrence_ids).size!==f.occurrence_ids.length) fail("duplicate within family "+f.family_id);
      for (const id of f.occurrence_ids) {
        if (claimed.has(id)) fail("occurrence claimed twice "+id);
        claimed.set(id,f.family_id);
      }
    }
  }
  if (sentences.size!==14) fail("distinct family sentence count mismatch");
  if (p.families.filter(f=>Array.isArray(f?.occurrence_ids)&&f.occurrence_ids.length===2).length!==4) fail("duplicate family count mismatch");
  for (const o of p.occurrences) {
    if (!o || typeof o!=="object") {fail("invalid occurrence object");continue;}
    if (ids.has(o.id)) fail("duplicate occurrence "+o.id);
    ids.add(o.id);
    const f=byFamily.get(o.family_id);
    if (!f) fail("unknown occurrence family "+o.id);
    else if (o.full_source_sentence!==f.source_sentence) fail("sentence mismatch "+o.id);
    if (claimed.get(o.id)!==o.family_id) fail("family binding mismatch "+o.id);
    if (o.id!==o.file+"#S"+o.sentence_no || !Number.isInteger(o.sentence_no) || o.sentence_no<1) fail("location ID mismatch "+o.id);
    if (!Object.prototype.hasOwnProperty.call(PINS,o.file) || o.source_blob_sha!==PINS[o.file]) fail("occurrence source pin mismatch "+o.id);
    if (o.queue!=="baseline") fail("occurrence queue mismatch "+o.id);
    if (o.review_status!=="UNREVIEWED") fail("occurrence status not UNREVIEWED "+o.id);
    if (o.evidence_assessed!==false || o.rights_assessed!==false || o.release_authorized!==false) fail("occurrence flags not HOLD "+o.id);
  }
  for (const id of claimed.keys()) if (!ids.has(id)) fail("family claims absent occurrence "+id);
  for (const id of ids) if (!claimed.has(id)) fail("unclaimed occurrence "+id);
  return {ok:errors.length===0,errors};
}
if (typeof module!=="undefined" && module.exports) module.exports={validateP1,PACKET_BLOB};
if (typeof require!=="undefined" && typeof module!=="undefined" && require.main===module) {
  const fs=require("fs"), crypto=require("crypto");
  const filename=process.argv[2];
  if (!filename) {console.error("usage: node f001_p1_family_binding_421.js <unchanged-P1-TRIAGE-420.json>");process.exit(2);}
  const raw=fs.readFileSync(filename);
  const sha=crypto.createHash("sha1").update("blob "+raw.length+"\0").update(raw).digest("hex");
  if (sha!==PACKET_BLOB) {console.error("FAIL: input Git blob pin mismatch",sha);process.exit(1);}
  let data;
  try {data=JSON.parse(raw.toString("utf8"));}catch(e){console.error("FAIL: invalid JSON");process.exit(1);}
  const r=validateP1(data);
  console.log(JSON.stringify({ok:r.ok,source_git_blob:sha,errors:r.errors},null,2));
  process.exit(r.ok?0:1);
}
