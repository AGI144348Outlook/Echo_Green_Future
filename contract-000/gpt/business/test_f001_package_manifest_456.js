#!/usr/bin/env node
"use strict";
/* Run456 reproducible Node test harness; V8 audit function 17/17 run in pre/post
 * Issue #137. This Node CLI harness was COMMITTED BUT NOT RUN in Run456.
 */
const assert = require("node:assert/strict");
const {audit} = require("./F-001-PACKAGE-MANIFEST-GATE-456.js");
const good={schema:"f001-draft-package-manifest-v1",project:"F-001",source_commit:"d46456a18fe412398d0ae37ec5a8c4eebb44e0c9",status:"HOLD / NOT LAUNCH-READY",release_authorized:false,final_approved_count:0,editorial_total:82,claude_proposed:72,pending:10,rights_verified:false,archaeology_verified:false,independent_scanner_replayed:false,assets:[]};
const draft=(filename="dist/draft.pdf",sha256="a".repeat(64),state="UNVERIFIED_DRAFT")=>({filename,sha256,state});
const cases=[
["valid blocked manifest",m=>{},true],
["wrong project",m=>{m.project="F-002"}],
["wrong source",m=>{m.source_commit="0".repeat(40)}],
["false ready",m=>{m.status="LAUNCH-READY"}],
["release authorized",m=>{m.release_authorized=true}],
["final approvals forged",m=>{m.final_approved_count=82}],
["proposals inflated",m=>{m.claude_proposed=82}],
["rights asserted",m=>{m.rights_verified=true}],
["scanner asserted",m=>{m.independent_scanner_replayed=true}],
["unknown release key",m=>{m.release_ready=true}],
["missing assets",m=>{delete m.assets}],
["path traversal",m=>{m.assets=[draft("dist/../x.pdf")]}],
["external URL",m=>{m.assets=[draft("https://x.test/file.pdf")]}],
["duplicate case insensitive",m=>{m.assets=[draft("dist/x.pdf"),draft("dist/X.PDF","b".repeat(64))]}],
["invalid digest",m=>{m.assets=[draft("dist/x.pdf","not-a-hash")]}],
["verified asset spoof",m=>{m.assets=[draft("dist/x.pdf","a".repeat(64),"VERIFIED")]}],
["valid unverified artifact",m=>{m.assets=[draft()]},true]
];
let count=0;
for(const [name,change,accept] of cases){
 const m=JSON.parse(JSON.stringify(good));change(m);
 if(accept){const r=audit(m);assert.equal(r.status,"HOLD / NOT LAUNCH-READY",name);assert.equal(r.assets_byte_verified,0,name);}
 else assert.throws(()=>audit(m),/F-001 HOLD:/,name);
 count++;
}
console.log(count+"/"+cases.length+" PASS (synthetic manifest policy only; no real asset bytes)");
