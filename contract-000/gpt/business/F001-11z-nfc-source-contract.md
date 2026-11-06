# F-001 — TAM Protocol ebook, 11Z continuation (single project)

**Project identifier:** F-001 (unchanged). **State:** HOLD / NOT LAUNCH-READY. Read shared `Business/ideas/F-001-candidate-ebook-gumroad.md` through Claude §210 (blob aecdce5), prior GPT 10Z attestation-envelope design (commit 94450ec6), and Claude #13 10Z handoff. This is a DRAFT, not an implemented/tested rights validator or legal determination.

## Deliverables checklist
- [x] Existing manuscript source identified: The-TAM-protocol; actual edition inventory/pins still need human verification.
- [x] Rights worksheet and B0–B4 source-range acceptance rules proposed.
- [x] Ten synthetic rights fixtures described; execution not claimed.
- [x] Distinct Timothy-controlled authorization envelope proposed (not an authenticated channel).
- [x] **11Z design increment:** specify fail-closed Unicode canonicalization and source span digest requirements below.
- [ ] Verify 69 rights units and 82 editorial decisions with source evidence and human review.
- [ ] Build and preregister a strict validator against synthetic pinned source; compare exact committed bytes.
- [ ] Produce and independently check accessible PDF/EPUB and truthful product listing.
- [ ] Timothy chooses personal attestation channel and gives product-specific release approval.

## 11Z NFC / source-span contract (PROPOSED, untested)
1. Require UTF-8 decode with strict errors, LF line endings, and NFC-normalized Unicode in the **pinned source bytes**. Do not silently normalize or mutate source; reject any noncanonical input with `noncanonical_source_encoding` and record the original SHA-256.
2. A worksheet `source_ref` binds repository, commit, path, source blob SHA, SHA-256 of original UTF-8 bytes, and selected product edition. A source path alone is insufficient.
3. Range grammar `L1:C1-L2:C2` uses 1-based inclusive **Unicode code-point** columns, line boundaries based on LF, no cross-line implicit whitespace; reject malformed, reversed, zero, or out-of-bounds ranges before computing length bands.
4. Compute `span_sha256` over the exact UTF-8 encoding of the selected inclusive code-point substring **including LF separators**; record `span_codepoints`, `span_bytes`, and B0–B4 band separately. A digest mismatch yields HOLD.
5. The source/worksheet validator outputs only `ELIGIBLE_FOR_EDITORIAL_REVIEW` or `HOLD`; it can never emit `AUTHORIZED_TO_PUBLISH`. Syntactically valid `ALLOW` text is not independent proof of rights.
6. The human authorization envelope binds a *canonical worksheet digest*, edition, scope, issued_at and expiry. A trusted Timothy-controlled verification channel is required; shared GitHub account authorship is insufficient.

## Acceptance and next action
**Acceptance:** exact source pins resolve, NFC and range rules pass, rights evidence is independently verified, all editorial decisions are recorded, accessible packages match listing, and Timothy personally authorizes release via a separately authenticated channel. Until then HOLD.

**Next GPT action:** preregister validator fixtures in a dedicated F-001 Issue before any diagnostic/test, implement a pure-stdlib validator on this GPT-only branch, run synthetic canonical-vs-decomposed Unicode and multiline span tests; report negative cases and commit exact output. **Claude complementary:** §210 worksheet/editorial and source custody; **Timothy:** rights decision and attestation channel. No storefront/account creation, outreach, publication, spending or payment.
