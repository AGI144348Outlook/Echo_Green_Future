# F-001 TAM Protocol ebook — Run498

**Sole project: F-001; HOLD / NOT LAUNCH-READY.** Reviewed Run497 checkpoint, H2 source, shared Business/README.md and Workshop/README.md. No second income pipeline.

New source-grounded static audit of `contract-000/gpt/business/f001_h2_reference_lint_496.js` (Git blob `e68d2296da15714de56b355da62d37035c4cfe96`): `reviewer_id` is only required to be a nonblank string; `source_locator` and `claimed_scope` are only truthiness-checked; `document_sha256` is format-checked but never matched to fetched document bytes; reviewer authority, rights holder identity, license scope and revocation are not authenticated. Thus a syntactically plausible forged rights claim can yield `FORMAT_ONLY` but never legal clearance; the output correctly says `NOT_DETERMINED` and `HOLD`. This is **source inspection, not an executed test**.

Deliverables checklist: [x] H1 parser defect observed; [x] H2 draft and synthetic local-reproduction 8/8 (not byte-pinned); [x] H2 static authority-gap inventory; [ ] byte-pinned H2 executable verification with prospective Issue #174 entry; [ ] six-file replay Issue #161; [ ] 82 authenticated editorial decisions; [ ] 69 quotation-rights units covering 77 passages with provenance and permissions; [ ] historical verification; [ ] final EPUB/PDF acceptance; [ ] physical Android accessibility; [ ] Timothy explicit release authority.

Acceptance: reproducible source-pinned build and adversarial verification, human editorial and rights approval, accessible final package and explicit release decision. Next GPT: pre-register and run exact-source H2 verification, then #161. Claude: complementary quotation provenance and rights review. No publication, outreach, accounts, payments or paid inference.
