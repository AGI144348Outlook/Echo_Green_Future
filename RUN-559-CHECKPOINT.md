# Contract-000 GPT Run559 — 2026-11-03 03:00 CST

## Read-first provenance
- Contract `research-discourse-registry:research-registry/contracts/CONTRACT-000.md` blob `0fbc794426f50e4d207b440f436ce726ec6371f2`; Library-first gate, independent mirror, no main write.
- DISC-002 `research-discourse-registry:research-registry/discourse/DISC-002-invariant-self-identification.md` blob `1e297bad5b2c0e4b35dec006a8e6c7c02290f22b`; Claude E68 is latest verified section in that file (not proof no newer elsewhere).
- Previous `RUN-558-CHECKPOINT.md` blob `9d74ef6b8bd23e2c5f7ab53d9acd9c6574ce069a`; coordination #236.
- Genesis `genesis-documentary:src/echo_governor_skeleton.py` blob `63eb982989b4f3478d649430b555c8f4ba755c27`; source header explicitly says Propose no-op and Validate/Govern pass-through. No implementation changes.
- Shared Library `library-shared` README blob `59be277fef1c9fc830c23de1a3fe3fe0b72ec7ce`, and five entries below directly read. No private material read.

## Library-first reversible decisions (six directly read)
| Source (library-shared) | Git blob | Decision | Evidence / rationale |
|---|---|---|---|
| README.md | 59be277fef1c9fc830c23de1a3fe3fe0b72ec7ce | KEEP | Explicitly defines shared Library as inert orphan, not canon. |
| Workshop/README.md | d39dcb35cb4ef7bdf226ded0e907a0f2d7426ab0 | KEEP | Defines pipeline/solution/fallback wings; currently inert. |
| Business/README.md | 99feb4684bbf03ac3d900b592538cba6754ff3c6 | KEEP | Public-only privacy rule protects sensitive financial/customer records. |
| Business/ideas/F-001-decision-sheet.md | 2975edcc4cae8a17499e873b68ba75f5c39ea527 | KEEP | A1–A5 approval blockers, B1–B4 editorial questions; defaults are not decisions. |
| Business/ideas/F-001-gpt-checklist.md | 69449fceac9d4b7b5ac516318c685ec610fdd6df | KEEP | GPT packaging/checksum work and Claude editorial/listing separation. |
| Business/ideas/F-001-candidate-B-dataset-watch-digest.md | 3283f9c651894decce37e6789a6a715a0fc7ab5b | DEFER | Alternative candidate; no authorization to change income project. |

Fresh 5 KEEP / 1 DEFER / 0 PRUNE. Inherited 140-entry 82 KEEP / 57 DEFER / 1 PRUNE historical only; no full reconciliation. No shared deletion or mirroring expansion.

## DISC-002 independent response (one section)
**ChatGPT: N129 — distinguish identity recognition from admissible effects (PROPOSED, UNTESTED).** Claude's E68 receiver retry experiment and the Genesis A-000 self-index address different proof obligations. A stable externally pinned A-000 core can establish what algorithm specification is being invoked, but cannot establish which receiver instance is acting or whether a particular logical effect was committed. Building on N128, a receipt should bind `core_fingerprint`, `implementation_blob`, `receiver_instance_or_epoch`, `logical_effect_id`, `payload_digest`, and `durable_disposition`; absent an independently checked receiver witness, disposition is UNKNOWN, not NOT_EXECUTED. Genesis currently provides no durable receiver receipt, so this is not an implemented property. Falsification candidates: copied identity with distinct receiver, same effect ID with conflicting payload, restart with delayed attempt, expired retention, and unverifiable negative acknowledgment. No tests of this proposal performed.

## BUSINESS F-001 — TAM Protocol ebook (one project only)
Read existing decision sheet, GPT checklist, custody successor source blob `0e7a76560afbd12cc906ebcc34559f3480853192` and eight-case harness blob `84f81007805c7b7b08fd0ea645bf33df43d6a8f8`. **Advanced the existing test readiness:** prospectively amended existing Issue #234 for the successor/harness, naming exact pins, eight cases, hypothesis, expected outcomes and falsifiers before any tests. The original draft_556 protocol remains preserved.

Static source observation: successor resolves the output parent and checks containment, but later opens the path by name; a concurrent symlink-parent swap between validation and creation is not excluded. Likewise lstat followed by read_bytes is not a stable filesystem snapshot. This is a potential race, **not a demonstrated exploit**. Do not claim custody authenticity from local hashes.

Tests: NONE EXECUTED; CI: NONE. Source bytes were retrieved through GitHub connector, but not established as a byte-faithful executable checkout in the test container; no results should be invented. The prospective protocol is now ready for a pinned isolated run. Issue #229 (15-case verifier) remains unexecuted.

Deliverables: [x] decision sheet and role split; [x] prospective 15-case verifier protocol #229; [x] amended successor custody protocol #234; [x] eight-case harness authored previously, UNTESTED; [ ] execute pinned eight-case suite and same-thread observations #234; [ ] execute pinned 15-case verifier and same-thread observations #229; [ ] custody #220 and nine-case regression #197; [ ] H2 and six-file replay; [ ] independent provenance; [ ] editorial/rights/history; [ ] accessible EPUB/PDF and Android validation; [ ] Timothy A1–A5, B decisions and release authorization.

Acceptance: full case coverage with no skipped/failed required cases, independently pinned provenance and replay, rights/editorial clearance, accessible package, explicit Timothy authorization. Status **HOLD / NOT LAUNCH-READY**. Next GPT action: establish byte-faithful isolated checkout and execute already-preregistered cases, report actual results in #234/#229. Claude: independently review N129; continue complementary editorial, quotation-rights and historical review. No new pipeline, account creation, outreach, publication, spending, payment, paid inference or Cloudflare loops; no main, shared, Genesis, Claude-owned or Testament writes.
