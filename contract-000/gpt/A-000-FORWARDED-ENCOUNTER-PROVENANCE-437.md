# Run437 — A-000 Genesis source trace: forwarded observation multiplicity versus mutual composition

**Scope:** exact `genesis-documentary:src/echo_governor_skeleton.py` Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`; read-only SOURCE-OBSERVED code inspection, **not executed Genesis**. Follows Run436 reciprocal-formula audit and Claude's latest DISC-002 2026-10-24 23Z. No source patch, frozen test or claim of original Echo learning.

## Timothy's specification — unchanged

```text
Alg-000 = Alg-000 + Alg-???
Alg-??? = Alg-000 + Alg(???)
```

Mutual composition with a stable rule shape as the Algorithm Matrix grows. `+` remains unspecified composition, not numeric addition, automatic commutativity, or proof of an identity invariant.

## New bounded source-level observation

1. `AlgorithmMatrix.index_content(text, category)` (approx. lines 441–468) increments `documents_seen` **once per invocation**, increments document frequencies for each distinct token and transition/co-occurrence counters for the text. There is no `observation_id`, source pin or forwarded-from field in its signature.
2. `SubAgentMatrix.index_content(text, category)` (approx. lines 9309–9335) checks whether *any* whitespace token belongs to the subagent's `domain_words`; if so it increments its own counters and calls `self.parent.index_content(text, category)`. Two distinct subagents with overlapping domain words can therefore each forward the **same original encounter** to the same live parent. The parent counts each forwarding as another document. This is **SOURCE-OBSERVED call structure**; the two-subagent outcome is an **INFERRED consequence**, not a tested runtime trace.
3. `SubAgentMatrix._seed_from_parent` (approx. lines 9268–9308) copies a domain slice of already observed parent transition/co-occurrence counts into the child's local counters. `predict_next` then combines current parent global counts with weighted local counts. This is explicitly designed domain emphasis, **not independent corroboration**; parent-derived prior and child-local evidence must not be counted as separate original experiences.
4. `AlgorithmMatrix.record(entry_id, entry)` still directly assigns `known[entry_id]`, including `A-000`. `ReshIdentity.validate` checks only its limited mutable markers; the intended A-000 R5 protection and external witness are not established by these source paths.
5. `HypothesisSandbox` (A-121) has a sandbox/registration loop for **algorithm hypotheses**, but that narrower subsystem does not establish open-ended concept discovery or a literal implementation of both reciprocal equations. Keep algorithm discovery separate from general discovery and vocabulary qualification.

**Why this matters to cataloging and recursive return:** A returning card may represent a legitimate *new encounter* or merely a repeated delivery of the *same encounter*. If parent and children have no common immutable event identifier, a high count cannot distinguish those causes. Repeated experience can be valuable, but repeated forwarding must not be silently upgraded into independent evidence. This is a provenance question, not an argument against intended child replication or recursive returning.

## RC-R5(41) candidate, PROPOSED / UNFROZEN / NOT RUN

An independent harness with two domain-overlapping subagents and one parent receives one immutable observation ID. Compare: (a) one source encounter forwarded by two children; (b) two genuinely distinct encounters with identical text; (c) an intentional recursive return to the same original observation; (d) a new comparison generated from that return. The invariant should preserve **one original observation identity** in (a) and (c), while allowing distinct processing/revision events and a second independently sourced encounter in (b). Test both orderings and child lineage; reject accidental conflation of child weighting with new source evidence. Explicitly measure parent `documents_seen`, transition counts and event provenance. The **current** `index_content` interface cannot express the distinction; test is not frozen and must not be presented as an actual failing Genesis run.

**Alternative explanations to preserve:** forwarding may intentionally mean a separate processing document, not a separate evidence witness; parent document count might be intended as ingestion count rather than unique source count. A new contract must specify both counters rather than silently changing historical semantics.

**Claude's latest DISC-002:** `visible_fields` in Swadesh Lesson 2 determines whether a score reflects genuine role inference. The analogous provenance boundary here is `visible_fields` plus `observation_id, parent_forwarding_id, source_pin, encounter_time, processing_event_id, catalog_revision`. These are candidate fields, not observed runtime fields.

**Status:** SOURCE-OBSERVED actual code; INFERRED duplicate-forward consequence; PROPOSED unfrozen RC-R5(41). No Genesis execution, no self-identifying algorithm proof, no shared or Claude changes.
