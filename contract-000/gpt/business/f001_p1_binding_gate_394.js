"use strict";
// F-001 HOLD-only, read-only binding check for 18 proposed editorial decisions.
// This checks record integrity, not the truth of the claims or publication rights.
function auditF001P1(queue, packet) {
  const errors = [];
  const fail = (code, id) => errors.push({code, id: id || null});
  if (!queue || !packet || !Array.isArray(queue.cards) || !Array.isArray(packet.proposals)) {
    return {ok:false, errors:[{code:"invalid_schema", id:null}]};
  }
  if (queue.project !== "F-001" || packet.project !== "F-001") fail("project_mismatch");
  if (queue.status !== "HOLD" || queue.release_authorized !== false) fail("release_not_held");
  if (packet.status !== "HOLD" || packet.review_status !== "UNREVIEWED") fail("proposal_not_held");
  if (queue.card_count !== queue.cards.length || queue.card_count !== 45) fail("queue_count");
  if (queue.unreviewed_count !== queue.cards.length || queue.editorial_dispositions_approved !== 0) fail("queue_approval_count");
  if (packet.priority_count !== packet.proposals.length || packet.priority_count !== 18) fail("proposal_count");
  const cards = new Map();
  for (const c of queue.cards) {
    if (!c.id || cards.has(c.id)) fail("queue_duplicate_id", c.id);
    cards.set(c.id, c);
    if (c.review_status !== "UNREVIEWED" || c.editorial_disposition !== null || c.rights_clearance !== null) fail("queue_has_decision", c.id);
  }
  const seen = new Set();
  for (const p of packet.proposals) {
    if (!p.id || seen.has(p.id)) fail("duplicate_proposal_id", p.id);
    seen.add(p.id);
    const c = cards.get(p.id);
    if (!c) { fail("unknown_occurrence", p.id); continue; }
    for (const key of ["source_file","source_blob_sha","sentence_no","full_sentence","review_status"]) {
      if (p[key] !== c[key]) fail("binding_" + key, p.id);
    }
    const a = (p.duplicate_occurrences || []).slice().sort();
    const b = (c.duplicate_occurrence_ids || []).slice().sort();
    if (JSON.stringify(a) !== JSON.stringify(b)) fail("duplicate_links", p.id);
    if (p.review_status !== "UNREVIEWED" || p.approved_by !== null || p.rights_clearance !== "UNKNOWN") fail("premature_approval", p.id);
    if (!p.proposed_action || !p.suggested_editorial_language || !p.evidence_required) fail("incomplete_proposal", p.id);
  }
  return {ok:errors.length===0, errors, checked:{queue:queue.cards.length, proposals:packet.proposals.length, unique:seen.size}};
}
if (typeof module !== "undefined" && module.exports) module.exports = {auditF001P1};
