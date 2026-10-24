# F-001 Run 312 — coordinator-v4 characterization evidence (2026-10-23 CT)

**Prospective pre-test registration:** [Issue #31](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/31), posted before local execution. **Candidate:** `PROPOSED-f001-source-pinned-coordinator-v4.py` Git blob `9eee2016d696d1584350d0b1bfa20826ddad2eb5`, SHA-256 `e2af6ef9389d67eb56d0be7dcaae1cbe7a44d70c273576015d09abe6dbf271d7`. **Harness:** `PROPOSED-f001-test-source-pinned-coordinator-v4.py` Git blob `a7282d55e5f2c6c2ccb4922e7dae9232ac3cfd49`. Both exact bytes were committed and independently re-fetched from GitHub. Python 3.13.5, Linux local process, `python -I -B test_v4.py`.

## Observations (EXECUTION-VERIFIED locally, not externally authenticated)

| Case | Expected | Observed |
|---|---|---|
| Real reviewed receipt-v3 + v5 parser/gate + v4 binding, archived public-derived Dataset A, synthetic EPUB/PDF and editorial record | PASS / HOLD / BLOCKED | **PASS / HOLD / BLOCKED**, three stages exit 0 |
| `link/../pins.json` path to forged outside file | FAIL / HOLD / BLOCKED | **FAIL**, `parent traversal component rejected`, zero stages |
| Stage returns JSON list `[]` (test-only stub script with explicitly overridden blob pin) | FAIL / HOLD / BLOCKED | **FAIL**, `subprocess stage output must be JSON object: receipt_v3` |
| Stage writes 1,052,672 stdout bytes (test-only stub script with overridden pin) | FAIL / HOLD / BLOCKED | **FAIL**, `subprocess output exceeds bound` |
| Symlink path ancestor without lexical parent traversal | FAIL / HOLD / BLOCKED | **FAIL**, `symlink path component rejected` |

**Final registered cases: 5/5 expected.** All returned `release=HOLD`, `readiness=BLOCKED`, `publication_authorization=ABSENT`, `source_pin_authenticated=false` and `approval_authenticated=false`. Test symlinks were created and removed in the local fixture; no repository source was changed during execution.

## Deviation and correction

Initial local control run failed **in both v3 and v4** because the archived Run 311 fixture's `receipt.json.environment.build_output_realpath` still pointed to `/mnt/data/contract311/artifacts`, while the extracted copy was under `/mnt/data/contract312/artifacts`. The receipt verifier correctly rejected that stale fixture location. Before the final five-case execution, the **synthetic fixture metadata only** was updated to the actual local artifact directory; neither verifier nor production source was modified for this correction. The successful run is not evidence that the old fixture was valid unchanged. This is a disclosed setup deviation, not an extra successful case.

## Interpretation and limits

The v4 candidate closes Claude's **§118 V1 lexical `symlink/../` mismatch** by rejecting `..` before normalizing and forwarding only canonical paths. It also gives explicit non-object and oversized-output failures. **It does not pin artifact file descriptors or prevent concurrent filesystem modification between preflight and child open; a full immutable artifact snapshot is still needed.** Linux/POSIX only. The EPUB/PDF are **invalid synthetic placeholders**, the source pin and editorial record are caller-controlled and **not independently authenticated**, and this test does not verify finished book formats, rights, accessibility, storefront claims, actual income or publication authority. No frozen RC-R5 tests or A-000 code were executed.

**Next:** Claude independently reviews v4 (especially path TOCTOU, source authentication and process isolation). GPT then proposes immutable artifact-input staging and real EPUB/PDF validation once legitimate artifacts exist. Keep sole F-001 project and publication HOLD. Timothy's A1–A6/B6, Dataset A CSV lines 6/7, identity-authority decisions and explicit release permission remain open.
