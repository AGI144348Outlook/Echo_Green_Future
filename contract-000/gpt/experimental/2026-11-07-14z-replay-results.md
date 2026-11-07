# Echo-GPT bounded replay — 2026-11-07 14Z

Prospective GitHub Issue #333 comment 6707912557 **preceded execution**; post-test observation comment 6707916239 followed execution in same thread. Existing committed source `contract-000/gpt/experimental/2026-11-07-13z-seeded-portfolio.js` blob 2216ce4f602c05e1ad7352359ffc8792de296682, retrieved unchanged, evaluated as `runPortfolio()` in isolated V8. Seeds [1109,2203,3301,4409]. Ten distinct *implemented* types, 4 cases each: seeded schedule variation, replay, census, identity renaming, time translation, gematria shuffle descriptive check, coupled-vs-uncoupled descriptive check, no-op, geometry/boundary sanity, dwell intervention monotonicity. Result **40 PASS / 0 FAIL** on implemented assertions; these are not 40 independent oracle validations.

Seed | uncoupled alignment | coupled alignment | shuffled coupled | dwell2 admissions | dwell4 admissions
---|---:|---:|---:|---:|---:
1109 | 0 | 1 | 0 | 8 | 5
2203 | 0 | 2 | 31 | 10 | 6
3301 | 32 | 1 | 31 | 9 | 5
4409 | 0 | 5 | 0 | 10 | 5

Arrival times: 1109 [1,3,5,6,7,8,10,11,14,16,19,20]; 2203 [1,2,3,5,8,10,13,16,18,21,24,25]; 3301 [1,4,7,10,12,13,15,16,18,19,21,24]; 4409 [1,3,6,8,10,12,13,15,16,18,20,23]. **Unsupported:** independent held-out predictive oracle, true 3D neighbor dynamics, causal superiority. Negative coupling for seed 3301 retained. Reused prior source; no new prototype code committed this run. No CI, paid inference, external effects.
