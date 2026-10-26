# F-001 — actual CSV precision and mass-rounding audit, ChatGPT Run 359

**Sole income project:** F-001 TAM Protocol ebook. **HOLD / NOT LAUNCH-READY.** This is a follow-up to the [actual-source rebuild Run 358](F-001-REAL-REBUILD-358.md) and shared [decision sheet](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-decision-sheet.md). No new pipeline, release, paid inference, outreach, spending, or shared content edit.

## Prospective record and correction

[PRE-TEST Issue #56 #6405203095](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6405203095) was published before running the precision audit. Initial in-memory harness attempt **FAILED** at parsing B's legitimate `1/16` unit string because it expected decimal-only input; no assertions completed or files were committed. [Amendment #6405229244](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6405229244) was posted **before** correcting the harness and retrying with exact fractional-unit parsing. [POST #6405238248](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6405238248) records the actual results in the same Issue.

## Source pins and method

Read the two **committed Run 358** CSV files directly through authenticated GitHub connector, confirming Git blob SHA-1 A `8ef7fa41ef0229ce9a2754737f0aa0e774fd3b7b` and B `0df0e4153cf2ae9c292dd05588485e13bfd999f3`. The upstream raw public TAM source was verified in Run 358; **this run did not re-execute the original Python builder**. Executed the [new pure-JS auditor](F-001-PRECISION-AUDIT-359.js) in the local V8 isolate on those exact CSV contents. It uses BigInt scaled-decimal arithmetic (six fractional places) and exact B fractions. Assumptions are **explicit, not observed measurement policy**: printed mass to nearest 0.01 g implies possible unrounded value in printed ±0.005 g; two-decimal numeric percent claims imply ±0.005 percentage-point bands; `<0.01` is interpreted as absolute percent deviation <0.01. Endpoint ties conservatively included. No empirical tolerance or release threshold was invented.

## Actual observations (9/9 assertions passed after correction)

- A: **6 rows**, **2 existing builder point flags False** (Silver Droplet, Small Scrap), **0 claimed percent bands disjoint from a possible rounded-mass interval**. This is not proof the claims are accurate; it means the two point-estimate flags alone do not establish impossibility at the printed mass precision.
- Silver Droplet: 3.42 g printed versus 3.425 g expected; point deviation approximately **−0.146%**, but plausible deviation interval from 3.415–3.425 g is **−0.292% to 0%**, overlapping the claimed −0.03% band.
- Small Scrap: 1.71 g printed versus 1.7125 g expected; point deviation approximately **−0.146%**, plausible interval **−0.438% to +0.146%**, overlapping the claim `<0.01%` under the explicitly stated absolute interpretation.
- B: **8/8 exact ratio/unit identities**, but that does **not** establish mass accuracy. At ratio **1**, printed **0.85 g** versus expected **0.85625 g** is outside the nearest-cent interval [0.845,0.855] g. At ratio **4**, **3.42** versus **3.425** g is exactly a rounding tie boundary; the rounding rule matters. Other six B rows lie within the nearest-cent interval. This does **not** prove the source's rule was nearest-cent rather than truncation or another convention.
- Three controls: a deliberately absurd Silver Droplet +9.99% claim was rejected by interval overlap; a corrupted B ratio-16 unit `0.50` was rejected by exact ratio/unit identity; changing B ratio-1 mass to `0.86` in a **counterfactual in-memory copy only** removed the nearest-cent exception. No source CSV was changed.

The [machine-readable evidence](F-001-PRECISION-RESULTS-359.json) records every A/B row, source blob pins, computed bounds, all nine assertions and the initial harness failure. The [auditor](F-001-PRECISION-AUDIT-359.js) can be run with Node and the two committed CSVs; the current run executed it as an identical in-memory function, not through the Node CLI. No CI was triggered.

## Interpretation and limitations

**Do not silently replace** the source's stated percent values with recomputed point values. The original measurement precision, rounding convention and whether source values are exact or illustrative remain **unverified**. Claude's independent arithmetic probe `CLAUDE-tam-arithmetic-check-134.py` was source-read but **not executed** here; this GPT audit is independent of its runtime. The results are arithmetic/format evidence only, not historical, archaeological, scientific or licensing validation. No real stage coordinator, EPUB/PDF, accessibility audit, release witness, claims signoff or rights verification was run.

**Next GPT action:** integrate these pinned real CSVs into the existing HOLD staging/package chain and prove failure on source/hash changes with an independent source pin; preregister tests first. **Claude complementary action:** editorially distinguish point deviations from rounding uncertainty, resolve Gerah naming and ratio-1 rounding convention, and review ~35 manuscript claims/rights/listing. **Timothy blockers:** A1–A6, B6/C1, editorial dispositions, credit, licence, source branch, book identifier, and publication authorization. **F-001 remains HOLD.**
