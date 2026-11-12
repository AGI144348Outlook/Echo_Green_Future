# F-001 — same TAM Protocol ebook: PDF listing-parity gate (GPT draft, 2026-11-12 22Z)

**Project ID:** F-001, sole active income product. **Status:** HOLD / NOT LAUNCH-READY. This is preparation, not publication authorization. Claude owns editorial/rights and source manuscript decisions; GPT owns packaging/validation draft. No second product pipeline.

## Source-grounded issue and improvement
Current `library-shared@403fd2d` `Business/ideas/F-001-tam-build/build_pdf.py` blob `c029cd67...` counts pages by matching `/Type\\s*/Page[^s]` in raw PDF bytes. This may miss compressed page dictionaries or count incidental tokens. A reported count alone is not a trustworthy listing parity receipt. The corrected `listing_check.py` blob `adc3123c...` now unconditionally requires nonempty `claims.csv`; preserve this improvement.

## Proposed packaging verifier (not implemented/tested)
- Input: delivered PDF byte path and SHA-256; pinned manifest (source revision, toolchain, chosen build engine, output hash); exact listing text; source rights and editorial receipts.
- Count PDF pages using an independent structural parser (e.g. `pdfinfo`/Poppler) **and** a second independent parser where available; disagreements or unavailable structural verification => `BLOCKED_PAGE_PARITY`, not a guessed number.
- Recompute delivered SHA-256 and require exact manifest match. Verify actual listing page claim if present; if absent, do not fabricate a page number. Require full artifact/license/rights/editorial/Timothy authorization gate regardless of listing phrasing.
- EPUB: pin the actual delivered hash; structural checks and accessibility review separately; warn-only missing metadata is not an accessibility pass.
- Never accept `timothy_authorized: true` as external authorization. Without authenticated trust root, primary verdict `BLOCKED_AUTHORITY`; preserve diagnostics for each evidence gap.

## Acceptance checklist
- [ ] Timothy decides A1–A6 in existing decision sheet (material, store, credit, framing, price/refund, license)
- [ ] Claude finishes rights and editorial receipts; no unresolved claim rows
- [ ] Delivered PDF/EPUB bytes and immutable source pins recorded
- [ ] Independent structural page count and listing parity, accessible EPUB/PDF QA
- [ ] Authentic approval bound to exact artifacts and verified trust root
- [ ] Timothy authorizes publication; only then external release

**Next GPT action:** preregister synthetic structural page-count failure vectors and implement an inert verifier on GPT branch, without invoking production build or publishing. **Next Claude action:** continue editorial/rights evidence and review this proposed page-count gate. No tests in this artifact.
