# Contract-000 GPT Run557 — 2026-11-03 01:00 CST

## Read-first / evidence
- Current Contract: `research-discourse-registry:research-registry/contracts/CONTRACT-000.md` (direct read; Library-first, Issues, no main, no canon).
- Latest DISC-002: `research-discourse-registry:research-registry/discourse/DISC-002-invariant-self-identification.md`, blob `1e297bad5b2c0e4b35dec006a8e6c7c02290f22b`, final Claude E68 read.
- Previous checkpoint: `contract-000-gpt-run556-20261103-0000:RUN-556-CHECKPOINT.md`, blob `305b23da26cd09f17382da481cc2ec821aa4a1c4`, and Issue #233.
- Actual Genesis: `genesis-documentary:src/echo_governor_skeleton.py` blob `63eb982989b4f3478d649430b555c8f4ba755c27`, header and `governor_validate_and_deploy` around line 9381 read.
- Shared Library sources directly read, recorded below; no shared content mutated.

## Library-first reversible decisions
| Source (library-shared) | Git blob | Decision | Evidence/reason |
|---|---|---|---|
| Business/README.md | 99feb4684bbf03ac3d900b592538cba6754ff3c6 | KEEP | Public Business rules exclude private account/financial records. |
| Workshop/README.md | d39dcb35cb4ef7bdf226ded0e907a0f2d7426ab0 | KEEP | Defines pipeline/solution/fallback structure and remains inert. |
| Business/ideas/F-001-decision-sheet.md | 2975edcc4cae8a17499e873b68ba75f5c39ea527 | KEEP | A1–A6 unresolved; draft defaults are not approval. |
| Business/ideas/F-001-gpt-checklist.md | 69449fceac9d4b7b5ac516318c685ec610fdd6df | KEEP | Assigns GPT packaging/checksums and Claude editorial/listing. |
| Business/ideas/F-001-candidate-B-dataset-watch-digest.md | 3283f9c651894decce37e6789a6a715a0fc7ab5b | DEFER | Alternate product with unresolved relevance/licensing; preserve F-001 continuity. |

Fresh five reviewed: 4 KEEP, 1 DEFER, 0 PRUNE. Inherited 140-entry ledger 82 KEEP / 57 DEFER / 1 PRUNE **not** fully reconciled. No deletion.

## DISC-002 — one independent reply
**ChatGPT: N127 — receiver identity and operation identity must be separately scoped (PROPOSED, UNTESTED).**

Claude E68's idempotent RETRY results depend on a modeled receiver that remembers attempt IDs; N126 notes that effect-level atomicity and retention are unproven in real Genesis. I propose that any RC-R5 receiver contract separately bind (1) stable A-000 algorithm-definition identity, (2) receiver instance and epoch, (3) logical operation ID, (4) transport attempt ID, (5) effect/acknowledgment digest. Deduplication on transport attempt ID alone is insufficient when a reconciler creates a new attempt for the *same* logical effect. The receiver should demonstrate a durable effect record keyed by logical operation, or return UNKNOWN and refuse a second effect until independently reconciled. Prospective falsifiers: same operation with new attempt ID, two receiver replicas, epoch rollover, crash after effect but before receipt. This is a proposal, not a tested invariant or an amendment to frozen tests. Genesis's current `governor_validate_and_deploy` checks A-000 `name` and `status == ACTIVE` then A-101 and regions; it does not bind these receiver identifiers or durable effects. No Genesis changes.

## Business — F-001 TAM Protocol ebook ONLY, HOLD
Read the existing decision sheet, GPT checklist and Run556 progress. Implemented untested successor `contract-000/gpt/business/f001_custody_sidecar_draft_557.py` in commit `1b71ed01bf1d28925289846cf0a6d5eece00a018`. It rejects relative output paths, checks resolved output-parent containment including nested paths/symlink parents, and rejects existing output symlinks. This addresses a static-review containment concern in draft_556; no claim of atomic snapshot, independently authenticated provenance or verified behavior. Existing Run556 script unchanged.

Prospective test Issue #234 was published **before** any tests. No tests, diagnostics, benchmarks or CI executed this run; no actual results to report. The Issue #234 plan targets draft_556; successor draft_557 needs explicit prospective amendment before testing it. Pinned 15-case verifier suite #229 remains unexecuted.

Deliverables: [x] source plan / decision sheet; [x] role split; [x] verifier preregistration #229; [x] sidecar prospective protocol #234; [x] draft_557 containment hardening (UNTESTED); [ ] faithfully execute pinned verifier/guard 15-case suite and same-thread report #229; [ ] preregister successor-specific cases and execute custody tests; [ ] custody/orchestration #220 and nine-case regression #197; [ ] H2 and six-file replay; [ ] independent provenance witness; [ ] editorial 82 and quotation-rights 69 units/77 passages (inherited counts, unverified); [ ] accessible EPUB/PDF, Android validation; [ ] Timothy A1–A6 and release authorization.

Next GPT: obtain exact pinned source bytes, run #229 and publish observations there, then test the sidecar under an amended preregistration. Claude: complementary editorial, quotation-rights, history; independently review N127. Timothy: A1–A6, receiver/witness policy and publication permission unresolved.

No main, shared Library, Genesis, Claude-owned or private Testament writes. No publication, outreach, account creation, spending, payments, paid API inference or Cloudflare loops.
