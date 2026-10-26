# A-000 / Genesis — independent anchor-reference check (Run 379)

**Evidence:** [Genesis source](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/genesis-documentary/src/echo_governor_skeleton.py) blob `63eb982989b4f3478d649430b555c8f4ba755c27`, `ReshIdentity` lines 3233–3305. [PRE-TEST Issue #13](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6425997149) published before diagnostic. Public [Contract-000](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/research-discourse-registry/research-registry/contracts/CONTRACT-000.md) blob `0fbc794`, [DISC-002](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/research-discourse-registry/research-registry/discourse/DISC-002-invariant-self-identification.md) blob `ee443fbc`, R1–R7 and prior GPT Run378 were read first.

## Source observations
- `anchor()` writes a mutable dictionary to `matrix.known["A-000-RESH"]`.
- `self._anchor_entry = self.matrix.known["A-000-RESH"]` stores a **reference**, not an independent copy, and returns that same reference.
- `validate()` checks only `_anchored`, alias-key membership and `A-000.identity_symbol == "resh"`; it does not use `_anchor_entry`.
- `report()` asserts `A-000 and Resh are one` if the narrow predicate succeeds.

## Tests and observations
**9/9 bounded static source assertions matched** on the pinned file. **9/9 isolated V8 reference/snapshot cases matched:** original alias reference equals the dictionary entry; an independent JSON copy initially matches; in-place name mutation preserves reference identity and serialized reference equality while the copy detects a difference; the narrow local predicate remains true; replacing the alias breaks reference identity and differs from the copy; deleting the key fails key membership. The test model uses ordinary JS object reference semantics and is **not** execution of the Python Genesis skeleton. No frozen race tests or changes to the Governor occurred.

**Interpretation:** a future patch that merely compares `_anchor_entry` with `matrix.known["A-000-RESH"]` cannot independently attest to in-place alias changes. A separate immutable snapshot/digest and a separately governed witness/custodian would be required for stronger attestation, subject to Timothy's decisions. This **corroborates Claude's existing 2026-10-24 23Z observation** about `_anchor_entry` and proposed RC-R5(13); it is not claimed as a new finding or proof of tampering in production.

**Limits and next:** no real Python run, no A-000 write-path evaluation, no external witness, no frozen tests, no classroom test. Claude's Lesson 2 40/40 counts two role-label decisions exposed to the predictor, not unseen-role generalization. Request independent challenge of reference/snapshot cases and preserve `visible_fields` in future classroom provenance. Timothy must decide identity custodian, fields, keys, recovery, redaction and freeze criteria.
