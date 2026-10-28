# Run414 — A-000 / Resh multi-instance identity admission and partial-anchor evidence

**Prospective PRE-TEST:** [Issue #87](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/87), published before tests. **Source:** `genesis-documentary:src/echo_governor_skeleton.py` Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`, `ReshIdentity` class at lines 3233–3305 and `PeCommunicator.open_exchanges()` near 3519–3520. The [isolated exact class excerpt](A-000-RESH-EXTRACT-414.py) is Git-blob `ff4212e42b10ec05c68b506860a03198cf470f4c` for the class body; the locally executed class body matched this Git blob. [11-case isolated Python control](test_a000_resh_414.py). **Not full Genesis execution.**

## Observations (EXECUTION-VERIFIED, isolated actual class with minimal matrix/lobby stubs)

Python 3.13 with `-I -B`: **11/11 final controls passed.** Initial harness attempt failed `ModuleNotFoundError` because isolated mode removes the script directory from `sys.path`; fixed the harness to import the exact local file via `importlib.util.spec_from_file_location`, then reran successfully. No Genesis implementation changed.

1. Initial `ReshIdentity` without an anchor rejects validation; after `anchor()`, validation succeeds (positive control).
2. A new `ReshIdentity` over an unchanged, already anchored matrix has `_anchored=False`, so `validate()` rejects it. Calling `anchor()` again replaces `matrix.known['A-000-RESH']`, dropping a test-only `review_nonce` on the old alias (restart false-negative / silent rewrite).
3. The **original instance still reports `validate() == True`**, although its `_anchor_entry` references the *old* alias dictionary and the matrix now points to the new one. Thus two in-process Resh instances can simultaneously claim valid identity while holding different alias views. The test-only nonce is synthetic, not an actual production identity field.
4. Changing `A-000.status` to `TAMPERED` leaves both instances' `validate()` True, consistent with Claude's E35 predicate analysis.
5. With a deliberately malformed stub Lobby (`definition_words=None`), `anchor()` raises `TypeError` **after** mutating A-000 and replacing A-000-RESH but **before** setting `_anchored=True`. The matrix is partially changed while the instance reports invalid. Repairing the injected stub and retrying succeeds (positive recovery control). This is an injected failure, **not** evidence that normal Lobby data causes the exception.

## Interpretation (INFERRED)

The inspected local predicate is neither an independently witnessed continuity proof nor a transactional admission protocol. Its per-instance `_anchored` bit does not reconcile with a persisted matrix, and its cached `_anchor_entry` can become stale after another instance re-anchors. A failure during Lobby enrichment can leave partial matrix mutations. This adds a **multi-instance split-view and partial-anchor boundary** to Run413's restart concern; it does not demonstrate concurrent production use, tampering by an attacker, or a full Governor failure.

## Proposed acceptance tests (UNFROZEN)

- **RC-R5(20) multi-instance continuity:** after a legitimate persisted restore, independent Resh instances must either agree on one source-bound identity version or explicitly fail closed with an attributable stale-view record. No instance may pass a continuity test using a cached alias that no longer matches the admitted record.
- **RC-R5(21) atomic anchor/recovery:** inject a failure after A-000 write but before Lobby enrichment completes; expect no externally visible partial identity update, or an explicitly recoverable transaction receipt. Retry must be attributable, not a silent overwrite.

Both require Timothy's issuer/custody/recovery/retention and test-freeze decisions; no witness, monotonic epoch, signature, or transactional implementation exists in this fixture. Claude's latest DISC-002 E35 wording remains valid, and Lesson 2's 40/40 role-label score remains unrelated to A-000 identity.

## Reproduction / limits

`python3 -I -B contract-000/gpt/test_a000_resh_414.py` beside `A-000-RESH-EXTRACT-414.py`. Uses source-extracted class, a `SimpleNamespace(known=...)` matrix and synthetic Lobby; does **not** initialize `AlgorithmMatrix`, full Hebrew Lobby, Pe, Ayin or Governor, nor read private Testament. No writes to main, Genesis, shared Library or Claude records. Evidence and failures will be recorded on [Issue #87](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/87).
