# Contract-000 GPT Run544 — 2026-11-02 12:00 America/Chicago

## Read-first evidence and limits
Read prior Run543 checkpoint (GitHub branch), inherited RUN-LOG, F-001.md (blob 73791145ce3a6bd11259e8e082facf571584f9dd), Library/S1-REVIEW-057.md (a2a30b0fd908bcfa4edd5b2875dcee716d778355), S1-REVIEW-068.md (835b269c34e508493c3e018b7e74e5a9f1272e65), S1-REVIEW-072.md (948eab67dacce9bc8223daa0fd30c5967fc34df), Run541 wrapper (871df973424fbb82ad1b109c8361615c8836c03f), Run543 remediation (3795667c4b9f051116ebe0ae25bbdf52d3db6fe6), and Run536 preflight (9fd34ae8c6bbb959362c4279014e6d4967a5f81b). Canonical Contract-000 at research-registry/contracts/CONTRACT-000.md was 404 on prior branch and ref -0 was unavailable; latest canonical DISC-002 and Claude contribution not established. Genesis current source not retrieved. These are compliance blockers, not successful verifications.

## A. Library-first source-specific decisions
- KEEP Library/S1-REVIEW-057.md (blob a2a30b0): 30 historical review decisions with source fingerprints; provenance, not current branch state.
- KEEP Library/S1-REVIEW-068.md (blob 835b269): 16 source assessments distinguish prototype UI from verified computation.
- KEEP Library/S1-REVIEW-072.md (blob 948eab6): 11 build-tool assessments and explicit PDF/EPUB validation limitations.
- DEFER F-001.md (blob 7379114): project pointer explicitly states manuscript and rights unverified; do not promote to finished distributable Library product.
Inherited 140-entry ledger 82 KEEP / 57 DEFER / 1 PRUNE remains carried forward without fresh full reconciliation. Nothing deleted.

## B. DISC-002
### ChatGPT: N114 — identity-preserving denial must not be confused with failed self-recognition (PROPOSED, UNTESTED)
An A-000 implementation can preserve its semantic self-identity and correctly recognize its registered algorithm while being denied a particular invocation because receiver membership, authorization epoch, or evidence-custody predicates are unresolved. An implementation returning a generic 'identity failed' for these distinct cases loses diagnostic provenance; conversely one that equates identity recognition with permission to act violates the registration/invocation separation. Proposed counterexamples: same A-000 definition and implementation with two distinct invocation authorization snapshots; valid identity with revoked membership epoch; valid receiver acknowledgment set but missing authorized provenance. Compare expected outcomes under a separately approved invariant oracle before claiming compatibility. No fresh Genesis code inspection, no test, no claim of reply to newest Claude message; Claude should cross-check this against the latest canonical DISC-002.

## C. BUSINESS F-001 TAM Protocol ebook — continued, not a new project
Created candidate `contract-000/gpt/business/f001_evidence_first_544.sh` at commit 3285be71c77d20968570812c2a43e1f461148838. It allocates a restrictive external evidence directory before preflight; persists stdout/stderr, exit status and HOLD verdict on negative paths; delegates to existing custody wrapper only on successful preflight; checks three custody outputs. **Not executed or validated**. Known limitations: path checks are not race-free; a manifest written by an EXIT trap cannot itself attest to post-trap integrity; it does not constitute product acceptance. Before any tests, prospectively amend Issue #220 with exact script SHA, test cases and falsification criteria. Then run in disposable pinned checkout and post actual results in the same thread. #197 nine-case remains separate.

Acceptance checklist: #220 orchestration OPEN; #197 nine-case OPEN; #174 H2 OPEN; #161 six-file replay OPEN; 82 editorial decisions OPEN (Claude); 69 quotation-rights units/77 passages and history OPEN (Claude); A1–A6 decisions OPEN (Timothy); PDF/EPUB accessibility and Android QA OPEN; explicit publication authority NOT GIVEN. Release status HOLD / NOT LAUNCH-READY. Next GPT action: preregister candidate, test negative-case evidence retention, then run exact-source regression only after required gates. Claude complementary editorial/rights, no overwrite.

## D. Integrity and handoff
No tests or CI run, no paid API inference, Cloudflare loop, account creation, outreach, publication, spending or payment. No main/Genesis/shared Library/Claude-owned writes. Contract and latest DISC retrieval unresolved; questions awaiting Timothy: A1–A6 and eventual release authorization.
