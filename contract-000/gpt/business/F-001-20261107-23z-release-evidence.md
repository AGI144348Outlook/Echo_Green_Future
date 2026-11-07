# F-001 TAM Protocol ebook — release-evidence package contract, 23Z
**Project identifier:** F-001. **Only income project:** TAM Protocol ebook. Existing plan F-001.md: GPT packaging/testing; Claude editorial/storefront draft. This is preparation only, no publication or outreach. The source of record is The-TAM-protocol repository per TJ R1, not a fabricated master file.

## Deliverables checklist
- [ ] U01–U03 original source quotation spans verified against immutable source blob SHA and UTF-8 byte offsets.
- [ ] U70 quotation provenance and rights decision documented.
- [ ] All 82 editorial decisions recorded with reviewer and source version.
- [ ] Manuscript units frozen to SHA-256 hashes; every changed source/quote invalidates dependent approvals.
- [ ] Accessible EPUB and tagged/readable PDF built and independently validated.
- [ ] Android reading QA: Hebrew RTL, Unicode grapheme integrity, navigation, links, zoom and reflow.
- [ ] Listing/sample content consistent with final package, with truthful claims.
- [ ] Timothy explicitly authorizes publication and any accounts/spending.

## New executable-spec draft: fail-closed evidence graph
For each unit, require `unit_id, source_repo, source_ref, source_path, source_blob_sha, source_sha256, start_byte, end_byte, quote_sha256, rights_status, rights_evidence_ref, editorial_status, editorial_reviewer, package_sha256`. `source_blob_sha` (Git object ID) and `source_sha256` (raw bytes) must not be conflated. Rights/editorial decisions bind to `source_sha256 + start_byte + end_byte + quote_sha256`, not just unit ID. Any missing field, mismatched source bytes, unresolved/revoked rights, editorial hold, or package hash drift => HOLD; a missing explicit release grant => HOLD even if all technical gates pass. This is a specification only, **not tested** and not a claim that any clearance exists.

## Complementary coordination
GPT: build source-span verifier, package validation scripts, Android QA rubric. Claude: obtain/curate editorial unit decisions and storefront draft, without publishing. Neither side may substitute a proposal for Timothy's rights/release authorization.

**Next action:** retrieve actual U01–U03 source references and implement a read-only span verifier against exact source blobs; preregister any repository test before running. **Acceptance:** all evidence checks pass, both formats verified, explicit Timothy release authorization. **Status:** HOLD / NOT LAUNCH-READY. **Blockers:** source spans, U70, rights, 82 editorial decisions, packages, Android QA, release authority. No private customer/payment data in public GitHub.
