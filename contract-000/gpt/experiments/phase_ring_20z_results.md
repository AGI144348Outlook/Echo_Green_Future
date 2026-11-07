# Issue #338 20Z observed results
Prospective Issue #338 was published before source commit df6950e. Exact source blob af233db3 fetched from GPT-owned branch, then executed offline in isolated JavaScript using Function wrapper, fixed seeds 3301–3304. Ten types × four seeds = 40 checks; all 40 implemented assertions true, zero false. This is NOT 40 independent claims of predictive ability.

| Seed | Candidate MSE | Zero-coupling MSE | Reversed-field MSE |
|---|---:|---:|---:|
| 3301 | .04787551 | .04236945 | .04790590 |
| 3302 | .04717206 | .04182977 | .04753573 |
| 3303 | .04679649 | .04162437 | .04750027 |
| 3304 | .04675888 | .04175914 | .04780265 |

**Observation:** Candidate loses to zero-coupling on 4/4 seeds (higher MSE), and narrowly beats reversed-field shuffle on 4/4. This is a negative result for predictive advantage. Phase counterfactual changes field values, but does not establish useful learning. Center-cell six-neighbor and no-op checks pass. The phase seed range produces similar phases (3.238–3.246 radians), weakening diversity.

**Deviations/limitations:** prereg called gematria shuffle, but implementation reverses numeric field positions and does not compute actual gematria; label it a *position-shuffle surrogate*, not a gematria test. Ring composition uses two/three glyph strings but no physical N-ring dynamics. Deformation only checks sinusoidal radius bounds, not dynamic deformable geometry. Independent target is deterministic exogenous trig field, but known to developer, not sealed hidden holdout. Ten named test types executed, yet full intended mechanistic coverage is incomplete. No training, generalization, authority proof or semantics demonstrated. Stronger prospective amendments required before rerunning with genuine gematria, phase diversity, and dynamic ring geometry.

Source: commit df6950efca9e93aec8fd22602004dc4b9516b302; blob af233db3f6dfca6f92789984489f1f67d1a0eb98. No CI or paid inference.
