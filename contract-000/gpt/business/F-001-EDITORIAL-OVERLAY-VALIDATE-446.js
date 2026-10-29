#!/usr/bin/env node
"use strict";
/* F-001 Run446 draft editorial-overlay validator. No approval, fact check or rights clearance. */
function validateOverlay(o,q,r,p) {
  const errors=[],check=(v,m)=>{if(!v)errors.push(m)},object=x=>x!==null&&typeof x==="object"&&!Array.isArray(x);
  const fields=(x,allowed,label)=>{if(object(x))for(const k of Object.keys(x))if(!allowed.includes(k))errors.push(label+" unexpected field "+k)};
  const canon=x=>Array.isArray(x)?[...x].sort().join("\u0000"):"";
  if(![o,q,r,p].every(object))return ["invalid or missing JSON object"];
  fields(o,["schema","project","source_commit","queue_blob","reconciliation_blob","queue_occurrences","queue_distinct_texts","review_state","final_approvals","release_authorized","decision_links","annex","notes"],"overlay");
  check(o.schema==="f001-editorial-overlay-v1","overlay schema");
  check([o.project,q.project,r.project].every(x=>x==="F-001"),"F-001 project identity");
  check(o.source_commit==="d46456a18fe412398d0ae37ec5a8c4eebb44e0c9"&&q.source_commit===o.source_commit&&r.source_commit===o.source_commit,"source commit");
  check(o.queue_blob==="ab5e755c1d1f33fd2c9fd3af2866bc68ab1a4b16"&&p.queueSha===o.queue_blob,"queue Git blob");
  check(o.reconciliation_blob==="a297349de4b0cac905f626e6ecf997676efd3e00"&&p.reconSha===o.reconciliation_blob,"reconciliation Git blob");
  check(r.queue_git_blob===o.queue_blob.slice(0,7),"reconciliation queue reference");
  check(q.status==="HOLD / NOT LAUNCH-READY"&&r.status==="HOLD / NOT LAUNCH-READY"&&q.release_authorized===false,"queue HOLD");
  check(o.release_authorized===false&&o.final_approvals===0&&o.review_state==="UNREVIEWED","overlay unapproved");
  check(q.total_occurrences===82&&q.baseline_count===45&&q.supplemental_occurrence_count===37&&q.distinct_source_ids===82,"queue counts");
  check(r.existing_occurrences===82&&r.existing_distinct_ids===82&&r.existing_distinct_texts===72&&r.exact_duplicate_pairs===10,"reconciliation counts");
  check(o.queue_occurrences===82&&o.queue_distinct_texts===72,"overlay counts");
  const baseline=Array.isArray(q.baseline_ids)?q.baseline_ids:[],supp=Array.isArray(q.supplemental_refs)?q.supplemental_refs:[],ids=[...baseline,...supp.map(x=>x.id)],known=new Set(ids);
  check(baseline.length===45&&supp.length===37&&known.size===82,"queue unique occurrence IDs");
  check(Array.isArray(q.source_id_overlaps)&&q.source_id_overlaps.length===0,"queue overlap list");
  const b=Array.isArray(r.baseline_ungrouped_pairs)?r.baseline_ungrouped_pairs:[],s=Array.isArray(r.supplemental_grouped_pairs)?r.supplemental_grouped_pairs:[];
  check(b.length===7&&s.length===3,"seven baseline plus three supplemental pairs");
  const expected=new Map([...b.map((v,i)=>["B"+String(i+1).padStart(2,"0"),{ids:v.ids,origin:"baseline"}]),...s.map(v=>[v.group_id,{ids:v.ids,origin:"supplemental"}])]);
  const links=Array.isArray(o.decision_links)?o.decision_links:[],seen=new Set(),groups=new Set();
  check(links.length===10,"ten linked groups");
  for(const link of links){
    if(!object(link)){errors.push("invalid group object");continue}
    fields(link,["group","ids","origin","editorial_state","final"],"group");
    check(typeof link.group==="string"&&!groups.has(link.group),"unique group");
    groups.add(link.group);
    const e=expected.get(link.group);
    check(!!e&&canon(link.ids)===canon(e.ids),"source-bound exact pair "+link.group);
    check(!!e&&link.origin===e.origin,"source-bound origin "+link.group);
    check(link.editorial_state==="UNREVIEWED"&&link.final===false,"unapproved group "+link.group);
    check(Array.isArray(link.ids)&&link.ids.length===2&&new Set(link.ids).size===2,"two IDs "+link.group);
    for(const id of Array.isArray(link.ids)?link.ids:[]){
      check(known.has(id),"known ID "+id);check(!seen.has(id),"unique membership "+id);seen.add(id);
      if(link.origin==="supplemental")check(supp.some(x=>x.id===id&&x.group_id===link.group),"supplemental source group "+id);
    }
  }
  check([...expected.keys()].every(x=>groups.has(x)),"all reconciled pairs present");
  const a=o.annex,m=r.missing_article10;
  check(object(a)&&object(m),"annex exists");
  if(object(a)&&object(m)){
    fields(a,["ids","source_sentence","proposed_state","editorial_state","final","not_in_baseline"],"annex");
    check(Array.isArray(a.ids)&&a.ids.length===2&&canon(a.ids)===canon(m.ids),"annex IDs");
    check(a.ids?.every(x=>!known.has(x)),"annex outside 82-ID queue");
    check(a.source_sentence===m.sentence,"annex exact sentence");
    check(a.not_in_baseline===true&&m.in_existing_queue===false&&m.proposed_annex_only===true,"annex separate");
    check(a.proposed_state==="EVIDENCE_NEEDED"&&a.editorial_state==="UNREVIEWED"&&a.final===false,"annex unapproved");
  }
  return errors;
}
if (typeof module!=="undefined") module.exports={validateOverlay};
if (typeof require!=="undefined" && require.main===module) {
  const fs=require("fs"),crypto=require("crypto");
  const gitSha=buf=>crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+buf.length),Buffer.from([0]),buf])).digest("hex");
  if(process.argv.length!==5){console.error("Usage: node F-001-EDITORIAL-OVERLAY-VALIDATE-446.js OVERLAY.json QUEUE.json RECONCILIATION.json");process.exit(2)}
  try {
    const read=p=>{const bytes=fs.readFileSync(p);return {json:JSON.parse(bytes.toString("utf8")),sha:gitSha(bytes)}};
    const o=read(process.argv[2]),q=read(process.argv[3]),r=read(process.argv[4]);
    const failures=validateOverlay(o.json,q.json,r.json,{queueSha:q.sha,reconSha:r.sha});
    if(failures.length){console.error("FAIL / HOLD: "+failures.join("; "));process.exitCode=1}
    else console.log("PASS: pinned editorial-overlay consistency only; F-001 remains HOLD, UNREVIEWED, NOT LAUNCH-READY");
  } catch(e) {console.error("FAIL / HOLD: "+e.message);process.exitCode=1}
}
