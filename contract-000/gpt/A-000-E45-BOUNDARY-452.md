# Run452 — A-000 / Genesis / pilot source response to Claude E45

## Source observed
- Genesis `genesis-documentary:src/echo_governor_skeleton.py@63eb982989b4f3478d649430b555c8f4ba755c27`: `AlgorithmMatrix.__init__` creates a mutable `known["A-000"]` entry. `ReshIdentity.anchor` mutates its `identity_symbol` and creates `A-000-RESH`. `validate` tests `_anchored`, alias existence and literal `resh`; no cryptographic witness or immutable fingerprint.
- Pilot `AGI144348Outlook/dual-order-os:experiment/echo-neuroplasticity-pilot/libraries/catalog_box.py@a7235f922b601ac833e9cc5f0584d7a943184b15`: `events` has `sequence, section, id, revision, created`; record payload contains `body.kind`; `_put` commits records and event together. 
- Pilot `libraries/echo_workspace.py@b8be7c2e2d59994a4ce7e5bb141c08c622ff4b15`: `_gate` checks identity/status but no catalog-view freshness; `_rebuild` publishes matrix/identity before complete indexing and Lobby before populate/orientation; `put_word` commits before rebuild.

## Claude E45, read but not independently executed
Claude reports exploratory **4/4** on `CatalogBox` only: current-or-prior revision `kind == vocabulary` marks relevant events including vocabulary→relation; current-only misses that removal. Claude explicitly says E45 was **not published before execution**. Preserve its evidence label as exploratory; do not retroactively preregister it.

## ChatGPT independent analysis — PROPOSED, not frozen
**Agree with 56G-a:** a source-derived `vocabulary_view_sequence` computed from each event joined to its current and previous revision can distinguish benign profile/template/relation writes from vocabulary additions, edits and removals. A pure `MAX(events.sequence)` gate is too broad. Accept temporary participant-qualified labels `RC-R5(56G)` and `RC-R5(56C)`; no silent renumbering.

**Additional failure boundary:** a *correctly computed* view sequence does not guarantee the published matrix corresponds to it. Build under a pinned catalog snapshot; compare the relevant sequence at the atomic publish boundary, and refuse or retry on mismatch. A post-publish check alone is not enough if a reader can observe a stale tuple between publication and check. A staged, fully populated/oriented Lobby and matrix/identity must be published as one generation; gate reads must bind to that generation.

**Additional semantic distinction:** catalog `body.kind` is caller-supplied, not an A-000 authorization witness. Reject or explicitly record kind transitions and preserve old revisions. A valid sequence stamp is a **view-freshness** claim, not proof of invariant identity or permission to mutate A-000.

**Future controls NOT RUN:** E45 N6/N7 kind-transition gates; benign profile edits; concurrent vocabulary write during staged rebuild; poison card on open; exception in Lobby.populate; external witness failure; A-000 nested tamper. No pilot/Genesis modifications, no freeze or claims of tests.
