#!/usr/bin/env node
// F-001 source-pinned HOLD-only 82-occurrence handoff; prospective PRE Issue #90.
// Usage: node f001_review_handoff_417.js CROSS-QUEUE.json EDITORIAL-QUEUE.json EXACT-GROUP.json P1-PACKET.json > manifest.json
// Does not edit any input, authorize release, or adjudicate claims.
const fs=require('node:fs');
function build(a,q,g,p) {
  function check(ok,msg){if(!ok)throw Error(msg)}
  check(a.project==="F-001"&&q.project==="F-001"&&g.project==="F-001"&&p.project==="F-001","project mismatch");
  check([q,g,p].every(x=>x.source_commit===a.source_commit),"source commit mismatch");
  check(a.release_authorized===false&&q.release_authorized===false&&g.release_authorized===false&&p.release_authorized===false,"upstream release flag");
  check(a.baseline_count===45&&a.supplemental_occurrence_count===37&&a.supplemental_group_count===34&&a.total_occurrences===82,"audit count mismatch");
  check(q.cards.length===45&&g.groups.length===34&&p.items.length===18,"source queue count mismatch");
  check(q.cards.every(c=>c.review_status==="UNREVIEWED"&&c.editorial_disposition===null&&c.rights_clearance===null),"baseline review state altered");
  check(g.groups.every(x=>x.human_review_status==="UNREVIEWED"&&x.editorial_disposition===null&&x.rights_clearance===null&&x.release_authorized===false),"supplemental review state altered");
  const p1=q.cards.filter(x=>x.review_priority==="P1").map(x=>x.id);
  check(p1.length===18&&JSON.stringify(p1.slice().sort())===JSON.stringify(p.items.map(x=>x.id).sort()),"P1 map mismatch");
  check(JSON.stringify(q.cards.map(x=>x.id))===JSON.stringify(a.baseline_ids),"baseline IDs/order mismatch");
  const supp=g.groups.flatMap(x=>x.source_refs.map(r=>({r,group:x})));
  check(supp.length===37&&new Set(g.groups.map(x=>x.group_id)).size===34,"supplemental group counts");
  const amap=new Map(a.supplemental_refs.map(x=>[x.id,x]));
  check(amap.size===37&&supp.every(({r,group})=>{const x=amap.get(r.id);return x&&x.group_id===group.group_id&&x.blob_sha===r.blob_sha&&x.file===r.file&&x.sentence_no===r.sentence_no;}),"supplemental refs mismatch");
  const rows=q.cards.map(c=>({
    queue:"baseline",id:c.id,file:c.source_file,sentence_no:c.sentence_no,source_blob_sha:c.source_blob_sha,
    source_commit:a.source_commit,group_id:null,review_priority:c.review_priority,source_excerpt:c.excerpt,
    excerpt_is_full_sentence:false,review_status:"UNREVIEWED",editorial_disposition:null,evidence_ref:null,
    rights_clearance:null,reviewer:null,release_authorized:false
  })).concat(supp.map(({r,group})=>({
    queue:"supplemental",id:r.id,file:r.file,sentence_no:r.sentence_no,source_blob_sha:r.blob_sha,
    source_commit:a.source_commit,group_id:group.group_id,review_priority:null,source_excerpt:group.full_sentence,
    excerpt_is_full_sentence:true,review_status:"UNREVIEWED",editorial_disposition:null,evidence_ref:null,
    rights_clearance:null,reviewer:null,release_authorized:false
  })));
  const ids=rows.map(x=>x.id);
  check(ids.length===82&&new Set(ids).size===82,"duplicate occurrence IDs");
  check(a.source_id_overlaps.length===0&&a.exact_text_overlaps.length===0,"audit overlap mismatch");
  check(rows.every(x=>x.id===x.file+"#S"+x.sentence_no&&/^[a-f0-9]{40}$/.test(x.source_blob_sha)),"invalid source binding");
  return {
    format:"f001-hold-review-handoff-v1",project:"F-001",source_commit:a.source_commit,
    upstream_blobs:{cross_queue:"fd0bdc8a3870a21a5987112dbc8b0fdf1b1ecfbb",baseline:"3346ad7583225d82ddf435f8daf691c78aca7330",supplemental:"32dfe75589a031de46c28145fe993122ee2ca0f2",p1:"a999d151a212369d52d0070397b9fea13e39a129"},
    status:"HOLD / NOT LAUNCH-READY",release_authorized:false,human_reviewed_count:0,
    baseline_count:45,baseline_p1_count:18,supplemental_count:37,supplemental_group_count:34,total_occurrences:82,
    note:"Draft handoff only. Baseline excerpt may be truncated; verify original source. Supplemental sentence is group text, not independent evidence. Human review, rights, real scanner, final EPUB/PDF and Timothy authorization remain outstanding.",
    rows
  };
}
function validate(a,q,g,p,m) {
  const canonical=build(a,q,g,p);
  if(JSON.stringify(m)!==JSON.stringify(canonical))throw Error("manifest differs from source-pinned canonical HOLD handoff");
  return {rows:m.rows.length,baseline:m.rows.filter(x=>x.queue==="baseline").length,
    supplemental:m.rows.filter(x=>x.queue==="supplemental").length,
    p1:m.rows.filter(x=>x.review_priority==="P1").length,
    groups:new Set(m.rows.filter(x=>x.queue==="supplemental").map(x=>x.group_id)).size,
    reviewed:m.rows.filter(x=>x.review_status!=="UNREVIEWED").length,release_authorized:m.release_authorized};
}
if(require.main===module){
  if(process.argv.length!==6){console.error('Usage: node f001_review_handoff_417.js <cross-queue> <baseline-queue> <supplemental-groups> <p1-packet>');process.exit(2);}
  try{const [a,q,g,p]=process.argv.slice(2).map(x=>JSON.parse(fs.readFileSync(x,'utf8')));const m=build(a,q,g,p);validate(a,q,g,p,m);console.log(JSON.stringify(m,null,2));}
  catch(e){console.error('FAIL/HOLD: '+e.message);process.exit(1);}
}
module.exports={build,validate};
