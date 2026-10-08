# NVE-D-IETF-001 — First executed IETF analogue test

Status: **Executed locally**, not a claim of GitHub Actions execution or autonomous learning.

## Test execution
A Python 3 test runner executed 15 independent seeded runs, at 250, 1,000, 2,500, 5,000 and 10,000 generations, each with seeds 7, 31 and 97. **Total: 56,250 completed generations**, approximately 0.816 seconds local execution.

Source expressions were preserved as opaque UTF-8 strings. For each generation the test selected one of four original expressions and used one of four explicitly artificial string operations (identity, trailing space, reversal, permutation). This is a **synthetic infrastructure test**; the operations do not express inferred Mashet or IETF semantics.

### Provisional relational outcomes
- Snapshot preservation: `=` (unchanged source digests).
- Experimental branch isolation: `=` (mutation of a branch did not change the snapshot).
- Deterministic checkpoint/resume: `=` (all 15 replay states identical to uninterrupted runs after halfway checkpoint).
- No claim that a source symbol's meaning was learned.

The comparator assigns `=` to exact byte-identical strings and `0` otherwise; this is an explicit provisional *fixture criterion*, not an independently established meaning of `0`. Other outcomes `<` and `>` were not justified by this experiment.

## Document Feedback Evaluation
**Step 5 Evaluation:** Compare these infrastructure results to previous NVE-D trials: these tests establish replay and isolation under a toy workload only; they do not establish semantic adaptation.

**Step 7 Meta-Audit:** The same synthetic test code generates and verifies states; this is not independent auditing. The comparison rule, transformation operations, RNG and digest-based state accumulation are imposed test fixtures and must not be promoted to substrate rules.

**Step 8 Revision:** Next experiment should use two independent implementations, intentionally introduce corrupted checkpoints, vary nesting depth independently from generation count, and preserve all counterexamples and original expressions. Add full-run checkpoints and separate evaluator hypotheses.

## Provenance and reproduction
The Python script and full JSON output were generated in the chat runtime as `/mnt/data/nve_d/ietf_test.py` and `/mnt/data/nve_d/NVE-D-IETF-001-results.json`. This document is a summary of that run, not an executable implementation committed to GitHub. Reproduction requires the script and its fixed seed values. The test implements finite approximations of the IETF codex's isolated nodes, snapshots and variable experimental durations, not its conceptual infinite parallelism or Chrono-Tool time dilation.

**Source specification:** `experiments/nve-d/sources/ietf/01-framework.txt` and `experiments/nve-d/sources/ietf/README.md`.
