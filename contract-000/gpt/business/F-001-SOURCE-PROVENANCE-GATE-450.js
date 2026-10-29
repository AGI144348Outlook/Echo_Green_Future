"use strict";
/** F-001 Article 1: offline, fail-closed *metadata* gate for six alleged excavation masses.
 * A PASS means a reviewer has supplied a complete traceable source packet, NOT that
 * the historical measurements are genuine. No network access, editing, or release.
 */
function validateProvenance(packet) {
  const errors = [];
  const nonblank = x => typeof x === "string" && x.trim().length > 0;
  const fail = (code,where) => errors.push(where ? code+" @ "+where : code);
  if (!packet || typeof packet !== "object" || Array.isArray(packet)) {
    return {metadata_complete:false,errors:["packet-object-required"],release_status:"HOLD"};
  }
  if (packet.claim_type !== "historical_item_mass") fail("claim-type");
  if (!nonblank(packet.derived_source_id)) fail("derived-source-id");
  const rows = Array.isArray(packet.rows) ? packet.rows : [];
  if (rows.length !== 6) fail("six-rows-required");
  const sources = Array.isArray(packet.sources) ? packet.sources : [];
  const sourceMap = new Map();
  for (const s of sources) {
    if (!s || !nonblank(s.id)) { fail("source-id"); continue; }
    if (sourceMap.has(s.id)) fail("duplicate-source-id",s.id);
    sourceMap.set(s.id,s);
    if (s.id === packet.derived_source_id || s.independent_of_derived !== true) fail("not-independent",s.id);
    if (!["excavation_inventory","peer_reviewed_item_catalogue"].includes(s.kind)) fail("not-itemized-source",s.id);
    if (s.access_status !== "full_text_checked") fail("source-not-read-in-full",s.id);
    if (!nonblank(s.url) || !/^https:\/\//.test(s.url)) fail("source-url",s.id);
    if (!Number.isInteger(s.year) || s.year < 1800 || s.year > 2100) fail("source-year",s.id);
  }
  const seen = new Set();
  for (let i=0;i<rows.length;i++) {
    const x=rows[i],where="row-"+(i+1);
    if (!x || typeof x !== "object") {fail("row-object",where);continue;}
    if (!nonblank(x.dataset_label)) fail("dataset-label",where);
    if (!Number.isFinite(x.dataset_mass_g) || x.dataset_mass_g<=0) fail("dataset-mass",where);
    if (!Number.isFinite(x.published_mass_g) || x.published_mass_g<=0) fail("published-mass",where);
    if (Number.isFinite(x.dataset_mass_g) && Number.isFinite(x.published_mass_g) &&
        Math.abs(x.dataset_mass_g-x.published_mass_g)>0.01+1e-9) fail("mass-disagreement",where);
    if (!nonblank(x.publication_id) || !sourceMap.has(x.publication_id)) fail("unknown-source",where);
    if (!nonblank(x.locator) || !/^(table|page|p\.|catalogue|inventory|figure)\b/i.test(x.locator))
      fail("itemized-locator-required",where);
    if (!Array.isArray(x.object_ids) || x.object_ids.length===0 || x.object_ids.some(v=>!nonblank(v)))
      fail("object-id-required",where);
    else for (const id of x.object_ids) {
      const key=x.publication_id+":"+id;
      if (seen.has(key)) fail("duplicate-object-id",where);
      seen.add(key);
    }
    if (x.measurement_basis === "aggregate" && (!Array.isArray(x.object_ids) || x.object_ids.length<2 ||
        !nonblank(x.aggregation_rule))) fail("aggregate-method-required",where);
    if (!["single","aggregate"].includes(x.measurement_basis)) fail("measurement-basis",where);
  }
  return {metadata_complete:errors.length===0,errors,release_status:"HOLD",
          interpretation:"Completeness is not verification of historical truth; human/source review required."};
}
if (typeof module !== "undefined") module.exports={validateProvenance};
