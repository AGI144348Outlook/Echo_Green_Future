#!/usr/bin/env node
/** F-001 Run 360 structural preflight ONLY; never release approval.
 * Usage: node F-001-SCHEMA-CROSSWALK-360.js dataset-a.csv dataset-b.csv dataset-check.json
 * Does not verify SHA-256, git checkout cleanliness, stage bytes, rights, EPUB/PDF or publication.
 * PRE-TEST: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6405917004
 */
const fs = require("node:fs");
function preflight(csvA,csvB,report){
  const errors=[];
  const expected={
    a:"object,measured_g,units,registry_sign,stated_deviation_pct,term,expected_g,recomputed_deviation_pct,within_0_01_pct_points_of_recomputed,calculation_method_from_source,terminology_conflict",
    b:"ratio,mass_g,registry_sign,units,relation_to_dataset_a,expected_g_from_units,deviation_pct,ratio_over_16_equals_units,terminology_conflict"
  };
  const source="d46456a18fe412398d0ae37ec5a8c4eebb44e0c9";
  const blobs={A:"b62c970a660e0a6685b58db1ef121690daa4fce7",B:"12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4"};
  const head=s=>s.split(/\r?\n/,1)[0];
  if(head(csvA)!==expected.a)errors.push("A_HEADER_NOT_334");
  if(head(csvB)!==expected.b)errors.push("B_HEADER_NOT_334");
  if(report.source_commit!==source)errors.push("SOURCE_COMMIT_NOT_ATTESTED");
  for(const [key,count] of [["A",6],["B",8]]){
    const record=report.files?.[key];
    if(record?.git_blob!==blobs[key])errors.push(key+"_SOURCE_BLOB_NOT_ATTESTED");
    if(record?.rows!==count||!Array.isArray(record?.rejected)||record.rejected.length!==0)errors.push(key+"_ROWS_OR_REJECTS_INVALID");
  }
  return {compatible:errors.length===0,errors};
}
if (require.main === module) {
 if (process.argv.length !== 5) { console.error("usage: node ... A.csv B.csv dataset-check.json"); process.exit(2); }
 try { const [a,b,j] = process.argv.slice(2); const report=JSON.parse(fs.readFileSync(j,"utf8"));
 const result=preflight(fs.readFileSync(a,"utf8"),fs.readFileSync(b,"utf8"),report);
 console.log(JSON.stringify({project:"F-001",release:"HOLD",publication_authorized:false,structural_only:true,...result}));
 process.exit(result.compatible?0:1);
 } catch(e) { console.error(String(e)); process.exit(2); }
}
module.exports={preflight};
