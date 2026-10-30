#!/usr/bin/env node
"use strict";
/* Reproducible HOLD-only adversarial coverage test. Usage:
 * node test_f001_coverage_455.js F-001-CROSS-QUEUE-407.json
 * Test preregistration: Echo_Green_Future Issue #136.
 */
const fs = require("fs");
const {audit} = require("./F-001-EDITORIAL-COVERAGE-GATE-455.js");
if (process.argv.length !== 3) { console.error("Expected pinned queue JSON path"); process.exit(2); }
const source = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const copy = () => JSON.parse(JSON.stringify(source));
let passed = 0;
function check(label, mutate, accept) {
  const x = copy(); if (mutate) mutate(x);
  let accepted = true;
  try { audit(x); } catch (_) { accepted = false; }
  const ok = accepted === accept;
  console.log((ok ? "PASS" : "FAIL") + " " + label);
  if (ok) passed++;
}
function replaceId(x, from, to) {
  const i = x.baseline_ids.indexOf(from);
  if (i >= 0) x.baseline_ids[i] = to;
  else { const r = x.supplemental_refs.find(z => z.id === from); if (!r) throw Error("missing test ID"); r.id = to; }
}
check("exact pinned queue", null, true);
check("tampered source commit", x => x.source_commit = "000000", false);
check("release authorization", x => x.release_authorized = true, false);
check("status promotion", x => x.status = "READY", false);
check("false final approval", x => x.final_approved_count = 1, false);
check("duplicate ID", x => x.baseline_ids[1] = x.baseline_ids[0], false);
check("missing ID", x => x.baseline_ids.pop(), false);
check("wrong declared total", x => x.total_occurrences = 83, false);
check("wrong project", x => x.project = "F-002", false);
check("mutated pending ID", x => replaceId(x, "Collective information#S126", "Collective information#S9999"), false);
check("mutated reviewed ID", x => replaceId(x, "Collective information#S68", "Collective information#S9998"), false);
check("changed supplemental ordering", x => x.supplemental_refs.reverse(), false);
console.log(passed + "/12 passed");
if (passed !== 12) process.exit(1);
