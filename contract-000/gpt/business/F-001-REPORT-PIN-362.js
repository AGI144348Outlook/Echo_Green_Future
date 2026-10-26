"use strict";
// F-001 Run 362: HOLD-only cross-check of a Run-334-style source report.
// Source SHA-256 references: Run 358 independent TAM source-read report.
// NOT a replacement for pinned Git source verification, stage gate, or human rights/editorial approval.
const PINS = Object.freeze({
  commit:"d46456a18fe412398d0ae37ec5a8c4eebb44e0c9",
  A:{git_blob:"b62c970a660e0a6685b58db1ef121690daa4fce7",sha256:"48437f58ee74a9a0226d901d1291b6c104764648fe7760ebbc91b74b6ba6a302",rows:6},
  B:{git_blob:"12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4",sha256:"bc16da657b19317e110cdcf4159a9118aa89f2cfc4f8183e7f1d94f2eb3b81",rows:8}
});
function exactKeys(x,keys){return x!==null && typeof x==="object" && !Array.isArray(x) && Object.keys(x).length===keys.length && keys.every(k=>Object.prototype.hasOwnProperty.call(x,k));}
function validate(report){
  const errors=[];
  if(!exactKeys(report,["base_g_per_unit","source_commit","files"]))errors.push("REPORT_SHAPE");
  if(!report || typeof report!=="object" || Array.isArray(report))return {status:"HOLD",consistent:false,errors,scope:"source-report cross-check only"};
  if(report.base_g_per_unit!==13.7)errors.push("BASE_MISMATCH");
  if(report.source_commit!==PINS.commit)errors.push("SOURCE_COMMIT_MISMATCH");
  if(!exactKeys(report.files,["A","B"]))errors.push("FILES_SHAPE");
  for(const key of ["A","B"]){
    const rec=report.files && report.files[key];
    if(!exactKeys(rec,["sha256","git_blob","rows","rejected"])){errors.push(key+"_SHAPE");continue;}
    for(const field of ["sha256","git_blob","rows"]){
      if(rec[field]!==PINS[key][field])errors.push(key+"_"+field.toUpperCase()+"_MISMATCH");
    }
    if(!Array.isArray(rec.rejected)||rec.rejected.length!==0)errors.push(key+"_REJECTED");
  }
  return {status:"HOLD",consistent:errors.length===0,errors,scope:"pinned report-field consistency only; not a byte read, stage receipt, source attestation, rights check or release approval"};
}
if(typeof module!=="undefined")module.exports={validate,PINS};
if(typeof require!=="undefined" && typeof module!=="undefined" && require.main===module){
  const fs=require("node:fs");
  const path=process.argv[2];
  if(!path){console.error("usage: node F-001-REPORT-PIN-362.js <dataset-check.json>");process.exit(2);}
  try{
    const st=fs.lstatSync(path);
    if(!st.isFile()||st.size>100000)throw Error("report must be a regular file of at most 100000 bytes");
    const report=JSON.parse(fs.readFileSync(path,"utf8"));
    const result=validate(report);
    console.log(JSON.stringify(result,null,2));
    process.exit(result.consistent?0:1);
  }catch(e){console.error(String(e));process.exit(2);}
}
