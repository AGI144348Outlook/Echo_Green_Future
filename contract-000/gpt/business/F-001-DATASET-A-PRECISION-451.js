"use strict";
/* F-001 Run451: offline Dataset A arithmetic/precision audit.
   Inputs transcribed from public TAM Dataset A b62c970a and Claude §150 script
   9eacd87b; not archaeological object-level measurements.
   Units: mass_centi = 0.01g, target_ten_thousandth = 0.0001g.
   Release always HOLD. No filesystem, network or dependencies.
*/
const ROWS = Object.freeze([
  {id:"heavy", mass_centi:13698, n:10, d:1, alt_n:12, alt_d:1, printed:"-0.01"},
  {id:"wire", mass_centi:6852, n:5, d:1, alt_n:6, alt_d:1, printed:"+0.03"},
  {id:"scraps", mass_centi:1371, n:1, d:1, alt_n:6, alt_d:5, printed:"+0.07"},
  {id:"foil", mass_centi:686, n:1, d:2, alt_n:3, alt_d:5, printed:"+0.14"},
  {id:"droplet", mass_centi:342, n:1, d:4, alt_n:3, alt_d:10, printed:"-0.03"},
  {id:"small", mass_centi:171, n:1, d:8, alt_n:3, alt_d:20, printed:"<0.01"}
]);
function audit(rows=ROWS) {
  if (!Array.isArray(rows) || rows.length!==6 || new Set(rows.map(r=>r.id)).size!==6)
    throw new Error("Require six distinct source rows");
  const report=rows.map(r=>{
    for(const k of ["mass_centi","n","d","alt_n","alt_d"])
      if(!Number.isSafeInteger(r[k]) || r[k]<=0) throw new Error("Invalid rational input "+k);
    const numerator=137000*r.n, altNumerator=114000*r.alt_n;
    if(numerator%r.d || altNumerator%r.alt_d) throw new Error("Nonintegral 0.0001g target");
    const target=numerator/r.d, alt=altNumerator/r.alt_d;
    const measured=r.mass_centi*100;
    const residual=measured-target, altResidual=measured-alt;
    const deviation=100*residual/target;
    const printedOk=r.printed.startsWith("<")
      ? Math.abs(deviation)<0.01
      : Number.isFinite(Number(r.printed)) && Math.abs(deviation-Number(r.printed))<0.01;
    return {id:r.id, mass_g:measured/10000, target_13_7_g:target/10000,
      target_alt_g:alt/10000, residual_g:residual/10000,
      alt_residual_g:altResidual/10000, deviation_percent:deviation,
      printed:r.printed, printed_consistent:printedOk,
      within_display_rounding:Math.abs(residual)<=50,
      alt_within_display_rounding:Math.abs(altResidual)<=50,
      exact_menu_ratio_6_over_5:5*r.alt_n*r.d===6*r.n*r.alt_d};
  });
  return {status:"HOLD", evidence:"arithmetic-only-derived-table",
    rows:report, printed_mismatches:report.filter(x=>!x.printed_consistent).map(x=>x.id),
    original_rounding_matches:report.filter(x=>x.within_display_rounding).map(x=>x.id),
    alternative_rounding_matches:report.filter(x=>x.alt_within_display_rounding).map(x=>x.id),
    all_ratios_6_over_5:report.every(x=>x.exact_menu_ratio_6_over_5)};
}
function tests() {
  let passed=0;const check=(condition,label)=>{if(!condition)throw new Error("FAIL "+label);passed++};
  const r=audit();
  check(r.status==="HOLD","release hold");
  check(r.rows.length===6,"six rows");
  check(r.printed_mismatches.join(",")==="droplet,small","two printed mismatches");
  check(r.original_rounding_matches.join(",")==="droplet,small","13.7 display rounding 2/6");
  check(r.alternative_rounding_matches.join(",")==="droplet,small","13.68 display rounding 2/6");
  check(r.all_ratios_6_over_5,"exact fraction menu rescaling");
  check(r.rows[0].residual_g===-0.02 && r.rows[1].residual_g===0.02,"large residuals exceed 0.005g");
  check(r.rows[4].residual_g===-0.005 && r.rows[5].residual_g===-0.0025,"small residuals");
  check(r.rows[4].deviation_percent<-.14 && r.rows[5].deviation_percent<-.14,"small percent errors");
  try{audit(ROWS.slice(1))}catch(e){check(/six distinct/.test(e.message),"missing row rejected")}
  try{audit([...ROWS.slice(0,5),ROWS[4]])}catch(e){check(/six distinct/.test(e.message),"duplicate row rejected")}
  try{audit(ROWS.map((r,i)=>i===0?{...r,d:0}:r))}catch(e){check(/Invalid rational/.test(e.message),"invalid fraction rejected")}
  if(passed!==12)throw new Error("Expected 12 assertions; got "+passed);
  return {passed,report:r};
}
if(typeof module!=="undefined")module.exports={ROWS,audit,tests};
