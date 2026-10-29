"use strict";
/* F-001 Run448: source-bound, non-release Article 1 dual-grid arithmetic.
 * Input is the original Dataset A UTF-8 text. No historical attribution is inferred.
 * The alternative 11.4g grid is a proposed gerah-based interpretation, not an authenticated standard.
 */
const LABELS = ["Ingot Slice (Heavy)", "Coiled Wire (Large)", "Hacksilber Scraps (x3)", "Flattened Foil", "Silver Droplet", "Small Scrap"];
const INDUS = [[10,1],[5,1],[1,1],[1,2],[1,4],[1,8]].map(([n,d]) => 13700*n/d);
const SHEKEL = [[12,1],[6,1],[6,5],[3,5],[3,10],[3,20]].map(([n,d]) => 11400*n/d);
const PIN = "b62c970a660e0a6685b58db1ef121690daa4fce7";
function parseRows(source) {
  if (!source.includes("Re-calculated for 13.7g Invariant")) throw Error("source header/provenance marker missing");
  const lines = source.split(/\r?\n/);
  return LABELS.map(name => {
    const found = lines.filter(line => line.startsWith(name + " "));
    if (found.length !== 1) throw Error("missing/duplicate row: " + name);
    const m = found[0].slice(name.length).match(/^\s+(\d+\.\d+)g\b/);
    if (!m) throw Error("malformed mass: " + name);
    return {name, mg: Math.round(Number(m[1])*1000)};
  });
}
function nearest(mg, grid) {
  return grid.map(target_mg => ({target_mg, delta_mg:mg-target_mg, percent:100*(mg-target_mg)/target_mg}))
    .sort((a,b) => Math.abs(a.delta_mg)-Math.abs(b.delta_mg))[0];
}
function analyze(source) {
  const rows = parseRows(source).map(row => ({...row, indus:nearest(row.mg,INDUS), shekel:nearest(row.mg,SHEKEL)}));
  return {rows, max_abs_percent:{indus:Math.max(...rows.map(r=>Math.abs(r.indus.percent))),
    shekel:Math.max(...rows.map(r=>Math.abs(r.shekel.percent)))},
    interpretation:"HOLD: arithmetic fit is not evidence of independent archaeological provenance, model uniqueness, or publication approval."};
}
if (typeof module !== "undefined") module.exports = {parseRows,nearest,analyze,PIN};
if (typeof require !== "undefined" && require.main === module) {
  const fs=require("fs"), crypto=require("crypto");
  const raw=fs.readFileSync(process.argv[2]);
  const sha=crypto.createHash("sha1").update("blob "+raw.length+"\0").update(raw).digest("hex");
  if (sha !== PIN) { console.error("FAIL: Dataset A Git blob mismatch: "+sha); process.exit(2); }
  console.log(JSON.stringify({git_blob:sha,...analyze(raw.toString("utf8"))},null,2));
}