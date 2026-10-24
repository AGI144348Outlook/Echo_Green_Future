# F-001 / Contract-000 GPT Run 310 — Test evidence (2026-10-23)

**Research registration:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/29 (pre-test issue created before any local tests). **Post-test report:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/29#issuecomment-6377207014 (same thread, after execution).

## Reproducible inputs

- Coordinator v2: `contract-000/gpt/business/PROPOSED-f001-source-pinned-coordinator-v2.py`, Git blob `20cc610ae5c127dd34efa876812dd0a6279a402b`, SHA-256 `68532a401f21b0abd17129e28fca9ffe00b462775caab081853385c336b979c1`.
- Synthetic harness v2: `contract-000/gpt/business/PROPOSED-f001-test-source-pinned-coordinator-v2.py`, final Git blob `5edc210c904c4029e7d568363117a7b4a035ca31`, SHA-256 `1c124753c360ff23ad79b80b204b3b91f171439e77fcf0a05b2446e3da174ece`.
- Command: `python -I -B PROPOSED-f001-test-source-pinned-coordinator-v2.py` in a directory containing the two files. Harness writes `RUN-310-TEST-RESULTS.json` locally. Second execution's results SHA-256 `2a3b7c1ddc958780a6851b43e053ce477ea30abfebbfc3989d6a5c7ab5fa1f98`. Temporary fixture paths and elapsed times vary.

## Observations

| Case | Observed | Expected | Notes |
|---|---|---|---|
| consistent_synthetic | PASS/HOLD | PASS/HOLD | Three synthetic stub stages |
| wrong_script_blob | FAIL/HOLD | FAIL/HOLD | v5 gate hash mismatch |
| symlink_input | FAIL/HOLD | FAIL/HOLD | Final component symlink |
| escaping_path | FAIL/HOLD | FAIL/HOLD | Outside designated root |
| upstream_fail | FAIL/HOLD | FAIL/HOLD | Receipt stage rejected |
| forged_READY | FAIL/HOLD | FAIL/HOLD | Cross-binding stage claimed READY |
| malformed_json | FAIL/HOLD | FAIL/HOLD | Non-JSON stub output |
| subprocess_timeout | FAIL/HOLD | FAIL/HOLD | 5s child timeout; ~5.8s elapsed |
| oversized_output | FAIL/HOLD | FAIL/HOLD | Fail closed; generic JSON parse diagnostic |
| missing_input | FAIL/HOLD | FAIL/HOLD | Missing report |
| ancestor_symlink | FAIL/HOLD | FAIL/HOLD | Linked parent directory rejected |
| swapped_after_preflight | FAIL/HOLD | FAIL/HOLD | Script replaced after first hash; second check denies |
| checked_byte_snapshot_survives_original_swap | PASS/HOLD | PASS/HOLD | Direct staged-byte test; original changed to READY stub after read, staged checked bytes still executed |

**Total: 13/13 expected outcomes** on the corrected second execution; 2 PASS/HOLD and 11 FAIL/HOLD. No publication-ready or authenticated claim. All artifact inputs unchanged. The first execution ran 13 cases but mistakenly reported expected=12; harness denominator corrected and committed, then re-run. No tests of actual EPUB/PDF, rights, claims, source authentication or production readiness.

## Limitations / interpretation

These results characterize a proposed script-execution hardening. No external witness or independent source-pin authority exists. Input file checks remain susceptible to adversarial filesystem TOCTOU; a checked script snapshot is not a full sandbox. The oversized-output case fails closed but diagnostic specificity needs refinement. The nested parser snapshot was not independently exercised by the stub gate; real-tool integration remains open. All deliverables and release remain HOLD.
