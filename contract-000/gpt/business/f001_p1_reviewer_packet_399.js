"use strict";
/* Contract-000 GPT Run399 — F-001 P1 human review packet, HOLD ONLY.
   Pure core accepts the exact source-bound queue and proposals JSON. It does not
   certify truth, rights, publication readiness, or approve any editorial choice.
   CLI: node f001_p1_reviewer_packet_399.js QUEUE.json PROPOSALS.json > packet.json
*/
const QUEUE_SHA = "06530d6729c3af39feebce9a6999650270008bf5";
const PROPOSALS_SHA = "5a4af09820c5842616cb26a3eefe3612195633d8";
function fail(code, detail) { throw new Error(code + ": " + detail); }
function validSha(s) { return typeof s === "string" && /^[0-9a-f]{40}$/.test(s); }
function sameArray(a,b) { return Array.isArray(a)&&Array.isArray(b)&&
  JSON.stringify([...a].sort()) === JSON.stringify([...b].sort()); }
function validateAndBuild(queue, proposals) {
  if (!queue || !proposals || queue.project!=="F-001" || proposals.project!=="F-001") fail("PROJECT","F-001 required");
  if (queue.status!=="HOLD" || queue.release_authorized!==false || proposals.status!=="HOLD")
    fail("HOLD","input release state is not HOLD");
  if (!Array.isArray(queue.cards) || queue.cards.length!==45 || queue.card_count!==45 ||
      queue.unreviewed_count!==45 || !Array.isArray(proposals.proposals) ||
      proposals.proposals.length!==18 || proposals.priority_count!==18)
    fail("COUNT","expected 45 unreviewed cards and 18 P1 proposals");
  if (!validSha(queue.source_commit)) fail("PIN","source commit missing");
  const cards = new Map();
  for (const c of queue.cards) {
    if (!c || typeof c.id!=="string" || cards.has(c.id)) fail("DUPLICATE_ID",c&&c.id);
    if (!validSha(c.source_blob_sha) || c.source_commit!==queue.source_commit ||
        !Number.isInteger(c.sentence_no) || c.sentence_no<1 ||
        c.id!==c.source_file+"#S"+c.sentence_no || typeof c.full_sentence!=="string" ||
        !c.full_sentence.trim()) fail("SOURCE",c.id);
    if (c.review_status!=="UNREVIEWED" || c.editorial_disposition!==null ||
        c.reviewer!==null || c.rights_clearance!==null) fail("UNREVIEWED",c.id);
    if (!Array.isArray(c.duplicate_occurrence_ids)) fail("DUPLICATE_SHAPE",c.id);
    cards.set(c.id,c);
  }
  const priorities = queue.cards.filter(c=>c.review_priority==="P1");
  if (priorities.length!==18) fail("P1_COUNT",priorities.length);
  const seen = new Set(), items = [];
  for (const p of proposals.proposals) {
    if (!p || typeof p.id!=="string" || seen.has(p.id)) fail("PROPOSAL_ID",p&&p.id);
    seen.add(p.id);
    const c=cards.get(p.id);
    if (!c || c.review_priority!=="P1") fail("P1_MATCH",p.id);
    for (const key of ["source_file","source_blob_sha","sentence_no","full_sentence"]) {
      if (p[key]!==c[key]) fail("BIND_"+key,p.id);
    }
    if (!sameArray(p.duplicate_occurrences,c.duplicate_occurrence_ids)) fail("DUPLICATE_LINK",p.id);
    for (const id of c.duplicate_occurrence_ids) {
      const d=cards.get(id);
      if (!d || !d.duplicate_occurrence_ids.includes(c.id)) fail("DUPLICATE_RECIPROCITY",p.id+" -> "+id);
    }
    if (p.review_status!=="UNREVIEWED" || p.approved_by!==null ||
        p.rights_clearance!=="UNKNOWN") fail("APPROVAL",p.id);
    if (typeof p.proposed_action!=="string" || !p.proposed_action ||
        typeof p.evidence_required!=="string" || !p.evidence_required ||
        typeof p.suggested_editorial_language!=="string") fail("PROPOSAL_SHAPE",p.id);
    items.push({
      id:c.id, source:{repo:queue.source_repo,commit:queue.source_commit,
        file:c.source_file,blob_sha:c.source_blob_sha,sentence_no:c.sentence_no},
      original_sentence:c.full_sentence,
      context:{previous:c.previous_sentence??null,next:c.next_sentence??null},
      related_occurrences:[...c.duplicate_occurrence_ids],
      flags:[...c.heuristic_flags], proposed_action:p.proposed_action,
      suggested_wording_NOT_APPROVED:p.suggested_editorial_language,
      evidence_needed:p.evidence_required,
      reviewer_record:{decision:null,evidence_reference:null,rights_review:null,
        reviewer:null,review_date:null,notes:null},
      review_status:"UNREVIEWED",release_authorized:false
    });
  }
  for (const c of priorities) if (!seen.has(c.id)) fail("P1_OMITTED",c.id);
  return {format:"f001-p1-review-packet-v1",project:"F-001",status:"HOLD",
    release_authorized:false, source_queue_blob:QUEUE_SHA,
    source_proposals_blob:PROPOSALS_SHA, source_commit:queue.source_commit,
    total_editorial_cards:45, priority_one_count:18,
    human_reviewed_count:0,
    instruction:"Human reviewer must inspect original sources, independent evidence, rights, and every duplicate occurrence. Suggested wording is NOT approved. This packet cannot authorize publication.",
    items};
}
if (typeof module!=="undefined") module.exports={validateAndBuild};
if (typeof require==="function" && typeof module!=="undefined" && require.main===module) {
  const fs=require("fs");
  try {
    if (process.argv.length!==4) fail("USAGE","QUEUE.json PROPOSALS.json required");
    const q=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
    const p=JSON.parse(fs.readFileSync(process.argv[3],"utf8"));
    process.stdout.write(JSON.stringify(validateAndBuild(q,p),null,2)+"\n");
  } catch(e) { process.stderr.write(String(e.message)+"\n"); process.exitCode=1; }
}
