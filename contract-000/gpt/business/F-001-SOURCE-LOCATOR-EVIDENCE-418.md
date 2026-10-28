# F-001 — exact-source editorial locator evidence, Run418

**Sole business project:** F-001 TAM Protocol ebook. **Status:** HOLD / NOT LAUNCH-READY. **Prospective pre-test:** [Issue #91](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/91), posted before Run418 diagnostics. **New source:** [`f001_source_locator_418.js`](f001_source_locator_418.js), final Git blob `096cd7ec8a286496b485eed66f7cb5dd6fd109c0`. **Input packet:** `F-001-REVIEW-HANDOFF-417.json` blob `cc0b19ab4c2afeb45e4aeed0215667e933ad4080`. **Original public TAM source commit:** `AGI144348Outlook/The-TAM-protocol@d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`.

## Method and actual observations

- Retrieved eight public source files through the GitHub connector and compared each returned Git blob SHA against every matching packet row. All eight source blobs matched. Used the same sentence-boundary regex as the public original `claim_scan.py`, translated into JavaScript for **location matching only**. This does **not** constitute original Python scanner execution or parity.
- Resolved **82/82** source locations with exact `file#S<n>` indices and excerpt inclusion: **45 baseline** (18 P1) and **37 supplemental** (34 groups). No source excerpt mismatch. Of baseline snippets, **25** equal their entire located sentence and **20** are shorter excerpts. All **37** supplemental snippets equal their located sentences. The baseline `excerpt_is_full_sentence=false` is deliberately conservative for all 45; it does not assert that 25 are partial.
- The locator checks the fixed project and source commit, HOLD state, zero human reviews, all 82 unreviewed rows, null editorial/evidence/rights/reviewer fields, release=false, row ID, file pin, sentence index, excerpt inclusion, 45+37 coverage, P1 count and the exact G001–G034 group set. It returns only IDs, source SHA and length/completeness metadata, not reproduced article text.
- **Final in-memory V8 controls on the exact committed JS blob:** **18/18 passed** (nine positive/coverage checks and nine negatives). Negatives: tampered excerpt, source SHA, sentence index, unauthorized review status, duplicate ID, missing source, substituted group ID, false full-sentence flag and changed source commit. No original-source Python scanner, Node filesystem CLI, Android or final EPUB/PDF was executed.

## Deviations, failures and corrections (not concealed)

1. First uncommitted dynamic-code test harness raised a `SyntaxError` because the Node shebang was fed directly to `new Function`; no product test ran and no file was committed.
2. Second uncommitted harness raised `ReferenceError: structuredClone is not defined` in the restricted V8 environment; again no valid product test result. Corrected by using JSON parse/stringify cloning in the test harness.
3. The first committed locator version passed **17/18** checks: replacing `G001` with `G999` retained 34 distinct groups and incorrectly passed the group-count-only guard. Corrected in a second commit to require exact G001–G034 membership. Re-fetched the updated committed source and reran **18/18**, all passed. The initial failed negative is retained as evidence of the fix.

## What this does not establish

- A valid source locator does not independently substantiate any archaeological or historical claim. No row has a human evidence verdict, rights clearance or editorial disposition; all **45+37 remain UNREVIEWED**.
- This is a JS translation of sentence splitting, not a run of the original `claim_scan.py` against all eight real source files. Run412's **42 scanner-trigger candidates** are a distinct subset concept from this **82-item editorial review queue** and cannot be equated.
- GitHub connector source-body fetches and V8 in-memory checks are not an actual Node filesystem CLI test, source ZIP materialization, Android test, full coordinator chain, final PDF/EPUB, publication or sale.
- Rights, A1–A6/B1/B4/B6/C1 decisions, review of 18 P1 cards, remaining 27 baseline cards and 37 supplemental occurrences, and explicit Timothy publication authorization are still missing.

**Next action / ownership:** GPT to run the exact committed locator as a real Node CLI on a pinned local source archive when materialized, then the original Python scanner and full coordinator; Claude to review source/evidence/rights for the 18 P1 and 34 supplemental groups using the resolved locations, without writing GPT-owned files. Timothy retains all editorial/rights and release decisions. **F-001 HOLD / NOT LAUNCH-READY.**
