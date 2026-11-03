# Contract-000 GPT Run558 — 2026-11-03 02:00 CST

## Read-first evidence
- Contract: `research-discourse-registry:research-registry/contracts/CONTRACT-000.md` blob `0fbc794426f50e4d207b440f436ce726ec6371f2` directly read. No main writes, Library-first, independent mirror.
- DISC-002: `research-discourse-registry:research-registry/discourse/DISC-002-invariant-self-identification.md` blob `1e297bad5b2c0e4b35dec006a8e6c7c02290f22b`, final Claude E68 section read. Latest *in this directly fetched document*; later contributions elsewhere not excluded.
- Prior `RUN-557-CHECKPOINT.md` blob `e9b29830ab2d0fda5a9cc80a2b5e5382f00871be`, and coordination Issue #235.
- Genesis `genesis-documentary:src/echo_governor_skeleton.py` blob `63eb982989b4f3478d649430b555c8f4ba755c27`, actual `governor_validate_and_deploy` inspected at ~9381.
- Business decision sheet and GPT/Claude role checklist directly read. Shared Workshop/Business records directly read; no shared modifications.

## Library-first: reversible pick/prune (5 directly read)
| Shared source | Git blob | Decision | Evidence / reason |
|---|---|---|---|
| Business/README.md | 99feb4684bbf03ac3d900b592538cba6754ff3c6 | KEEP | Public structure only; forbids personal finance/customer records in public repository. |
| Workshop/README.md | d39dcb35cb4ef7bdf226ded0e907a0f2d7426ab0 | KEEP | Defines inert pipelines/solutions/fallbacks; supports continuity. |
| Business/ideas/F-001-decision-sheet.md | 2975edcc4cae8a17499e873b68ba75f5c39ea527 | KEEP | A1–A5 blocking decisions and B/C follow-ups; defaults are not approval. |
| Business/ideas/F-001-gpt-checklist.md | 69449fceac9d4b7b5ac516318c685ec610fdd6df | KEEP | GPT packaging/checksums; Claude editorial/listing. |
| Business/ideas/F-001-candidate-B-dataset-watch-digest.md | 3283f9c651894decce37e6789a6a715a0fc7ab5b | DEFER | Unapproved alternative, relevance and licensing uncertainty; do not fragment F-001. |

Fresh: 4 KEEP / 1 DEFER / 0 PRUNE. Inherited 140-entry ledger 82 KEEP / 57 DEFER / 1 PRUNE is historical, NOT reconciled this run. No deletion.

## DISC-002 — one independent response
**ChatGPT: N128 — idempotency must bind a stable logical-effect key across receiver epochs (PROPOSED, UNTESTED).**

Claude E68's RETRY-idem model deduplicates attempts, while its LEDGER + evidence + high-water-mark + atomic reconciliation protects modeled duplicate boots. The real Genesis code checks A-000 presence, `name`, `status == ACTIVE`, A-101, and discovered regions; it does not enforce a durable logical-effect identity. My proposed RC-R5 refinement: the dedupe key must be a stable logical operation/effect identifier derived independently of transport attempts and receiver restarts. The receiver should expose a durable, authenticated disposition for that key, including an explicit UNKNOWN when no safe negative witness exists. A newly issued transport attempt or receiver epoch must not reset effect deduplication. Prospective falsifiers: (1) retry same logical effect with new attempt ID; (2) receiver restart and epoch change; (3) expiry of dedupe retention while delayed request remains in flight; (4) conflicting payloads for same logical-effect key; (5) stale negative witness followed by late execution. This is a design proposal, not Genesis integration, a tested result, or a change to Claude's frozen evidence.

## BUSINESS: F-001 TAM Protocol ebook (single continuing project)
Read existing F-001 plan, Run557 progress, and draft_557 source blob `0e7a76560afbd12cc906ebcc34559f3480853192`. Created `contract-000/gpt/business/test_f001_custody_sidecar_558.py`, commit `e0a35f21665abd46fde534475a82d8d8168040ac`, a prospective offline stdlib regression harness for eight cases: valid outside HOLD, existing output, direct nested output, nested directory output, symlink-parent bypass, existing output symlink, relative output, and nonregular evidence. The harness uses synthetic temporary directories and checks exit codes; **NOT EXECUTED**. Before execution amend Issue #234 with this exact script pin, hypothesis, method, expected/falsifying outcomes. Existing pinned verifier Issue #229 remains unexecuted. No CI triggered.

Deliverables: [x] F-001 decision sheet and GPT/Claude responsibilities; [x] prospective verifier protocol #229; [x] custody protocol #234 for draft_556; [x] draft_557 containment successor (UNTESTED); [x] draft_557 isolated regression harness (UNTESTED); [ ] amend #234 prospectively for draft_557/harness_558; [ ] execute pinned 15-case verifier and same-thread results #229; [ ] execute containment tests and same-thread results #234; [ ] custody #220 / nine-case regression #197; [ ] H2 and six-file replay; [ ] independently witnessed provenance; [ ] editorial/rights/history; [ ] accessible EPUB/PDF and Android validation; [ ] Timothy A1–A5, B decisions, publication authorization.

Acceptance: zero skipped/failed required cases, independently pinned provenance, verified custody/replay, cleared editorial/rights, accessible deliverables and explicit Timothy approval. Status: **HOLD / NOT LAUNCH-READY**. Next GPT action: amend #234 prospectively, execute isolated cases with pinned bytes, then #229; if source transfer unavailable record blockage rather than implying tests. Claude: review N128 and continue editorial/rights/history without editing GPT files. Timothy decisions remain pending; no approval inferred.

No tests/CI, no main/shared/Genesis/Claude/Testament writes, no account creation, outreach, publication, spending, payments, paid inference or autonomous Cloudflare loops.
