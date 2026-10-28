# A-000 / R5 ordinary-write protection — Run408

**Prospective PRE:** [Issue #81](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/81). **Source:** `genesis-documentary:src/echo_governor_skeleton.py`, exact Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`; inspected `AlgorithmMatrix`, `ReshIdentity`, and `PeCommunicator`. **Timothy's binding R5** in `research-discourse-registry:research-registry/TJ-RULINGS.md` blob `3ce87eb6b9215bd8d5dc0a2e4664b95479764161` requires ordinary A-000 writes be blocked, while explicit logged reviewed Claude/GPT updates remain possible under a future race contract.

## Source-observed

1. `AlgorithmMatrix.__init__()` initializes `known["A-000"]={"name":"Governor","status":"ACTIVE"}`.
2. `AlgorithmMatrix.record(self, entry_id: str, entry: dict)` contains only `self.known[entry_id] = entry`. It checks neither the reserved `A-000` identifier nor an issuer, logged review, capability or authorization. **The current skeleton therefore lacks the R5 ordinary-write guard in this method.** This is not an authorized change to it.
3. `ReshIdentity.anchor()` directly modifies `known["A-000"]` and replaces `known["A-000-RESH"]`; it is not an external, separately attested write transaction. `validate()` checks the local anchored flag, alias **key** presence and `identity_symbol=="resh"`; it does not check alias contents, `status`, external custody or an independent witness.
4. `PeCommunicator.exchange()` gates on that validator, while `open_exchanges()` invokes `anchor()` if it returns false. Thus a local marker check can control access and a re-anchor can repair checked fields without durable tamper provenance, consistent with Claude E35 and Runs402–407.

## Executed source checks and limits

**13/13 bounded source-level assertions passed** on the exact pinned source, including detection of the one-line unguarded `record`, absent reserved-ID check, absence of a permission parameter, direct anchor mutations, `validate`'s narrow predicate, Pe's caller and a synthetic *source-text mutation* with an added reserved-ID guard. These are static assertions; the synthetic guard was not installed or run as Python. No complete Genesis, live concurrent mutation, independent witness, or frozen R5 acceptance test was executed. Other callers and guards outside these inspected methods are not ruled out.

## Proposed (not implemented or frozen)

Candidate RC-R5(16), separate from (13)–(15): an ordinary `record("A-000", payload)` attempt must be denied **before** changing the existing A-000 value, with an attributable rejection record; an authorized explicit update must be scoped, independently reviewed, preserve pre/post digests and failure evidence, and be distinguishable from an alias repair. Include direct `known` dictionary mutation in the threat model; guarding `record` alone is insufficient because the dictionary remains publicly mutable.

**Challenges:** a separate authoritative write gateway could narrow this observation, but none is visible in the inspected method; permission design, issuer, custody, revocation, canonicalization and test freeze remain Timothy's decisions. No source, shared Library, frozen tests or main branch changed.
