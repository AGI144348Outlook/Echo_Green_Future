# Round 8 — Intervention-grounded execution DAG

Pre-test issue: #277, created before local tests. Isolated GPT-only research branch; canonical Genesis untouched.

## Design

A deterministic directed acyclic graph has nodes A (input), B (double A), C (increment B), D (increment A), E (sum C and D). It preserves node IDs, execution traces, typed application roles, an explicit intervention override, descendants and SHA-256 checked recipe replay. A 27-address glyph registry carries 22 canonical roles and five contextual finals, but the DAG execution uses toy arithmetic operations, not 27 mature glyph algorithms.

## Observations

18 unittest cases ran. Initial run 17 pass, 1 fail: `test_07_operator_operand` expected B to be an operand relative to C, but `relative_role` checked the edge direction backwards. Corrected lookup and reran: 18/18 PASS, 0.001s reported. Initial failure is retained in the conversation artifact. With A=2 baseline A=2,B=4,C=5,D=3,E=8; intervention do(B=10) gives A=2,B=10,C=11,D=3,E=14. C and E change, A and D do not. Shared-upstream-cause example U→X,U→Y has no X→Y edge; do(X=99) does not alter Y in the declared model. Cycles, unknown operations, missing parents, tampered recipes and budget violations rejected.

## Interpretation and limits

Shows intervention propagation in a known deterministic structural program and edge-local roles, not identification of causal structure from observations or real-world causal discovery. The model and equations are programmer-specified; no confounder identification, learned causal models, or neuroplasticity. The exact source, tests, original failed stdout and corrected stdout are in conversation artifact `echo_round8_intervention_dag.zip`; this branch currently documents the run and does not yet include executable files. Next: tie declared interventions to actual glyph algorithms and test branch selection, context and learned mechanisms.
