"use strict";
/* Contract-000 GPT Run449. F-001 Article 1 model-grid sensitivity audit.
 * Reproduces arithmetic on exactly the six public Dataset A masses.
 * Alternative 11.4g menu is a HYPOTHETICAL reparameterization, not a
 * historically authenticated Levantine/Egyptian weight standard.
 * No archaeological inference, release decision or source rewrite.
 */
const PIN = "b62c970a660e0a6685b58db1ef121690daa4fce7";
const LABELS = ["Ingot Slice (Heavy)","Coiled Wire (Large)","Hacksilber Scraps (x3)","Flattened Foil","Silver Droplet","Small Scrap"];
const ORIGINAL = [[10,1],[5,1],[1,1],[1,2],[1,4],[1,8]];
const ALTERNATIVE = [[12,1],[6,1],[6,5],[3,5],[3,10],[3,20]];
function parseRows(source) {
  if (!source.includes("Re-calculated for 13.7g Invariant")) throw Error("provenance marker missing");
  const lines = source.split(/\r?\n/);
  return LABELS.map(name => {
    const found = lines.filter(s => s.startsWith(name + " "));
    if (found.length !== 1) throw Error("missing/duplicate row: "+name);
    const m = found[0].slice(name.length).match(/^\s+(\d+\.\d+)g\b/);
    if (!m) throw Error("invalid mass: "+name);
    return {name,mg:Math.round(Number(m[1])*1000)};
  });
}
function fit(rows,base_mg,menu) {
  const fitted = rows.map(r => {
    const targets=menu.map(([n,d]) => ({fraction:`${n}/${d}`,target_mg:base_mg*n/d}));
    const nearest=targets.sort((a,b)=>Math.abs(r.mg-a.target_mg)-Math.abs(r.mg-b.target_mg))[0];
    return {name:r.name,measured_mg:r.mg,...nearest,delta_mg:r.mg-nearest.target_mg,
      abs_percent:100*Math.abs(r.mg-nearest.target_mg)/nearest.target_mg};
  });
  const abs=fitted.map(x=>x.abs_percent);
  return {fitted,max_abs_percent:Math.max(...abs),mean_abs_percent:abs.reduce((a,b)=>a+b,0)/abs.length,
    leave_one_out_max:fitted.map((x,i)=>({omitted:x.name,max_abs_percent:Math.max(...abs.filter((_,j)=>i!==j))}))};
}
function audit(source) {
  const rows=parseRows(source);
  const scaling=ORIGINAL.map(([n,d],i)=>{const [m,q]=ALTERNATIVE[i];return m*d*5===n*q*6});
  return {rows,original:fit(rows,13700,ORIGINAL),alternative:fit(rows,11400,ALTERNATIVE),
    controlled_same_fractions_114:fit(rows,11400,ORIGINAL),
    alternative_is_exact_6_over_5_scaling:scaling.every(Boolean),
    alternative_effective_base_mg:11400*6/5,
    provenance:"Dataset A is explicitly recalculated for 13.7g; neither menu establishes a historical standard."};
}
if (typeof module !== "undefined") module.exports={PIN,LABELS,ORIGINAL,ALTERNATIVE,parseRows,fit,audit};
if (typeof require !== "undefined" && require.main === module) {
  const fs=require("fs"),crypto=require("crypto");
  if (process.argv.length!==3) {console.error("Usage: node F-001-ARTICLE1-GRID-AUDIT-449.js <pinned-Dataset-A-file>");process.exit(2);}
  const bytes=fs.readFileSync(process.argv[2]);
  const sha=crypto.createHash("sha1").update("blob "+bytes.length+"\0").update(bytes).digest("hex");
  if (sha!==PIN) {console.error("FAIL: Git blob mismatch "+sha);process.exit(2);}
  console.log(JSON.stringify({git_blob:sha,...audit(bytes.toString("utf8"))},null,2));
}
