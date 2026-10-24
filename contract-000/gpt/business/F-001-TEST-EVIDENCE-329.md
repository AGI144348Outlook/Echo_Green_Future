# F-001 — independent source-pinned precision-method comparison, Run 329

**Status:** research evidence only; `F-001` is the sole continuing TAM Protocol ebook candidate. **HOLD / BLOCKED / publication_authorization=ABSENT.** No release build, manuscript authorization, paid service, account or outreach.

**Pre-test:** [Issue #48](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/48), created **before** the isolated check. **Post-test:** [same Issue comment](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/48#issuecomment-6387654989). The prospective hypothesis, method, expected results and falsifiers are in the Issue body. This record was prepared after the check; it is not a retrospective pre-registration.

**Pinned inputs (Git blob SHA-1 verified by connector):** `AGI144348Outlook/The-TAM-protocol` commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`; Dataset A `Dataset A: The Eshtemoa Inventory (Forensic Weight Distribution)` blob `b62c970a660e0a6685b58db1ef121690daa4fce7`; Dataset B `Dataset_B_Binary_Matrix.md` blob `12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4`. These Git fingerprints are content IDs, not authorship or scientific authenticity attestations.

## Executed method (not GitHub CI)

The connected GitHub tool read both pinned source texts. An isolated V8 script parsed A rows with mass/unit/printed percent and B rows with ratio/mass. For B it represented the base `13.7g` as **1370 integer hundredths of a gram**, compared each printed hundredth against the exact rational `1370 × ratio / 16`, then separately applied half-up, half-even and truncation-toward-zero rules to 0.01g. For A it recomputed `100 × (printed mass - 13.7g × printed units)/(13.7g × printed units)`, rounded to two percentage decimals (half-away from zero), and compared the displayed percent. No source file was edited, no deployment or model API was called, and no independent historic measurements were available.

## Actual observations

| Predeclared check | Expected | Observed | Result |
|---|---:|---:|---|
| A source rows | 6 | 6 | PASS |
| A displayed deviation matches | 3 | 3 (rows 1–3) | PASS |
| B source rows | 8 | 8 | PASS |
| B nearest 0.01g, half-up matches | 6 | 6 | PASS |
| B nearest 0.01g, half-even matches | 7 | 7 | PASS |
| B truncation to 0.01g matches | 8 | 8 | PASS |

**B details:** printed 0.85g for 1/16 unit vs exact 0.85625g fails both nearest-cent modes but matches truncation. Printed 3.42g for 1/4 unit vs exact 3.425g is an exact two-decimal tie: half-even/truncation match; half-up predicts 3.43g. All other six printed values match all three modes. **A details:** calculated deviations from displayed masses, in row order, approximately `-0.014599%, +0.029197%, +0.072993%, +0.145985%, -0.145985%, -0.145985%`. Printed A deviations match the first three when displayed to 0.01 percentage point, not rows 4–6. These are arithmetic facts about displayed values, not measurements.

**Interpretation / limitation:** Matching all 8 under truncation does **not** establish truncation as the author's actual method. Half-even matches 7; half-up matches 6. The original measurement precision, any method for A's deviations, archaeological provenance, and the terminology conflict (A `Gerah` at 1/8 vs B `Trace/Gerah` at 1/16) remain unresolved. Claude §134 also distinguishes interpreting printed percentages as rounded **bands** rather than exact points; this isolated check did not rerun the uncertainty-band comparison. No real EPUB, PDF, CSV release artifact or accessibility check was executed. The experiment is not a frozen race or an external scholarly replication.

**Deviations:** None of the six predeclared checks failed. No parser exclusions beyond header/prose lines; exact row counts matched. No unanticipated tool failures. The computation was read-only and V8-local; it did not execute Claude's Python `CLAUDE-tam-arithmetic-check-134.py`, which remains an independent source record in the shared Library.

**Next:** Claude independently reviews the neutral reader note and disputed method/terminology; Timothy decides A1–A6/B6 and the editorial disclosures. Do not insert the note into a for-sale manuscript or alter source tables without approval.
