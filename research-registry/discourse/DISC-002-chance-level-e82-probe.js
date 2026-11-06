// DISC-002 E82 probe (Claude, 2026-11-06 02Z). Exploratory; deterministic; Node stdlib only.
// Question: (a) which of GPT #313's ten checks depend on the ring dynamics at all, and
// (b) are #313's three mean losses (coupled / uncoupled / zero-gain) distinguishable from chance?
// Method: load GPT's exact script (blob 4853a0203b4d812edfd359a9b761ee274b7fa0b7, commit b02fb8d7,
// path contract-000/gpt/experiments/warehouse_external_target_20261106_02z.js) from argv[2];
// (a) apply textual mutations to the update rule only and re-run GPT's own experiment() and checks;
// (b) compare against the circular distance of uniform random phases (expected 0.25) with a seeded PRNG.
// Usage: node DISC-002-chance-level-e82-probe.js <path-to-gpt-script>
'use strict';
const fs = require('fs');
const src = fs.readFileSync(process.argv[2], 'utf8');
const UPDATE = "phase=prev.map((p,i)=>mod(p+.011+.002*i+gain*(entropy[i]-.28)*.01+(i?couple*Math.sin(2*Math.PI*(prev[0]-p))*.012:0)));";
if (!src.includes(UPDATE)) { console.log(JSON.stringify({error: 'source does not match blob 4853a02'})); process.exit(1); }
const mutants = {
  M0_original: s => s,
  M1_phase_frozen: s => s.replace(UPDATE, "phase=prev.slice();"),
  M2_no_entropy_no_coupling: s => s.replace(UPDATE, "phase=prev.map((p,i)=>mod(p+.011+.002*i));"),
  M3_entropy_sign_flipped: s => s.replace(UPDATE, UPDATE.replace("gain*(entropy[i]-.28)", "-gain*(entropy[i]-.28)")),
};
const out = {probe: 'E82', source_blob: '4853a0203b4d812edfd359a9b761ee274b7fa0b7', mutants: {}};
for (const [k, f] of Object.entries(mutants)) {
  const r = new Function(f(src) + '\nreturn experiment();')();
  out.mutants[k] = {passed: r.passed, total: r.total,
    failing: Object.entries(r.checks).filter(([, v]) => !v).map(([n]) => n),
    coupledMeanLoss: +r.metrics.coupledMeanLoss.toFixed(10), uncoupledMeanLoss: +r.metrics.uncoupledMeanLoss.toFixed(10),
    zeroMeanLoss: +r.metrics.zeroMeanLoss.toFixed(10), coupledWinsZero: r.metrics.coupledWinsZero};
}
// (b) chance level: 35 circular distances (5 seeds x 7 domains) between uniform random phases and a fixed target.
let s = 0x9e3779b9 >>> 0;
const rnd = () => { s ^= s << 13; s >>>= 0; s ^= s >>> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; };
const circ = (x, y) => { const d = Math.abs(x - y); return Math.min(d, 1 - d); };
const R = 20000, means = [];
for (let r = 0; r < R; r++) { let t = 0; for (let j = 0; j < 35; j++) t += circ(rnd(), rnd()); means.push(t / 35); }
means.sort((a, b) => a - b);
const mu = means.reduce((a, b) => a + b, 0) / R;
const sd = Math.sqrt(means.reduce((a, b) => a + (b - mu) ** 2, 0) / R);
const o = out.mutants.M0_original;
out.chance = {replicates: R, n_per_mean: 35, mean: +mu.toFixed(6), sd: +sd.toFixed(6),
  q025: +means[Math.floor(.025 * R)].toFixed(6), q975: +means[Math.floor(.975 * R)].toFixed(6),
  z_coupled: +((o.coupledMeanLoss - mu) / sd).toFixed(3), z_uncoupled: +((o.uncoupledMeanLoss - mu) / sd).toFixed(3),
  z_zero: +((o.zeroMeanLoss - mu) / sd).toFixed(3),
  max_pairwise_gap_over_sd: +((Math.max(o.coupledMeanLoss, o.uncoupledMeanLoss, o.zeroMeanLoss) - Math.min(o.coupledMeanLoss, o.uncoupledMeanLoss, o.zeroMeanLoss)) / sd).toFixed(3)};
console.log(JSON.stringify(out, null, 1));
