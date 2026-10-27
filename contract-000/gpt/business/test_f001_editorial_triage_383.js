"use strict";
const fs=require("fs");
const assert=require("assert");
const {buildQueue}=require("./f001_editorial_triage_383.js");
if(process.argv.length!==3)throw Error("usage: node test_f001_editorial_triage_383.js F-001-REAL-CLAIMS-378.json");
const raw=fs.readFileSync(process.argv[2],"utf8"),input=JSON.parse(raw);
const result=buildQueue(input);
const cases=[];
function test(name,fn){fn();cases.push(name);}
test("45 candidates",()=>assert.strictEqual(result.card_count,45));
test("8 sources",()=>assert.strictEqual(Object.keys(result.source_counts).length,8));
test("42 baseline",()=>assert.strictEqual(result.cards.filter(x=>x.detection_group==="baseline").length,42));
test("3 supplemental",()=>assert.strictEqual(result.cards.filter(x=>x.detection_group==="supplemental").length,3));
test("unique IDs",()=>assert.strictEqual(new Set(result.cards.map(x=>x.id)).size,45));
test("source pins preserved",()=>assert(result.cards.every(c=>c.source_blob_sha===input.sources.find(s=>s.file===c.source_file).blob_sha)));
test("excerpts preserved",()=>assert(result.cards.every(c=>[...input.baseline,...input.supplemental].find(x=>x.id===c.id).excerpt===c.excerpt)));
test("all unreviewed",()=>assert(result.cards.every(c=>c.review_status==="UNREVIEWED"&&c.editorial_disposition===null&&c.evidence_reference===null)));
test("hold",()=>assert.strictEqual(result.status,"HOLD"));
test("priorities",()=>assert(result.cards.every(c=>["P1","P2"].includes(c.review_priority))));
const negatives=[
["duplicate",x=>{x.supplemental[0]={...x.supplemental[0],...x.baseline[0]};}],
["source-sha",x=>{x.baseline[0].source_blob_sha="0".repeat(40);}],
["status",x=>{x.baseline[0].review_status="APPROVED";}],
["excerpt",x=>{x.baseline[0].excerpt="";}],
["sentence",x=>{x.baseline[0].sentence_no=999;}],
["release",x=>{x.release_authorized=true;}],
["source-count",x=>{x.sources.pop();}],
["claim-count",x=>{x.baseline.pop();}]
];
for(const [name,mutate] of negatives)test("reject "+name,()=>{
  const x=JSON.parse(raw);mutate(x);assert.throws(()=>buildQueue(x));
});
console.log("F-001 Run383 editorial triage: "+cases.length+"/"+cases.length+" checks PASS");
