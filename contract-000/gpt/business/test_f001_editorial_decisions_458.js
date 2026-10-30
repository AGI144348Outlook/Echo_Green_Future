#!/usr/bin/env node
"use strict";
/* Run458 reproducible integrity tests. No EPUB/reader/Genesis execution. */
const fs=require("fs"),assert=require("assert"),{audit}=require("./F-001-EDITORIAL-DECISIONS-GATE-458.js");
const base=fs.readFileSync(process.argv[2]||__dirname+"/F-001-EDITORIAL-DECISIONS-458.tsv","utf8");
const cases=[];
function run(name,edit,accept=false){let a=base.trimEnd().split("\n");if(edit)edit(a);let ok=false;try{const x=audit(a.join("\n")+"\n");ok=accept&&x.occurrences===82&&x.final_approved===0;}catch(e){ok=!accept;}assert(ok,name);cases.push(name);}
run("valid exact 82-source register",null,true);
run("missing row rejected",a=>a.pop());
run("duplicate row rejected",a=>a[3]=a[2]);
run("unknown occurrence rejected",a=>a[5]=a[5].replace("Article","Alien"));
run("reorder rejected",a=>{[a[3],a[4]]=[a[4],a[3]]});
run("forged approval rejected",a=>a[2]=a[2].replace("PROPOSED_NOT_APPROVED","APPROVED"));
run("release status rejected",a=>a[2]=a[2].replace("HOLD / NOT LAUNCH-READY","LAUNCH READY"));
run("source pin mutation rejected",a=>a[2]=a[2].replace("d46456a18fe412398d0ae37ec5a8c4eebb44e0c9","0000000000000000000000000000000000000000"));
run("copy link mutation rejected",a=>{const i=a.findIndex(x=>x.includes("Collective information#S293"));a[i]=a[i].replace("Article 10#S3","Article 10#S5")});
run("empty proposed state rejected",a=>{const z=a[2].split("\t");z[4]="";a[2]=z.join("\t")});
run("unexpected section rejected",a=>{const z=a[2].split("\t");z[2]="§999";a[2]=z.join("\t")});
console.log(JSON.stringify({passed:cases.length,total:11,cases},null,2));
