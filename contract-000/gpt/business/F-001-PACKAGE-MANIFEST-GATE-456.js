#!/usr/bin/env node
"use strict";
/* F-001 Run456: read-only HOLD-only draft package manifest validator.
 * Synthetic manifest policy checks only. Does NOT hash actual files, build
 * PDF/EPUB, approve rights, or authorize release. Source TAM d46456a.
 */
const audit = function audit(m) {
  const fail = reason => { throw new Error("F-001 HOLD: "+reason); };
  const required = ["schema","project","source_commit","status","release_authorized","final_approved_count","editorial_total","claude_proposed","pending","rights_verified","archaeology_verified","independent_scanner_replayed","assets"];
  if (!m || typeof m!=="object" || Array.isArray(m) || Object.keys(m).sort().join("|")!==required.slice().sort().join("|")) fail("manifest keys");
  if (m.schema!=="f001-draft-package-manifest-v1" || m.project!=="F-001" || m.source_commit!=="d46456a18fe412398d0ae37ec5a8c4eebb44e0c9") fail("source or project pin");
  if (m.status!=="HOLD / NOT LAUNCH-READY" || m.release_authorized!==false || m.final_approved_count!==0) fail("release or approval");
  if (m.editorial_total!==82 || m.claude_proposed!==72 || m.pending!==10) fail("editorial snapshot mismatch");
  if (m.rights_verified!==false || m.archaeology_verified!==false || m.independent_scanner_replayed!==false) fail("unsupported verification claim");
  if (!Array.isArray(m.assets) || m.assets.length>8) fail("invalid assets");
  const seen = new Set();
  for (const a of m.assets) {
    if (!a || typeof a!=="object" || Array.isArray(a) || Object.keys(a).sort().join("|")!=="filename|sha256|state") fail("asset fields");
    if (typeof a.filename!=="string" || !/^dist\/[a-z0-9][a-z0-9._-]{0,79}\.(?:epub|pdf)$/i.test(a.filename) || a.filename.includes("..")) fail("unsafe filename");
    const key=a.filename.toLowerCase();
    if (seen.has(key)) fail("duplicate filename");
    seen.add(key);
    if (typeof a.sha256!=="string" || !/^[a-f0-9]{64}$/.test(a.sha256)) fail("invalid sha256 syntax");
    if (a.state!=="UNVERIFIED_DRAFT") fail("unsupported asset state");
  }
  return {project:"F-001",status:"HOLD / NOT LAUNCH-READY",release_authorized:false,final_approved_count:0,assets_listed:m.assets.length,assets_byte_verified:0,limitation:"Manifest-only syntax and policy gate. No real artifact bytes, historical claims, source rights, or publication clearance verified."};
};
module.exports={audit};
if (require.main===module){const fs=require("fs");if(process.argv.length!==3){console.error("usage: node F-001-PACKAGE-MANIFEST-GATE-456.js manifest.json");process.exit(2)}try{console.log(JSON.stringify(audit(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2))}catch(e){console.error(String(e));process.exit(2)}}
