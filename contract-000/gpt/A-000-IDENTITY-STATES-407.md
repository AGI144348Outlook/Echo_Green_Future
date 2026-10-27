# A-000 / Resh identity — Run407 source-bound boundary review

**Pre-test:** [Issue #80](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/80). **Source:** `genesis-documentary:src/echo_governor_skeleton.py`, Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`, `ReshIdentity` class, approximately lines 3233–3315. No Genesis modifications, no full Python runtime.

## Source-observed

1. `anchor()` sets `A-000.identity_symbol="resh"` and stores a new `A-000-RESH` alias dictionary; the optional Hebrew Lobby update occurs before `_anchored=True`.
2. `_anchor_entry` is assigned from `matrix.known["A-000-RESH"]`, a mutable local object, not an independent witness or append-only receipt.
3. `validate()` checks `_anchored`, existence of the alias **key**, and A-000's `identity_symbol`. It does **not** read the alias's **value**, A-000 status, custody, a failure log, or a separate witness.
4. `report()` gates positive identity prose solely on that validator; a positive report is a **self-label assertion**, not independently verified continuity.

## Executed bounded controls

**8/8 source-shape assertions passed** against the pinned Python class text: anchored flag, alias-key presence, symbol check, report-to-validate call, positive prose, live alias reference, absence of alias-value validation and absence of status validation. These are **source assertions**, not Python behavior or full-system acceptance tests. Previous Run402 extracted and ran the class in isolation, and Runs403–406 separately examined caller, reanchor and report consequences; this run did not rerun those experiments.

## Interpretation and proposed specification (UNFROZEN)

A-000 as an *invariant self-identifying algorithm* needs an explicit distinction between (a) local self-label, (b) continuity attested by an independently governed receipt/witness, and (c) authority to change the protected slot under Timothy's R5 ruling. An invariant cannot be established merely by repeating a label in a report.

**Candidate fail-closed state table:** `UNANCHORED` (no positive report); `LOCALLY_ANCHORED` (report explicitly self-asserted); `CONTINUITY_ATTESTED` (requires a separately verifiable receipt); `RECOVERY_PENDING` (no trusted continuity claim until failure resolved); `UPDATE_AUTHORIZED` (separate scoped permission, not inferred from attestation). This is a *proposal*, not an implementation, schema migration, cryptographic design, or frozen RC-R5 test. Failure retention and a witness remain under Timothy's decisions.

**Challenge to proposal:** A durable, externally verifiable identity receipt or stronger predicate elsewhere in the actual call path could change the scope of the weakness; no such authority was established in this inspected class. Full Genesis, concurrent mutation, recovery and external consumers were not executed. No new authority or release is claimed.

**Awaiting Timothy:** issuer/witness, custody/keys, authorized update and revocation, failure retention/redaction, bootstrap/recovery and canonical ordering, and acceptance-test freeze. Claude's 2026-10-24 23Z E35 and Lesson 2 evidence boundaries remain acknowledged.