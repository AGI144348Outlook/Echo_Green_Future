# F-001 TAM Protocol ebook — release preflight refinement
Project ID: F-001, unchanged. Status: HOLD / NOT LAUNCH-READY.
Source: Business decision sheet blob 2975edcc4cae8a17499e873b68ba75f5c39ea527; GPT checklist 69449fceac9d4b7b5ac516318c685ec610fdd6df; Run533 packaging acceptance blob 195435b130ad29579c3de0264ea90e6e74e1ff1c.
## Deliverables and acceptance gates
- [ ] Exact pinned nine-case source regression with 6+3 named cases, both summaries, zero failures, clean source provenance, retained raw log and same-thread actual results in Issue #197.
- [ ] H2 Issue #174 and six-file replay Issue #161 with pre-test entry before execution and actual follow-up in same threads.
- [ ] Claude editorial dispositions for 82 items; historical fact review; rights dispositions for 69 units/77 passages.
- [ ] Timothy A1–A6 answered (material, storefront, credit, framing, price/refunds, source/license) and separate publication authorization.
- [ ] PDF selectable text, headings, links, readable Android typography; EPUBCheck, navigation, reflow and metadata; cross-format chapter/reference/notice parity.
- [ ] Manifest containing exact source revision, dependency versions, build inputs, stable book ID, reproducibility policy, and artifact SHA-256 values.
- [ ] Actual Android acceptance with observed accessibility limitations.
## New practical packaging refinement
Prepare a *release candidate directory* that cannot be mistaken for published product: `F-001-RC/README-HOLD.md`, `manifest-draft.json`, `QA-checklist.md`, `artifacts/`. Until A3 and A6 are answered, author/license metadata must be `UNRESOLVED`, not guessed. The release gate must reject placeholders, absent rights dispositions, missing EPUB/PDF, and missing actual regression evidence; checksum presence alone is not validation. This is a specification, not an executed gate.
Next GPT action: obtain pinned checkout, post/update pre-test record in Issue #197 before execution, run exact nine-case suite and report evidence in same issue. Claude continues editorial/rights; Timothy decisions outstanding. No tests executed or publishing authorized.
