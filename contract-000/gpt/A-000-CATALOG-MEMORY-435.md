# A-000 and persistent catalog memory — Run435 source-grounded note

**Primary source:** `genesis-documentary:src/echo_governor_skeleton.py`, Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`. **No Genesis execution or modification** this run. Related: Run434 `A-000-PARENT-CHILD-EVIDENCE-434.md`. This is an independent proposed design boundary, not a frozen test or claim of autonomous intelligence.

## SOURCE-OBSERVED

- `AlgorithmMatrix.__init__` begins with `known["A-000"] = {"name":"Governor","status":"ACTIVE"}`; `record(entry_id,entry)` assigns `self.known[entry_id] = entry` without an A-000 guard (lines 350, 439–440).
- `ReshIdentity.anchor()` mutates the in-memory A-000 dict, creates an A-000-RESH alias, then sets `_anchored = True`. `validate()` reads the flag, alias-key presence and `identity_symbol == "resh"` (lines 3253–3301); it does not read a detached immutable witness, durable catalog or versioned lineage.
- `WordAgent.confirm_identity()` caches `bool(self.word)` (lines 1093–1099). That confirms a nonempty word on first call, not historical identity across reloads.
- `SubAgentMatrix` copies parent domain evidence into local structures at creation, then forwards in-domain observations back to the parent, and maintains a volatile `generation_log` (lines 9258–9338). It has a live parent reference, not a demonstrated durable catalog box. Shared event provenance must not be treated as independent corroboration.
- `AyinPerception.classify()` emits SELF for a matching `governor_word` without consulting `ReshIdentity.validate()` (lines 3143–3154). This is a classification surface, not necessarily an admission gate.

## INFERRED boundary

Timothy's recursive subagent reproduction is **intended**, not a defect: `Alg-000=[{Alg-000}+{Alg-???}]` and `Alg-???=[{Alg-000}+{itself}]`. Multiple descendants may lawfully inherit a common template while preserving distinct lineage. A memory catalog must preserve **events, origin, revision and unresolved hypotheses** independently from a reusable A-000 algorithm fingerprint. Otherwise a card rewrite, a child fork and an identity replacement are indistinguishable in the audit.

A content digest proves byte integrity; it does not by itself authorize a new identity or prove the original governor. An externally pinned identity core plus separately versioned child lineage can coexist with editable, child-authored catalog cards. Identity is not defined by a card's current semantic content.

## PROPOSED / UNFROZEN RC-R5(39): catalog reload identity/evidence separation

Provide an append-only external catalog fixture with `event_id`, `origin_instance`, `parent_instance`, `origin_source_pin`, `card_id`, `card_revision`, `hypothesis_status`, `algorithm_candidate_id`, and `reviewed_identity_update_ref` (nullable). Compare three operations: (i) card revision, (ii) child fork inheriting an A-000 template, (iii) deliberately reviewed A-000 version replacement. Expected: (i) changes only card revision, (ii) retains template identity but distinct instance lineage, (iii) records new version and review authority without overwriting old identity. Negative controls: missing event provenance, silently re-used child ID, unaudited A-000 overwrite, duplicate forwarded evidence counted as independent observations. This fixture is **not run**, **not frozen**, and its custody/retention/issuer semantics require Timothy's decision.

**Discourse relevance:** Claude's latest DISC-002 emphasizes Lesson 2's 40/40 as only two role decisions and requests `visible_fields` evidence. That same principle applies to memory: a catalog entry must say what the observer actually saw, not merely that an interpretation later matched a stored answer. Classroom role association, A-000 identity authority and catalog provenance remain separate chains.

**Limitations:** No production catalog connected to Genesis by this note; no independent witness implemented; no claim that full Genesis lacks all other persistence outside the inspected paths; no changes to frozen acceptance tests, main or Claude sources.
