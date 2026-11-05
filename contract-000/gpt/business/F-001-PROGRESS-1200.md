# F-001 TAM ebook — GPT run1200 packaging acceptance increment
**Project ID:** F-001. **Status:** HOLD / NOT LAUNCH READY. This continues the same TAM Protocol ebook; no new product selection, outreach, publication, payments or account creation.

## Sources reviewed
- library-shared Business/ideas/F-001-decision-sheet.md blob 2975edcc4cae8a17499e873b68ba75f5c39ea527 — A1–A5 and B1–B6 undecided.
- library-shared Business/ideas/F-001-gpt-checklist.md blob 69449fceac9d4b7b5ac516318c685ec610fdd6df — GPT packaging/integrity, Claude editorial/listing.
- library-shared Business/ideas/F-001-tam-build/APPLY-ORDER.md blob 43e9d5b40fcc78507dbcde9e70f00b6454a6342e — proposed patch dependency chain not applied.
- GPT run1100 F-001-PROGRESS-1100.md blob a0199d488785be01c379ec38c71620a314238aa5 — G1–G6 release gates and H3c fail-closed design.

## New deliverable: H3c evidence manifest contract (draft, not executed)
Proposed JSON manifest fields: schema_version; project_id=F-001; source_repository; source_ref; source_blob_sha; build_tool_versions; source_files[{relative_path,sha256,size}]; output_files[{format,relative_path,sha256,size,accessibility_evidence_ref}]; editorial_disposition_ref; rights_decision_ref; user_release_approval_ref; verification_timestamp_utc; verifier_version; outcome in {HOLD,REJECT,ACCEPT}. Unknown/missing evidence is HOLD, never inferred ACCEPT. No private manuscript contents or customer information in the public repository.

**Fail-closed verification order:** (1) trusted immutable source-root binding; (2) open and hash exact bytes, not separate pathname preflight; (3) reject traversal, parent symlinks and nonregular files; (4) bounded input/output size; (5) compare against pinned hashes; (6) verify PDF/EPUB structure and metadata; (7) attach independent accessibility evidence; (8) require explicit editorial/rights decisions and Timothy's affirmative release approval; (9) preserve primary failure and append any close failure to audit. For TOCTOU safety, an open-descriptor or trusted directory-handle model is needed; string normalization alone does not prove containment. All output artifacts remain withheld from release while any gate is unresolved.

## Checklist / acceptance
- [ ] G1 pinned source and independent byte custody
- [ ] G2 Claude editorial dispositions (82 items, as reported in prior checkpoint)
- [ ] G3 quotation-rights dispositions (69 decisions/77 passages as reported)
- [ ] G4 reproducible source-pinned PDF/EPUB build
- [ ] G5 integrity, EPUB/PDF accessibility, Android manual navigation
- [ ] G6 Timothy's A1–A5/B1–B6 decisions and separate publication authorization

**Next GPT action:** implement an H3c verifier in a GPT-owned branch, preregister adversarial source-custody and close-error tests before execution, and compare output to actual pinned source bytes. **Claude's complementary action:** continue editorial/rights and listing reconciliation, without overwriting GPT packaging. **Timothy pending:** decisions and release approval. No tests of H3c were performed in this run.