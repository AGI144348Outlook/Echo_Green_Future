# F-001 TAM Protocol ebook — rights-gate v2 acceptance fixture specification (08Z, DRAFT)
Single project ID: F-001. Status: HOLD. This is a draft test matrix, **not** a run, a release decision, a rights grant, or a new project.
Sources: shared `Business/ideas/F-001-candidate-ebook-gumroad.md` §§205–207 (blob 0e21e81e), GPT `contract-000/gpt/business/F001-rights-gate-v2-interface-07z.md`, mirror `F-001.md` (blob 73791145).
Inputs to deterministic validator: (1) pinned commit and ordered `(path,source_blob_sha)` inventory, (2) canonical NFC UTF-8 LF worksheet TSV with sorted passage_id and terminal LF, (3) explicit `as_of` UTC, (4) separate human-only attestation binding `worksheet_sha256`, (5) proposed release scopes. `source_blob_sha` is a Git blob ID, not the worksheet SHA-256. A reviewer field or shared GitHub authorship alone MUST NOT authenticate Timothy.
## Proposed fixture cases (all remain UNEXECUTED)
1. No attestation => HOLD: missing_authority.
2. Assistant-authored attestation => HOLD: invalid_authority.
3. Attestation digest differs from worksheet bytes => HOLD: mismatched_worksheet_sha256.
4. Noncanonical NFC/whitespace passage ID => HOLD: noncanonical_passage_id.
5. Duplicate passage ID => HOLD: duplicate_passage_id.
6. Source blob absent from pinned tree => HOLD: unknown_source_blob.
7. Reviewed timestamp > explicit as_of => HOLD: future_review.
8. Source scope absent or disputed => HOLD: scope_or_rights_disputed.
9. Third-party rights permission without evidence => HOLD: missing_rights_evidence.
10. Fully canonical synthetic worksheet with separately verifiable approval => eligibility for *editorial review only*, NOT automatic publication.
For all cases: stable sorted rejection codes, reproducible report, no wall clock, no private passage text in public fixtures.
## Checklist / next action
[ ] Claude's 69 rights units populated with pinned references (not private text).
[ ] Human-only rights decisions and independently verifiable approval channel selected by Timothy.
[ ] 82 editorial decisions reconciled with actual manuscript.
[ ] Rights validator implementation and prospective Issue preregistration before tests.
[ ] Accessible PDF/EPUB and listing-parity checks.
[ ] Explicit publication permission and human launch review.
**Acceptance:** no AI can self-authorize rights; identical inputs yield identical output; fail closed on all unknowns; publication remains gated even after passing a validator.
**Coordination:** Claude retains worksheet/editorial; GPT owns validator/fixtures; Timothy owns rights and release approval. No account creation, outreach, payment, or publication.
