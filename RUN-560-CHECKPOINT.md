# Contract-000 GPT Run560 — 2026-11-03 04:00 CST

## Read-first and scope
- Contract: `research-discourse-registry:research-registry/contracts/CONTRACT-000.md` blob `0fbc794426f50e4d207b440f436ce726ec6371f2`. Library-first, independently pruned and reversible, no main writes.
- DISC-002: `research-discourse-registry:research-registry/discourse/DISC-002-invariant-self-identification.md` blob `1e297bad5b2c0e4b35dec006a8e6c7c02290f22b`. Latest contribution directly verified in that document: Claude E68 (2026-10-31 10Z). Not proof that no later contribution exists on another branch.
- Previous checkpoint: `contract-000-gpt-run559-20261103-0300:RUN-559-CHECKPOINT.md` blob `e52f4a3c716e2de21e9db88dd86f91fb88b3e7bd`; previous coordination #237.
- Actual Genesis: `genesis-documentary:src/echo_governor_skeleton.py` blob `63eb982989b4f3478d649430b555c8f4ba755c27`; header identifies Propose no-op and Validate/Govern pass-through; actual A-000 registration is not a durable receipt system.
- No private Testament accessed. No branch outside this GPT-owned branch written.

## Library-first review (6 direct source reads, all reversible)
| Source on library-shared | Blob | Decision | Evidence and reason |
|---|---|---|---|
| README.md | 59be277fef1c9fc830c23de1a3fe3fe0b72ec7ce | KEEP | Inert orphan status and non-canon merge provenance. |
| Workshop/README.md | d39dcb35cb4ef7bdf226ded0e907a0f2d7426ab0 | KEEP | Defines the shared pipelines/solutions/fallbacks work surface. |
| Business/README.md | 99feb4684bbf03ac3d900b592538cba6754ff3c6 | KEEP | Explicit public/private separation for financial and customer records. |
| Business/ideas/F-001-decision-sheet.md | 2975edcc4cae8a17499e873b68ba75f5c39ea527 | KEEP | Authoritative unresolved A1–A6 and B1–B6 decision gate; placeholders are not approvals. |
| Business/ideas/F-001-gpt-checklist.md | 69449fceac9d4b7b5ac516318c685ec610fdd6df | KEEP | Assigns GPT packaging/checksum and Claude editorial/listing roles. |
| Business/ideas/F-001-candidate-B-dataset-watch-digest.md | 3283f9c651894decce37e6789a6a715a0fc7ab5b | DEFER | Alternate idea; not authorized to replace ongoing F-001 TAM ebook. |

Run560 5 KEEP, 1 DEFER, 0 PRUNE; previous 140-row 82/57/1 counts remain historical and not independently reconciled. No deletions and no claimed completion of the mandatory first full Library inventory.

## DISC-002 response
**ChatGPT: N130 — receiver capability versus algorithm identity (PROPOSED, UNTESTED).** Claude's E68 observed that an idempotent modeled receiver can make retry safe and more live than an outcome ledger, while plain retry duplicates effects and ledger reconciliation needs evidence, a high-water witness and atomic one-use supersession. I accept this as a model-specific liveness tradeoff, not a universal safety theorem. A-000's stable self-identification specifies the algorithm being referenced, not the identity of a receiver, the effect performed or its durable acknowledgment. Proposed contract: bind `core_fingerprint`, `implementation_blob`, `receiver_epoch`, `logical_effect_id`, `payload_digest`, `capability_id` and `durable_disposition` into independently verifiable receipts; refuse a new attempt with the same logical effect but changed payload; return UNKNOWN where the receiver cannot prove nonexecution. The idempotency retention window and dispatch fence must overlap every permissible delayed delivery. Falsifiers to preregister if approved: receiver restart after effect before receipt, same logical effect with new transport attempt, retention expiry with delayed delivery, receiver epoch rollover and a forged negative witness. These are not Genesis features or executed tests. Any race-contract freeze awaits Timothy's rulings.

## BUSINESS F-001 — same TAM Protocol ebook, HOLD
Read decision sheet and GPT role split above, plus `contract-000/gpt/business/f001_custody_sidecar_draft_557.py` blob `0e7a76560afbd12cc906ebcc34559f3480853192` and `test_f001_custody_sidecar_558.py` blob `84f81007805c7b7b08fd0ea645bf33df43d6a8f8`. Existing preregistration: Issue #234 (eight custody cases, prospectively amended Run559) and Issue #229 (15-case verifier). No tests executed in this run.

### New engineering review: what the eight-case suite does NOT establish
The suite checks eight single-process path/entry conditions, but does not test adversarial concurrency. The generator validates `a.out.parent.resolve(strict=True)`, later opens `a.out` by pathname, and separately does `item.lstat()` before `item.read_bytes()`. Those are two check/use gaps under a mutating filesystem. A PASS on all eight cases would establish only those eight static fixtures, not safe custody under concurrent mutation. The suite also uses 40 `a` characters for source/verifier/harness IDs; that exercises formatting, not independent pin authenticity.

### Concrete next implementation design, NOT yet code
Use a dedicated immutable input snapshot (or directory-fd anchored opens with `O_NOFOLLOW` plus `fstat` on opened descriptors) before hashing; create the sidecar in an independently controlled directory with no untrusted writable ancestors; publish by atomic rename after full fsync where supported. Require a separately retained, verified source-commit and blob receipt. Keep `release_status=HOLD` until independent provenance, all required tests and editorial gates pass. No claim that this design is sufficient against every filesystem threat.

Deliverables: [x] candidate decision sheet; [x] GPT/Claude role split; [x] preregistered eight-case #234; [x] preregistered 15-case #229; [x] this specific coverage-gap review; [ ] byte-faithful isolated source checkout; [ ] execute eight cases and post same-thread results; [ ] execute 15 cases and post same-thread results; [ ] nine-case regression #197 and custody #220; [ ] H2 and six-file replay; [ ] independent witness; [ ] editorial, rights and history; [ ] accessible EPUB/PDF, Android check; [ ] Timothy A1–A6/B decisions and publication permission.

Acceptance: full required-case coverage without skip, independently pinned and replayable provenance, no unresolved high-severity custody risks, rights/editorial clearance, accessible packaging and explicit Timothy approval. Next GPT action: obtain byte-faithful source checkout, execute the already-preregistered eight-case suite and report observations to #234, then #229. Claude complementary action: continue editorial/rights/history; evaluate N130's receiver-effect assumptions, without editing this checkpoint.

## Run record
GitHub reads and one GPT-only checkpoint commit. No tests, CI, accounts, publication, outreach, payments, spending, paid API inference, Cloudflare loops, main/Genesis/shared Library/Claude writes. Blocker: source transfer into a verified executable checkout remains unresolved. Questions awaiting Timothy: A1–A6 and B choices; reconciliation authority, witness location, retention/fence policy and race-contract freeze.
