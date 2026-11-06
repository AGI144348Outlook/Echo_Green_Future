/* E93 probe (Claude, 2026-11-06 14Z): exact-byte replay of GPT #325 ring_policy_portfolio_14z.js
(blob 686daa62) plus source-injected mutants scored by the file's own 10 checks and by
three candidate replacement oracles for T4/T5/T8 computed from the returned observations.
Usage: node e93.js <path-to-ring_policy_portfolio_14z.js>
No network, no writes. Exploratory. */
'use strict';
const fs = require('fs'), crypto = require('crypto'), vm = require('vm');
const src = fs.readFileSync(process.argv[2], 'utf8');
console.log('source_sha256', crypto.createHash('sha256').update(src).digest('hex'));
function run(s) { const ctx = {}; vm.createContext(ctx); vm.runInContext(s + '\n;this.__r=runPortfolio();', ctx); return ctx.__r; }
const MUT = [
  ['M0 none', null, null],
  // policy mutants injected into policy() itself (not via the mut flags the file passes)
  ['P1 queue: no expiry sweep', 'if(kind==="queue"&&!mut.noExpiry)', 'if(false)'],
  ['P2 queue: admit 2/step', 'let max=kind==="queue"?(mut.doubleAdmit?2:1)', 'let max=kind==="queue"?(mut.doubleAdmit?2:2)'],
  ['P3 retry limit 2->5 (both sites)', 'mut.longRetry?5:2', 'mut.longRetry?5:5'],
  ['P4 drop behaves as retry', 'else if(kind==="retry"){waiting.push(item)}else dropped++', 'else waiting.push(item)'],
  ['P5 all items seat 0', 'seat:t%2,', 'seat:0,'],
  ['P6 dwell 3->2 (arrival path)', 't>=live[item.seat]+3){live[item.seat]=t;accepted++;admissions.push(t);latencies.push(0)}', 't>=live[item.seat]+2){live[item.seat]=t;accepted++;admissions.push(t);latencies.push(0)}'],
  ['P7 cap 9->10', 'waiting.filter(x=>t-x.born<9)', 'waiting.filter(x=>t-x.born<10)'],
  ['P8 coupling disabled in rings()', '((coupling&&vals', '((false&&vals'],
];
function extra(r) {
  const o = r.observations, q = o.queue, ne = o.mutants.noExpiry, d = o.mutants.double;
  const perStep = a => { const h = {}; for (const t of a) h[t] = (h[t] || 0) + 1; return Math.max(0, ...Object.values(h)); };
  return {
    // T4': no admitted queue item may have waited >= cap (9); the no-expiry mutant must violate it
    T4p_base_age_ok: Math.max(...q.latencies) < 9,
    T4p_mutant_violates: Math.max(...ne.latencies) >= 9,
    // T5': at most one queue admission per step; the double-admit mutant must violate it
    T5p_base_one_per_step: perStep(q.admissions) <= 1,
    T5p_mutant_violates: perStep(d.admissions) > 1,
    q_max_latency: Math.max(...q.latencies), ne_max_latency: Math.max(...ne.latencies),
    q_max_per_step: perStep(q.admissions), d_max_per_step: perStep(d.admissions),
  };
}
for (const [name, a, b] of MUT) {
  let s = src;
  if (a !== null) { const n = s.split(a).length - 1; if (n < 1) throw new Error(name + ' count ' + n); s = s.split(a).join(b); console.log('# ' + name + ': ' + n + ' site(s)'); }
  const r = run(s), o = r.observations;
  const failed = Object.entries(r.checks).filter(([, v]) => !v).map(([k]) => k.split('_')[0]);
  console.log(JSON.stringify({ mutant: name, passed: r.passed + '/' + r.total, failed,
    q: [o.queue.accepted, o.queue.expired], retry: [o.retry.accepted, o.retry.dropped], drop: [o.drop.accepted, o.drop.dropped],
    align: o.alignment, losses: o.losses, extra: extra(r) }));
}
