#!/usr/bin/env node
"use strict";
/* Run382 real-source F-001 regression runner. Requires a separate checkout
   of AGI144348Outlook/The-TAM-protocol pinned to d46456a18fe412398d0ae37ec5a8c4eebb44e0c9.
   Run: node test_f001_real_source_binding_382.js <tam-dir> <F-001-REAL-CLAIMS-378.json>
   No writes; negative controls are in memory only. */
const fs=require("fs");
const {audit,loadSources}=require("./f001_real_source_binding_382.js");
if(process.argv.length!==4) throw Error("usage: node test_f001_real_source_binding_382.js <tam-dir> <inventory.json>");
const inventory=JSON.parse(fs.readFileSync(process.argv[3],"utf8"));
const sources=loadSources(process.argv[2]);
const clone=x=>JSON.parse(JSON.stringify(x));
let pass=0,total=0;
function check(label,inv,src,expected) {
  total++;
  const got=audit(inv,src);
  if(got.ok===expected) pass++;
  else console.error("FAIL",label,got.errors);
}
check("actual",inventory,sources,true);
let x=clone(inventory);x.baseline[0].excerpt="wrong excerpt";check("excerpt",x,sources,false);
x=clone(inventory);x.baseline[0].sentence_no=100000;check("index",x,sources,false);
x=clone(inventory);x.baseline[0].id="README.md#S1";check("id",x,sources,false);
x=clone(inventory);x.baseline.push(clone(x.baseline[0]));x.baseline_candidates++;x.combined_review_queue++;x.sources[0].baseline_candidates++;check("duplicate",x,sources,false);
x=clone(inventory);x.baseline[0].review_status="APPROVED";check("status",x,sources,false);
x=clone(inventory);x.sources[0].blob_sha="0".repeat(40);check("metadata",x,sources,false);
let s=clone(sources);s["README.md"].text="x"+s["README.md"].text;check("bytes",inventory,s,false);
s=clone(sources);delete s["README.md"];check("missing",inventory,s,false);
s=clone(sources);s["README.md"].sha="f".repeat(40);check("SHA",inventory,s,false);
console.log(JSON.stringify({passed:pass,total,release:"HOLD"}));
if(pass!==total) process.exitCode=1;
