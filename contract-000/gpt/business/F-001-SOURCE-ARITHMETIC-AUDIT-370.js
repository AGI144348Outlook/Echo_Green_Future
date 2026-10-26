#!/usr/bin/env node
/** F-001 HOLD-only independent source arithmetic audit. No writes to TAM source.
 * Usage: node F-001-SOURCE-ARITHMETIC-AUDIT-370.js <dataset-A-file> <dataset-B-file>
 * This CLI wrapper has NOT been independently run in this automation environment.
 * Core auditF001 function was executed in V8 against pinned GitHub-fetched UTF-8 text.
 */
const fs=require("node:fs"),crypto=require("node:crypto");
function auditF001(sourceA,sourceB){
 const aRegex=/^(?<object>.+?) (?<mass>\d+\.\d+)g (?<units>\d+(?:\.\d+)?) Units? \((?<sign>[^)]*)\) (?<dev>[<+\-]?\d+\.\d+)\\?% (?<term>.+)$/;
 const bRegex=/^(?<ratio>\d+) (?<mass>\d+\.\d+)g (?<sign>.+?) (?<units>\d+(?:\/\d+)?(?:\.\d+)?) Units? (?<relation>.+)$/;
 const a=[],b=[],rejectA=[],rejectB=[];
 for(const raw of sourceA.split(/\r?\n/)){const s=raw.trim();if(!s||s.startsWith("Source:")||s.startsWith("Object Description"))continue;const m=s.match(aRegex);if(m)a.push(m.groups);else rejectA.push(s);}
 for(const raw of sourceB.split(/\r?\n/)){const s=raw.trim();if(!s||s.startsWith("This table")||s.startsWith("Ratio Mass"))continue;const m=s.match(bRegex);if(m)b.push(m.groups);else rejectB.push(s);}
 const numUnits=s=>s.includes("/")?Number(s.split("/")[0])/Number(s.split("/")[1]):Number(s);
 const round3=x=>Math.round((x+Number.EPSILON)*1000)/1000;
 const fmt=x=>Number(x.toFixed(6));
 const computedA=a.map(r=>{
  const measured=Number(r.mass),units=numUnits(r.units),expected=13.7*units;
  const rec=round3((measured-expected)/expected*100);
  const claimed=r.dev;
  const pass=claimed.startsWith("<")?Math.abs(rec)<Number(claimed.slice(1)):Math.abs(rec-Number(claimed))<=0.01;
  return {...r,expected_g:fmt(expected),nominal_deviation_pct:rec,stated_deviation_pct:claimed,stated_within_0_01pp:pass,delta_pp:claimed.startsWith("<")?null:fmt(rec-Number(claimed))};
 });
 const computedB=b.map(r=>{
  const measured=Number(r.mass),units=numUnits(r.units),expected=13.7*units;
  return {...r,expected_g:fmt(expected),nominal_deviation_pct:round3((measured-expected)/expected*100),ratio_over_16_equals_units:Math.abs(Number(r.ratio)/16-units)<1e-9};
 });
 return {base_g_per_unit:13.7,A:{count:a.length,rejected:rejectA,rows:computedA,nominal_mismatch_count:computedA.filter(r=>!r.stated_within_0_01pp).length},B:{count:b.length,rejected:rejectB,rows:computedB,ratio_invariant_fail_count:computedB.filter(r=>!r.ratio_over_16_equals_units).length},gerah:{A:a.filter(r=>/gerah/i.test(r.term)).map(r=>({object:r.object,units:r.units})),B:b.filter(r=>/gerah/i.test(r.relation)).map(r=>({ratio:r.ratio,units:r.units}))}};
}
const [a,b]=process.argv.slice(2);
if(!a||!b){console.error("usage: node F-001-SOURCE-ARITHMETIC-AUDIT-370.js A B");process.exit(2);}
function blobSha(x){return crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+x.length+" "),Buffer.from([0]),x])).digest("hex");}
const aa=fs.readFileSync(a),bb=fs.readFileSync(b);
const ap=blobSha(aa),bp=blobSha(bb);
if(ap!=="b62c970a660e0a6685b58db1ef121690daa4fce7"||bp!=="12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4"){console.error("PIN_MISMATCH");process.exit(2);}
const result=auditF001(aa.toString("utf8"),bb.toString("utf8"));
if(result.A.count!==6||result.B.count!==8||result.A.rejected.length||result.B.rejected.length){console.error("PARSE_MISMATCH");process.exit(2);}
console.log(JSON.stringify({status:"HOLD_SOURCE_AUDIT_ONLY",source_git_blobs:{A:ap,B:bp},...result},null,2));
