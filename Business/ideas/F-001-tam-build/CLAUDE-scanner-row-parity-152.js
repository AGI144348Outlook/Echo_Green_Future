// F-001 §152 (Claude 21Z): row-level comparison of GPT run 452 JS port vs the Python claims.csv.
// Usage: node F001-row-parity-152.js <gpt452.js> <tam-dir> <claims.csv-as-json>
const fs=require("fs"), path=require("path");
const [js, tam, pyjson]=process.argv.slice(2);
const m=require(path.resolve(js));
const src={}; for (const f of m.FILES) src[f]=fs.readFileSync(path.join(tam,f),"utf8");
const r=m.scanSources(src);
const py=JSON.parse(fs.readFileSync(pyjson,"utf8"));
let same=0, diff=[];
const n=Math.max(py.length,r.rows.length);
for(let i=0;i<n;i++){const a=py[i],b=r.rows[i];
  if(a&&b&&a.file===b.file&&+a.sentence_no===b.sentence_no&&a.triggers===b.triggers&&a.sentence===b.sentence) same++; else diff.push(i);}
console.log(JSON.stringify({py_rows:py.length, js_rows:r.rows.length, identical_rows:same, differing_indexes:diff, selfTests:m.selfTests()}));
process.exit(diff.length?1:0);
