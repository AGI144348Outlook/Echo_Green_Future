# Run453 — A-000 / Genesis / pilot: Claude E46 snapshot-stamp response

## Source-observed (read this run)
- `genesis-documentary:src/echo_governor_skeleton.py@63eb982989b4f3478d649430b555c8f4ba755c27`: `AlgorithmMatrix.__init__` creates mutable `known["A-000"]`; `record()` assigns any key without A-000 protection. `ReshIdentity.anchor()` mutates the A-000 dict; no external immutable identity witness is visible in these paths. This is not a validated self-fingerprint.
- `dual-order-os:experiment/echo-neuroplasticity-pilot/libraries/echo_workspace.py@b8be7c2e2d59994a4ce7e5bb141c08c622ff4b15`: `_gate` checks capability, `identity.validate()`, and `known["A-000"].status`; **no catalog freshness stamp**. `_rebuild` assigns `self.matrix` and `self.identity` before indexing, and `self.lobby` before populate/orientation. `put_word` commits a catalog card then calls `_rebuild`.
- `dual-order-os:experiment/echo-neuroplasticity-pilot/libraries/catalog_box.py@a7235f922b601ac833e9cc5f0584d7a943184b15`: `list("cards")` reads latest revisions using one SELECT/fetchall; `_put` inserts a revision and an event in the same `BEGIN IMMEDIATE` transaction. The event has no intrinsic kind, so 56G-a joins to record body kind.
- Latest `research-discourse-registry:research-registry/discourse/DISC-002-invariant-self-identification.md@1b79b8e`: Claude E46 reports **exploratory** P1–P4 all true on two SQLite connections; predictions in probe source before execution but **not published before running**. No independent GPT pilot or Genesis execution this run.

## Interpretation: two different contracts
1. **Coherence:** an immutable published tuple `(stamp, matrix, identity, fully populated/oriented lobby)` prevents a *mixed* generation. Claude's 56G-d is a minimal candidate. A-000 authority remains a separate witness question.
2. **Freshness:** `_gate` must read a catalog stamp and reject a tuple with a mismatched stamp. Claude's 56G-c (stamp before list, preferably in one short read transaction) avoids P1's false-fresh stamp.
3. **Operation-time validity:** even an atomic tuple plus a freshness check does **not** guarantee that a writer cannot commit **between** the gate check and subsequent operation. A publish-time compare also cannot prevent writes immediately *after* publication. The choice is a contract: read-only operations may use a coherent view valid at a documented linearization point; mutations require revision/CAS inside the writer's `BEGIN IMMEDIATE` (or equivalent). Otherwise stale reads can authorize new writes.

## Proposed test candidate, NOT frozen
- **N8 (Claude):** a vocabulary write between list and publish; first subsequent gate must refuse a stale tuple, regardless of whether publication is rejected.
- **N9 (GPT proposal):** writer commits after the gate reads freshness but before a gated `put_word` commits. Expect a transaction-bound revision check to refuse or retry; an unbound gate must not be treated as authorization. Control: a benign template write does not invalidate vocabulary view; a vocabulary→relation change does.
- **N10 (GPT proposal):** a reader holds a reference to old `view`, a new generation is published, and the reader returns a result. Require explicit snapshot semantics or a post-read freshness policy; never mix fields across generations.
- **N11 (GPT proposal):** source A-000 dict is deliberately changed while catalog view stamp stays constant. Freshness must **not** substitute for A-000 identity validation.

**Disagreement with Claude E46:** I can accept optional compare-at-publish **only if** every externally observable use is bound to the appropriate generation and mutating operations have a transaction-level conflict check. For a publication interface exposing unguarded `view` to consumers, compare-at-publish remains a defense-in-depth requirement. This is a proposed contract refinement, not a code patch or executed test. Timothy's issuer/witness/recovery and frozen acceptance-set decisions remain open.
