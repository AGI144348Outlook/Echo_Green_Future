/* F-001 precision audit — ChatGPT Run 359. HOLD-only; arithmetic is not historical truth or release authority.
Node CLI: node F-001-PRECISION-AUDIT-359.js dataset-a.csv dataset-b.csv
No external dependencies, network, file mutations, or assumed scientific tolerance. */
"use strict";
const S=1000000n, HALF=5000n, BASE=13700000n;
function dec(s){
  const m=/^([+-]?)(\d+)(?:\.(\d{1,6}))?$/.exec(String(s).trim());
  if(!m)throw Error("invalid decimal: "+s);
  return (m[1]==="-"?-1n:1n)*(BigInt(m[2])*S+BigInt((m[3]||"").padEnd(6,"0")||"0"));
}
function units(s){
  const f=/^(\d+)\/(\d+)$/.exec(String(s).trim());
  if(!f)return dec(s);
  const n=BigInt(f[1]),d=BigInt(f[2]);
  if(d===0n||n*S%d!==0n)throw Error("nonrepresentable fraction: "+s);
  return n*S/d;
}
function fmt(v){const sign=v<0n?"-":"";if(v<0n)v=-v;return sign+(v/S)+"."+(v%S).toString().padStart(6,"0");}
function pct(m,e){return Number((m-e)*100n*S/e)/Number(S);}
function parseCsv(s){
  const rows=[];let row=[],cell="",q=false;
  for(let i=0;i<s.length;i++){
    const c=s[i];
    if(q){if(c==='"'&&s[i+1]==='"'){cell+='"';i++;}else if(c==='"')q=false;else cell+=c;}
    else if(c==='"'){if(cell)throw Error("invalid quote");q=true;}
    else if(c===','){row.push(cell);cell="";}
    else if(c==='\n'){row.push(cell.replace(/\r$/,""));rows.push(row);row=[];cell="";}
    else cell+=c;
  }
  if(q)throw Error("unterminated quote");
  if(cell||row.length){row.push(cell.replace(/\r$/,""));rows.push(row);}
  const header=rows.shift();
  if(!header||new Set(header).size!==header.length)throw Error("missing/duplicate header");
  return rows.filter(r=>!(r.length===1&&!r[0])).map(r=>{
    if(r.length!==header.length)throw Error("CSV column mismatch");
    return Object.fromEntries(header.map((h,i)=>[h,r[i]]));
  });
}
function auditDatasets(csvA,csvB){
  const out={status:"HOLD / NOT RELEASE EVIDENCE",assumptions:{
    base_g_per_unit:"13.7",mass_printed_precision_g:"0.01",
    measured_mass_interval:"printed ±0.005 g; endpoints included conservatively for rounding ties",
    numeric_deviation_claim:"printed percent ±0.005 percentage points",
    less_than_claim:"<0.01 means absolute deviation <0.01 percent",
    mass_accuracy_tolerance:"NONE ADOPTED"},A:[],B:[]};
  for(const r of parseCsv(csvA)){
    const m=dec(r.measured_g),u=units(r.units),e=BASE*u/S;
    if(e<=0n)throw Error("A invalid expected mass");
    const lo=m-HALF,hi=m+HALF,L=(lo-e)*100n*S,H=(hi-e)*100n*S;
    const claim=r.stated_deviation_pct.trim();
    let compatible;
    if(claim==="<0.01"){const bound=dec("0.01");compatible=H>-(e*bound)&&L<e*bound;}
    else{const p=dec(claim),delta=dec("0.005");compatible=H>=e*(p-delta)&&L<=e*(p+delta);}
    out.A.push({object:r.object,measured_g:r.measured_g,units:r.units,expected_g:fmt(e),
      stated_deviation_pct:claim,builder_point_flag:r.stated_matches_recomputed,
      point_deviation_pct:pct(m,e),mass_interval_g:[fmt(lo),fmt(hi)],
      deviation_interval_pct:[pct(lo,e),pct(hi,e)],claimed_band_intersects_mass_precision:compatible});
  }
  for(const r of parseCsv(csvB)){
    const ratio=BigInt(r.ratio),m=dec(r.mass_g),u=units(r.units),e=BASE*ratio/16n;
    if(ratio<=0n||e<=0n)throw Error("B invalid ratio");
    const lo=m-HALF,hi=m+HALF;
    out.B.push({ratio:r.ratio,mass_g:r.mass_g,units:r.units,expected_g:fmt(e),
      ratio_units_exact:u===ratio*S/16n,point_deviation_pct:pct(m,e),
      expected_within_nearest_cent_interval:lo<=e&&e<=hi,
      rounding_tie_boundary:lo===e||hi===e,mass_interval_g:[fmt(lo),fmt(hi)]});
  }
  out.summary={A_rows:out.A.length,A_builder_false:out.A.filter(x=>x.builder_point_flag==="False").length,
    A_claim_interval_challenges:out.A.filter(x=>!x.claimed_band_intersects_mass_precision).map(x=>x.object),
    B_rows:out.B.length,B_ratio_unit_failures:out.B.filter(x=>!x.ratio_units_exact).map(x=>x.ratio),
    B_nearest_cent_incompatible:out.B.filter(x=>!x.expected_within_nearest_cent_interval).map(x=>x.ratio),
    B_tie_boundaries:out.B.filter(x=>x.rounding_tie_boundary).map(x=>x.ratio)};
  return out;
}
if(typeof module!=="undefined"){
  module.exports={auditDatasets,parseCsv};
  if(require.main===module){
    const fs=require("fs");
    if(process.argv.length!==4){console.error("usage: node script A.csv B.csv");process.exit(2);}
    console.log(JSON.stringify(auditDatasets(fs.readFileSync(process.argv[2],"utf8"),fs.readFileSync(process.argv[3],"utf8")),null,2));
  }
}
