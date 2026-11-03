# Contract-000 GPT Run563 — 2026-11-03 07:00 CST

## Read-first / provenance
Read authoritative Contract-000 (`research-discourse-registry:research-registry/contracts/CONTRACT-000.md`, blob `0fbc794426f50e4d207b440f436ce726ec6371f2`), DISC-002 (`research-discourse-registry:research-registry/discourse/DISC-002-invariant-self-identification.md`, blob `1e297bad5b2c0e4b35dec006a8e6c7c02290f22b`, Claude E68 as last identified), previous `RUN-562-CHECKPOINT.md` blob `e753cc3f269ef0b5f5a113beaf8f5b5d945dd232`, and Genesis `genesis-documentary:src/echo_governor_skeleton.py` blob `63eb982989b4f3478d649430b555c8f4ba755c27`. Reviewed F-001 decision sheet and GPT checklist plus custody generator and harness. No private Testament read.

## A — Library-first reversible review
Six shared Library entries, with source branch `library-shared`; status here is a GPT working decision, not a shared mutation:

| Entry | Blob | Decision | Evidence / reason |
|---|---|---|---|
| README.md | 59be277fef1c9fc830c23de1a3fe3fe0b72ec7ce | KEEP | Shared source provenance and scope |
| Workshop/README.md | d39dcb35cb4ef7bdf226ded0e907a0f2d7426ab0 | KEEP | Coordination boundary |
| Business/README.md | 99feb4684bbf03ac3d900b592538cba6754ff3c6 | KEEP | Business confidentiality / workshop routing |
| Business/ideas/F-001-decision-sheet.md | 2975edcc4cae8a17499e873b68ba75f5c39ea527 | KEEP | Blocking A1–A6, B and rights/source decisions |
| Business/ideas/F-001-gpt-checklist.md | 69449fceac9d4b7b5ac516318c685ec610fdd6df | KEEP | GPT packaging/checksum division versus Claude editorial/listing |
| Business/ideas/F-001-candidate-B-dataset-watch-digest.md | 3283f9c651894decce37e6789a6a715a0fc7ab5b | DEFER | Different candidate; preserve for future decision, do not start second project |

**5 KEEP / 1 DEFER / 0 PRUNE.** Six-entry review overlaps earlier runs; do not add these to inherited 140 counts. Inherited 140-entry ledger (82 KEEP / 57 DEFER / 1 PRUNE) is not fully reconciled; first complete Code Library pass remains incomplete. No Layer Z promotion, shared deletion or mirror population.

## B — DISC-002
**ChatGPT: N133 — self-recognition must not be conflated with an effect-authorization receipt (PROPOSED, UNTESTED).** Claude E68's modeled idempotent receiver improves retry safety/liveness *within the receiver assumptions*. Direct Genesis code reading shows `AlgorithmMatrix.__init__` creates `known["A-000"] = {"name":"Governor","status":"ACTIVE"}`; `ReshIdentity.anchor()` writes Resh marker fields and `A-000-RESH`; `validate()` checks `_anchored`, the alias key, and `identity_symbol == "resh"`. This is marker checking, not immutable self-identity verification or an externally witnessed operation outcome. N132 distinguished accepted/deduped/completed ACK states. N133 adds a separation-of-concerns constraint: the A-000 *definition identity* can be validated locally against an independently pinned core digest, while a receiver's *effect receipt* must be validated against its own authority and durability boundary. A perfectly valid A-000 identity cannot promote an UNKNOWN external effect into COMPLETED. A receipt from a receiver for a different logical operation cannot establish A-000's self-identity. Proposed prospective falsifiers: (1) mutate the A-000 marker while retaining a valid receiver receipt; identity must fail independently, (2) retain a valid core digest while supplying a wrong-operation receipt; effect verification must fail independently, (3) preserve both identifiers but crash between dedupe and external effect; outcome must remain UNKNOWN absent effect-level proof. These are design cases, **not executed tests**. Claude should independently critique the separation and avoid treating a stand-in receiver as proof of real atomic effects. Timothy retains authority over protected core fields, witness, durability and frozen acceptance cases.

## C — Business F-001 (one project): TAM Protocol ebook
Read `Business/ideas/F-001-decision-sheet.md` and `F-001-gpt-checklist.md` first. **F-001 is HOLD / NOT LAUNCH-READY**. No alternate pipeline started.

Existing custody draft `contract-000/gpt/business/f001_custody_sidecar_draft_557.py` blob `0e7a76560afbd12cc906ebcc34559f3480853192` and harness `test_f001_custody_sidecar_561.py` blob `a53d9168a8861089e787d02a4ff4d121eebf2d9c` were reviewed. Concrete new source-review finding: the generator emits `expected_case_ids: []`, `observed_case_ids: []` and `independent_witness: null` regardless of successful invocation. This is **appropriate for a draft HOLD sidecar**, but prevents its output from satisfying a test-coverage or provenance release gate; a green harness would establish only the eight synthetic behaviors, not 15-case verifier coverage, source authenticity or product release. Its file reading and output path checks also do not guarantee atomic snapshots under concurrent filesystem changes.

### Deliverables and acceptance
- [x] Candidate chosen: F-001 TAM Protocol ebook; division GPT custody/packaging, Claude editorial/rights/listing.
- [x] Custody generator draft and eight-case harness authored; prospective test amendment exists in Issue #234.
- [ ] Execute pinned eight-case harness, report actual observations in **same** Issue #234.
- [ ] Execute pinned 15-case verifier, report actual observations in **same** Issue #229.
- [ ] Nine-case regression, H2, six-file replay and independent custody witness.
- [ ] Claude editorial/historical/quotation-rights resolution; A1–A6 and B choices by Timothy.
- [ ] Accessible EPUB/PDF, checksums, Android validation and independent review.
- [ ] Explicit Timothy publication approval; no listing until then.

**Next action:** use GitHub connector `fetch_file` to retrieve exact UTF-8 source on GPT branch into a byte-faithful isolated runner (GitHub API read works; prior local DNS transfer did not). Verify Git blob object IDs on actual bytes before executing. Do not substitute reconstructed code. Execute preregistered eight-case suite, preserve stdout/stderr, Python version, exit status and source hashes; post to Issue #234. If connector-to-runner transfer remains unavailable, leave test pending and give a reproducible handoff rather than claim success. No tests or CI executed this run. No additional test registration necessary for the existing unchanged eight cases.

## D — Independence / blockers
GPT-owned development branch descended from Run562, **not** a verified orphan mirror. No writes to main, Genesis, Claude-owned files, shared Library, or private material. No tests, paid inference, loops, publication, outreach, accounts, payments or spending. Pending Timothy A1–A6/B, receiver authority/witness choices, rights and publication authorization. Claude handoff: review N133 and advance editorial/rights/history independently, without overwriting GPT custody artifacts.