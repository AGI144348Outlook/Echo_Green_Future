#!/usr/bin/env node
"use strict";
/* F-001 Run458 HOLD-only editorial decision register gate. Exact queue blob ab5e755c1d1f33fd2c9fd3af2866bc68ab1a4b16; Claude manuscript blob b015fab385b0baf68d88956cb86888b094a69ca2. */
const EXPECTED_IDS=["README.md#S24","Article 1 Hacksilber#S9","Article 1 Hacksilber#S18","Article 2 Water Weight Computes#S5","Article 2 Water Weight Computes#S18","Article 2 Water Weight Computes#S24","The Color Dyed and Dental Records#S23","The Color Dyed and Dental Records#S33","The Color Dyed and Dental Records#S37","Article 5#S7","Article 5#S8","Article 5#S22","Article 6#S4","Article 6#S23","Article 6#S29","Article 10#S3","Article 10#S4","Article 10#S5","Article 10#S8","Collective information#S26","Collective information#S27","Collective information#S39","Collective information#S55","Collective information#S57","Collective information#S68","Collective information#S69","Collective information#S97","Collective information#S100","Collective information#S110","Collective information#S128","Collective information#S147","Collective information#S149","Collective information#S153","Collective information#S172","Collective information#S178","Collective information#S230","Collective information#S236","Collective information#S271","Collective information#S293","Collective information#S294","Collective information#S295","Collective information#S298","README.md#S8","The Color Dyed and Dental Records#S14","Collective information#S90","README.md#S4","README.md#S7","README.md#S18","Article 1 Hacksilber#S15","Article 1 Hacksilber#S17","Article 2 Water Weight Computes#S1","Article 2 Water Weight Computes#S15","Article 2 Water Weight Computes#S19","Article 2 Water Weight Computes#S20","The Color Dyed and Dental Records#S5","The Color Dyed and Dental Records#S15","Article 5#S4","Article 5#S17","Article 5#S19","Article 6#S1","Collective information#S150","Article 6#S12","Collective information#S161","Article 6#S19","Collective information#S168","Collective information#S3","Collective information#S11","Collective information#S35","Collective information#S37","Collective information#S46","Collective information#S53","Collective information#S60","Collective information#S76","Collective information#S82","Collective information#S109","Collective information#S115","Collective information#S117","Collective information#S126","Collective information#S129","Collective information#S141","Collective information#S222","Collective information#S276"];
const COPIES={"Collective information#S293":"Article 10#S3","Collective information#S294":"Article 10#S4","Collective information#S295":"Article 10#S5","Collective information#S298":"Article 10#S8","Collective information#S150":"Article 6#S1","Collective information#S153":"Article 6#S4","Collective information#S161":"Article 6#S12","Collective information#S168":"Article 6#S19","Collective information#S172":"Article 6#S23","Collective information#S178":"Article 6#S29"};
const COLUMNS=["project","occurrence_id","proposal_section","short_text","claude_proposed_state","same_text_as","editorial_approval","publication_status","tam_source_commit","manuscript_git_blob"];
const MANUSCRIPT="b015fab385b0baf68d88956cb86888b094a69ca2", SOURCE_COMMIT="d46456a18fe412398d0ae37ec5a8c4eebb44e0c9";
function audit(text) {
 if(typeof text!=="string")throw Error("invalid register");
 const lines=text.trimEnd().split(/\r?\n/),header=lines.shift().split("\t");
 if(JSON.stringify(header)!==JSON.stringify(COLUMNS))throw Error("header changed");
 if(lines.length!==82)throw Error("expected exactly 82 rows");
 const seen=new Set(),byId=new Map();
 for(let i=0;i<lines.length;i++){
  const c=lines[i].split("\t");if(c.length!==COLUMNS.length)throw Error("malformed row "+i);
  const [project,id,section,short,proposal,copy,approval,status,commit,blob]=c;
  if(project!=="F-001"||id!==EXPECTED_IDS[i]||seen.has(id))throw Error("unknown/duplicate/out-of-order ID "+i);
  seen.add(id);
  if(!/^§(?:142|144|145|147|148|149|150|153|155|156)$/.test(section)||!short.trim()||!proposal.trim())throw Error("missing proposal evidence");
  if(copy!==(COPIES[id]||""))throw Error("copy provenance changed "+id);
  if(approval!=="PROPOSED_NOT_APPROVED"||status!=="HOLD / NOT LAUNCH-READY")throw Error("approval/release boundary changed");
  if(commit!==SOURCE_COMMIT||blob!==MANUSCRIPT)throw Error("source pin mismatch");
  byId.set(id,{section,copy});
 }
 for(const [id,orig] of Object.entries(COPIES))if(!byId.has(orig)||!byId.has(id))throw Error("unresolved exact-text copy");
 return {project:"F-001",occurrences:82,claude_proposed:82,final_approved:0,copies:Object.keys(COPIES).length,publication_authorized:false,status:"HOLD / NOT LAUNCH-READY",manuscript_git_blob:MANUSCRIPT,source_commit:SOURCE_COMMIT};
}
if(typeof module!=="undefined")module.exports={audit};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs");if(process.argv.length!==3){console.error("usage: node F-001-EDITORIAL-DECISIONS-GATE-458.js REGISTER.tsv");process.exit(2)}
 try{console.log(JSON.stringify(audit(fs.readFileSync(process.argv[2],"utf8")),null,2))}
 catch(e){console.error("F-001 HOLD: "+e.message);process.exit(2)}
}
