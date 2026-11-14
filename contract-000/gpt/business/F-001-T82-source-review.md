# F-001 — T82 exact-source packaging review (GPT-owned, 2026-11-14 10Z)

**Project:** F-001 TAM Protocol ebook. **Status:** HOLD / NOT LAUNCH-READY. No publication, account creation, outreach, payment, or spending.

## Source reviewed
- Existing GPT candidate `contract-000/gpt/business/f001_epub_zip_preflight_t77_candidate.py`, Git blob `6cc986cedb090c0b0146fb15d7af0e8ca3ad91ae`, read from GPT branch.
- Prior GPT handoff `contract-000/gpt/business/F-001-T81-packaging-handoff.md`, blob `f8535d381060300f7aca50595a3c76407f9a41e7`.
- Prior preregistration Issue #466; no new execution.

## New static-review findings (NOT execution-confirmed)
1. The candidate correctly expresses single-backslash refusal with `"\\" in name` (source-inspected only).
2. `ZipFile.read(first)` occurs before checking the first member's encryption bit, but only after checking declared mimetype size and stored compression. Refusal ordering should be explicitly tested, not presumed.
3. Archive member `external_attr` is not inspected for Unix symbolic-link metadata. Current function only inspects the ZIP, not extraction; do not call this an exploitable extraction vulnerability without an extraction path.
4. Duplicate detection uses raw names. Normalization and Unicode collision policy remain undecided; never silently normalize EPUB paths without specifying URI semantics.
5. Declared ZIP sizes and ratios are metadata; preflight does not certify decompression safety, PDF validity, rights, accessibility or EPUB conformance.
6. The function rejects zero-length internal path segments and traversal; an EPUB-valid parent-relative OPF reference is a separate question for the OPF validator, not a reason to accept `../` ZIP member paths.

## Deliverables / acceptance
- [x] Single-project ownership and Claude/GPT division preserved
- [x] GPT candidate source inspected and exact Git blob identified
- [x] Prospective Issue #466 exists for bounded fixture execution
- [ ] Independent byte-certified execution of the committed source; 10 adversarial fixture types and post-test evidence in #466
- [ ] Add synthetic symlink-metadata, first-member encrypted, Unicode path and malformed ZIP cases under prospective amendment
- [ ] Integrate EPUB ZIP + container/OPF/spine validation without overwriting original validator
- [ ] Independently validate PDF, accessibility, Android readers, rights and source provenance
- [ ] Resolve Claude's A1–A6 decision gates; explicit Timothy release authorization

**Next action:** transfer exact blob to a controlled runtime with SHA verification, amend Issue #466 *before* any materially new fixtures, execute bounded synthetic cases, report actual observations in that issue. **Acceptance:** safe fixtures accepted, unsafe fixtures refused as specified, no hidden mutation or publication; synthetic success is not security certification.
