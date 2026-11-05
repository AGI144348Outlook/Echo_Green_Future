# Round 10 — Integrated Echo causal DSL prototype

Pre-test Issue #280 published before tests. Online research: Wang et al. ICML 2025 https://proceedings.mlr.press/v267/wang25bp.html; Elahi et al. ICML 2024 https://proceedings.mlr.press/v235/elahi24a.html; Choo et al. AISTATS 2024 https://proceedings.mlr.press/v238/choo24a.html; Akbari et al. JMLR 2025 https://jmlr.org/papers/volume26/22-1516/22-1516.pdf.

## Integrated experimental components

A standalone Python stdlib package (`echo.py` and `test_echo.py`) consolidates: 27 unique glyph addresses (22 canonical base roles + five final variants), bounded typed execution of subset `ע ד מ ם פ ף ת`, operator/operand execution trace, perspective-relative cause/effect queries for explicitly asserted edges, SHA-256 recipe tamper rejection, and an active two-model experimenter that ranks candidate interventions by squared predictive disagreement / intervention cost and updates model weights using Gaussian observation likelihood. Noise is seeded for deterministic replay. Unsupported glyphs raise `NotImplementedError`.

## Actual tests

22 unittest tests executed locally, 22 PASS, 0 FAIL, 0.001s reported. Coverage includes registry uniqueness and role mapping; glyph composition, trace, type, budget, seal, unknown/unsupported glyph, recipe replay and tamper; relative operator/operand and cause/effect; temporal precedence not causal; intervention selection and budget/cost; posterior discrimination of chain/fork under simulated Gaussian noise; evidence provenance, deterministic seed and invalid action rejection. No test failures or deviations observed.

## Evidence and reproducibility

Exact executed source, tests, README and stdout provided in the conversation file `echo_round10_integrated_causal_dsl.zip`. The GitHub branch currently stores this report only, not the runnable files; it cannot be independently rerun from GitHub alone. Do not mistake this for a verified integration of prior round source files: it is a new consolidated prototype using the preceding concepts.

## Limits

Causal models and ground truth are programmer-provided; likelihood confidence is conditional on only two candidate models and assumed Gaussian noise. Intervention cost is synthetic. No real-world causal discovery, unknown-model detection, full 27-glyph algorithm suite, adaptive topology, or persistent runtime service. Next: commit source/test files directly, compare against independent baselines, incorporate model-mismatch/abstention and off-target interventions, and integrate the interpreter with actual 3³ neuroplastic graph under governance.
