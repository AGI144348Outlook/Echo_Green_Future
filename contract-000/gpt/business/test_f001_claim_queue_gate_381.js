#!/usr/bin/env node
"use strict";
/* Run 381 reproducible checks: node test_f001_claim_queue_gate_381.js F-001-REAL-CLAIMS-378.json
   Requires the committed inventory in the same directory. Read-only. */
const fs = require("fs");
const assert = require("assert");
const {auditClaimQueue} = require("./f001_claim_queue_gate_381.js");
if (process.argv.length !== 3) throw new Error("expected pinned inventory JSON path");
const original = JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
const clone = () => JSON.parse(JSON.stringify(original));
const tests = [
 ["actual-pinned",d=>d,true],
 ["drop-claim",d=>{d.baseline.pop();return d;},false],
 ["duplicate-claim",d=>{d.supplemental[0]={...d.baseline[0]};return d;},false],
 ["stale-blob",d=>{d.baseline[0].source_blob_sha="0".repeat(40);return d;},false],
 ["forged-reviewed",d=>{d.baseline[0].review_status="CLAIMED";d.reviewed_count=1;return d;},false],
 ["missing-source",d=>{d.sources.pop();return d;},false],
 ["wrong-count",d=>{d.combined_review_queue=44;return d;},false],
 ["out-of-range",d=>{d.baseline[0].sentence_no=999;d.baseline[0].id=d.baseline[0].file+"#S999";return d;},false],
 ["tampered-trigger",d=>{d.baseline[0].triggers=["unknown"];return d;},false],
 ["release-authorized",d=>{d.release_authorized=true;return d;},false],
];
const results = tests.map(([name,change,expect])=>{
  const result = auditClaimQueue(change(clone()));
  const pass = (result.integrity === "PASS") === expect;
  assert(pass, name+" unexpected "+JSON.stringify(result));
  return {name,pass,integrity:result.integrity,errors:result.errors};
});
console.log(JSON.stringify({passed:results.length,total:tests.length,results},null,2));
