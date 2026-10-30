# F-001 TAM ebook — Run471 static accessibility audit and continuation

**Project F-001 only; HOLD / NOT LAUNCH-READY.** Read prior progress, shared F-001 decision sheet, Workshop and Claude §168. 82 editorial occurrences remain PENDING / 0 authenticated approvals.

## Prospective record and observations

[Issue #152 PRE and POST](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/152) was posted before diagnostics. Inspected v470 HTML Git blob `7bf0a1c1455473d91b1e5e7c4d63399d78dc23cb`. Initial static HTML scan found 0 article elements and 6 IDs: PRE expected 82 articles, but this is a client-rendered page, not a static document. Follow-up parsed embedded CARDS: **82 rows, 82 unique occurrence IDs**. Source shows a per-card loop constructing article, heading, disposition select, note textarea, two associated labels and `aria-labelledby`. No APPROVED option in the draft disposition choices. **Static code inspection only**: not a Chromium, Android, DOM runtime, keyboard, screen-reader, or authenticated-approval pass. The static pre-test expectation was corrected openly in the POST, not rewritten retrospectively.

## Deliverables / next action / acceptance

- [x] Pinned 82-entry editorial register, provenance, custody and draft-only offline review companion.
- [x] v470 source-level markup audit, with documented test-design correction.
- [ ] Claude's independent v470 real Node/Chromium DOM and accessibility-tree replay (publish PRE before testing, POST afterward); real Android remains unverified.
- [ ] Timothy's 82 authenticated editorial decisions; historical claims, rights, EPUB/PDF, listing, and explicit release authorization.
- [ ] Timothy A1–A6/B1/B4/B6/C1, credit, price/refund, payout, publication decisions.

**Acceptance:** no launch until every editorial/rights/claim/package/listing gate and Timothy's publication authorization are recorded. Complementary task to Claude: verify v470 real DOM and keyboard labels; GPT will refine any resulting defects. No accounts, publication, outreach, payments, spending, CI, paid inference or Cloudflare loops.
