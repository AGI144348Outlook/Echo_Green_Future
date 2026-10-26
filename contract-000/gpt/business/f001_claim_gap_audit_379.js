"use strict";
// F-001 Run379 — read-only opt-in JS crosswalk; not a replacement for Python claim_scan.py.
// Usage: node f001_claim_gap_audit_379.js <pinned-source-dir> OR --self-test.
const FILES=[
["README.md","213bcfaf560dcc54fbb7ae79fad932e86b660357"],
["Article 1 Hacksilber","237bd3335abdcc0f0465817dffe01ad6eaa86055"],
["Article 2 Water Weight Computes","ec657c3fa0f70da9686fb1ae52983d28f77c6c4c"],
["The Color Dyed and Dental Records","b525ad60ab37cb2d72ea43c40ba687b0fe2a348d"],
["Article 5","c8c1bf617c0d81389f6c2408ed975131695857ff"],
["Article 6","662d745f0b9b41236d1053cdbaa9351f7c020dd0"],
["Article 10","e82be564872f636662652d34dcb8d3437559f84f"],
["Collective information","710ad3cd4feeae7bafa329d7437a78df4c40cfa8"]];
const BASE={
 certainty:/\b(prove[sd]?|proof|proven|confirm(s|ed)?|undeniabl[ey]|definitive(ly)?|certain(ly)?|irrefutabl[ey]|conclusive(ly)?|demonstrat(es|ed)|establish(es|ed))\b/i,
 percent:/\d+(\.\d+)?\s?%/i,
 accuracy:/\b(accura(te|cy)|precision|precise(ly)?|correlat(es|ed|ion))\b/i,
 superlative:/\b(only|exactly|always|never|impossible)\b/i
};
const EXT={...BASE,
 certainty:/\b(prove[sd]?|proof|proven|confirm(s|ed)?|undeniabl[ey]|definitive(ly)?|certain(ly)?|irrefutabl[ey]|conclusive(ly)?|demonstrat(es|ed|ing)|establish(es|ed))\b/i,
 percent:/\d+(?:\.\d+)?\s?\\?%/i
};
function scanText(text){
 const parts=text.split(/(?<=[.!?])\s+|\n{2,}/).map(x=>x.trim()).filter(Boolean),old=[],newer=[],added=[];
 parts.forEach((sentence,i)=>{
  const a=Object.keys(BASE).filter(k=>BASE[k].test(sentence)),b=Object.keys(EXT).filter(k=>EXT[k].test(sentence));
  if(a.length)old.push(i+1);if(b.length)newer.push(i+1);
  if(b.length&&!a.length)added.push({sentence_no:i+1,triggers:b,excerpt:sentence.slice(0,160)});
 });
 return {baseline:old.length,extended:newer.length,baseline_retained:old.every(x=>newer.includes(x)),added};
}
function selfTest(){
 const cases=[
 [EXT.percent.test("13.7\\%")&&!BASE.percent.test("13.7\\%"),"escaped percentage"],
 [EXT.percent.test("13.7%")&&BASE.percent.test("13.7%"),"ordinary percentage"],
 [EXT.certainty.test("demonstrating")&&!BASE.certainty.test("demonstrating"),"demonstrating"],
 [EXT.certainty.test("demonstrated")&&BASE.certainty.test("demonstrated"),"demonstrated"],
 [EXT.certainty.test("demonstrates")&&BASE.certainty.test("demonstrates"),"demonstrates"],
 [!EXT.certainty.test("demonstration"),"no demonstration"],
 [!Object.values(EXT).some(r=>r.test("A quiet page about water.")),"neutral"],
 [EXT.accuracy.test("accuracy"),"accuracy"],
 [!EXT.percent.test("%"),"bare percent"],
 [!EXT.percent.test("20/100"),"slash"],
 [EXT.percent.test("0.25\\%"),"decimal escaped"],
 [EXT.superlative.test("always"),"superlative"],
 [!EXT.certainty.test("demonstrat"),"incomplete token"],
 [EXT.percent.test("13.7 \\%"),"space escaped"]
 ];
 return {passed:cases.filter(x=>x[0]).length,total:cases.length,failures:cases.filter(x=>!x[0]).map(x=>x[1])};
}
module.exports={FILES,BASE,EXT,scanText,selfTest};
if(require.main===module){
 const fs=require("fs"),path=require("path"),crypto=require("crypto");
 if(process.argv[2]==="--self-test"){
  const x=selfTest();console.log(JSON.stringify(x,null,2));if(x.passed!==x.total)process.exitCode=1;
 }else{
  if(process.argv.length!==3)throw Error("Usage: node f001_claim_gap_audit_379.js <source-dir> | --self-test");
  const root=path.resolve(process.argv[2]),records=[];let baseline=0,extended=0;
  for(const [name,pin] of FILES){
   const buf=fs.readFileSync(path.join(root,name));
   const sha=crypto.createHash("sha1").update("blob "+buf.length+"\0").update(buf).digest("hex");
   if(sha!==pin)throw Error("Source pin mismatch: "+name);
   const x=scanText(buf.toString("utf8"));
   if(!x.baseline_retained)throw Error("Baseline candidate lost: "+name);
   records.push({file:name,git_blob:sha,...x});baseline+=x.baseline;extended+=x.extended;
  }
  console.log(JSON.stringify({project:"F-001",status:"HOLD / UNREVIEWED",source_commit:"d46456a18fe412398d0ae37ec5a8c4eebb44e0c9",baseline,extended,records},null,2));
  if(baseline!==42||extended!==45)process.exitCode=2;
 }
}
