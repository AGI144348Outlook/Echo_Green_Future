# F-001 Run470 — prospective Issue #151 test and actual results (2026-10-30 ~10 CT)

**PRE published first:** [Issue #151](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/151) before any Run470 executable checks. No retrospective pre-registration. **Project F-001 only, HOLD / NOT LAUNCH-READY.**

## Inputs and source pins

- Source register `F-001-EDITORIAL-DECISIONS-458.tsv` Git blob `300dfcf0ba9e9d236326d09b2a4b6c5467d3874c`.
- Source-location map `F-001-SOURCE-LOCATION-RESULTS-462.tsv` Git blob `7fb5cd952127de7a0469cfb3d0139d7bdfb60b86`.
- Pending intake `F-001-DECISION-INTAKE-PENDING-463.tsv` Git blob `4cc1617d1f1bbea1661f74ba931f86660c087939`.
- Parent generator `f001_review_companion_468.js@a43e95b`, old HTML `@983ca1f`, previous fake-DOM harness `test_f001_review_dom_469.js@a758ad5`.
- New GPT-only generator `f001_review_companion_470.js@f3c34568409730e0c93eb72ff53b72b46f2d2db7`.
- New HTML `F-001-82-EDITORIAL-REVIEW-DRAFT-470.html@7bf0a1c1455473d91b1e5e7c4d63399d78dc23cb`.
- New harness `test_f001_review_dom_470.js@2717218a64bec090370c8c2860c9e20840d726ee`.

## Observed tests (executed by ChatGPT in the isolated V8 tool environment using GitHub connector-returned exact UTF-8 source text)

1. **Generator source edit:** six replacement sites checked (first occurrence appears twice for CLI filename; other five exactly once); a first attempt **failed before any writes** because the filename appeared twice, not once. Corrected the edit count expectation; no old file overwritten.
2. **New generator execution:** `buildReview(register, location, intake, observedPins)` generated **82 cards** from the three pinned files; emitted inline JS parsed with `new Function`; status HOLD; tampered source-register blob refused. All eight precommit assertions true (source pins, 82 cards, valid script, linked label code, heading association, HOLD, original source identity, tampered pin refusal).
3. **Deterministic generation:** re-running the committed new generator on the exact same three GitHub-returned TSVs produced HTML **byte-identical** to the new committed HTML.
4. **New fake-DOM V8 regression:** **24/24 checks passed** on the exact new HTML Git blob, including 82 rendered cards, 10 duplicate-text references, 246 unique deterministic heading/control DOM IDs, 82 `aria-labelledby` region-to-heading associations, 164 explicit `label.htmlFor` targets, search, draft export/restore, Unicode note, no approval/release flags, five forged import refusals without partial restore, and no outbound request in the simulated environment.
5. **Adversarial negatives:** modified label target refused at the association check; malformed inline script refused at parse; wrong Git blob refused at the source-pin check. For the first two diagnostics the exact-blob check was intentionally bypassed by supplying the expected pin to the test function, so the deeper assertion could be reached. **All three negative controls rejected.**
6. **Library metadata diagnostic:** nontruncated shared tree `62c741d` had 126 blobs; previous ledger 125; 124 unchanged, 1 changed manuscript, 1 new Claude §168 replay; **68 KEEP / 57 DEFER / 1 PRUNE**, 0 missing or invalid reason. Only two changed bodies fresh-read. No deletions.

## Interpretation and limitations

This shows deterministic, source-pinned *simulated-DOM behavior* and explicit programmatic label association code. It **does not** establish actual browser label-click behavior, accessible-name computation, screen-reader speech, touch behavior, Android file-picker/download behavior, or WCAG conformance. The fake DOM does not implement browser accessibility semantics. The Node CLI no-clobber check was proposed but **not executed**: this environment could not download GitHub raw files to the local Node runtime (DNS resolution failed). Claude's earlier real Chromium evidence covers **v468 only**, not this v470 page. No paid inference, CI, browser network or publication.

## Next

Claude independently run v470 Node CLI on the three pinned TSVs and Chromium keyboard/label-click/accessibility smoke after its own prospective PRE; real Android remains separate. GPT to refine if browser findings require it. Await Timothy's authenticated 82 editorial decisions and A1–A6/B1/B4/B6/C1, historical verification, rights and final EPUB/PDF approval. **0 approved; HOLD.**
