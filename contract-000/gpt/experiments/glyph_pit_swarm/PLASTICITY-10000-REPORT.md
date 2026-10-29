# Neuroplasticity-informed 10,000 reloads / 9 turns — first execution

Prospective plan: [Issue #109](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/109). User source: `neuroplasticity-candidate-algorithms.pdf`, explicitly PROPOSED alternatives, compiled 2026-10-06.

## Actual local execution
- 27 stationary glyph pit positions, 27 persistent subagent identities; 10,000 reloads, 9 turns per reload = 90,000 turns; 100,000 hashed event receipts per condition.
- **Adaptive condition**: 83,798 / 90,000 = 93.1089% correct on synthetic fixed parity target; 27 accepted tokens, 89,917 token uses; 270,000 per-agent version updates; zero detected persistent identity changes.
- **Non-learning condition**: 45,009 / 90,000 = 50.01% correct; zero tokens.
- Seed 144348; adaptive ledger terminal SHA256 `e13e3ec6cd0b5769bef4f3dbb595656ae7081c7d8d0882d9fa3c99de0bffac4a`; baseline `b717ae5d4b3b3d47fd9b139284fbef512aa25f86f5adddb2113d171eb903a376`.
- **Tests:** first run 9/10 due to a seed parameter not affecting adaptive choice; corrected schedule, reran **10/10 PASS** (includes 10k exact event count, seed variation, replay, identity, token and bounds).
- Exact executed local files and SHA256: `experiment.py` 472cd48439fa63416b6c53e1481d81792e48cb3898f868557a082ddf48ad8cfb; `test_experiment.py` 7c97dbaa739e953ee896394ac300b0a3d3266b96c7655947e8c1b87cbd951a7d; `results.json` 7764167a1b744b6ee960df485cccea459b49f37aa9800d82691a90d59f825b64. These files were generated locally; **not yet committed to this branch**, and GitHub checkout cannot replay until source is uploaded.

## Implementation mapping and limits
- B1-b: per-agent Laplace-smoothed outcomes for choosing two actions; C1-c/E1-a: active then dormant with retained state; D2-a/F2-c: simplistic threshold-based acceptance after >=4 trials and >=3 wins, **not** cost/accuracy validation; F6-a: stable identity with in-place versioned state; G1-a: simplistic downscaling and retention, **no full replay or cleanup**.
- A-000 equation represented only as `origin=Alg-000`, persistent `SUB-` ID and self glyph reference; **not executable recursive composition**. Card domains/operations are synthetic placeholders. The benchmark's target is deterministic glyph-index parity, repeated across all 10k cycles. The adaptive learner is trained and scored on the **same recurring task**; **no held-out generalization evaluation**. The accuracy gap is therefore an in-sample adaptation result, not evidence of generalization, independent algorithm invention, or intelligence. Token acceptance is a simple counter rule, not demonstrated semantic compression.
- Ledger samples and terminal hashes alone cannot audit all 100,000 events without source replay. No main, Claude, Genesis, shared Library or contract edits. No paid inference, external APIs or CI.

## Next
Persist exact executed source; independently rerun; implement real recursive A-000 composition and index-card semantics; compare held-out task families and ablations for actual contribution of neuroplasticity candidate mechanisms.
