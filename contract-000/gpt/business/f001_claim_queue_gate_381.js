#!/usr/bin/env node
"use strict";
/* F-001 TAM ebook: read-only 45-candidate inventory integrity gate.
   Validates inventory structure, NOT source text, editorial truth or release.
   Run: node f001_claim_queue_gate_381.js F-001-REAL-CLAIMS-378.json
   SOURCE PIN: The-TAM-protocol d46456a18fe412398d0ae37ec5a8c4eebb44e0c9
   SOURCE MANIFEST: GPT Run 378, 8 Git-pinned public source files.
*/
const PINNED_SOURCES = Object.freeze({
  "README.md": {
    "sha": "213bcfaf560dcc54fbb7ae79fad932e86b660357",
    "bytes": 2561
  },
  "Article 1 Hacksilber": {
    "sha": "237bd3335abdcc0f0465817dffe01ad6eaa86055",
    "bytes": 2345
  },
  "Article 2 Water Weight Computes": {
    "sha": "ec657c3fa0f70da9686fb1ae52983d28f77c6c4c",
    "bytes": 2535
  },
  "The Color Dyed and Dental Records": {
    "sha": "b525ad60ab37cb2d72ea43c40ba687b0fe2a348d",
    "bytes": 2974
  },
  "Article 5": {
    "sha": "c8c1bf617c0d81389f6c2408ed975131695857ff",
    "bytes": 3969
  },
  "Article 6": {
    "sha": "662d745f0b9b41236d1053cdbaa9351f7c020dd0",
    "bytes": 3210
  },
  "Article 10": {
    "sha": "e82be564872f636662652d34dcb8d3437559f84f",
    "bytes": 812
  },
  "Collective information": {
    "sha": "710ad3cd4feeae7bafa329d7437a78df4c40cfa8",
    "bytes": 33708
  }
});
function auditClaimQueue(d) {
  const errors = [];
  const fail = (message) => errors.push(message);
  if (!d || typeof d !== "object" || Array.isArray(d))
    return {integrity:"FAIL",release:"HOLD",errors:["root:not-object"]};
  if (d.project !== "F-001") fail("project:mismatch");
  if (d.source_commit !== "d46456a18fe412398d0ae37ec5a8c4eebb44e0c9") fail("source:commit-mismatch");
  if (d.shared_scanner_blob !== "31f3dcff486c4c8cc96d514eb425da86834d00c3") fail("scanner:blob-mismatch");
  if (d.status !== "HOLD" || d.release_authorized !== false || d.claim_truth_verified !== false)
    fail("release:must-remain-HOLD");
  const sha = s => typeof s === "string" && /^[a-f0-9]{40}$/.test(s);
  const sources = Array.isArray(d.sources) ? d.sources : [];
  if (sources.length !== 8) fail("sources:expected-eight");
  const sourceMap = new Map();
  for (const s of sources) {
    if (!s || typeof s.file !== "string" || !sha(s.blob_sha) ||
        !Number.isInteger(s.bytes) || s.bytes <= 0 ||
        !Number.isInteger(s.sentences) || s.sentences < 1) {
      fail("source:invalid-record"); continue;
    }
    if (sourceMap.has(s.file)) fail("source:duplicate:"+s.file);
    const pin = PINNED_SOURCES[s.file];
    if (!pin || s.blob_sha !== pin.sha || s.bytes !== pin.bytes)
      fail("source:pin-mismatch:"+s.file);
    sourceMap.set(s.file,s);
  }
  const baseline = Array.isArray(d.baseline) ? d.baseline : [];
  const supplemental = Array.isArray(d.supplemental) ? d.supplemental : [];
  if (baseline.length !== 42 || d.baseline_candidates !== 42) fail("baseline:expected-42");
  if (supplemental.length !== 3 || d.supplemental_unflagged_candidates !== 3) fail("supplemental:expected-3");
  if (d.combined_review_queue !== 45) fail("queue:expected-45");
  const seen = new Set(), counts = new Map(), triggerCounts = {};
  let reviewed = 0;
  for (const [kind, entries] of [["baseline",baseline],["supplemental",supplemental]]) {
    for (const c of entries) {
      if (!c || typeof c.file !== "string" || !Number.isInteger(c.sentence_no) ||
          c.sentence_no < 1 || typeof c.id !== "string") {fail(kind+":invalid-record"); continue;}
      const source = sourceMap.get(c.file);
      if (!source) {fail("claim:unknown-source:"+c.file);continue;}
      if (c.sentence_no > source.sentences) fail("claim:sentence-out-of-range:"+c.id);
      if (c.id !== c.file+"#S"+c.sentence_no) fail("claim:id-mismatch:"+c.id);
      if (seen.has(c.id)) fail("claim:duplicate:"+c.id);
      seen.add(c.id);
      if (c.source_blob_sha !== source.blob_sha) fail("claim:stale-source:"+c.id);
      if (typeof c.excerpt !== "string" || !c.excerpt.trim()) fail("claim:empty-excerpt:"+c.id);
      if (c.review_status !== "UNREVIEWED") {
        reviewed++;
        fail("claim:non-pinned-review-status:"+c.id);
        if (!c.review_evidence || typeof c.review_evidence !== "string" ||
            !c.review_evidence.trim()) fail("claim:review-without-evidence:"+c.id);
      }
      const key = kind+":"+c.file;
      counts.set(key,(counts.get(key)||0)+1);
      if (kind === "baseline") {
        if (!Array.isArray(c.triggers) || c.triggers.length === 0)
          fail("claim:missing-triggers:"+c.id);
        else for (const t of c.triggers) {
          if (!["certainty","percent","accuracy","superlative"].includes(t))
            fail("claim:unknown-trigger:"+c.id);
          triggerCounts[t]=(triggerCounts[t]||0)+1;
        }
      } else if (typeof c.extra_trigger !== "string" || !c.extra_trigger.trim()) {
        fail("claim:missing-extra-trigger:"+c.id);
      }
    }
  }
  for (const file of Object.keys(PINNED_SOURCES))
    if (!sourceMap.has(file)) fail("source:missing-pin:"+file);
  for (const s of sources) if (s && typeof s.file === "string") {
    if (counts.get("baseline:"+s.file)!==s.baseline_candidates) fail("source:baseline-count:"+s.file);
    if ((counts.get("supplemental:"+s.file)||0)!==s.supplemental_candidates) fail("source:supplemental-count:"+s.file);
  }
  for (const k of ["certainty","percent","accuracy","superlative"])
    if ((triggerCounts[k]||0)!==(d.trigger_counts||{})[k]) fail("trigger:count:"+k);
  if (reviewed!==d.reviewed_count) fail("reviewed:count-mismatch");
  if (seen.size !== 45) fail("queue:unique-count");
  return {integrity:errors.length?"FAIL":"PASS",release:"HOLD",
    project:"F-001",sources:sourceMap.size,baseline:baseline.length,
    supplemental:supplemental.length,unique:seen.size,reviewed,errors};
}
if (typeof module !== "undefined" && module.exports) {
  module.exports = {auditClaimQueue};
  if (require.main === module) {
    const fs = require("fs");
    if (process.argv.length !== 3) {console.error("Usage: node f001_claim_queue_gate_381.js inventory.json");process.exit(2);}
    const result = auditClaimQueue(JSON.parse(fs.readFileSync(process.argv[2],"utf8")));
    console.log(JSON.stringify(result,null,2));
    if (result.integrity !== "PASS") process.exitCode = 2;
  }
}
