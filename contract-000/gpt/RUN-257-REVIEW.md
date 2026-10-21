# Contract-000 / GPT Run 257 — independent source review and handoff
Date: 2026-10-21. Status: DRAFT, NO TESTS EXECUTED. GPT-owned mirror only.

## Source baseline
- Contract: research-discourse-registry:research-registry/contracts/CONTRACT-000.md @ 0fbc794426f50e4d207b440f436ce726ec6371f2.
- Timothy rulings: research-discourse-registry:research-registry/TJ-RULINGS.md @ 3ce87eb6b9215bd8d5dc0a2e4664b95479764161.
- DISC-002: research-discourse-registry:research-registry/discourse/DISC-002-invariant-self-identification.md @ ee5753b25417077cb46f8fa1466cfbf02180e0c8.
- Previous committed GPT checkpoint: mirror-chatgpt-root:contract-000/gpt/RUN-251-STATUS.md @ a6f9fb22d7b10c235fb1cfd6df871578c65fa81e; local Run-256 handoff consulted separately (not a commit).
- Dev Suite: dev-suite:pwa/python/algorithm_matrix.py @ f7cf46584a7c787367196ec0d1aae7178dd976e3.
- Genesis: genesis-documentary:src/echo_governor_skeleton.py @ 63eb982989b4f3478d649430b555c8f4ba755c27.
- F-001 builder @ ede8da6f9e33631bd7d329f0ace5a880258fac18, claim_scan @ 31f3dcff486c4c8cc96d514eb425da86834d00c3, listing_check @ adc3123c303168650e03270701cd3123afe0ce28.
- Claude's PATCH-75 @ 1f5fad3bfe95b676e61eb816ad13cacfc0b38e07 and APPLY-ORDER @ 1b8e47921a3dc416d782a444c800af5d79a7ad9d. Both PROPOSED.

## A. Library-first: 10 independently re-fetched blobs
These are source-identity and relevance classifications, not comprehensive functional audits. All matched the historical Run-255 ledger. PRUNE is reversible exclusion only. Nothing deleted. Seven KEEP, three DEFER, zero PRUNE.

| Decision | Source path (library-shared) | Git blob SHA | Reason |
|---|---|---|---|
| KEEP | Formulas/F-0001-Echo-Harness-Usability-Criterion.md | 09e5c0ec7e5b2e362b2b6fc05f7849c69bf36987 | Exact user notation preserved; semantics explicitly provisional. |
| KEEP | Workshop/pipelines/P-001-budgeted-inference/README.md | cae451754258a855ea914be8e0cbcec316bb246d | Budget architecture reference, no activation. |
| DEFER | Workshop/pipelines/P-001-budgeted-inference/reference-bot-run.yml | 1d643ee021cd395e509aecc35a66a46b8b0448bd | Executable scheduled inference path, not authorized. |
| DEFER | Workshop/pipelines/P-001-budgeted-inference/reference-worker.mjs | e912294e5344f442de8b39f39e28930ef5092eea | Executable inference path, not authorized. |
| KEEP | Workshop/pipelines/P-001-budgeted-inference/test-worker.mjs | e430c4bf9538eb634103d2e0f3af9ff3c196a721 | Inert offline test reference, not run. |
| DEFER | Business/tax/CALENDAR.md | 44dac4a981935e2f76dc5202d70fde87e0135616 | Tax dates/treatment require verification. |
| KEEP | Business/ledger/SCHEMA.md | 1a330a172d62775fc5a708502d7bdf4ada05e310 | Private ledger schema; no personal transactions. |
| KEEP | Business/records/RETENTION.md | a303c78e739c2592f90dffdeb6991f1aacbe8e51 | Records policy draft, review retention law before use. |
| KEEP | Business/ideas/F-001-tam-build/rebuild_datasets.py | fa3a62f76549ecaea6e226ba5cca41597000d790 | Offline dataset parser, review-only. |
| KEEP | Business/ideas/F-001-tam-build/claim_scan.py | 31f3dcff486c4c8cc96d514eb425da86834d00c3 | Claim evidence inventory; new source-binding gap below. |

## B. DISC-002 — one independent response

**ChatGPT:** SOURCE-OBSERVED: Dev Suite alg_001 compares the invariant matrix slot, but alg_002 only checks status, permit, infrastructure and layout digest. Thus alg_002 is not a continuous invariant-slot validator. Genesis ReshIdentity.validate() checks anchor presence and identity_symbol == resh, while governor_validate_and_deploy() checks only name/status presence and ACTIVE status. These predicates are not equivalent. I agree with Claude's proposed single declared identity policy per adapter, lifecycle authority versioning, foundation precedence, and denial without automatic re-anchoring. Additional PROPOSED acceptance condition: every authority-bearing action must verify that its evidence binds to the *current* protected identity fingerprint AND lifecycle version, with explicit failure on missing, stale, or mismatched witness. A self-reported status alone is not an independent witness. This remains design, not implemented or tested. Timothy must decide protected fields, legal transitions, and the independent witness holder. Preserve audit mutability as a separately visible evidence gap.

## C. Business: F-001 TAM Protocol ebook only
Plan and decision sheet read. No new income pipeline. Claude's 12 patches remain PROPOSED. Product release remains HOLD.

New SOURCE-OBSERVED gap: claim_scan.py hashes source files in claims-report.json and writes claims.csv, but listing_check.py only checks whether claims.csv rows have allowed statuses. It does not check claims-report.json against the current build-report.json, nor does it authenticate the marked claims.csv. Thus a stale or substituted fully marked claims worksheet may be accepted after a manuscript change (INFERRED, not experimentally demonstrated). Note claim_scan.py scans Article 6/10 regardless of whether build.py includes them as independent chapters; a source inventory policy must account for that difference explicitly rather than silently ignoring them.

PROPOSED correction: a read-only release gate checks (i) source identity of every included manuscript chapter against a claim-inventory source hash, (ii) a recorded fingerprint of the reviewed claims.csv, (iii) an explicit inclusion/coverage map for conditional Article 6/10, and (iv) no missing or extra unreviewed manuscript sources. Keep claim_scan.py and Claude's existing scripts unchanged pending joint review.

Deliverables checklist:
- [x] Identified single product F-001 and source repository.
- [x] Existing draft builder, claims worksheet and listing gate available.
- [x] Claude's 12 proposed patch application order documented.
- [ ] Timothy A1–A6 decisions (material, storefront, credit, framing, price/refunds, source/licence).
- [ ] Editorial review of claims and manuscript completeness.
- [ ] Integrate jointly approved patch stack in isolated GPT/Claude staging.
- [ ] Pre-test Issue entry, then synthetic characterization tests with post-test evidence.
- [ ] Build and validate PDF/EPUB and datasets, produce reproducible source/output checksums.
- [ ] Cross-check listing, accessibility, rights, pricing, terms and refund policy.
- [ ] Timothy explicitly authorizes any publication, outreach, spending or payment actions.

Next action: publish the prospective test notice in Issue #13; after it succeeds, test the claim inventory binding with synthetic fixtures (unchanged, modified source, replaced claims.csv, missing source, conditional chapters). Acceptance: all expected failures fail closed, valid build passes, provenance evidence is reproducible and independently reviewed.

## D. Run evidence and blockers
Attempted pre-test Issue #13 comment before any diagnostics or tests. Connector response: "This tool call was blocked by OpenAI's safety checks. Please double check what you are sending." Exact reason unknown. Therefore NO tests, CI, benchmarks, diagnostics, builds, paid inference or deployments performed. No shared or main branch writes, no deletion, no publication, outreach or spending. This document is a development checkpoint only if a resulting GitHub commit is confirmed; otherwise retain as local handoff. Questions awaiting Timothy: A-000 protected identity fields, allowed lifecycle transitions and external witness holder; F-001 A1–A6.
