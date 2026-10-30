"use strict";
/* F-001 Run468: regression checks for the generated offline review page.
 * Node CLI: node test_f001_review_companion_468.js old467.js new468.js register.tsv locations.tsv intake.tsv
 * No network, publication, approval, or file writes. Does not execute browser DOM.
 */
function runSuite(oldGen,newGen,register,location,intake,pins){
 const out=[];
 function check(ok,label){if(!ok)throw Error("FAIL: "+label);out.push("PASS: "+label);}
 function inline(html){
  const a=html.indexOf("<script>"),b=html.indexOf("</script>");
  if(a<0||b<=a)throw Error("missing inline script");
  return html.slice(a+8,b);
 }
 const texts=[register,location,intake];
 check(["register","location","intake"].every((k,i)=>pins[k]===newGen.PINS[k]),"three exact source Git blob pins");
 const oldHtml=oldGen.buildReview(...texts,pins);
 let oldRejected=false;
 try{new Function(inline(oldHtml));}catch(_){oldRejected=true;}
 check(oldRejected,"Run467 emitted script is invalid (negative control)");
 const html=newGen.buildReview(...texts,pins);
 new Function(inline(html));
 check(true,"Run468 emitted script parses");
 check(html===newGen.buildReview(...texts,pins),"deterministic generation");
 check(html===oldHtml.replace('JSON.stringify(data,null,2)+"\n"','JSON.stringify(data,null,2)+"\\n"'),"only escaped newline differs in HTML");
 const start=html.indexOf("const CARDS="),end=html.indexOf(";\nconst SOURCE_PINS=",start);
 check(start>=0&&end>start,"embedded cards payload present");
 const cards=JSON.parse(html.slice(start+"const CARDS=".length,end));
 check(cards.length===82&&new Set(cards.map(x=>x.id)).size===82,"82 unique source-linked cards");
 check(cards.filter(x=>x.copy).length===10,"10 duplicate-text references");
 check(html.includes("HOLD / NOT LAUNCH-READY"),"HOLD banner present");
 check(!html.includes('option value="APPROVED"'),"no APPROVED option");
 check(html.includes('timothy_approval_authenticated:false,publication_authorized:false,editorial_overlay_applied:false'),"draft export authority false");
 check(!/fetch\s*\(|XMLHttpRequest|sendBeacon/.test(inline(html)),"no outbound request primitives");
 const valid={format:"F-001-review-feedback-DRAFT/v1",project:"F-001",authority:"NONE",timothy_approval_authenticated:false,publication_authorized:false,editorial_overlay_applied:false,source_pins:pins,items:cards.map(x=>({occurrence_id:x.id,draft_status:"",draft_note:""}))};
 check(newGen.validateDraftFeedback(valid,cards,pins).length===82,"valid DRAFT feedback accepted");
 const negatives=[
  ["approval forgery",x=>x.timothy_approval_authenticated=true],
  ["publication forgery",x=>x.publication_authorized=true],
  ["source pin forgery",x=>x.source_pins.register="0".repeat(40)],
  ["status escalation",x=>x.items[0].draft_status="APPROVED"],
  ["unknown occurrence",x=>x.items[0].occurrence_id="forged"],
 ];
 for(const [label,mutate] of negatives){
  const data=JSON.parse(JSON.stringify(valid));mutate(data);
  let refused=false;try{newGen.validateDraftFeedback(data,cards,pins)}catch(_){refused=true;}
  check(refused,label+" refused");
 }
 return out;
}
if(typeof module!=="undefined"&&module.exports)module.exports={runSuite};
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("node:fs"),crypto=require("node:crypto"),path=require("node:path");
 const args=process.argv.slice(2);
 if(args.length!==5){console.error("Usage: node test_f001_review_companion_468.js old467.js new468.js register.tsv locations.tsv intake.tsv");process.exit(2);}
 const [oldPath,newPath,...inputPaths]=args;
 const blob=b=>crypto.createHash("sha1").update(Buffer.from("blob "+b.length+"\0")).update(b).digest("hex");
 try{
  const files=inputPaths.map(p=>fs.readFileSync(p));
  const pins=Object.fromEntries(["register","location","intake"].map((k,i)=>[k,blob(files[i])]));
  const checks=runSuite(require(path.resolve(oldPath)),require(path.resolve(newPath)),...files.map(b=>b.toString("utf8")),pins);
  for(const c of checks)console.log(c);
  console.log(JSON.stringify({project:"F-001",status:"HOLD / NOT LAUNCH-READY",passed:checks.length,total:checks.length,authority:"NONE"}));
 }catch(error){console.error("F-001 HOLD / regression refused: "+error.message);process.exitCode=2;}
}