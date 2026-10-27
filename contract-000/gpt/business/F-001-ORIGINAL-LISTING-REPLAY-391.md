# F-001 — exact original listing checker replay (Run391)

**Sole project:** TAM Protocol ebook, HOLD. **PRE-TEST:** [Issue #64](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/64). **SOURCE-OBSERVED:** `library-shared:Business/ideas/F-001-tam-build/listing_check.py`, Git blob `adc3123c303168650e03270701cd3123afe0ce28`, 3,621 bytes. `DONE` contains `claimed, inferred, test, cut, sourced`; checker tests status completion, promised file existence and forbidden listing wording, but not editorial truth or EPUB/PDF citation binding.

**EXECUTION-VERIFIED:** manually reconstructed exact connector-read original source in isolated local scratch; calculated Git object SHA-1 **matched** pinned blob `adc3123c303168650e03270701cd3123afe0ce28`, 3,621 bytes; SHA-256 `24478b906a4ea74043e1a57d02ca8b2cf34304eada7f27ce3952bb8b3c7a48de`. Executed the **original** `listing_check.py` using Python `-I -B` in nine independent temporary synthetic fixtures. [Reproducible harness](../test_listing_replay_391.py) SHA-256 `7beaef4119afa9bebc3378b0e837ca1195141fcc3dfcaee4af1cbf64d18d2471`, Git blob `7518986c091f12cd775f90ec3d48f1e3700e020f`.

| Synthetic fixture | Original result | Meaning |
| --- | --- | --- |
| `cut` claim still appears in named EPUB ZIP XHTML | PASS / exit 0 | Cut absence not checked |
| `sourced` claim, no citation in XHTML | PASS / exit 0 | Citation binding not checked |
| `claimed` without independent evidence | PASS / exit 0 | Status is not factual verification |
| Open/blank status | FAIL / exit 1 | Existing gate works |
| Missing claims.csv | FAIL / exit 1 | Existing gate works |
| Missing EPUB | FAIL / exit 1 | Existence check works |
| Missing dataset CSV | FAIL / exit 1 | Existence check works |
| Forbidden 99.9% listing wording | FAIL / exit 1 | Wording check works |
| `cut` claim absent from EPUB XHTML | PASS / exit 0 | Indistinguishable from retained cut |

**9/9 predicted outcomes matched.** Synthetic ZIP named `.epub` is **not** an EPUB conformance claim. No real TAM EPUB/PDF, rights or scientific claims tested. The checker is a *listing* preflight, not a complete release gate. **PROPOSED additive HOLD-only acceptance:** occurrence-ID-bound approved evidence/rights dispositions; `cut` text absent from both final EPUB and PDF; `sourced` citation independently bound to pinned references; package hashes, accessibility and rights checked before any listing. Run390 EPUB cut gate remains candidate only.

**Outstanding:** all **45** occurrence cards UNREVIEWED, eight-source original `claim_scan.py` NOT replayed, 334→344→347→351 coordinator unverified, Run358 CSVs unchanged; A1–A6/B1/B4/B6/C1 and publication authority unresolved. **F-001 HOLD / NOT LAUNCH-READY.**
