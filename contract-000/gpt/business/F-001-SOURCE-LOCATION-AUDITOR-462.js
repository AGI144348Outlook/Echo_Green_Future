/* F-001 Run462 HOLD-only source-location auditor. No edits, approvals, or release.
 * Node CLI not independently executed in Run462; V8 core tested with GitHub source bytes.
 * The pins must be supplied by a separately trusted source. */
"use strict";
const COLS=["project","occurrence_id","proposal_section","short_text","claude_proposed_state","same_text_as","editorial_approval","publication_status","tam_source_commit","manuscript_git_blob"];
function sentences(t){return t.split(/(?<=[.!?])\s+|\n{2,}/).map(s=>s.trim()).filter(Boolean);}
function norm(t){return t.normalize("NFKC").replace(/[“”‘’]/g,'"').replace(/\s+/g," ").trim().toLowerCase();}
function audit(tsv,sources,pins){
 if(typeof tsv!=="string"||!tsv.endsWith("\n"))throw Error("noncanonical TSV");
 const lines=tsv.trimEnd().split("\n").map(s=>s.split("\t"));
 if(lines.length!==83||lines[0].join("\t")!==COLS.join("\t"))throw Error("register header or count");
 const rows=lines.slice(1).map(x=>{if(x.length!==COLS.length)throw Error("column count");return Object.fromEntries(COLS.map((k,i)=>[k,x[i]]));});
 const seen=new Set(),lookup=new Map(),results=[],counts={LITERAL:0,PREFIX:0,MANUAL:0};
 for(const row of rows){
  const m=/^(.*)#S([1-9][0-9]*)$/.exec(row.occurrence_id);
  if(row.project!=="F-001"||!m||seen.has(row.occurrence_id))throw Error("invalid occurrence");
  seen.add(row.occurrence_id);
  if(row.editorial_approval!=="PROPOSED_NOT_APPROVED"||row.publication_status!=="HOLD / NOT LAUNCH-READY")throw Error("approval/release state");
  if(row.tam_source_commit!=="d46456a18fe412398d0ae37ec5a8c4eebb44e0c9")throw Error("source commit");
  const src=sources[m[1]];
  if(!src||src.sha!==pins[m[1]])throw Error("missing or unpinned source");
  const ss=sentences(src.content),sentence=ss[Number(m[2])-1];
  if(!sentence)throw Error("out-of-range sentence "+row.occurrence_id);
  lookup.set(row.occurrence_id,sentence);
  const excerpt=norm(row.short_text).replace(/^["']+/,"").replace(/["']+$/,"").replace(/[…]+$/,"").trim();
  const actual=norm(sentence);
  const cls=excerpt.length>15&&actual.includes(excerpt)?"LITERAL":excerpt.length>20&&actual.includes(excerpt.slice(0,28))?"PREFIX":"MANUAL";
  counts[cls]++;
  results.push({id:row.occurrence_id,file:m[1],position:Number(m[2]),sha:src.sha,cls,copy:row.same_text_as,sentence});
 }
 let copies=0;
 for(const row of rows)if(row.same_text_as){if(!lookup.has(row.same_text_as)||lookup.get(row.occurrence_id)!==lookup.get(row.same_text_as))throw Error("copy mismatch "+row.occurrence_id);copies++;}
 return {results,counts,copies,sourceFiles:Object.keys(sources).length,approved:0,release:false};
}
if(typeof module!=="undefined"&&module.exports)module.exports={audit,sentences};
