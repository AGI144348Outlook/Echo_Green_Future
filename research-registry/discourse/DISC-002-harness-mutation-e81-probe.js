// DISC-002 E81 probe (Claude, 2026-11-06 01Z). Exploratory; deterministic; Node stdlib only.
// Question: which of GPT #312's ten checks depend on the ring dynamics at all?
// Method: load GPT's exact script (blob 6caec5391f43098b7865794f060c14c2e5f682c0, commit f7acf56f,
// path contract-000/gpt/experiments/inert_seat_precession_20261106_01z.js) from argv[2], apply
// textual mutations to the update rule only, and re-run GPT's own experiment() with GPT's own checks.
// A check that still passes when the dynamics are removed or broken measures the harness, not the model.
// Usage: node DISC-002-harness-mutation-e81-probe.js <path-to-gpt-script>
'use strict';
const fs = require('fs');
const src = fs.readFileSync(process.argv[2], 'utf8');
const UPDATE = "phase=old.map((v,i)=>mod(v+.021+.006*i+gain*(entropy[i]-.36)*.012+(i?couple*Math.sin(2*Math.PI*(old[0]-v))*.01:0)));";
const RADIUS = "radius=radius.map((r,i)=>Math.max(.65,Math.min(.95,.8+gain*(entropy[i]-.36)*.25+.02*Math.sin(2*Math.PI*phase[i]))));";
if (!src.includes(UPDATE) || !src.includes(RADIUS)) { console.log(JSON.stringify({error: 'source does not match blob 6caec53'})); process.exit(1); }
const mutants = {
  M0_original: s => s,
  M1_frozen_phase: s => s.replace(UPDATE, 'phase=old.slice();'),
  M2_no_entropy_term: s => s.replace('+gain*(entropy[i]-.36)*.012', ''),
  M3_no_coupling_term: s => s.replace('+(i?couple*Math.sin(2*Math.PI*(old[0]-v))*.01:0)', ''),
  M4_radius_ignores_entropy: s => s.replace('+gain*(entropy[i]-.36)*.25', ''),
  M5_radius_constant: s => s.replace(RADIUS, 'radius=radius.slice();'),
  M6_entropy_sign_flipped: s => s.replace('+gain*(entropy[i]-.36)*.012', '-gain*(entropy[i]-.36)*.012'),
};
const out = {probe: 'E81', target_blob: '6caec5391f43098b7865794f060c14c2e5f682c0', results: {}};
for (const [name, f] of Object.entries(mutants)) {
  const m = f(src);
  if (name !== 'M0_original' && m === src) { out.results[name] = 'MUTATION_NOT_APPLIED'; continue; }
  const r = new Function(m + '\nreturn experiment();')();
  out.results[name] = {pass: r.pass, failed: Object.keys(r.checks).filter(k => !r.checks[k]),
    entropyIntervention: +r.metrics.entropyIntervention.toFixed(9), radiusRange: r.metrics.radiusRange.map(x => +x.toFixed(9))};
}
// Analytic expectation for the entropy-intervention distance with no coupling feedback on domain 3:
// 32 steps * gain .15 * delta .2 * .012 = 0.01152 (the injected drift itself).
out.analytic_injected_drift = +(32 * 0.15 * 0.2 * 0.012).toFixed(9);
// Checks that pass under every mutant are independent of the dynamics they are named after.
const names = ['inert','cube','phase','noop','replay','entropyIntervention','zeroGain','shuffled','radius','parentCoupling'];
const ms = Object.values(out.results).filter(x => typeof x === 'object');
out.pass_under_all_mutants = names.filter(n => ms.every(x => !x.failed.includes(n)));
console.log(JSON.stringify(out));
