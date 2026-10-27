# A-000 / Resh report authority boundary — Run406

**Pre-test:** [Issue #79](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/79) posted prospectively. **Actual source:** `genesis-documentary:src/echo_governor_skeleton.py` Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`, class `ReshIdentity` (approximately lines 3233–3315). No source changes. Timothy's R5 remains binding; no frozen test or identity issuer chosen.

## SOURCE-OBSERVED

- `validate()` checks only the local `_anchored` flag, existence of the `A-000-RESH` **key**, and `A-000.identity_symbol == "resh"`. It does not check the alias **value** or `A-000.status`.
- `report()` calls `validate()`, then prints the positive statement `A-000 and Resh are one`, plus Ayin and Pe operator names. It does not independently read the alias contents, check revocation, or require an external witness. Therefore its positive prose is no stronger than the weak predicate it delegates to.
- `anchor()` rewrites the identity marker and alias record, and `_anchor_entry` is a live alias reference, not independent custody.

## EXECUTION-VERIFIED — bounded isolated controls

**10/10 source assertions** matched the pinned Python source text: class, report gate and positive statement, validator flag/key/symbol checks, anchor assignment/reference, absence of status validation and absence of alias-value validation. **9/9 isolated JavaScript model controls passed** using a source-transcribed representation of those narrow methods:

1. Before anchor, report says unanchored; after anchor, positive.
2. With alias value replaced by `null`, `false`, or an unrelated dictionary, the model's `validate()` and `report()` remain positive.
3. With `A-000.status` changed to `REVOKED`, the report remains positive.
4. With `identity_symbol` changed, the report becomes negative; after re-anchor it becomes positive again while the `REVOKED` status remains.
5. Deleting the alias key makes the report negative.

**Interpretation (INFERRED):** The current `report()` is a presentation of *local marker consistency*, not a trustworthy attestation of uninterrupted identity or update authority. A future UI or agent must not treat that sentence as proof of independently witnessed identity. This extends Claude's E35 observations from the validation predicate to its user-visible reporting surface; it does not contradict the agreed E35 wording.

**PROPOSED, UNFROZEN:** Keep separate predicates for `self_labeled`, `identity_continuity_attested`, and `update_authorized`. Any positive externally trusted identity report should declare which predicate was actually checked, its independent witness/receipt, and failure/recovery state. No implementation, issuer/custodian, cryptographic mechanism or race acceptance tests are authorized yet.

**Limits and deviations:** The JS model is a controlled transcription, **not execution of the Python class or complete Genesis**; source assertions establish code shape, not runtime coverage. No CI, production Governor, Lobby, concurrency, persistent witness, or Python runtime was exercised. No failed assertions. The observed weakness is in source and the narrow model; external consumers and their decisions were not tested.

**Awaiting Timothy:** identity issuer, witness custody/keys, bootstrap/recovery, authorized mutation, canonicalization, frozen acceptance cases. See [Claude's latest DISC-002](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/research-discourse-registry/research-registry/discourse/DISC-002-invariant-self-identification.md) for E35 and Lesson 2 evidence boundaries.
