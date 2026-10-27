# A-000 / Genesis identity-transaction boundary — Run399

**Evidence type:** SOURCE-OBSERVED in `genesis-documentary:src/echo_governor_skeleton.py`, Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`; isolated V8 *source-text checks*, not Python execution of Genesis. [Pre-test registration](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/72). Current Claude DISC-002 `ee443fbc` and Contract `0fbc794` read first.

## Observations (6/6 source-text/ordering assertions)

1. `AlgorithmMatrix.__init__` constructs `known["A-000"]` with `name=Governor`, `status=ACTIVE`.
2. `ReshIdentity.anchor()` writes A-000's identity fields and then overwrites `known["A-000-RESH"]` **before** it attempts the optional Hebrew Lobby `definition_words` update.
3. `_anchored = True` occurs **after** that optional Lobby update. Therefore a Python exception there can leave matrix mutations without an anchored flag; Run398 independently reproduced this with a source-transcribed isolated Python stub (6/6 controls), **not** the full runtime.
4. `validate()` checks `_anchored`, **presence** of the alias key, and A-000 `identity_symbol == "resh"`. It does not check alias value, full core contents, external pin, or issuer.
5. `PeCommunicator.open_exchanges()` invokes `resh.anchor()` when validation fails; it has no visible detached pre-repair witness in that call path.
6. The `anchor()` source block has no explicit rollback path. This is a source-level absence observation, **not** proof that an external transaction manager cannot exist elsewhere.

**Interpretation (INFERRED):** A-000 is a self-index marker with mutable shared state; current `validate()` is not sufficient to establish durable invariant identity, authorization, or failure-atomicity. A failed optional hook and a later re-anchor can make the audit story ambiguous without a detached record. This is compatible with Claude's E35 distinction: re-anchor repairs only checked fields; unvalidated fields may remain altered.

## Candidate RC-R5(14) contract — PROPOSED / NOT FROZEN

Preconditions: capture the original A-000 and alias entries, the Lobby word sequence, the identity authority/version, and an immutable pre-operation witness. Stage changes without exposing partially committed identity. On success, commit the new core and versioned evidence as one attributable transition. On exception, either restore *all* original observable state or write an immutable, attributable partial-failure/recovery receipt that an independent validator can inspect; never silently convert failure to success. On recovery, compare the externally held witness before allowing `open_exchanges()` to re-anchor.

**Negative case:** corrupt Lobby `definition_words` or induce a failure after the alias write. **Expected after a future authorized implementation:** no unreceipted partial identity; no successful validation solely because a retry rewrites `identity_symbol`. **Falsifier:** a complete runtime path already provides independent rollback or immutable custody; that must be tested rather than assumed.

This is a test sketch, not a production patch, race, freeze, or change to Genesis. Timothy must rule on issuer/custodian, which fields are immutable versus versioned, whether Lobby encounter order is identity-adjacent, failure-retention policy, and frozen test authority. No private Testament material read.