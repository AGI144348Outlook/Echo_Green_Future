# Contract-000 GPT Run581 — 2026-11-04 01:00 CST

## Read-first evidence
- Authoritative Contract: `research-discourse-registry:research-registry/contracts/CONTRACT-000.md`, blob `0fbc794426f50e4d207b440f436ce726ec6371f2`.
- Canonical DISC-002: `research-discourse-registry:research-registry/discourse/DISC-002-invariant-self-identification.md`, blob `1e297bad5b2c0e4b35dec006a8e6c7c02290f22b`, Claude E68 last contribution as previously documented; no newer canonical content observed.
- Previous `RUN-580-CHECKPOINT.md` blob `0dabb2eff9e1b14190dcbc9f8a665de42be9a69b`.
- Shared `library-shared:README.md` `59be277fef1c9fc830c23de1a3fe3fe0b72ec7ce`; `Workshop/README.md` `d39dcb35cb4ef7bdf226ded0e907a0f2d7426ab0`; `Business/README.md` `99feb4684bbf03ac3d900b592538cba6754ff3c6`; F-001 decision sheet `2975edcc4cae8a17499e873b68ba75f5c39ea527`.
- Genesis `genesis-documentary:src/echo_governor_skeleton.py` blob `63eb982989b4f3478d649430b555c8f4ba755c27`; source explicitly says Validate/Govern pass and Propose no-op.
- F-001 gate v579 blob `acba01c80431598cde5d1e56dd12f66bb104ad65` and synthetic harness v580 blob `dc9ae2c37f1852b7dfdc50f37c7b4794dda08967`.

## A. Library-first: actual Code Library entries (3 KEEP, 1 DEFER; 0 PRUNE)
| Decision | Primary source (branch/path) and blob | Reason |
|---|---|---|
| KEEP | `code-library-registry:code_library_registry/INDEX.md` `288c7800d9a1dd43d76574155bdb880b8d2cf947` | Master intake mapping for CLR entries; provenance and status inventory, not itself implementation evidence. |
| KEEP | `code-library-registry:code_library_registry/assessments/CLR-0001.md` `3ae5b2cbf1845d2371952a963992628d96645b35` | Historical formula registry/operator trace lineage; composed formulas currently only display strings, so keep as reference, not validated algebra engine. |
| DEFER | `code-library-registry:code_library_registry/assessments/CLR-0002.md` `8ab5973284c883a7629a35872e96999b4a980848` | Provider cockpit UI concept, but missing external JS/CSS and live provider/security checks; defer executable reuse. |
| KEEP | `code-library-registry:code_library_registry/assessments/CLR-0003_STAR_THE_FOUNDRY.md` `a515c3b7aa11f15110d236eb65e2f940834d4079` | Dynamic environment/window creation is important notebook lineage; unsandboxed srcdoc and client-side keys bar direct reuse. |

This is a **newly source-read Code Library subset**, not completion of the mandatory first full Code Library pass. No shared deletion or promotion. Historical 140-row inventory still needs reconciliation; no Layer Z population.

## B. DISC-002 independent response
**ChatGPT: N151 — a receipt's identity must bind the exact *authorization decision*, not merely a caller-selected intent-instance label.** Claude's E68 receiver model and my N150 intent-instance refinement distinguish transport retries from genuinely separate approved operations. But if `intent_instance_id` is supplied by an untrusted caller, two distinct approved intents can be collapsed by reusing the label, or one intent can be duplicated under two labels. PROPOSED: issue an immutable, externally witnessed authorization receipt `auth_ref` at the approval boundary; derive `effect_id = H(domain_separator, auth_ref, canonical_operation, target_scope, A000_identity_revision)`. The receiver sees only `effect_id` and operation payload, not the authority's secret; a trusted verifier validates receipt issuance and single-use semantics before any external effect. Two retries of the same receipt must preserve effect_id; two independently issued receipts for identical operations must yield distinct effect_ids. If receipt issuance or receiver deduplication continuity cannot be proven, outcome UNKNOWN and no automatic replay. Falsifiers for a prospective frozen test: replay with changed transport attempt performs twice; independent receipts for identical operations are wrongly collapsed; forged/reused receipt is accepted; receiver restoration without state continuity silently executes. **No experiment run and no change to Genesis.** Claude: assess whether E68's witness can represent authorization-receipt identity without conflating receiver execution with approval.

Source-observed: Genesis seeds A-000 with name/status, and its `ReshIdentity.validate()` uses markers and instance state rather than cryptographic/authorization evidence; the Governor's permissive Validate/Govern placeholders cannot establish the proposed receipt contract. N151 is a proposal, not a demonstrated invariant.

## C. Sole Business project F-001 — TAM Protocol ebook
Read existing plan/decision sheet and Run580 checkpoint. Prepared `F001-PINNED-RUNNER-581.py`, a stdlib offline execution wrapper for existing Issue #258's **already preregistered** six-case synthetic harness. It obtains gate/harness bytes from exact Git blob IDs, recomputes Git blob IDs before execution, runs isolated Python, and writes raw JSON evidence with stdout, stderr, exit code, SHA-256, interpreter and UTC timestamp. No manuscript content is embedded. Runner commit `2a6e94d77211bb0eeeecf653e25c2155b79d9308`. **UNTESTED runner; no harness execution or CI.** Attempted raw GitHub source transfer from execution container; DNS failed (`Could not resolve host: raw.githubusercontent.com`), so do not claim execution. Offline clone with objects present is the handoff route; do not trigger tests without checking Issue #258 remains the pre-test record.

Checklist: [x] F-001 single identity; [x] v579 gate and v580 prereg harness; [x] pinned offline evidence runner; [ ] run six cases and post observations in #258; [ ] v577 nine cases #256; [ ] VER-15 #229; [ ] REG-9/H2/REPLAY-6; [ ] Claude editorial/rights/segmentation; [ ] independent provenance and PDF/EPUB/Android checks; [ ] Timothy A1–A6 and explicit release authorization. Acceptance requires verified reproducible tests, editorial/rights clearance, artifacts and explicit Timothy approval. **HOLD / NOT LAUNCH-READY**.

## D. Coordination and boundaries
Claude complementary work: assess N151's authorization boundary and review F-001 editorial status semantics, source provenance and quotation rights. Timothy decisions pending A1–A6, identity issuer/witness, and first Library completion. No test executed, no CI triggered, no main/Genesis/Claude/shared/Testament write, no spending, outreach, accounts, publication, paid inference or Cloudflare loops.
