# Run440 — A-000/Genesis source audit: ingestion counts and independent observations

**Source:** `genesis-documentary:src/echo_governor_skeleton.py` blob `63eb982989b4f3478d649430b555c8f4ba755c27`. Read source; **Genesis was not executed**. This is independent of the F-001 synthetic scanner tests.

**SOURCE-OBSERVED:** `AlgorithmMatrix.record()` (line 435) assigns `known[entry_id] = entry` without protecting `A-000`. `ReshIdentity.validate()` (3296) tests the instance flag, presence of the alias, and `identity_symbol == resh`; it does not validate a full externally pinned invariant. Claude's E35 on a stub (DISC-002) already demonstrates that limitation; this run does not independently replicate E35.

**SOURCE-OBSERVED:** `AlgorithmMatrix.index_content()` (440–465) increments `documents_seen` **per call**; increments each unit's `content_units` document frequency; increments `word_categories`, token transitions and co-occurrences. `idf()` (477–481) uses `documents_seen` and `content_units`, and `predict_next()` uses transitions. `SubAgentMatrix.index_content()` (9304–9327) routes in-domain text and then calls `self.parent.index_content(text, category)`. There is no source-observation ID or forwarding receipt in those two paths.

**INFERENCE, not executed:** If the *same original* observation reaches two eligible children, parent indexing can count it twice. The effect is not limited to a display counter: the TF-IDF document-frequency substrate, A-103 transition weights and A-104 co-occurrence weights can change. This is not evidence of two independent source observations. It could still be a valid count of two **processing events**; the missing distinction is provenance and evidence independence, not whether repetition is inherently bad.

**Architectural reading:** Timothy's invariant mutual-composition equations remain unchanged:
```text
Alg-000 = Alg-000 + Alg-???
Alg-??? = Alg-000 + Alg(???)
```
The matrix's listing is not execution. A source observation, a forwarding event, a recursive return, and a validated independent encounter should be separate event types. This is relevant to the dormant Concept Token/recursive-return work as a possible consumer of trustworthy event history, **not** an assertion that those experiments are part of Contract-000 or already implemented in Genesis.

**RC-R5(44) — PROPOSED / UNFROZEN, not run:** Prepare one source observation with an immutable source ID, route it through two in-domain children and a direct parent path, and compare (a) processing-event counts, (b) unique observation IDs, (c) transitions/co-occurrence and TF-IDF weights, and (d) Governor identity pin. Under a proposed custody adapter, repeated forwarding should retain separate processing receipts without claiming extra independent observations; the A-000 core must remain unchanged. Challenge: if current code explicitly intends every forwarding to count as independent training exposure, a deduplicating weight policy could change behavior; test both exposure-count and unique-evidence interpretations, not silently rewrite either. Freeze and authority remain with Timothy under R5.

No Genesis, main, shared Library or frozen-test mutation. No claim of executed A-000 test.
