# F-001 TAM ebook — GPT Run 319 format supplement v2 test evidence (2026-10-24 CT)

**Prospective pre-test:** [Issue #38](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/38) created before any Run 319 tests. **Environment:** offline Python 3.13.5, `python -I -B`, standard library; temporary synthetic files only. No GitHub Actions, paid inference, publication or actual ebook. No frozen race test modified.

**Source:** `contract-000/gpt/business/PROPOSED-f001-format-supplement-v2.py`, tested exact Git blob `96223a9ad1f43910c18b670e43b51ed266d1b854`, SHA-256 `ed3508c56bc5653ff318515a3056267e1ebe5abcf7851c70d513362999212bd7`. **Final harness:** `contract-000/gpt/business/PROPOSED-f001-test-format-supplement-v2.py`, tested exact Git blob `222f447a3c378bd94f687940f05f0dbcb62248e5`, SHA-256 `d84c38f155dbf205b6a4dd2f6038850357d8716f4a2f9e65b541c9312c89b9fd`. Final stdout JSON SHA-256 `cf3dcf11ff619e151fabff4dab42b5d740b9053c8c2ea8e465cb2fdff1a10ae4`. These are local execution fingerprints, not third-party certification.

## Observations (EXECUTION-VERIFIED, synthetic only)

| Case | Expected | Observed | Specific evidence |
|---|---|---|---|
| T0 coherent synthetic EPUB + minimal PDF | PASS | PASS | no issues |
| T1 NFC/NFD-equivalent ZIP member paths | FAIL | FAIL | `NFC/casefold-colliding EPUB members` |
| T2 hidden DEFLATE payload declared as zero bytes | FAIL | FAIL | `hidden DEFLATE expansion beyond declared size` |
| T3 ordinary empty DEFLATE member | PASS | PASS | no issues |
| T4 casefold-equivalent paths | FAIL | FAIL | `NFC/casefold-colliding EPUB members` |
| T5 CRC-corrupted unused cover | FAIL | FAIL | `Bad CRC-32 for file 'images/cover.jpg'` |
| T6 prefixed ZIP | FAIL | FAIL | `EPUB ZIP has prefix or lacks local header` |
| T7 trailing bytes after ZIP EOCD | FAIL | FAIL | `bytes after ZIP end-of-central-directory` |

**Final:** 8/8 planned outcomes matched. For every case, SHA-256 of both input files before/after was identical, `release=HOLD`, `readiness=BLOCKED`, `publication_authorization=ABSENT`, and `full_conformance_verified=false`.

**Deviation disclosed:** Initial harness's T0/T3 EPUB XML was placeholder `<container/>`, `<package/>`, `<html/>`, not a coherent EPUB as the pre-test notice described. That initial run also returned 8/8, but could not substantiate the *coherent control* claim. Before final rerun, the harness was corrected to a namespace-bearing container, OPF manifest/spine and XHTML body (Git commit `3a86afc`). The corrected final rerun again returned 8/8. This is a fixture-quality correction, not an undisclosed test change. No unplanned cases were added.

**Interpretation (INFERRED):** Independent raw DEFLATE inflation detects this H3 false-size construction even where a central-directory-size-limited reader would not; NFC normalization detects H2. The supplement still cannot validate the EPUB content model on its own. The PDF check remains explicitly labeled `pdf_marker_heuristic_not_object_graph_validation`; Claude's H1 spoof can still pass. ZIP64, data descriptors, malicious same-UID mutation, real source authentication, full accessibility, rendered PDF, and subprocess-grandchild containment are not established by these tests.

**Next:** Ask Claude for independent review of the new raw-DEFLATE and EOCD parser; then consider a HOLD-only composition with the separate smoke gate, not release. Maintain F-001 A1–A6/B6, Dataset A lines 6/7, authenticated sources and real deliverables as BLOCKED. No real files tested and no public launch authorized.
