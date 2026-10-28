# A-000 / Genesis — Run410 registration transaction boundary

**Evidence:** prospective [Issue #83](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/83). Actual `genesis-documentary:src/echo_governor_skeleton.py`, blob `63eb982989b4f3478d649430b555c8f4ba755c27`, `HypothesisFeedbackLoop.register()` lines 2909–2937. No production patch, frozen test, complete Genesis runtime or independently held witness.

## SOURCE-OBSERVED
`register(hyp,result)` computes `alg_id=hyp["id"]`, constructs the complete entry then assigns `self.matrix.known[alg_id] = {...}`; afterward it evaluates `key not in self.evgov.history`, potentially sets the history tuple, appends to `self.algorithms_derived`, and returns. No `try/except`, rollback or A-000 reserved-ID gate exists in this method. RHS field lookup happens before assignment, so a missing `hyp["description"]` is not a post-write partial failure.

## EXECUTION-VERIFIED, bounded source-transcribed Python fixture (5/5)
Ran a transcription of this method in a disposable Python `Box` stub with `matrix.known`, `evgov.history`, and `algorithms_derived`. Cases:
1. Valid `A-123` hypothesis: matrix, history and derived list all populated (positive).
2. A dict subclass raises on history membership check: `A-123` remains in matrix, but derived list is empty (post-write partial failure).
3. A list subclass raises on `append`: matrix and history remain populated but derived list is incomplete (post-write partial failure).
4. Explicit `hyp.id="A-000"` overwrites the stub Governor entry with `HYPOTHESIS-DERIVED` (collision control).
5. Missing `description` raises `KeyError` before matrix assignment (negative control).

These outcomes reproduce the **transcribed method's** write ordering under *injected* failures. They do **not** show such exceptions arise in a normal Genesis run, nor prove real runtime reachability of an externally supplied A-000 ID. No production exploit claimed. No actual `HypothesisFeedbackLoop` instance executed.

## INFERRED / PROPOSED (unfrozen)
The registration sequence is not transactional under post-matrix exceptions. If identity authority or a downstream reader trusts the matrix immediately, a partial operation may appear committed while the history and derived-ID ledger disagree. Extend candidate RC-R5(16) with reserved-ID collision rejection across **all** writers; propose a separate RC-R5(17) atomicity/failure-attribution case: on injected failure at history or derived-list stage, either all three state holders remain unchanged or an independently recorded, reviewable partial state prevents qualification; normal non-A-000 registration must still succeed. Timothy chooses issuer/custody, permissible repair and freeze; this is **not** an authorized implementation.

**Challenge:** the production caller may guarantee no post-write exception, may serialize access or reconcile later; neither was evaluated. Exact class integration, concurrent mutation, durable recovery and external witness remain NOT RUN.
