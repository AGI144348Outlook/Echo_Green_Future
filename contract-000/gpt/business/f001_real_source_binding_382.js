#!/usr/bin/env node
"use strict";
/* F-001 GPT read-only real-source claim binder, Run382.
   CLI: node f001_real_source_binding_382.js <tam-source-dir> <inventory.json>
   No writes, network, paid APIs, editorial approvals or release actions. */
const PINNED = Object.freeze({"README.md":{"sha":"213bcfaf560dcc54fbb7ae79fad932e86b660357","bytes":2561,"sentences":24},"Article 1 Hacksilber":{"sha":"237bd3335abdcc0f0465817dffe01ad6eaa86055","bytes":2345,"sentences":22},"Article 2 Water Weight Computes":{"sha":"ec657c3fa0f70da9686fb1ae52983d28f77c6c4c","bytes":2535,"sentences":41},"The Color Dyed and Dental Records":{"sha":"b525ad60ab37cb2d72ea43c40ba687b0fe2a348d","bytes":2974,"sentences":37},"Article 5":{"sha":"c8c1bf617c0d81389f6c2408ed975131695857ff","bytes":3969,"sentences":26},"Article 6":{"sha":"662d745f0b9b41236d1053cdbaa9351f7c020dd0","bytes":3210,"sentences":29},"Article 10":{"sha":"e82be564872f636662652d34dcb8d3437559f84f","bytes":812,"sentences":9},"Collective information":{"sha":"710ad3cd4feeae7bafa329d7437a78df4c40cfa8","bytes":33708,"sentences":299}});
function utf8Bytes(s) { return unescape(encodeURIComponent(s)).length; }
function splitSentences(text) {
  return text.split(/(?<=[.!?])\s+|\n{2,}/u).map(s=>s.trim()).filter(Boolean);
}
function audit(inventory, sources, pins=PINNED) {
  const errors=[], details=[], names=Object.keys(pins);
  if (!inventory || inventory.project!=="F-001" || inventory.status!=="HOLD" ||
      inventory.release_authorized!==false || inventory.reviewed_count!==0) errors.push("release/status mismatch");
  if (!Array.isArray(inventory?.sources) || !Array.isArray(inventory?.baseline) ||
      !Array.isArray(inventory?.supplemental)) return {ok:false,errors:["malformed inventory"],details:[]};
  if (inventory.sources.length!==names.length || Object.keys(sources).length!==names.length)
    errors.push("source set/count mismatch");
  const byName=new Map(inventory.sources.map(x=>[x.file,x]));
  if (byName.size!==inventory.sources.length) errors.push("duplicate inventory source");
  const all=[...inventory.baseline,...inventory.supplemental], seen=new Set();
  if (inventory.baseline.length!==inventory.baseline_candidates ||
      inventory.supplemental.length!==inventory.supplemental_unflagged_candidates ||
      all.length!==inventory.combined_review_queue) errors.push("claim totals mismatch");
  for (const name of names) {
    const p=pins[name], meta=byName.get(name), src=sources[name];
    if (!meta || !src || typeof src.text!=="string") {errors.push("missing source: "+name);continue;}
    if (meta.blob_sha!==p.sha || meta.bytes!==p.bytes || src.sha!==p.sha ||
        utf8Bytes(src.text)!==p.bytes) {errors.push("source pin mismatch: "+name);continue;}
    const sentences=splitSentences(src.text);
    if (sentences.length!==p.sentences || meta.sentences!==p.sentences) errors.push("sentence count: "+name);
    const candidates=all.filter(c=>c.file===name);
    if (candidates.filter(c=>inventory.baseline.includes(c)).length!==meta.baseline_candidates ||
        candidates.filter(c=>inventory.supplemental.includes(c)).length!==meta.supplemental_candidates)
      errors.push("per-file candidate count: "+name);
    for (const c of candidates) {
      const key=name+"#S"+c.sentence_no;
      if (seen.has(key)) errors.push("duplicate candidate: "+key);
      seen.add(key);
      if (c.id!==key || !Number.isInteger(c.sentence_no) || c.sentence_no<1 ||
          c.sentence_no>sentences.length) {errors.push("candidate index: "+c.id);continue;}
      if (c.source_blob_sha!==p.sha || c.review_status!=="UNREVIEWED" ||
          typeof c.excerpt!=="string" || c.excerpt.length<8 ||
          !sentences[c.sentence_no-1].startsWith(c.excerpt))
        errors.push("candidate text/status: "+c.id);
    }
    details.push({file:name,sentences:sentences.length,candidates:candidates.length,source_pin:p.sha});
  }
  for (const c of all) if (!pins[c.file]) errors.push("unexpected candidate source: "+c.file);
  return {ok:errors.length===0,errors,details,candidates:all.length,baseline:inventory.baseline.length,supplemental:inventory.supplemental.length,release:"HOLD"};
}
function loadSources(root,pins=PINNED) {
  const fs=require("fs"), path=require("path"), crypto=require("crypto"), out={};
  for(const name of Object.keys(pins)) {
    const p=path.join(path.resolve(root),name), st=fs.lstatSync(p);
    if (!st.isFile() || st.isSymbolicLink()) throw Error("nonregular source: "+name);
    const buf=fs.readFileSync(p);
    const sha=crypto.createHash("sha1").update("blob "+buf.length+"\0").update(buf).digest("hex");
    out[name]={text:buf.toString("utf8"),sha};
  }
  return out;
}
if (typeof module!=="undefined") module.exports={audit,loadSources,PINNED,splitSentences};
if (typeof require!=="undefined" && require.main===module) {
  try {
    if(process.argv.length!==4) throw Error("usage: node f001_real_source_binding_382.js <tam-source-dir> <inventory.json>");
    const data=JSON.parse(require("fs").readFileSync(process.argv[3],"utf8"));
    const result=audit(data,loadSources(process.argv[2]));
    process.stdout.write(JSON.stringify(result,null,2)+"\n");
    if(!result.ok) process.exitCode=1;
  } catch(e) {process.stderr.write(String(e.message||e)+"\n");process.exitCode=1;}
}
