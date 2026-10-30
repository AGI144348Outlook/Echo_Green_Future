"use strict";
/* F-001 Run476: dependency-free V8 fake-DOM regression for the exact offline DRAFT HTML.
 * CLI: node test_f001_review_dom_476.js F-001-82-EDITORIAL-REVIEW-DRAFT-470.html
 * This is NOT a Chromium/Android/screen-reader test. No network or source writes.
 */
const EXPECTED_BLOB=null; // v472 generated HTML not yet committed; caller supplies independently captured expected SHA.
async function runSuite(html,observedBlob){
 const out=[];function check(name,ok){if(!ok)throw Error("FAIL "+name);out.push(name);}
 check("source Git blob is explicit 40-hex",/^[0-9a-f]{40}$/.test(observedBlob));
 const start=html.indexOf("<script>"),end=html.indexOf("</script>",start);
 check("inline script exists",start>=0&&end>start);
 const script=html.slice(start+8,end);
 new Function(script);check("inline script compiles",true);
 function makeDom(){
  const byId={},network=[],exported={value:null};
  class El{
   constructor(tag){this.tagName=tag;this.children=[];this.dataset={};this.events={};this.value="";this.textContent="";this.hidden=false;this.files=[];}
   append(...items){this.children.push(...items);}
   addEventListener(event,fn){this.events[event]=fn;}
   setAttribute(k,v){this[k]=v;}
   click(){this.clicked=true;}
  }
  for(const id of ["cards","query","count","export","restore","message"])byId[id]=new El(id);
  const document={createElement:tag=>new El(tag),getElementById:id=>byId[id]};
  class BlobMock{constructor(parts){this.textValue=parts.join("");}}
  const url={createObjectURL:blob=>{exported.value=blob.textValue;return "blob:local";},revokeObjectURL:()=>{}};
  const noNetwork=kind=>()=>{network.push(kind);throw Error("unexpected network");};
  new Function("document","Blob","URL","setTimeout","fetch","XMLHttpRequest","navigator",script)(
    document,BlobMock,url,fn=>fn(),noNetwork("fetch"),noNetwork("XHR"),{sendBeacon:noNetwork("beacon")});
  return {byId,network,exported};
 }
 const dom=makeDom(),boxes=dom.byId.cards.children;
 check("82 rendered articles",boxes.length===82);
 const ids=boxes.map(x=>x.children[0].textContent);
 check("82 unique IDs",new Set(ids).size===82);
 check("HOLD banner",html.includes("HOLD / NOT LAUNCH-READY"));
 check("10 duplicate references",boxes.filter(x=>x.children.some(y=>String(y.textContent).startsWith("Duplicate text reference:"))).length===10);
 check("draft selects",boxes.every(x=>x.children.some(y=>y.tagName==="select")));
 const targets=boxes.map(x=>{
  const heading=x.children.find(y=>y.tagName==="h2"),select=x.children.find(y=>y.tagName==="select"),note=x.children.find(y=>y.tagName==="textarea"),labels=x.children.filter(y=>y.tagName==="label");
  return {heading,select,note,labels,region:x["aria-labelledby"]};
 });
 const idsAll=targets.flatMap(t=>[t.heading.id,t.select.id,t.note.id]);
 check("246 stable unique control and heading IDs",idsAll.length===246&&idsAll.every(Boolean)&&new Set(idsAll).size===246);
 check("82 heading-labeled regions",targets.every(t=>t.region===t.heading.id));
 check("164 explicit label-control associations",targets.every(t=>t.labels.length===2&&t.labels[0].htmlFor===t.select.id&&t.labels[1].htmlFor===t.note.id));
 check("82 draft warning labels",targets.every(t=>t.labels[0].textContent.includes("NOT an approval")));
 check("source IDs remain separate from DOM tokens",targets.every((t,i)=>t.heading.textContent===ids[i]&&t.select.id==="f001-card-"+(i+1)+"-disposition"));
 const first=boxes[0],select=first.children.find(x=>x.tagName==="select"),note=first.children.find(x=>x.tagName==="textarea");
 select.value="DRAFT_REVISE";select.events.change();
 note.value="Synthetic Unicode ש";note.events.input();
 dom.byId.query.value=ids[0];dom.byId.query.events.input();
 check("search filters",boxes.some(x=>x.hidden)&&boxes.some(x=>!x.hidden));
 dom.byId.export.events.click();
 const draft=JSON.parse(dom.exported.value);
 check("export has 82 items",draft.items.length===82);
 check("export has no approval/release",draft.authority==="NONE"&&draft.timothy_approval_authenticated===false&&draft.publication_authorized===false&&draft.editorial_overlay_applied===false);
 check("draft edits exported",draft.items[0].draft_status==="DRAFT_REVISE"&&draft.items[0].draft_note==="Synthetic Unicode ש");
 const restored=makeDom();
 async function importData(data){
  const field=restored.byId.restore;
  field.files=[{size:JSON.stringify(data).length,text:async()=>JSON.stringify(data)}];
  await field.events.change({target:field});
 }
 await importData(draft);
 const restoredFirst=restored.byId.cards.children[0];
 const sel=restoredFirst.children.find(x=>x.tagName==="select"),txt=restoredFirst.children.find(x=>x.tagName==="textarea");
 check("draft restore exact",sel.value==="DRAFT_REVISE"&&txt.value==="Synthetic Unicode ש");
 check("restore says no approval",restored.byId.message.textContent.includes("No editorial approval"));
 const negative=[
  ["approval flag",d=>{d.timothy_approval_authenticated=true;}],
  ["release flag",d=>{d.publication_authorized=true;}],
  ["source pin",d=>{d.source_pins.register="0".repeat(40);}],
  ["duplicate ID",d=>{d.items[1].occurrence_id=d.items[0].occurrence_id;}],
  ["oversize note",d=>{d.items[1].draft_note="X".repeat(1001);}]
 ];
 for(const [name,mutate] of negative){
  const forged=JSON.parse(JSON.stringify(draft));mutate(forged);await importData(forged);
  check("refuse "+name+" without partial restore",restored.byId.message.textContent.startsWith("No changes restored:")&&sel.value==="DRAFT_REVISE"&&txt.value==="Synthetic Unicode ש");
 }
 check("no outbound request",dom.network.length===0&&restored.network.length===0);
 return {passed:out.length,total:out.length,checks:out,source_blob:observedBlob,status:"HOLD / NOT LAUNCH-READY",scope:"V8 fake DOM only; not Chromium or Android"};
}
if(typeof module!=="undefined"&&module.exports)module.exports={runSuite,EXPECTED_BLOB};
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("node:fs"),crypto=require("node:crypto");
 (async()=>{try{
  if(process.argv.length!==4)throw Error("Usage: node test_f001_review_dom_476.js page.html expected-git-blob-sha");
  const bytes=fs.readFileSync(process.argv[2]);
  const sha=crypto.createHash("sha1").update(Buffer.from("blob "+bytes.length+"\0")).update(bytes).digest("hex");
  if(!/^[0-9a-f]{40}$/.test(process.argv[3])||sha!==process.argv[3])throw Error("expected Git blob pin mismatch");
  const result=await runSuite(bytes.toString("utf8"),sha);
  console.log(JSON.stringify(result,null,2));
 }catch(e){console.error("F-001 HOLD: "+e.message);process.exitCode=2;}})();
}
