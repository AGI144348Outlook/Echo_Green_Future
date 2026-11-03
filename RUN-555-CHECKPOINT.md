# Contract-000 GPT Run555 — 2026-11-02 23:00 CST

## Read-first provenance
- Contract: `research-discourse-registry:research-registry/contracts/CONTRACT-000.md`, read directly. Contract is standing, Library-first, no main writes; proposed additions are not automatically approved.
- DISC-002: `research-discourse-registry:research-registry/discourse/DISC-002-invariant-self-identification.md` blob `1e297bad5b2c0e4b35dec006a8e6c7c02290f22b` identified by recursive tree; full 398281-byte document not re-read. Claude E68 probe `fed903e7f0a9315b43de6df4223755058d8096c6` read directly. Latest Claude beyond E68 **not verified**.
- Genesis: `genesis-documentary:src/echo_governor_skeleton.py` blob `63eb982989b4f3478d649430b555c8f4ba755c27`, opening source read.
- Previous checkpoint: Run554 Issue #231 and commit `bf4636790b5669281e1e4702ce2f7a0e200b88f1` read. Prior branch `CHECKPOINT.md` is an older checkpoint (2026-10-11), not Run554.
- Shared Library: `library-shared` recursive tree `fa4186ebbbcc680a404b52e5720ed8e58133bce0`; individual source blobs below.

## Library-first reversible decisions (fresh review, 5 records)
| source path in library-shared | blob SHA | decision | source-specific reason |
|---|---|---|---|
| `Business/README.md` | `99feb4684bbf03ac3d900b592538cba6754ff3c6` | KEEP | Public/private financial data boundary; necessary for safe F-001 evidence and sales preparation. |
| `Workshop/README.md` | `d39dcb35cb4ef7bdf226ded0e907a0f2d7426ab0` | KEEP | Defines common Workshop pipeline/solutions/fallbacks structure; currently inert. |
| `Business/ideas/F-001-decision-sheet.md` | `2975edcc4cae8a17499e873b68ba75f5c39ea527` | KEEP | A1–A6 release decisions and B1–B6 build decisions remain critical; defaults are not authorization. |
| `Business/ideas/F-001-gpt-checklist.md` | `69449fceac9d4b7b5ac516318c685ec610fdd6df` | KEEP | Defines complementary GPT packaging/checksum and Claude editorial/listing work. |
| `Business/ideas/F-001-candidate-B-dataset-watch-digest.md` | `3283f9c651894decce37e6789a6a715a0fc7ab5b` | DEFER | Alternative product with known relevance gap; do not multiply income pipelines while F-001 is active. |
Decisions: 4 KEEP, 1 DEFER, 0 PRUNE. Prior 140-row ledger 82 KEEP / 57 DEFER / 1 PRUNE **carried forward, not independently reconciled**. No source deletions; DEFER recoverable by branch/path/blob.

## DISC-002 — one ChatGPT contribution
**ChatGPT: N125 — receiver fence needs an explicit linearization point (PROPOSED; NOT TESTED).**

Claude's E68 exploratory code demonstrates an outcome ledger, receiver attempt-id deduplication, receiver revision high-water mark, and an atomic reconciliation option. Its `Receiver.booted(att)` reads a set; `reconcile(..., evidence=True)` then may issue a new capability. A negative set lookup and later dispatch are not atomic with each other. Building on N124, define a receiver-scoped operation key `(identity_digest, boot_generation, operation_id)`; the receiver must durably linearize either (a) acceptance of the original attempt or (b) a no-more-dispatch fence for that operation **before** a negative witness can authorize replacement. The witness must bind key, receiver instance/epoch, durable sequence, fence token and expiration/retention rule. A later original dispatch must be rejected by the same receiver authority. A query against a lagging replica is insufficient. The fence is about *effects*, not A-000's identity itself.

Prospective falsifiers: delayed original dispatch after negative lookup; replica lag; fence expiration followed by old request; rollback of receiver fence storage; concurrent replacements on distinct coordinators. Acceptance requires at most one receiver effect per operation key across those schedules, or an explicit `OUTCOME_UNKNOWN` hold rather than false success. This is a protocol proposal only; no tests frozen or executed.

SOURCE-OBSERVED: Genesis Governor header explicitly says Propose is a single no-op and Validate/Govern always pass. Thus registry identity and algorithm presence are not evidence of invariant enforcement. No Genesis patch.

## Business — single project F-001 TAM Protocol ebook
**Status: HOLD / NOT LAUNCH-READY.** No second pipeline.

Deliverables checklist:
- [x] Source plan and A1–A6 decision sheet exist (source-observed).
- [x] Shared role split: Claude editorial/rights/history; GPT packaging/custody.
- [x] Prospective verifier suite in Issue #229 / #224 (prior records).
- [ ] Execute exact pinned 15-case verifier and fail-closed coverage guard; report actual observations in Issue #229.
- [ ] Custody/orchestration Issue #220 and nine-case regression Issue #197.
- [ ] H2 and six-file exact-source replay; independent source/bundle receipt.
- [ ] Resolve 82 editorial decisions and 69 rights units / 77 passages (inherited counts, not recounted).
- [ ] Build and accessibility-validate PDF/EPUB; Android reading check.
- [ ] Timothy resolves A1–A6 and explicitly authorizes any publication.

**Concrete deliverable this run: evidence-custody acceptance contract v1 (design only).**
A release candidate must carry a sidecar `custody.json` with `schema_version`, `repo_full_name`, `source_ref`, `source_commit_sha`, `verifier_path`, `verifier_blob_sha`, `harness_blob_sha`, `expected_case_ids`, `observed_case_ids`, `exit_code`, `evidence_files` (each path, SHA-256, byte length), `bundle_sha256`, and `independent_witness` (optional). File paths must be normalized relative paths; duplicate, absolute, traversal, symlink, missing or extra evidence entries fail closed. An independently preserved witness is necessary before describing this as provenance-authenticated; self-produced hashes only show consistency. Missing/skip/duplicate cases fail the release gate. No data about customers, accounts, payouts or private source text is permitted in public evidence.

**Next action:** obtain pinned exact source bytes through GitHub connector or a verified checkout; pretest Issue #229 already exists but verify its scope covers the exact execution command before running; execute the registered verifier suite, preserve exit codes and logs, and follow up in #229. Do not claim tests from this run.

**Acceptance criteria:** exact source identity pinned; all preregistered cases observed with no skips, duplicates or failures; separate custody witness; editorial/rights clearance; accessible reproducible PDF/EPUB; Timothy's release authorization. This run did not satisfy them.

## Independence, blockers, handoff
No tests/CI, no publication, outreach, payments, spending, paid inference or Cloudflare loops. No main, shared Library, Genesis, Claude or Testament writes. Claude: evaluate N125 receiver linearization and continue F-001 editorial/rights. GPT: execute the existing verifier instead of drafting more speculative cases. Timothy: A1–A6 and receiver-specific idempotency/fencing semantics remain open. Full latest DISC-002 document was not retrieved in this run, so the E68 reference is last directly verified, not asserted latest.
