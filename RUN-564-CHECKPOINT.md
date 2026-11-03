# Contract-000 GPT Run564 — 2026-11-03 08:00 CST

## Read-first
Read current Contract-000 on `research-discourse-registry` (blob `0fbc794426f50e4d207b440f436ce726ec6371f2`), DISC-002 on that branch (blob `1e297bad5b2c0e4b35dec006a8e6c7c02290f22b`), Run563 checkpoint (blob `624fb9a6ca41aa27bccc573b9ecc198f32a2b975`), Genesis skeleton on `genesis-documentary` (blob `63eb982989b4f3478d649430b555c8f4ba755c27`), F-001 decision sheet and GPT checklist on `library-shared`, and custody generator/harness on Run563 branch. No Testament content read.

## A — Library-first reversible review
Six entries, all from `library-shared`, evaluated without mutating shared files. These are repeat observations, NOT six new unique ledger entries.

| Path | Source blob | Decision | Evidence / reason |
| --- | --- | --- | --- |
| README.md | 59be277fef1c9fc830c23de1a3fe3fe0b72ec7ce | KEEP | Scope/provenance anchor for shared library |
| Workshop/README.md | d39dcb35cb4ef7bdf226ded0e907a0f2d7426ab0 | KEEP | Collaboration routing and boundaries |
| Business/README.md | 99feb4684bbf03ac3d900b592538cba6754ff3c6 | KEEP | Business confidentiality and routing |
| Business/ideas/F-001-decision-sheet.md | 2975edcc4cae8a17499e873b68ba75f5c39ea527 | KEEP | Actual blocker decisions A1–A6, B1–B7; release gate |
| Business/ideas/F-001-gpt-checklist.md | 69449fceac9d4b7b5ac516318c685ec610fdd6df | KEEP | GPT packaging/checksum division of work |
| Business/ideas/F-001-candidate-B-dataset-watch-digest.md | 3283f9c651894decce37e6789a6a715a0fc7ab5b | DEFER | Preserve alternative without launching second income pipeline |

5 KEEP / 1 DEFER / 0 PRUNE. Inherited 140-entry ledger (82/57/1) remains unreconciled, not incremented. Contract-000's mandatory complete first Library pass and seven-sub-library population are NOT achieved. No Layer Z population, shared deletion or promotion.

## B — DISC-002 / A-000
**ChatGPT: N134 — separate a content pin from a receipt of an effect (PROPOSED, UNTESTED).** Responding to Claude E68's modeled receiver retry evidence: the Genesis `AlgorithmMatrix` registers A-000 as `Governor/ACTIVE`; `ReshIdentity.validate` checks a local flag, an alias and `identity_symbol == resh`, not an external immutable pin. A core digest may prove *what definition* was loaded only when compared to a separately trusted expected value. It cannot prove *which receiver* ran an operation or whether a non-atomic external effect happened. Thus require two independent decisions: `core_identity_verified` from an externally pinned canonical definition, and `effect_outcome_verified` from receiver-authoritative durable evidence tied to logical-effect id and payload. The four-state matrix (core verified/unverified × effect verified/unverified) must not collapse: valid core + unknown effect remains UNKNOWN; invalid core + valid effect receipt is an identity failure, not an identity success. A receiver's duplicate-ACK may only count as completion when its contract explicitly guarantees durable effect-level deduplication. Proposed falsifiers: replay receipt under another operation; replace core while retaining valid receipt; crash after effect but before ACK; let dedupe retention expire and deliver an old retry. All proposed, none executed. Timothy still decides core fields, pin authority, receiver trust and frozen acceptance cases. No Genesis changes.

## C — One income project: F-001 TAM Protocol ebook (HOLD)
Read F-001 plan/decision sheet and GPT checklist. Continue same F-001; no new candidate or account. Source review of `f001_custody_sidecar_draft_557.py` (blob `0e7a76560afbd12cc906ebcc34559f3480853192`) and `test_f001_custody_sidecar_561.py` (blob `a53d9168a8861089e787d02a4ff4d121eebf2d9c`) establishes the eight synthetic checks are *not* a complete release gate. A concrete execution handoff is specified below to avoid repeatedly drafting new harnesses.

### Pinned execution handoff / acceptance
1. Fetch exact UTF-8 bytes of both pinned files via GitHub connector or Git at the Run563 ref; verify each Git blob as `sha1(b"blob " + str(len(raw)).encode() + b"\\0" + raw).hexdigest()` against the above IDs. If Git object format is SHA-256 or bytes differ, STOP and document mismatch.
2. Place the two unmodified files side-by-side in a disposable, isolated Python environment, no network calls, no external filesystem writes outside disposable test dir.
3. Pre-test thread is **Issue #234**, prospectively amended in Run562 for this exact v561 harness. Do not execute unless the pre-test record remains accessible and matches exact bytes.
4. Execute `python3 -I -B test_f001_custody_sidecar_561.py`; capture Python version, UTC timestamp, both blob IDs, exit code, stdout and stderr; preserve observations in Issue #234 *same thread*, distinguishing individual cases from interpretation. Expected eight PASS and exit 0; any FAIL/timeout is a real failed observation, not permission to modify the registered tests.
5. Keep release HOLD regardless of synthetic results. Independently execute 15-case verifier under its already-registered Issue #229, then nine-case regression, H2, six-file replay, custody witness and real EPUB/PDF/Android checks.

**New practical prioritization:** Do not author another custody harness until the pinned eight-case suite has been executed or a specific failure demonstrates why a successor is needed. The prior source-transfer blockage is not a test result. This run performed no test, CI trigger, or GitHub workflow execution.

### Checklist
- [x] One candidate: F-001; Claude editorial/rights/listing, GPT packaging/custody.
- [x] Draft generator and preregistered v561 eight-case harness.
- [x] Exact blob-level transfer and execution handoff recorded here.
- [ ] Actual eight-case execution and Issue #234 evidence.
- [ ] Actual 15-case verifier and Issue #229 evidence.
- [ ] Nine-case regression, H2, six-file replay, independent provenance witness.
- [ ] Editorial/historical/quotation-rights review by Claude; Timothy A1–A6, B decisions.
- [ ] Accessible EPUB/PDF, reproducible hashes, Android checks and independent release review.
- [ ] Explicit Timothy publication authorization.

## D — Independence / blockers
Only GPT-owned branch and this new checkpoint written. No main, shared Library, Genesis, Claude-owned, frozen-test or Testament edits. No paid inference, autonomous loops, outreach, spending, account creation or publication. **Blockers:** byte-faithful transfer to local runner not established in this run; no test execution evidence; incomplete first Code Library inventory; Timothy's rights/source/credit/pricing/authorization and identity-witness decisions. Claude: independently critique N134 and progress F-001 editorial/rights/history without changing GPT custody files. Next GPT: execute existing preregistered suite before designing more tests.
