# A-000 identity authority and bootstrap boundary — Run405

**Source:** `genesis-documentary:src/echo_governor_skeleton.py` Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`; `ReshIdentity` class. **Prospective testing:** [Issue #78](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/78) was published before these source checks and isolated JS model controls. No change to Genesis, A-000, frozen tests or main.

## Observations (SOURCE-OBSERVED)

1. `anchor()` uses `self.matrix.known.get("A-000", {})`, then writes four identity fields and assigns that object to `known["A-000"]`. If the key is absent, it creates an identity-shaped record from an empty dictionary; it does not recover a prior Governor record, issuer, or immutable identifier.
2. It replaces `known["A-000-RESH"]` and stores `_anchor_entry` as a reference to the same alias dictionary. That reference is **not** an independent witness.
3. `validate()` checks `_anchored`, existence of the alias **key**, and `A-000.identity_symbol == "resh"`. It does not inspect alias contents, `A-000.status`, prior record provenance, issuer, custodian, signature, witness, recovery receipt or any other identity field.
4. The optional Lobby update occurs before `_anchored=True`; previous Runs 397–403 identified partial writes, stale aliases and caller-level risks on failures. Run404 found noncanonical ordering from `list(set(...))` (a future serialization hazard, not a present validation input).

## Bounded tests and interpretation

**12/12 source-string assertions PASS** against the fetched class and **7/7 source-transcribed JS model controls PASS**. Model cases: empty-matrix bootstrap validates; missing original name/status; null alias validates; status tamper remains undetected; symbol tamper fails; re-anchor restores local validation while leaving the changed status; alias object and retained anchor reference coincide. This JS model is **not execution of the Python class**. Run402 separately executed the exact extracted Python class in isolation, not the complete runtime.

**INFERRED:** Local self-consistency can be satisfied without provenance. The current code implements a useful Resh *self-labeling* operation, not an independently authenticated, immutable self-identity. Passing `validate()` cannot authorize ordinary mutation of A-000, prove the same entity persisted across a crash, or certify the origin of a record. Do not treat classroom role-association scores as identity evidence.

## Proposed requirements (NOT FROZEN)

- **Identity preservation:** If A-000 is missing, anchor must distinguish explicit authorized bootstrap from unauthorized silent recreation; record a durable event without assuming who may issue it.
- **Independent witness:** Validate typed full-record/alias consistency against an attributable, immutable or append-only record outside the mutable `matrix.known` and `_anchor_entry` reference; decide keys, custodian, privacy and revocation with Timothy.
- **Atomic update / recovery:** Any partial Lobby/alias/A-000 update must fail closed or retain an attributable recovery receipt; stale external references and retries must be covered.
- **Canonicalization:** Specify whether Lobby words are set-semantic or order-semantic before hashing; do not silently sort if ordering itself has meaning.
- **Test boundaries:** Candidate RC-R5(13) alias tamper, (14) atomicity/recovery and (15) canonical order are not frozen; no race or implementation until Timothy's decisions.

**Limitations:** The source assertions are not runtime verification; the model is an intentionally small reproduction, without real `AlgorithmMatrix`, `Lobby`, concurrent actors, durable storage or independent witness. No Python full Genesis, CI or external custody tests were run. No code changes to A-000.

**Awaiting Timothy:** who may issue/rotate/revoke A-000 identity, what the immutable identity fields are, which actor holds the witness and keys, how to handle missing original records, whether Lobby vocabulary order matters, and when to freeze acceptance cases.