# Echo-GPT noncanonical independent ledger oracle — 09Z results
**Prospective registration:** Issue #331 comment 6704782114 posted BEFORE test execution. **Actual observations:** Issue #331 comment 6704787329 posted AFTER execution. Source commit 422e799413d643a2024d87446ee32143d82fc2fb; file independent_oracle_09z.py; local source SHA-256 999c5953e16bbfb7d131a15f2dbfe6d297e5f0193a8a58f05da4c853a874685c, 3937 bytes.
Run offline Python 3: `python independent_oracle_09z.py > results_09z.json`; four fixed seeds 1106–1109, 32 candidate arrivals, 45 ticks, 3-tick dwell. JSON output SHA-256 4959511d2203682e49696162cd9e6e75e81b3c01266372a838213d96d80685bc, 9105 bytes. Raw JSON generated locally; available separately as run attachment, not embedded here.
| Type | Activated | Detected |
|---|---:|---:|
| duplicate arrival | 4 | 4 |
| missing arrival | 4 | 4 |
| duplicate terminal | 4 | 4 |
| missing terminal | 4 | 4 |
| premature release | 4 | 4 |
| delayed release | 4 | 4 |
| seat overlap | 4 | 4 |
| FIFO wrong ID | 4 | 4 |
| unknown arrival ID | 4 | 4 |
| omitted last release | 4 | 4 |
Total: 40/40 activated and detected, baseline no-op 4/4 clean. Escapes 0 in this bounded fixture. Not 40 independent hypotheses. Source and result digests permit reproduction; a full raw JSON commit remains a follow-up.
Interpretation: independent checker detects deliberately injected synthetic ledger errors, not evidence of semantic intelligence, learned causality, or genuine spatial 3³ coupling. Oracle and generator share event semantics; external held-out data, cross-implementation comparisons and stronger event-order checks remain open. No canonical changes, CI or paid inference.
