/* F-001 TAM editorial reconciliation, GPT Run 376.
   Read-only review; not a release gate. Node: node f001_editorial_reconcile_376.js A.csv B.csv
   In browser/V8: reconcile(aCsvText,bCsvText). */
function parseCSV(text) {
  const rows=[]; let row=[], field="", quoted=false;
  for(let i=0;i<text.length;i++){
    const c=text[i];
    if(quoted){if(c==='"' && text[i+1]==='"'){field+='"';i++;}
      else if(c==='"') quoted=false; else field+=c;}
    else if(c==='"' && field==="") quoted=true;
    else if(c===','){row.push(field);field="";}
    else if(c==='\n'){row.push(field.replace(/\r$/,""));rows.push(row);row=[];field="";}
    else field+=c;
  }
  if(quoted) throw Error("unclosed CSV quote");
  if(field!==""||row.length){row.push(field.replace(/\r$/,""));rows.push(row);}
  const header=rows.shift();if(!header) throw Error("missing header");
  return rows.map((cells,i)=>{if(cells.length!==header.length)throw Error("column mismatch at "+(i+2));
    return Object.fromEntries(header.map((h,j)=>[h,cells[j]]));});
}
function num(s){if(!/^[-+]?\d+(?:\.\d+)?$/.test(String(s)))throw Error("invalid number: "+s);return Number(s);}
function units(s){const t=String(s).split("/");return t.length===2?num(t[0])/num(t[1]):num(s);}
function close(x,y,t=0.001){return Math.abs(x-y)<=t;}
function reconcile(aText,bText){
  const A=parseCSV(aText),B=parseCSV(bText),checks=[],add=(name,ok)=>checks.push({name,pass:!!ok});
  add("A has 6 rows",A.length===6);add("B has 8 rows",B.length===8);
  add("A has expected 9 columns",A.every(x=>Object.keys(x).length===9));
  add("B has expected 8 columns",B.every(x=>Object.keys(x).length===8));
  const rowsA=A.map((r,i)=>{
    const expected=13.7*units(r.units),pct=(num(r.measured_g)-expected)/expected*100;
    const flags=[];
    if(r.stated_matches_recomputed==="False")flags.push("SOURCE_FLAGGED_DEVIATION");
    if(r.object==="Small Scrap")flags.push("A_GERAH_1_8_LABEL");
    add("A"+(i+1)+" expected mass",close(num(r.expected_g),expected,0.0001));
    add("A"+(i+1)+" recomputed percent",close(num(r.recomputed_deviation_pct),pct,0.0006));
    return {dataset:"A",csv_line:i+2,object:r.object,units:r.units,measured_g:r.measured_g,
      stated_deviation_pct:r.stated_deviation_pct,computed_pct:Number(pct.toFixed(5)),
      source_matches:r.stated_matches_recomputed,flags,status:"EDITORIAL_REVIEW_ONLY"};
  });
  const rowsB=B.map((r,i)=>{
    const u=units(r.units),expected=13.7*u,pct=(num(r.mass_g)-expected)/expected*100;
    const flags=[];
    if(r.ratio==="1")flags.push("B_GERAH_1_16_LABEL","B_0_85_DISPLAY_PRECISION");
    const match=rowsA.find(a=>close(units(a.units),u,1e-12));
    const diff=match?Number((num(r.mass_g)-num(match.measured_g)).toFixed(4)):null;
    if(match && !close(diff,0,0.0001))flags.push("SAME_UNIT_DISTINCT_DISPLAY_MASS");
    add("B"+(i+1)+" ratio/16",close(num(r.ratio)/16,u,1e-12));
    add("B"+(i+1)+" expected mass",close(num(r.expected_g_from_units),expected,0.0001));
    add("B"+(i+1)+" deviation",close(num(r.deviation_pct),pct,0.006));
    return {dataset:"B",csv_line:i+2,ratio:r.ratio,units:r.units,mass_g:r.mass_g,
      relation_to_dataset_a:r.relation_to_dataset_a,computed_pct:Number(pct.toFixed(5)),
      comparable_a_object:match?.object||null,mass_delta_vs_a_g:diff,flags,status:"EDITORIAL_REVIEW_ONLY"};
  });
  const flaggedA=rowsA.filter(x=>x.flags.includes("SOURCE_FLAGGED_DEVIATION"));
  add("exact A source flags",flaggedA.length===2&&flaggedA.map(x=>x.object).join("|")==="Silver Droplet|Small Scrap");
  add("A Gerah at 1/8",rowsA.some(x=>x.object==="Small Scrap"&&x.units==="0.125"));
  add("B Gerah at 1/16",rowsB[0].ratio==="1"&&rowsB[0].units==="1/16"&&rowsB[0].relation_to_dataset_a.includes("Gerah"));
  add("B first 0.85",rowsB[0].mass_g==="0.85");
  add("A/B 14 provenance rows",rowsA.length+rowsB.length===14);
  const ok=checks.every(x=>x.pass);
  return {project_id:"F-001",status:"HOLD_EDITORIAL_REVIEW",release_authorized:false,
    evidence_kind:"DERIVED_LEGACY_CSV_NOT_ORIGINAL_HISTORICAL_PROOF",
    checks:{passed:checks.filter(x=>x.pass).length,total:checks.length,all_pass:ok,detail:checks},
    editorial_questions:[
      "Explain or qualify Dataset A Silver Droplet and Small Scrap deviation flags; do not silently correct original figures.",
      "Resolve Gerah terminology: Dataset A labels 1/8 U, Dataset B labels 1/16 U; preserve both pending author decision.",
      "Explain Dataset B 0.85 g display versus 0.85625 g model at 1/16 U; truncation is a hypothesis, not established source method.",
      "Qualify same-unit A/B displayed mass differences (0.01-0.02 g); distinct objects/precision may explain them.",
      "Resolve Article 4, source rights/licence, claim worksheet and publication choices before release."
    ],rows:[...rowsA,...rowsB]};
}
if(typeof require==="function" && typeof module!=="undefined" && require.main===module){
  const fs=require("fs");
  if(process.argv.length!==4){console.error("usage: node f001_editorial_reconcile_376.js A.csv B.csv");process.exit(2);}
  const out=reconcile(fs.readFileSync(process.argv[2],"utf8"),fs.readFileSync(process.argv[3],"utf8"));
  process.stdout.write(JSON.stringify(out,null,2)+"\n");
  if(!out.checks.all_pass)process.exitCode=1;
}
if(typeof module!=="undefined")module.exports={reconcile,parseCSV};
