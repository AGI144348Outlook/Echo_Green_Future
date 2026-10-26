/* F-001 TAM public-source rounding audit, GPT Run373.
   HOLD-only pure function, no I/O or publication authority.
   Assumptions: positive masses displayed to 0.01g, nearest interval
   [m-.005,m+.005); percentages to 0.01 point; <0.01 means absolute.
   Source pins are external; this function does not compute hashes.
*/
function auditF001Rounding(textA, textB) {
  const a = textA.split(/\r?\n/).map(s => s.match(/^(.+?) ([0-9.]+)g ([0-9.]+) Units? \(([^)]+)\) ([<+-]?[0-9.]+)\\% (.+)$/)).filter(Boolean)
    .map(m => {
      const name=m[1], mass=Number(m[2]), units=Number(m[3]), claim=m[5];
      const expected=13.7*units, nominal=100*(mass-expected)/expected;
      const lower=100*(mass-.005-expected)/expected;
      const upper=100*(mass+.005-expected)/expected;
      const claimLower=claim.startsWith("<")?-.01:Number(claim)-.005;
      const claimUpper=claim.startsWith("<")?.01:Number(claim)+.005;
      return {name,mass_g:mass,units,claim,term:m[6],expected_g:expected,
        nominal_deviation_pct:nominal,possible_pct_interval:[lower,upper],
        claim_pct_interval:[claimLower,claimUpper],
        possible_under_assumptions:lower<claimUpper&&upper>claimLower};
    });
  const b = textB.split(/\r?\n/).map(s => s.match(/^(\d+) ([0-9.]+)g (.+?) ((?:\d+\/\d+)|(?:\d+(?:\.\d+)?)) Units? (.+)$/)).filter(Boolean)
    .map(m => {
      const ratio=Number(m[1]), mass=Number(m[2]), unitsLabel=m[4];
      const units=unitsLabel.includes("/")?Number(unitsLabel.split("/")[0])/Number(unitsLabel.split("/")[1]):Number(unitsLabel);
      const expected=13.7*units, tol=1e-10;
      return {ratio,mass_g:mass,units_label:unitsLabel,relation:m[5],expected_g:expected,
        nearest_half_up_possible:expected>=mass-.005-tol&&expected<mass+.005-tol,
        truncation_possible:expected>=mass-tol&&expected<mass+.01-tol,
        exactly_half_cent_tie:Math.abs(Math.abs(expected-mass)-.005)<tol,
        ratio_over_16_matches_units:Math.abs(ratio/16-units)<tol};
    });
  return {status:"REVIEW_ONLY_HOLD",assumptions:"nearest 0.01g; percentage rounded to 0.01 point; <0.01 means absolute deviation",A:a,B:b};
}
if (typeof module !== "undefined" && module.exports) module.exports = {auditF001Rounding};
