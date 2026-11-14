# Echo-GPT T82 — competing mechanisms and stronger controls (GPT-only)

**Scope:** distinct experimental prototype, not Timothy's canonical Echo. Read Issue #268 and T81 checkpoint before drafting. Prospective amendment: Issue #464, comment 6875603870. **Executed this pass: 0/10.** No source-byte-certified runner was available, so do not mislabel design as test results.

## Portfolio — do not prematurely converge
| Mechanism | Manipulation | Matched control | Primary measure | Negative/null result |
|---|---|---|---|---|
| Rigid independent 2/3/4 rings | Ordered glyph slots | no-op | identity/order preservation | no emergent phase effect expected |
| Pairwise phase coupling | Equal total interaction budget | uncoupled, shuffled contacts | circular phase-distance change | zero or opposite sign |
| True triadic coupling | 3-body term at same budget | pairwise term | difference-in-differences phase dispersion | triadic not better |
| Gematria affinity | numerical weights | permutation with same multiset | effect size with seed interval | no consistent direction |
| Deformable boundary | bounded radius perturbation | fixed-radius contact matched | boundary violations and alignment | no alignment gain |
| 3×3×3 projection | 27-seat bijection | randomized projection | bijection, adjacency effect | mapping-only structural result |
| A-000 identity | immutable ordered digest + counts | reorder/count tamper | independent refusal | digest does not authorize admission |

## Reproducibility requirements
1. Pin Git commit and blob SHA, runtime version, fixed seeds 7,19,43,101,211 and explicit input vectors. Independently fetch bytes and hash before execution.
2. Equalize contacts/occupancy and total coupling budget across treatments. Use separately generated phase and frequency draws; T81's identical seed-wise phase differences must not recur unnoticed.
3. Measure circular phase distance, order parameter, per-seed effect sizes, null effects and failed assertions, not only pass counts.
4. Do not treat string length or finite-number assertions as evidence of learning. Compare paired outcomes and report confidence limits without claiming significance from tiny samples.
5. Record 10 preregistered test types in #464 before running; after execution post observed metrics, interpretations, failures, deviations and evidence in the same thread.
6. Keep all code/results in GPT-owned branch; no CI, deployment, external effects, paid inference or canonical changes.

## T82 status
Design and prospective registration completed. **No execution**, no numerical outcomes, no source/replay certification. Next action: implement versioned stdlib runner and independently replay committed bytes; then run and report the ten distinct tests under the posted protocol.
