"use strict";
// F-001 Run 372 supplementary, HOLD-only structural crosswalk.
// Takes already retrieved text. No filesystem/network, no hashing, no release authority.
// PRE: Echo_Green_Future Issue #56 comment 6416753260.
const A371=["object","measured_g","units","registry_sign","stated_deviation_pct","term","expected_g","recomputed_deviation_pct","stated_matches_recomputed"];
const B371=["ratio","mass_g","registry_sign","units","relation_to_dataset_a","expected_g_from_units","deviation_pct","ratio_over_16_equals_units"];
const A334=["object","measured_g","units","registry_sign","stated_deviation_pct","term","expected_g","recomputed_deviation_pct","within_0_01_pct_points_of_recomputed","calculation_method_from_source","terminology_conflict"];
const B334=[...B371,"terminology_conflict"];
const APIN=[["Ingot Slice (Heavy)","136.98","10.0","UU","-0.01","Maneh (Decimal Base)","137.0","-0.015","True"],["Coiled Wire (Large)","68.52","5.0","U+V","+0.03","5-Shekel (Redemption)","68.5","0.029","True"],["Hacksilber Scraps (x3)","13.71","1.0","U","+0.07","Shekel Ha-Kodesh","13.7","0.073","True"],["Flattened Foil","6.86","0.5","Harrow","+0.14","Beqa (The Half)","6.85","0.146","True"],["Silver Droplet","3.42","0.25","1/4","-0.03","Reva (The Quarter)","3.425","-0.146","False"],["Small Scrap","1.71","0.125","1/8","<0.01","Gerah (Metric Sub-unit)","1.7125","-0.146","False"]];
const BPIN=[["1","0.85","(Stroke)","1/16","Trace/Gerah Base","0.8562","-0.73","True"],["2","1.71","(II)","1/8","Matches \"Small Scrap\"","1.7125","-0.146","True"],["4","3.42","(IIII)","1/4","Matches \"Silver Droplet\"","3.425","-0.146","True"],["8","6.85","Harrow","1/2","The Beqa Invariant","6.85","0.0","True"],["16","13.70","Jar (U)","1.00","The Sanctuary Shekel","13.7","0.0","True"],["32","27.40","U+II","2.00","Commercial Standard","27.4","0.0","True"],["80","68.50","U+V","5.00","Matches \"Coiled Wire\"","68.5","0.0","True"],["160","137.00","UU","10.0","Matches \"Ingot Slice\"","137.0","0.0","True"]];
const SOURCE_A="48437f58ee74a9a0226d901d1291b6c104764648fe7760ebbc91b74b6ba6a302";
const SOURCE_B="bc16da657b19317e110cdcf4159a9118aa89f2cfc4f8183e7e3f1d94f2eb3b81";
function csv(text){
  if(typeof text!=="string"||text.length>100000)throw Error("invalid CSV size/type");
  const out=[];let row=[],field="",q=false,after=false;
  for(let i=0;i<text.length;i++){
    const ch=text[i];
    if(q){if(ch==='"'){if(text[i+1]==='"'){field+='"';i++;}else{q=false;after=true;}}else{field+=ch;}continue;}
    if(ch==='"'){if(field!==""||after)throw Error("invalid quote");q=true;continue;}
    if(after&&ch!==","&&ch!=="\r"&&ch!=="\n")throw Error("text after closing quote");
    if(ch===","){row.push(field);field="";after=false;continue;}
    if(ch==="\n"||ch==="\r"){
      if(ch==="\r"&&text[i+1]==="\n")i++;
      row.push(field);out.push(row);row=[];field="";after=false;continue;
    }
    field+=ch;
  }
  if(q)throw Error("unclosed quote");
  if(field!==""||row.length){row.push(field);out.push(row);}
  if(!out.length)throw Error("empty CSV");
  const header=out.shift();
  if(new Set(header).size!==header.length)throw Error("duplicate header");
  if(out.some(x=>x.length!==header.length))throw Error("ragged CSV");
  return {header,rows:out};
}
function same(a,b){return JSON.stringify(a)===JSON.stringify(b);}
function crosswalk(a,b,reportText){
  const errors=[];
  let A,B,rep;
  try{A=csv(a);B=csv(b);rep=JSON.parse(reportText);}
  catch(e){return {status:"REJECT",release:"HOLD",errors:[String(e.message)],source_rows_usable_for_review:false};}
  if(!same(A.header,A371))errors.push("A Run371 schema mismatch");
  if(!same(B.header,B371))errors.push("B Run371 schema mismatch");
  if(A.rows.length!==6||B.rows.length!==8)errors.push("row count mismatch");
  if(!rep||!rep.files||!rep.files.A||!rep.files.B||rep.files.A.sha256!==SOURCE_A||rep.files.B.sha256!==SOURCE_B||rep.files.A.rows!==6||rep.files.B.rows!==8||!same(rep.files.A.rejected,[])||!same(rep.files.B.rejected,[]))errors.push("source report mismatch");
  if(!errors.length){
    for(let i=0;i<6;i++)if(!same(A.rows[i],APIN[i]))errors.push("A pinned row "+(i+1)+" mismatch");
    for(let i=0;i<8;i++)if(!same(B.rows[i],BPIN[i]))errors.push("B pinned row "+(i+1)+" mismatch");
    if(A.rows.filter(x=>x[8]==="False").length!==2||A.rows.some(x=>!["True","False"].includes(x[8])))errors.push("A deviation flags mismatch");
    if(B.rows.some(x=>x[7]!=="True"))errors.push("B ratio flags mismatch");
  }
  return {status:errors.length?"REJECT":"REVIEW_ONLY",release:"HOLD",source_rows_usable_for_review:errors.length===0,
    a_rows:A.rows.length,b_rows:B.rows.length,errors,
    pinned_334_compatible:false,
    pinned_334_blockers:["Run371 A header 9 fields vs Run334 11","Run371 B header 8 fields vs Run334 9","Run371 report lacks source_commit and git_blob fields","Run371 CSV bytes differ from independent Run334 SHA-256 pins"],
    editorial_flags:["Dataset A two stated/recomputed deviation disagreements","Gerah label differs between datasets"],
    limitations:"Exact 14-row fixture equality from Run371 output only; no independent SHA-256 computed, no Run334 execution, no release authorization."};
}
module.exports={crosswalk,csv,A334,B334,A371,B371};
