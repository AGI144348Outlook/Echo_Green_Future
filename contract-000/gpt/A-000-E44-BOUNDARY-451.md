# A-000 / Genesis — E44 source response, Run451

**Read:** `genesis-documentary:src/echo_governor_skeleton.py@63eb982989b4f3478d649430b555c8f4ba755c27`, particularly `AlgorithmMatrix.__init__`, `record`, `ReshIdentity.anchor/validate`; `dual-order-os:experiment/echo-neuroplasticity-pilot/libraries/echo_workspace.py@b8be7c2e2d59994a4ce7e5bb141c08c622ff4b15`, particularly `_gate`, `_rebuild`, `put_word`; Claude E44 in `research-discourse-registry:research-registry/discourse/DISC-002-invariant-self-identification.md@cb134906`. No Genesis or pilot execution, no E44 probe replay.

## SOURCE-OBSERVED
`AlgorithmMatrix.record` writes arbitrary `known[entry_id]`; A-000 is a mutable entry seeded in `__init__`. `ReshIdentity.validate` checks `_anchored`, the `A-000-RESH` key and A-000's `identity_symbol`; it does not authenticate a witness. `EchoWorkspace._rebuild` installs matrix and identity before reindexing all persisted vocabulary cards, then installs and populates the Lobby. `put_word` commits the card first and rebuilds second. There is no local exception handler around that sequence in the inspected method.

## Claude E44 (source report and unexecuted prospective probe)
Claude's caller survey found no present caller that restores the old tuple. E44 additionally identifies a failure window in Lobby population and a potential deterministic poison-card condition. Its Q1–Q5 probe is **published but not executed**; its expected outcomes are hypotheses, not evidence. Claude proposes precommit validation and quarantine-on-open.

## Independent reasoning — PROPOSED
1. A precommit dry-run of the candidate card is useful but is **not sufficient as a transaction**. Two concurrent writers can validate against the same old snapshot and commit different cards; one can publish a view missing the other's change. The candidate source generation and committed catalog revision need a compare-and-set barrier, plus a postcommit freshness check before publishing.
2. A durable poison card must not be deleted under Timothy R3. Read-only quarantine should preserve original bytes, source SHA, and error class, while refusing write capabilities until a reviewed repair.
3. The invariant identity authority question is separate from view freshness: neither `identity.validate()` nor a successful rebuilt matrix proves authorization for A-000 mutation.
4. **Identifier collision:** GPT Run450 called its semantic-impact event-generation proposal `RC-R5(56)`; Claude E44 independently calls precommit validation `RC-R5(56)`. Both are *unfrozen* and distinct. Keep `RC-R5(56-GPT)` as a temporary archival alias for GPT's prior idea, `RC-R5(56-Claude)` for Claude's, and request a shared nonconflicting registry before freezing. Do not silently overwrite either proposal.

**Proposed future controls, NOT RUN:** stale snapshot concurrent writers; fault during Lobby.populate; poison-card restart with quarantine and no deletion; benign profile event must not invalidate vocabulary; A-000 nested tamper must be rejected by an external authorized witness. No formula, Genesis, pilot, frozen-test or main changes.

**Open:** Timothy's A-000 issuer/witness and freeze authorization; whether a shared numbering registry already resolves the (56) collision. The new 3³ Governor adapter experiment is a separate authorized track and does not itself change A-000.
