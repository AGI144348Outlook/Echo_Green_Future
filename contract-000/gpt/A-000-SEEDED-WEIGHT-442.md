# A-000 / Genesis source audit — Run442: seeded prior is amplified as domain signal

**Source inspected:** `genesis-documentary:src/echo_governor_skeleton.py@63eb982989b4f3478d649430b555c8f4ba755c27` (actual `SubAgentMatrix` lines ~9248–9340). **Claude latest DISC-002:** `research-discourse-registry:research-registry/discourse/DISC-002-invariant-self-identification.md@d059cf8`, 2026-10-29 11Z, E37 probe `ea56a405`. Read-only source analysis; **GPT did not execute Genesis or independently rerun E37**. Claude labels E37 execution-verified by Claude but not preregistered.

**SOURCE-OBSERVED:** `_seed_from_parent` copies parent transition/co-occurrence counts and document frequencies for domain words/boundary neighbors into child mutable stores at creation. `index_content` increments child local stores for in-domain text and calls `parent.index_content(text, category)`. `predict_next` combines `global_opts` from the *live* parent and `domain_weight × domain_opts` from the child; `domain_opts` includes the *copied prior plus new local exposures*. No immutable `inherited_from` or `original_observation_id` is passed or recorded in those method signatures. Child has no independent `documents_seen` denominator.

**Algebraic interpretation (INFERRED from code, not the invariant Echo Equation):** for a transition present at child creation, `score = parent_live + w × (seeded_parent_snapshot + child_local_exposures)`. A seeded count `c` already present in live parent contributes `(1+w)c`, while a new local encounter forwarded to parent contributes `(1+w)` per occurrence. Thus the weighting mechanism treats historical parent evidence as if it were domain-acquired evidence. With `w=2`, Claude's E37 reports seeded “river→meets” twice and new “river→runs” twice both scoring 6, with insertion-order tie favoring “meets”; the unseeded control scores meets 2 versus runs 6. **This table is Claude's reported run, not a new independent GPT result.**

**Additional boundary:** a child copies the prior once, while `parent` is a live reference. Later parent-only updates affect `global_opts` but not the seeded child copy. Without source markers, an evaluator cannot reliably separate inherited snapshot contribution, local processing and other agents' later parent updates. This is a provenance/weight-policy issue, not evidence that repeated exposures must be suppressed or that the formula is invalid.

**Timothy's invariant mutual-composition notation remains unchanged:**
```text
Alg-000=Alg-000+Alg-???
Alg-???=Alg-000+Alg(???)
```
The second line denotes the growing Algorithm Matrix; the matrix may grow without changing the governing formula. A-000 remains a protected self-identifying slot per R5; no ordinary `record()` mutation or patch is authorized.

**Proposed RC-R5(46) / Claude C-16 (NOT FROZEN, NOT RUN):** compare child predictions after (a) a parent snapshot seeded before child creation, (b) two new domain observations, (c) two later parent-only observations, using explicit independent receipts `inherited_from_snapshot_id`, `original_observation_id`, `processing_event_id`, and source-class `self_generated|outside`. Expected: current code's scores depend on the seeded prior and insertion order; a future *candidate* implementation could expose separately weighted prior/local/global components while preserving raw counts. **Challenge:** an existing caller supplies immutable provenance or the score does not match the code-derived decomposition. Do not execute or freeze this race without the contract's pre-test and independent adjudication. RC-R5(45) and C-14 are overlapping forwarded-observation candidates, not separate successful tests.

**Open:** Timothy's witness/custodian and race-freeze decision; whether domain prior should be discounted, kept equal, or treated as a distinct explicitly visible weight. This run does not decide policy. No source, shared, Claude or Genesis changes.
