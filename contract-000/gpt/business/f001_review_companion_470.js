"use strict";
/* F-001: offline 82-occurrence draft-only review companion with bounded restore and explicit accessible label targets. No approval authority.
 * CLI: node f001_review_companion_470.js register.tsv locations.tsv intake.tsv output.html
 * Exact Git blob pins are checked before rendering. No network.
 */
const PINS={"register":"300dfcf0ba9e9d236326d09b2a4b6c5467d3874c","location":"7fb5cd952127de7a0469cfb3d0139d7bdfb60b86","intake":"4cc1617d1f1bbea1661f74ba931f86660c087939"};
const HOLD="HOLD / NOT LAUNCH-READY";
const HEADERS={"register":"project\toccurrence_id\tproposal_section\tshort_text\tclaude_proposed_state\tsame_text_as\teditorial_approval\tpublication_status\ttam_source_commit\tmanuscript_git_blob","location":"occurrence_id\tsource_file\tsentence_no\tsource_git_blob\tquote_match_class\tcopy_target\tsource_sentence_preview","intake":"project\toccurrence_id\tproposal_register_blob\tlocation_map_blob\tsource_git_blob\tdecision\treplacement_text\tapproved_by\tdecision_evidence\trelease_authorized"};
function insist(condition,message){if(!condition)throw new Error("F-001 HOLD: "+message)}

function parseTsv(text,kind){
 insist(typeof text==="string"&&!text.includes("\r"),kind+" must be LF-only UTF-8 text");
 const lines=text.trimEnd().split("\n");
 insist(lines[0]===HEADERS[kind],kind+" header differs");
 const keys=lines[0].split("\t");
 insist(lines.length===83,kind+" must contain exactly 82 rows");
 return lines.slice(1).map((line,i)=>{
   const fields=line.split("\t");
   insist(fields.length===keys.length,kind+" row "+(i+1)+" column count");
   return Object.fromEntries(keys.map((key,j)=>[key,fields[j]]));
 });
}

function validateDraftFeedback(data,expectedCards,expectedPins){
 const rootKeys=["format","project","authority","timothy_approval_authenticated","publication_authorized","editorial_overlay_applied","source_pins","items"];
 const itemKeys=["occurrence_id","draft_status","draft_note"];
 const pinKeys=["register","location","intake"];
 const exact=(obj,keys)=>obj!==null&&typeof obj==="object"&&!Array.isArray(obj)&&Object.keys(obj).length===keys.length&&keys.every(k=>Object.prototype.hasOwnProperty.call(obj,k));
 const fail=msg=>{throw new Error("DRAFT import refused: "+msg)};
 if(!exact(data,rootKeys))fail("unknown or missing root fields");
 if(data.format!=="F-001-review-feedback-DRAFT/v1"||data.project!=="F-001"||data.authority!=="NONE")fail("wrong draft format or authority");
 if(data.timothy_approval_authenticated!==false||data.publication_authorized!==false||data.editorial_overlay_applied!==false)fail("authority flag is not false");
 if(!exact(data.source_pins,pinKeys)||!pinKeys.every(k=>data.source_pins[k]===expectedPins[k]))fail("source pins mismatch");
 if(!Array.isArray(expectedCards)||!Array.isArray(data.items)||data.items.length!==expectedCards.length||data.items.length!==82)fail("expected exactly 82 items");
 const statuses=new Set(["","DRAFT_ACCEPT","DRAFT_REVISE","DRAFT_REJECT","DRAFT_DEFER"]);
 return data.items.map((item,i)=>{
  if(!exact(item,itemKeys))fail("unknown or missing item fields at "+i);
  if(item.occurrence_id!==expectedCards[i].id)fail("unknown, duplicate or reordered occurrence at "+i);
  if(!statuses.has(item.draft_status))fail("invalid draft status at "+i);
  if(typeof item.draft_note!=="string"||item.draft_note.length>1000)fail("invalid or oversized note at "+i);
  return {occurrence_id:item.occurrence_id,draft_status:item.draft_status,draft_note:item.draft_note};
 });
}

function safeJson(value){
 return JSON.stringify(value).replace(/&/g,"\\u0026").replace(/</g,"\\u003c").replace(/>/g,"\\u003e").replace(/\u2028/g,"\\u2028").replace(/\u2029/g,"\\u2029");
}

function renderHtml(cards){
 const payload=safeJson(cards),pins=safeJson(PINS),validator=validateDraftFeedback.toString();
 return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>F-001 · 82 editorial draft reviews (HOLD)</title>
<style>
:root{color-scheme:light;font-family:system-ui,sans-serif;color:#173341;background:#f5f7f8}
body{margin:0}header{padding:16px;background:#173d50;color:#fff}h1{font-size:1.35rem;margin:0}
main{max-width:940px;margin:auto;padding:12px}.hold{background:#fff2d5;border-left:5px solid #a95b00;padding:12px;margin:10px 0}
.controls{position:sticky;top:0;background:#fff;padding:12px;border:1px solid #cad7dc;border-radius:8px}
input,select,textarea,button{font:inherit;max-width:100%;padding:9px;border-radius:6px}
input,textarea,select{width:100%;border:1px solid #8babb7}button{background:#005e78;color:#fff;border:0;margin:8px 0}
button:focus,input:focus,textarea:focus,select:focus{outline:3px solid #88c9dd}
article{background:white;border:1px solid #d2dce0;padding:14px;margin:12px 0;border-radius:8px;overflow-wrap:anywhere}
h2{font-size:1.08rem}.source{white-space:pre-wrap;background:#f0f5f7;padding:10px;border-left:3px solid #006d85}
.proposal{white-space:pre-wrap;background:#faf5ed;padding:10px;border-left:3px solid #a77a2d}
.meta{font-size:.84rem;color:#4d626e}label{display:block;margin:8px 0 3px;font-weight:600}
@media(max-width:620px){.controls{position:static}}
</style></head><body>
<header><h1>F-001 · TAM Protocol — 82 editorial draft reviews</h1><p>Offline, mobile-friendly companion. No account, network, publishing or payments.</p></header>
<main><div class="hold"><strong>HOLD / NOT LAUNCH-READY.</strong> Claude's proposals are unapproved. Selections here are <strong>draft feedback only</strong>; they are not Timothy's authenticated decisions, editorial approval, rights clearance or permission to publish. Export for later independent review.</div>
<div class="controls"><label for="query">Search occurrence, source or proposal</label><input id="query" type="search">
<p id="count" role="status" aria-live="polite">82 pending editorial occurrences</p>
<button type="button" id="export">Export DRAFT feedback JSON (not approval)</button><label for="restore">Restore previously exported DRAFT feedback JSON (local file only)</label><input type="file" id="restore" accept=".json,application/json"><p id="message" role="status"></p></div>
<section id="cards" aria-label="Editorial occurrences"></section>
<p class="meta">Immutable source pins: register ${PINS.register}; location ${PINS.location}; intake ${PINS.intake}. The exported file has no approval or release authority. Nothing is saved or transmitted automatically.</p>
</main><script>
"use strict";
${validator}
const CARDS=${payload};
const SOURCE_PINS=${pins};
const root=document.getElementById("cards"),query=document.getElementById("query"),count=document.getElementById("count");
const choices=new Map(),fields=new Map();
function element(tag,cls,text){const x=document.createElement(tag);if(cls)x.className=cls;if(text!==undefined)x.textContent=text;return x;}
let cardIndex=0;
for(const c of CARDS){
 const cardToken="f001-card-"+(++cardIndex);
 const box=element("article");box.setAttribute("aria-labelledby",cardToken+"-heading");box.dataset.search=(c.id+" "+c.source+" "+c.proposal).toLowerCase();
 const heading=element("h2","",c.id);heading.id=cardToken+"-heading";
 box.append(heading,element("p","meta","Source "+c.source+" · sentence "+c.sentence+" · "+c.match+" · "+c.section));
 box.append(element("div","source",c.preview),element("div","proposal","Claude's PROPOSED (not approved): "+c.proposal));
 if(c.copy)box.append(element("p","meta","Duplicate text reference: "+c.copy+" (separate decision required)"));
 const label=element("label","", "Draft disposition (NOT an approval)");
 const select=element("select");select.id=cardToken+"-disposition";label.htmlFor=select.id;select.setAttribute("aria-label","Draft disposition for "+c.id);
 for(const [v,t] of [["","No draft decision"],["DRAFT_ACCEPT","Draft: accept proposal"],["DRAFT_REVISE","Draft: revise"],["DRAFT_REJECT","Draft: reject"],["DRAFT_DEFER","Draft: defer"]]){
  const opt=element("option","",t);opt.value=v;select.append(opt);
 }
 const noteLabel=element("label","","Draft note / suggested wording (unverified)");
 const note=element("textarea");note.id=cardToken+"-note";noteLabel.htmlFor=note.id;note.rows=2;note.maxLength=1000;note.setAttribute("aria-label","Draft note for "+c.id);
 select.addEventListener("change",()=>choices.set(c.id,{status:select.value,note:note.value}));
 note.addEventListener("input",()=>choices.set(c.id,{status:select.value,note:note.value}));
 box.append(label,select,noteLabel,note);fields.set(c.id,{select,note});root.append(box);
}
function filter(){const term=query.value.trim().toLowerCase();let shown=0;for(const box of root.children){box.hidden=!box.dataset.search.includes(term);if(!box.hidden)shown++;}count.textContent=shown+" of "+CARDS.length+" occurrences visible · all remain PENDING";}
query.addEventListener("input",filter);filter();
document.getElementById("restore").addEventListener("change",async event=>{
 const input=event.target,notice=document.getElementById("message");
 try{
  const file=input.files&&input.files[0];if(!file)return;
  if(file.size>262144)throw new Error("DRAFT import refused: file exceeds 256 KiB");
  const parsed=JSON.parse(await file.text());
  const validated=validateDraftFeedback(parsed,CARDS,SOURCE_PINS);
  // Validate ALL records before changing ANY controls.
  choices.clear();
  for(const item of validated){
   const ui=fields.get(item.occurrence_id);
   ui.select.value=item.draft_status;ui.note.value=item.draft_note;
   choices.set(item.occurrence_id,{status:item.draft_status,note:item.draft_note});
  }
  notice.textContent="Restored 82 DRAFT entries locally. No editorial approval or release authority.";
 }catch(error){notice.textContent="No changes restored: "+error.message;}
 finally{input.value="";}
});
document.getElementById("export").addEventListener("click",()=>{
 const items=CARDS.map(c=>({occurrence_id:c.id,draft_status:(choices.get(c.id)||{}).status||"",draft_note:(choices.get(c.id)||{}).note||""}));
 const data={format:"F-001-review-feedback-DRAFT/v1",project:"F-001",authority:"NONE",timothy_approval_authenticated:false,publication_authorized:false,editorial_overlay_applied:false,source_pins:SOURCE_PINS,items};
 const blob=new Blob([JSON.stringify(data,null,2)+"\\n"],{type:"application/json"});
 const url=URL.createObjectURL(blob);const a=document.createElement("a");a.href=url;a.download="F-001-82-review-DRAFT.json";a.click();setTimeout(()=>URL.revokeObjectURL(url),0);
 document.getElementById("message").textContent="Draft-only JSON exported. It is NOT approval or release authorization.";
});
</script></body></html>\n`;
}

function buildReview(registerText,locationText,intakeText,observedPins){
 insist(observedPins&&Object.keys(PINS).every(k=>observedPins[k]===PINS[k]),"input Git blob pins not verified");
 const reg=parseTsv(registerText,"register"),loc=parseTsv(locationText,"location"),intake=parseTsv(intakeText,"intake");
 const seen=new Set();let copyCount=0;const cards=[];
 for(let i=0;i<82;i++){
  const a=reg[i],b=loc[i],c=intake[i],id=a.occurrence_id;
  insist(id&&!seen.has(id),"duplicate or blank occurrence ID");seen.add(id);
  insist(b.occurrence_id===id&&c.occurrence_id===id,"row order or occurrence ID mismatch at "+i);
  insist(a.project==="F-001"&&c.project==="F-001","project mismatch");
  insist(a.editorial_approval==="PROPOSED_NOT_APPROVED"&&a.publication_status===HOLD,"register must remain unapproved HOLD");
  insist(c.proposal_register_blob===PINS.register&&c.location_map_blob===PINS.location,"intake source pin mismatch");
  insist(c.source_git_blob===b.source_git_blob,"source Git blob mismatch");
  insist(c.decision==="PENDING"&&!c.replacement_text&&!c.approved_by&&!c.decision_evidence&&c.release_authorized==="false","intake must be PENDING with no authority or edits");
  insist(a.same_text_as===b.copy_target,"duplicate target mismatch");
  insist(["LITERAL","PREFIX","MANUAL"].includes(b.quote_match_class),"unrecognized source match class");
  insist(/^\d+$/.test(b.sentence_no)&&Number(b.sentence_no)>0,"invalid sentence number");
  if(a.same_text_as)copyCount++;
  cards.push({id,source:b.source_file,sentence:b.sentence_no,match:b.quote_match_class,section:a.proposal_section,preview:b.source_sentence_preview,proposal:a.claude_proposed_state,copy:a.same_text_as});
 }
 insist(copyCount===10,"expected ten duplicate-text references");
 const html=renderHtml(cards);
 const scriptStart=html.indexOf("<script>"),scriptEnd=html.indexOf("</script>");
 insist(scriptStart>=0&&scriptEnd>scriptStart,"generated inline script missing");
 const inline=html.slice(scriptStart+8,scriptEnd);
 try{new Function(inline);}catch(error){throw new Error("F-001 HOLD: generated inline script syntax invalid: "+error.message);}
 return html;
}

if(typeof module!=="undefined"&&module.exports)module.exports={PINS,HOLD,parseTsv,safeJson,renderHtml,buildReview,validateDraftFeedback};
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("node:fs"),crypto=require("node:crypto");
 const args=process.argv.slice(2);
 if(args.length!==4){console.error("Usage: node f001_review_companion_470.js register.tsv locations.tsv intake.tsv output.html");process.exit(2);}
 try{
  const data=args.slice(0,3).map(x=>fs.readFileSync(x));
  const blob=b=>crypto.createHash("sha1").update(Buffer.from("blob "+b.length+"\0")).update(b).digest("hex");
  const observed={register:blob(data[0]),location:blob(data[1]),intake:blob(data[2])};
  const html=buildReview(...data.map(x=>x.toString("utf8")),observed);
  fs.writeFileSync(args[3],html,{flag:"wx"});
  console.log(JSON.stringify({project:"F-001",status:HOLD,cards:82,output:args[3],approval_authenticated:false,publication_authorized:false}));
 }catch(e){console.error("F-001 HOLD / REVIEW GENERATION REFUSED: "+e.message);process.exitCode=2;}
}
