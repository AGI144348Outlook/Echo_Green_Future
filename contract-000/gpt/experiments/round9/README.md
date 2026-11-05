# Round 9 — Active causal hypothesis discrimination

Pretest GitHub Issue #279 was published before any local test. Research first: Wang et al., ICML 2025 https://proceedings.mlr.press/v267/wang25bp.html; Elahi et al., ICML 2024 https://proceedings.mlr.press/v235/elahi24a.html; Huber 2024 https://doi.org/10.1186/s41937-024-00131-4.

## Method

Standalone Python stdlib deterministic causal-hypothesis simulator. Two structural models: chain A→B→C and fork B→A, B→C. Observational root=2 yields A=B=C=2 in both. A bounded experimenter predicts each candidate model's outcome for each allowed intervention and chooses first with maximum number of distinct predictions (a crude disagreement heuristic, NOT Bayesian active learning). It then queries a simulated oracle, eliminates inconsistent candidates, logs provenance and can report non-identifiability. Separate pure functions represent relative cause/effect and operator/operand roles.

## Results

16 Python unittest tests, 16 PASS, 0 FAIL, 0.001s. `do(A=5)` chosen over `do(C=5)` because it separates chain/fork. If chain true, observed A=B=C=5 and fork eliminated. If fork true, observed A=5,B=C=2 and chain eliminated. Duplicate structural models remain unresolved as expected. Checks include observational equivalence, active choice, elimination both ground truths, heldout intervention, role relativity, no temporal causal inference, budget, provenance, invalid intervention, deterministic replay, zero budget and non-discriminating options. No test failures or deviations. Source, tests and raw stdout in conversation artifact `echo_round9_active_causal_discovery.zip`; GitHub branch currently has documentation only.

## Limits

Synthetic ground truth and complete candidate list supplied by programmer; no actual discovery from empirical data, no uncertain/noisy measurements, no confounding, no 27-glyph execution or neuroplastic learning. Intervention choice based on disagreement counts, not optimized information gain. Next round: noisy interventions, confounding, richer candidate generation, cost-sensitive selection, holdout validation and integration with glyph algorithms.
