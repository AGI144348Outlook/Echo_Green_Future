# F-001 — actual TAM source-text claim binding — Run 382

**Project:** F-001 TAM Protocol ebook, continuing Run381; **HOLD / NOT LAUNCH-READY**. **Pre-test:** [Issue #56 PRE 6429358349](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6429358349). **Input inventory:** [Run378 45 candidates](F-001-REAL-CLAIMS-378.json) at pinned source commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`. Shared original Python scanner blob `31f3dcff` remains unchanged.

## New executed evidence

Fetched the **eight actual public TAM files** from the pinned Git commit via authenticated GitHub connector; checked **8/8 Git blob SHAs and UTF-8 byte sizes** against the previously pinned source manifest. Independently segmented the actual text using the documented `(?<=[.!?])\\s+|\\n{2,}` JavaScript translation of the Python scanner. Per-file sentence totals matched **24, 22, 41, 37, 26, 29, 9, 299**. All **45/45 candidate excerpts** (42 baseline and three supplemental) match the beginning of the claimed numbered sentence in their actual source file; zero excerpt/index mismatches. All 45 remain UNREVIEWED.

Developed [read-only Node/JS binder](f001_real_source_binding_382.js) and [reproducible runner](test_f001_real_source_binding_382.js). The Node CLI computes Git blob SHA-1 from the **actual local bytes** (`blob <len>\\0<bytes>`) and rejects missing files, symlinks, SHA/size drift, missing/duplicate/renumbered claims, altered excerpts, changed editorial status, and inconsistent counts. It performs no writes or network requests.

**V8 execution:** 10/10 expected outcomes matched: one positive run using all eight GitHub-fetched real source texts and nine in-memory negative controls (tampered excerpt, out-of-range index, incorrect ID, duplicate claim, forged approval, altered source metadata, altered source text length, missing file, altered blob SHA). These were V8 function calls using connector-verified SHA metadata; **the Node CLI/test runner was committed but NOT executed in a local Node process**. For independent reproduction, checkout the pinned TAM commit and run `node test_f001_real_source_binding_382.js <tam-dir> <F-001-REAL-CLAIMS-378.json>`.

## Interpretation, limitations and next actions

This advances the earlier metadata-only inventory gate: each excerpt now has a **source-text location witness** in the eight real files. It does **not** prove a claim is true, that the inventory contains every claim needing review, or that the original Python scanner produces the identical 42 rows; JS/Python Unicode sentence semantics remain a parity question. The V8 audit trusts GitHub-provided source SHA metadata; the unexecuted Node CLI independently hashes bytes. No editorial statuses were changed.

**Next GPT:** execute the committed Node CLI and exact Python scanner on an independently pinned eight-file checkout; compare all baseline keys; continue dataset stage and final PDF/EPUB packaging only after editorial decisions. **Next Claude:** independent Article 4, claim dispositions, Gerah/precision, rights and listing review. **Timothy:** A1–A6, B1/B4/B6, C1, editorial authority and explicit release permission remain open. No publication, spending, outreach, account creation, paid inference, CI or Cloudflare loops.
