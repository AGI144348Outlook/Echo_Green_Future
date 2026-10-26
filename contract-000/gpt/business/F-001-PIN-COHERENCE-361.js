"use strict";
// F-001 HOLD-only source-pin coherence preflight. Static inspection, NOT stage execution.
// Usage: node F-001-PIN-COHERENCE-361.js <builder334.py> <gate344.py> <consumer347.py> <coordinator351.py>
const PIN={
  builder:"e8af6e5f011ec3e827c94737c717937944924eb8",
  gate:"5d5bb8f85db7f21c50ca71625e82c51102fed088",
  consumer:"b2a97390ba39959cd2f86a5e51ea186348f31fb2",
  coordinator:"68eea27de6e9a961f31122a08585ee6e24fed2df",
  commit:"d46456a18fe412398d0ae37ec5a8c4eebb44e0c9",
  a:"b62c970a660e0a6685b58db1ef121690daa4fce7",
  b:"12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4",
  csvA:"989d83c16568f23a97251d93919068f3a5e726c738644625af909b278f395fdb",
  csvB:"ff442e48acaf00900a3bc3d7900bf987995355a34226b749dbd5b81878e2f7c0"
};
function scalar(content,key) {
  const re=new RegExp("\\b"+key+"\\s*=\\s*[\"']([0-9a-f]{40})[\"']");
  const m=re.exec(content); return m?m[1]:null;
}
function csv(content,key) {
  const block=/\bEXPECTED_CSV_SHA256\s*=\s*\{([\s\S]*?)\}/.exec(content);
  if(!block)return null;
  const re=new RegExp("[\"']"+key.replace(".","\\.")+"[\"']\\s*:\\s*[\"']([0-9a-f]{64})[\"']");
  const m=re.exec(block[1]);return m?m[1]:null;
}
function audit(sources) {
  const errors=[];
  for(const k of ["builder","gate","consumer","coordinator"]) {
    if(!sources[k]||typeof sources[k].content!=="string") {errors.push("MISSING_"+k.toUpperCase());continue;}
    if(sources[k].blob!==PIN[k])errors.push("BLOB_"+k.toUpperCase());
  }
  function check(file,key,want) {
    if(!sources[file])return;
    const got=scalar(sources[file].content,key);
    if(got!==want)errors.push(file.toUpperCase()+"_"+key+"_MISMATCH");
  }
  check("builder","PIN_COMMIT",PIN.commit);
  check("builder","PIN_A_BLOB",PIN.a);
  check("builder","PIN_B_BLOB",PIN.b);
  for(const file of ["gate","consumer"]) {
    check(file,"PIN_COMMIT",PIN.commit);
    check(file,"PIN_A",PIN.a);
    check(file,"PIN_B",PIN.b);
    check(file,"PIN_BUILDER_BLOB",PIN.builder);
  }
  check("coordinator","PIN_SOURCE_COMMIT",PIN.commit);
  check("coordinator","PIN_GATE_BLOB",PIN.gate);
  check("coordinator","PIN_CONSUMER_BLOB",PIN.consumer);
  check("coordinator","PIN_BUILDER_BLOB",PIN.builder);
  for(const file of ["gate","consumer","coordinator"]) {
    if(!sources[file])continue;
    if(csv(sources[file].content,"dataset-a.csv")!==PIN.csvA)errors.push(file.toUpperCase()+"_CSV_A_MISMATCH");
    if(csv(sources[file].content,"dataset-b.csv")!==PIN.csvB)errors.push(file.toUpperCase()+"_CSV_B_MISMATCH");
  }
  return {pass:errors.length===0,errors,scope:"static source-pin coherence only; no Python/staging/runtime/rights verification"};
}
if(typeof require!=="undefined" && typeof module!=="undefined" && require.main===module) {
  const fs=require("node:fs"),crypto=require("node:crypto");
  const args=process.argv.slice(2);
  if(args.length!==4){console.error("usage: node pin-coherence.js builder gate consumer coordinator");process.exit(2);}
  const files={};
  for(let i=0;i<4;i++){
    const raw=fs.readFileSync(args[i]),name=["builder","gate","consumer","coordinator"][i];
    const blob=crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+raw.length+"\0"),raw])).digest("hex");
    files[name]={blob,content:raw.toString("utf8")};
  }
  const result=audit(files);console.log(JSON.stringify(result,null,2));process.exit(result.pass?0:1);
}