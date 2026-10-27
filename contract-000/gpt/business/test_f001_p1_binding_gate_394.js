"use strict";
// Synthetic tamper-negative cases plus one actual pinned F-001 queue/packet binding.
function runF001P1Tests(audit, queue, packet) {
  const copy = x => JSON.parse(JSON.stringify(x));
  const cases = [
    ["actual_18", null, null],
    ["alter_source_sha", (a,b)=>{b.proposals[0].source_blob_sha="0".repeat(40);}, "binding_source_blob_sha"],
    ["alter_sentence", (a,b)=>{b.proposals[0].full_sentence+=" altered";}, "binding_full_sentence"],
    ["alter_sentence_number", (a,b)=>{b.proposals[0].sentence_no++;}, "binding_sentence_no"],
    ["remove_duplicate", (a,b)=>{const p=b.proposals.find(x=>x.duplicate_occurrences.length);p.duplicate_occurrences=[];}, "duplicate_links"],
    ["approve_without_authority", (a,b)=>{b.proposals[0].approved_by="unapproved";}, "premature_approval"],
    ["duplicate_proposal_id", (a,b)=>{b.proposals[1].id=b.proposals[0].id;}, "duplicate_proposal_id"],
    ["unknown_occurrence", (a,b)=>{b.proposals[0].id="invented#S0";}, "unknown_occurrence"],
    ["delete_evidence_requirement", (a,b)=>{b.proposals[0].evidence_required="";}, "incomplete_proposal"],
    ["queue_edited_status", (a,b)=>{a.cards[0].review_status="APPROVED";}, "queue_has_decision"],
    ["queue_release_true", (a,b)=>{a.release_authorized=true;}, "release_not_held"],
    ["packet_count_drift", (a,b)=>{b.priority_count=17;}, "proposal_count"],
    ["queue_count_drift", (a,b)=>{a.card_count=44;}, "queue_count"]
  ];
  return cases.map(([name,mutate,expected])=>{
    const a=copy(queue),b=copy(packet);
    if(mutate) mutate(a,b);
    const result=audit(a,b);
    const pass=expected ? result.errors.some(e=>e.code===expected) : result.ok;
    return {name,pass,observed:result.ok?"PASS":result.errors.map(e=>e.code)};
  });
}
if (typeof module !== "undefined" && module.exports) module.exports={runF001P1Tests};
