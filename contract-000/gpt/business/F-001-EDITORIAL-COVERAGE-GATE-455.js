#!/usr/bin/env node
"use strict";
/* F-001 Contract-000 Run455: source-pinned editorial coverage receipt.
 * Read-only, HOLD-only. Proposals are Claude-reported, not editorial approval.
 * Source: F-001-CROSS-QUEUE-407.json (Git blob ab5e755c), TAM main d46456a.
 * §155: 72 proposed occurrence states, 10 remaining, 0 final. Claude proposals only.
 */
const EXPECTED_SOURCE = "d46456a18fe412398d0ae37ec5a8c4eebb44e0c9";
const REVIEWED_155 = Object.freeze([68,69,76,82,97,100,109,110,115,117].map(n => 'Collective information#S' + n));
const PENDING_NUMBERS = Object.freeze([126,129,141,147,149,222,230,236,271,276]);
const PENDING = Object.freeze(PENDING_NUMBERS.map(n => "Collective information#S" + n));
const EXPECTED_IDS = Object.freeze(["README.md#S24","Article 1 Hacksilber#S9","Article 1 Hacksilber#S18","Article 2 Water Weight Computes#S5","Article 2 Water Weight Computes#S18","Article 2 Water Weight Computes#S24","The Color Dyed and Dental Records#S23","The Color Dyed and Dental Records#S33","The Color Dyed and Dental Records#S37","Article 5#S7","Article 5#S8","Article 5#S22","Article 6#S4","Article 6#S23","Article 6#S29","Article 10#S3","Article 10#S4","Article 10#S5","Article 10#S8","Collective information#S26","Collective information#S27","Collective information#S39","Collective information#S55","Collective information#S57","Collective information#S68","Collective information#S69","Collective information#S97","Collective information#S100","Collective information#S110","Collective information#S128","Collective information#S147","Collective information#S149","Collective information#S153","Collective information#S172","Collective information#S178","Collective information#S230","Collective information#S236","Collective information#S271","Collective information#S293","Collective information#S294","Collective information#S295","Collective information#S298","README.md#S8","The Color Dyed and Dental Records#S14","Collective information#S90","README.md#S4","README.md#S7","README.md#S18","Article 1 Hacksilber#S15","Article 1 Hacksilber#S17","Article 2 Water Weight Computes#S1","Article 2 Water Weight Computes#S15","Article 2 Water Weight Computes#S19","Article 2 Water Weight Computes#S20","The Color Dyed and Dental Records#S5","The Color Dyed and Dental Records#S15","Article 5#S4","Article 5#S17","Article 5#S19","Article 6#S1","Collective information#S150","Article 6#S12","Collective information#S161","Article 6#S19","Collective information#S168","Collective information#S3","Collective information#S11","Collective information#S35","Collective information#S37","Collective information#S46","Collective information#S53","Collective information#S60","Collective information#S76","Collective information#S82","Collective information#S109","Collective information#S115","Collective information#S117","Collective information#S126","Collective information#S129","Collective information#S141","Collective information#S222","Collective information#S276"]);
const PREFIX = /^(?:README\.md|Article 1 Hacksilber|Article 2 Water Weight Computes|The Color Dyed and Dental Records|Article 5|Article 6|Article 10|Collective information)#S[1-9][0-9]*$/;
function fail(reason) { throw new Error("F-001 HOLD: " + reason); }
function audit(queue) {
  if (!queue || typeof queue !== "object" || Array.isArray(queue)) fail("invalid queue");
  if (queue.project !== "F-001" || queue.format !== "f001-cross-queue-audit-v1") fail("wrong project/format");
  if (queue.source_commit !== EXPECTED_SOURCE) fail("source commit mismatch");
  if (queue.status !== "HOLD / NOT LAUNCH-READY" || queue.release_authorized !== false) fail("release boundary altered");
  if (queue.final_approved_count || (Array.isArray(queue.final_approvals) && queue.final_approvals.length)) fail("unsupported final approval");
  if (queue.total_occurrences !== 82 || queue.baseline_count !== 45 ||
      queue.supplemental_occurrence_count !== 37) fail("declared counts changed");
  if (!Array.isArray(queue.baseline_ids) || queue.baseline_ids.length !== 45 ||
      !Array.isArray(queue.supplemental_refs) || queue.supplemental_refs.length !== 37) fail("queue arrays incomplete");
  const ids = [...queue.baseline_ids, ...queue.supplemental_refs.map(r => r && r.id)];
  if (ids.some(id => typeof id !== "string" || !PREFIX.test(id))) fail("unknown/malformed occurrence ID");
  if (new Set(ids).size !== 82) fail("duplicate occurrence ID");
  if (ids.some((id,i) => id !== EXPECTED_IDS[i])) fail("source-pinned occurrence sequence changed");
  const all = new Set(ids);
  if (PENDING.length !== 10 || PENDING.some(id => !all.has(id))) fail("pending §155 ID missing");
  if (REVIEWED_155.length !== 10 || REVIEWED_155.some(id => !all.has(id) || PENDING.includes(id))) fail("§155 reviewed ID mismatch");
  const pending = ids.filter(id => PENDING.includes(id));
  if (pending.length !== 10 || ids.length - pending.length !== 72) fail("editorial coverage mismatch");
  return {
    project:"F-001", source_commit:EXPECTED_SOURCE, status:"HOLD / NOT LAUNCH-READY",
    queue_occurrences:82, pending_unreviewed:10, claude_reported_proposed:72,
    final_approved:0, release_authorized:false,
    pending_ids:PENDING.slice(),
    limitation:"72 are Claude-reported proposals, not independently checked editorial approvals; all 82 remain release-blocked."
  };
}
if (typeof module !== "undefined") module.exports = {audit, PENDING, REVIEWED_155, EXPECTED_SOURCE};
if (typeof require !== "undefined" && typeof module !== "undefined" && require.main === module) {
  const fs = require("fs");
  if (process.argv.length !== 3) { console.error("usage: node F-001-EDITORIAL-COVERAGE-GATE-455.js QUEUE.json"); process.exit(2); }
  try { console.log(JSON.stringify(audit(JSON.parse(fs.readFileSync(process.argv[2], "utf8"))), null, 2)); }
  catch (e) { console.error(String(e)); process.exit(2); }
}
