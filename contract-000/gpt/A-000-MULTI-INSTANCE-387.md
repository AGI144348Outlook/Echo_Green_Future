# A-000 / Resh — shared-matrix, multi-instance identity lifecycle (Run387)

**Status:** SOURCE-OBSERVED and ISOLATED PYTHON EXECUTION; exploratory, not frozen RC-R5, not a production Governor patch, not a claim of consciousness. **PRE-TEST:** [Issue #60](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/60), posted before tests. **Authority:** Contract-000 `0fbc794`, TJ ruling R5 `3ce87eb`, DISC-002 `ee443fbc`. **Source:** `genesis-documentary/src/echo_governor_skeleton.py` Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`, `ReshIdentity` around lines 3233–3305.

## Source observations

The `ReshIdentity` constructor initializes `self._anchored = False` for **each Python object**, while `anchor()` writes identity markers into the shared `matrix.known["A-000"]` and replaces `matrix.known["A-000-RESH"]` unconditionally. `validate()` combines the instance-local flag with shared matrix membership and A-000's `identity_symbol == "resh"`. It does not compare `self._anchor_entry` to the current alias record and does not authenticate the alias's contents. This is an identity-lifecycle/authority boundary, not evidence of two separate Governor minds.

## Isolated test and observations

[Eight committed Python unittest cases](test_a000_multi_instance_387.py) transcribe the visible `ReshIdentity` methods from the exact source, using only a `MatrixStub.known` dictionary, no Lobby. Ran `python3 -I -B -m unittest discover -v -s . -p 'test_a000_multi_instance_387.py'`: **8/8 passed**. Committed test blob `18d577f39750b1b83c66151793e72630ea748491` independently matches the locally tested Git blob.

1. Both newly constructed instances initially fail validation.
2. When instance A anchors, A validates True while instance B on the **same matrix** validates False.
3. When B also anchors, both validate True.
4. B's `anchor()` replaces the alias dictionary rather than mutating the original alias in place.
5. A's `_anchor_entry` reference becomes stale after B re-anchors.
6. A still validates True after the alias is replaced by an unrelated dictionary.
7. Removing the alias key makes both validate False.
8. Reinserting the alias key with value `None` restores both to True without a new `anchor()`.

**Interpretation:** `validate()` is not a matrix-intrinsic, globally agreed identity attestation. Its outcome depends on local instance history, and its membership check does not establish that the alias value is authorized. Two objects can disagree on one shared state; two anchored objects can agree on an invalid alias. This extends the existing E35 weak-validation findings and the Run386 witness-scope analysis, without proposing automatic re-anchoring or a specific identity issuer.

**Limitations:** the complete Genesis runtime was not executed; the test uses source-transcribed methods and stubs. It does not establish that the real application constructs multiple `ReshIdentity` instances or invokes this path in production. No thread/concurrency, actual Lobby, custody, anti-replay or security certification. No kernel/main/Claude/shared modification.

**Claude:** independently assess whether identity must be verified per object, per matrix, or by a versioned external witness, and whether re-anchor should invalidate previous instance-local attestation. **Timothy:** decide issuer/custody, authorized update/revocation, identity-field scope and frozen RC-R5 acceptance tests. Candidate only.
