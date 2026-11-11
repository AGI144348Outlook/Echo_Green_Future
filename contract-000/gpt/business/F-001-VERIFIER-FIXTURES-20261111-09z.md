# F-001-TAM — GPT release-verifier negative fixture plan (09Z)
**Single project ID:** F-001-TAM-PROTOCOL-EBOOK. Read shared `Business/ideas/F-001-decision-sheet.md` blob 35ece85d203b8f1a5bac5a2bf3b5d6b8780ac2eb and `F-001-gpt-checklist.md` blob 69449fceac9d4b7b5ac516318c685ec610fdd6df. Claude owns editorial/listing; GPT owns read-only packaging, checksums and fail-closed verifier specification. No publication or payment authorization.

## Deliverables checklist
- [ ] 82 editorial dispositions with source-bound evidence and authenticated approval
- [ ] 70 rights decisions and source-branch/license A6 resolution
- [ ] A1–A6 / B1–B6 explicit Timothy decisions (draft defaults do not count)
- [ ] Independent issuer authority and replay-resistant receipt schema
- [ ] Accessible EPUB/PDF generated from approved source with pinned build inputs
- [ ] Exact-byte hashes and receipt binding, strict parser, path containment
- [ ] Android EPUB/PDF QA and final listing/claims verification
- [ ] Timothy's express publication approval

## Proposed 10-fixture release-verifier matrix — NOT EXECUTED
1. Valid synthetic receipt and pinned artifacts -> PASS (only if independent authority fixture is trusted).
2. Artifact SHA-256 mismatch -> FAIL.
3. Duplicate JSON key, including duplicate issuer -> FAIL.
4. Parent-path traversal (`../`) -> FAIL.
5. Absolute path outside approved artifact root -> FAIL.
6. Outward-pointing symlink under approved root -> FAIL.
7. Wrong issuer or unauthenticated self-assertion -> FAIL.
8. Nonce reuse with persistent ledger -> FAIL.
9. Missing one of 82 editorial approvals or 70 rights decisions -> FAIL.
10. Inaccessible/malformed EPUB or PDF with apparently valid receipt -> FAIL.

The fixture harness must be preregistered on GitHub before first execution; avoid testing canonical or shared source. Strict path containment must use resolved paths, not string prefix checks. JSON duplicate-key refusal must happen before interpreting signatures. Signed receipt validates *who* approved and exact bytes, not correctness of the underlying rights decision. A synthetic test pass cannot authorize real release.

**Next GPT action:** implement a standalone no-network strict verifier and ten synthetic fixtures on GPT branch, preregister before running; coordinate with Claude for immutable editorial/rights evidence fields and exact artifact schema. **Claude complement:** continue editorial provenance, licensing, rights and issuer-custody research; do not edit GPT files. **Acceptance:** all fixtures pass against committed code; real rights/editorial evidence and issuer authority independently verified; accessibility QA; Timothy explicitly approves release. **Current state: HOLD / NOT LAUNCH-READY.** No sales, listing, outreach, paid inference, or spending.
