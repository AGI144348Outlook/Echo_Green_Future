"use strict";
/** Synthetic fixture harness for F-001-SOURCE-PROVENANCE-GATE-450.js.
 * Metadata tests only; synthetic citations never assert real archaeological evidence.
 * Usage (Node): node test_f001_source_gate_450.js
 */
function runTests(validateProvenance) {
  const masses=[136.98,68.52,13.71,6.86,3.42,1.71];
  const original={
    claim_type:"historical_item_mass",derived_source_id:"TAM-DATASET-A",
    sources:[{id:"SYNTHETIC-INVENTORY",independent_of_derived:true,
      kind:"excavation_inventory",access_status:"full_text_checked",
      url:"https://example.org/synthetic-fixture",year:2000}],
    rows:masses.map((m,i)=>({dataset_label:"synthetic-row-"+(i+1),
      dataset_mass_g:m,published_mass_g:m,publication_id:"SYNTHETIC-INVENTORY",
      locator:"Table 1 row "+(i+1),object_ids:["SYNTHETIC-OBJECT-"+(i+1)],
      measurement_basis:"single"}))
  };
  const clone=()=>JSON.parse(JSON.stringify(original));
  const cases=[
    ["complete synthetic metadata",true,clone()],
    ["missing item locator",false,(()=>{const x=clone();x.rows[0].locator="";return x;})()],
    ["same source as derived",false,(()=>{const x=clone();x.sources[0].id="TAM-DATASET-A";x.rows.forEach(r=>r.publication_id="TAM-DATASET-A");return x;})()],
    ["overview is not inventory",false,(()=>{const x=clone();x.sources[0].kind="hoard_overview";return x;})()],
    ["five rows",false,(()=>{const x=clone();x.rows.pop();return x;})()],
    ["abstract only",false,(()=>{const x=clone();x.sources[0].access_status="abstract_only";return x;})()],
    ["mass discrepancy",false,(()=>{const x=clone();x.rows[2].published_mass_g=14.1;return x;})()],
    ["duplicate artifact",false,(()=>{const x=clone();x.rows[1].object_ids=["SYNTHETIC-OBJECT-1"];return x;})()],
    ["aggregate lacks method",false,(()=>{const x=clone();x.rows[2].measurement_basis="aggregate";x.rows[2].object_ids=["SYNTHETIC-3a","SYNTHETIC-3b"];return x;})()],
    ["real TAM rows without primary item locators",false,{
      claim_type:"historical_item_mass",derived_source_id:"TAM-DATASET-A",
      sources:[],rows:masses.map((m,i)=>({dataset_label:"TAM-row-"+(i+1),dataset_mass_g:m}))}]
  ];
  const results=cases.map(([name,expected,packet])=>{
    const actual=validateProvenance(packet);
    return {name,expected,actual:actual.metadata_complete,
      hold:actual.release_status==="HOLD",errors:actual.errors,
      pass:actual.metadata_complete===expected&&actual.release_status==="HOLD"};
  });
  return {passed:results.filter(x=>x.pass).length,total:results.length,results};
}
if (typeof module!=="undefined") {
  module.exports={runTests};
  if (typeof require!=="undefined" && require.main===module) {
    const gate=require("./F-001-SOURCE-PROVENANCE-GATE-450.js");
    const r=runTests(gate.validateProvenance);
    for (const t of r.results) console.log((t.pass?"PASS ":"FAIL ")+t.name);
    console.log(r.passed+"/"+r.total);
    if (r.passed!==r.total) process.exitCode=1;
  }
}
