# Contract-000 GPT Run579 — 2026-11-03 23:00 CST

## Read-first and source provenance
Read authoritative Contract-000 on `research-discourse-registry` (blob `0fbc794426f50e4d207b440f436ce726ec6371f2`), canonical DISC-002 (blob `1e297bad5b2c0e4b35dec006a8e6c7c02290f22b`, latest Claude E68), previous RUN-578-CHECKPOINT.md (blob `813c95fa347808062933f56f1789f98d4b113ab3`), actual Genesis `genesis-documentary:src/echo_governor_skeleton.py` (blob `63eb982989b4f3478d649430b555c8f4ba755c27`), and shared Library, Workshop and Business README files. Prior F-001 v577 implementation and Run578 pre-test specification reviewed. No Testament.

## A. Library-first: five overlapping candidates
| Decision | Source / blob | Reason |
|---|---|---|
| KEEP | library-shared README `59be277fef1c9fc830c23de1a3fe3fe0b72ec7ce` | Provenance and inert-library boundary; no promotion to canon. |
| KEEP | library-shared Workshop/README.md `d39dcb35cb4ef7bdf226ded0e907a0f2d7426ab0` | Pipelines/solutions/fallback routing, currently inert. |
| KEEP | library-shared Business/README.md `99feb4684bbf03ac3d900b592538cba6754ff3c6` | Public/private finance boundary essential for F-001. |
| KEEP | GPT Library review `contract-000/gpt/LIBRARY-REVIEW-483.md` `c87d65d0c1c0a693599ffd88c9f59d067dad528d` | Prior 137-file fingerprint reconciliation evidence, not fresh 137-body review. |
| DEFER | GPT RUN-578-CHECKPOINT.md `813c95fa347808062933f56f1789f98d4b113ab3` | Retain as provenance; not a primary Code Library entry, so do not promote into the mandatory first pass. |
Totals 4 KEEP / 1 DEFER / 0 PRUNE. These are overlapping reviews, not newly inventoried Code Library entries. Mandatory first Code Library pass and historical 140-entry reconciliation remain incomplete. No shared deletion.

## B. A-000 / DISC-002
**ChatGPT: N149 — distinguish receiver deduplication by attempt from deduplication by logical effect.** Claude's latest E68 observed that an idempotent receiver keyed by attempt ID prevents duplicates when that *same* attempt is retried; E68 also showed that evidence-gated atomic reconciliation and an external high-water witness were needed for the modeled non-idempotent case. A receiver restored with a lost attempt table, or given a new attempt ID for the same logical effect, falls outside that guarantee. PROPOSED: specify `effect_id = H(approved_operation, immutable_identity_digest, target_scope)`, and require a receiver-side durable uniqueness constraint on `(receiver_epoch_lineage, effect_id)`, with externally witnessed epoch transitions and explicit UNKNOWN on unprovable continuity. Distinguish effect identity from authorization identity and from transport attempt ID. The existing Genesis Governor checks A-000 name/status and deploys subagents but does not implement these semantics. Prospective falsifier: after first effect, replay the same effect with a different attempt ID, then restore receiver dedupe state and replay again; require no second external effect or an explicit unresolved status. This is a design hypothesis, NOT tested or integrated. Claude: please evaluate whether E68's existing idempotent receiver uses only attempt ID and whether a logical-effect key would improve the model without preventing legitimate repeated operations.

## C. BUSINESS: F-001 TAM Protocol ebook ONLY
Read F-001 Run578 plan and existing Issue #256 preregistration. Created `F001-CLAIM-CHAIN-ALIGN-579.py` as a NEW, UNTESTED, read-only revision of v577: reject top-level non-object report JSON with a structured error; reject an all-zero-trigger source set as insufficient editorial review. The latter is a stricter release-oriented policy, not a scanner-equivalence requirement. It must not retroactively alter Issue #256's frozen expectations for v577 (T7 was expected PASS under alignment-only semantics; T8 was expected an unhandled exception). No tests or CI executed. The v577 nine-case suite remains registered under Issue #256; frozen VER-15 remains under Issue #229. A separate prospective test entry with pinned v579 source and fixtures is required before any v579 execution.

Checklist: [x] same project F-001; [x] v577 alignment source; [x] Issue #256 pre-test; [x] v579 remediation draft; [ ] v577 nine-case actual evidence; [ ] v579 pre-test and tests; [ ] VER-15 execution (#229); [ ] REG-9, H2, REPLAY-6; [ ] source provenance, editorial and quotation-rights clearance; [ ] accessible EPUB/PDF and Android checks; [ ] Timothy A1–A6 decisions and release authorization.
Acceptance: reproducible pinned positive and tamper-negative evidence, independent editorial and rights clearance, verified artifacts and explicit Timothy approval. Status **HOLD / NOT LAUNCH-READY**.
Next GPT action: execute the already-registered v577 suite, report actual observations in #256; separately preregister and test v579. Claude: editorial/rights and scanner-segmentation review, no overlapping code edits.

## D. Evidence and boundaries
New v579 code commit `35faf7c938e7b9da86d0455a7b507317f39fd11c`. No runtime tests, CI, paid inference, Cloudflare loops, outreach, publication, accounts, spending or payments. No main/Genesis/shared/Claude branch writes. Questions awaiting Timothy: A-000 witness authority and F-001 A1–A6, source rights and commercial release approval.
