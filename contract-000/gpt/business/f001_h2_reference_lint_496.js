#!/usr/bin/env node
// F-001 H2 DRAFT: evidence-reference lint only. NEVER grants copyright clearance.
// Usage: node f001_h2_reference_lint_496.js manifest.json decisions.json evidence.json
// No tests were executed when this draft was committed.
'use strict';
const fs = require('node:fs');
function fail(s){ throw new Error(s); }
function readJson(p){return JSON.parse(fs.readFileSync(p,'utf8'));}
function unique(a){return new Set(a).size===a.length;}
function lint(manifest, decisions, evidence){
  if(!Array.isArray(manifest)||manifest.length!==69||!manifest.every(x=>typeof x==='string'&&x.trim())||!unique(manifest))fail('expected 69 unique nonempty manifest identifiers');
  if(!Array.isArray(decisions)||decisions.length!==69)fail('expected 69 decisions');
  if(!Array.isArray(evidence))fail('evidence registry must be an array');
  const refs=new Map();
  for(const e of evidence){
    if(!e||typeof e.ref!=='string'||!e.ref.trim()||refs.has(e.ref))fail('invalid or duplicate evidence ref');
    refs.set(e.ref,e);
  }
  const ids=new Set(), allowed=new Set(['PENDING','LICENSED','PERMISSION_GRANTED','ORIGINAL','REWRITE','REMOVE']);
  let positive=0;
  for(const d of decisions){
    if(!d||typeof d.id!=='string'||ids.has(d.id)||!manifest.includes(d.id))fail('duplicate or unknown decision ID');
    ids.add(d.id);
    if(!allowed.has(d.classification))fail('invalid classification');
    if(['LICENSED','PERMISSION_GRANTED'].includes(d.classification)){
      positive++;
      for(const key of ['evidence_ref','reviewer_id','decision_date']){
        if(typeof d[key]!=='string'||!d[key].trim())fail('rights-positive row missing '+key);
      }
      if(!/^\d{4}-\d{2}-\d{2}$/.test(d.decision_date)||Number.isNaN(Date.parse(d.decision_date+'T00:00:00Z'))||new Date(d.decision_date+'T00:00:00Z').toISOString().slice(0,10)!==d.decision_date)fail('invalid ISO date');
      const e=refs.get(d.evidence_ref);
      if(!e||!e.document_sha256||!(/^[a-f0-9]{64}$/i.test(e.document_sha256))||!e.source_locator||!e.claimed_scope)fail('unresolved/incomplete evidence reference');
      // Presence of a reference and hash is NOT proof of authenticity, authority, license or scope.
    }
  }
  if(ids.size!==manifest.length)fail('missing manifest ID');
  return {structure:'PASS',evidence_reference:'FORMAT_ONLY',rights_clearance:'NOT_DETERMINED',release:'HOLD',rights_positive_claims:positive};
}
if(require.main===module){
  try{
    if(process.argv.length!==5)fail('expected manifest, decisions, evidence JSON paths');
    const result=lint(...process.argv.slice(2).map(readJson));
    console.log(JSON.stringify(result)); // even successful lint is NOT publication clearance
  }catch(e){console.error('H2 REJECT: '+e.message);process.exitCode=1;}
}
module.exports={lint};
