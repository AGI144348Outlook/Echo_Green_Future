# F-001 — precision supplement v331 (editorial draft, not an author-approved manuscript)

**Sole project:** F-001, TAM Protocol research notebook / ebook. **HOLD / BLOCKED / NOT LAUNCH-READY.** This is a *replacement candidate for the wording* in [Run 329 supplement](F-001-PRECISION-METHODS-SUPPLEMENT-329.md), not a change to the source tables, existing manuscript, Claude's files, or Timothy's editorial decisions. Source evidence: public `AGI144348Outlook/The-TAM-protocol@d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`, Dataset A Git blob `b62c970a660e0a6685b58db1ef121690daa4fce7`, Dataset B blob `12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4`; Claude §134, §136 cross-review on shared F-001 plan blob `d1a194c0ce7419022d7742ecce34f1b0a260a269`; previous GPT Runs 328–330. **No new calculation or test was executed in this run.** The values below are source-reviewed and rely on the independently reported prior calculations.

## Proposed reader-facing appendix note (subject to Timothy's approval)

> **Displayed precision and alternative calculations.** Dataset A and Dataset B present masses to 0.01 gram, but the source does not state whether they are measurements, rounded calculations, or truncated calculations. Using the source's stated 13.7-gram unit, all eight printed masses in Dataset B are *compatible with* truncating the corresponding fractional calculations to 0.01 gram. Nearest-hundredth rounding instead reproduces seven of eight values using ties-to-even, or six of eight using ties-away-from-zero. For example, 1/16 of 13.7 grams is exactly 0.85625 grams, printed as 0.85 grams; 1/4 is exactly 3.425 grams, printed as 3.42 grams. These comparisons do not establish the author's original calculation method or independently verify any historical measurement.
>
> Dataset A cannot be reproduced using one of those conventions throughout: nearest-hundredth rounding reproduces the printed percentage deviations in rows 1–3, while truncation reproduces rows 1, 3 and 4; rows 5 and 6 are not reproduced by either convention when calculated from the displayed masses. The original input precision and method are not supplied. Its printed `<0.01%` entry is an inequality, not an exact measured percentage. All printed values remain unchanged. The source also uses *Gerah* for both 1/8 of a unit in Dataset A and 1/16 of a unit in Dataset B; that terminology remains unresolved pending the author's decision.

**Placement recommendation (PROPOSED):** an appendix plus a short footnote at the first table, as Claude §136 suggested; never quietly substitute this explanation into the author's historical argument. Label alternative computations `RECOMPUTED_FROM_DISPLAYED_VALUES`, source claims `SOURCE_STATED`, and origin-method claims `UNVERIFIED`. Do not assert that the author truncated or rounded; the source lacks that method statement. A printed mass to 0.01 g does not establish ±0.005 g instrumental uncertainty; display precision and measurement uncertainty are different concepts.

## Source-preserving numerical comparison (previously checked, not re-run here)

| B fraction | Printed g | Exact 13.7 × fraction g | Half-up | Half-even | Truncated |
|---|---:|---:|---:|---:|---:|
| 1/16 | 0.85 | 0.85625 | 0.86 | 0.86 | 0.85 |
| 2/16 | 1.71 | 1.7125 | 1.71 | 1.71 | 1.71 |
| 4/16 | 3.42 | 3.425 | 3.43 | 3.42 | 3.42 |
| 8/16 | 6.85 | 6.85 | 6.85 | 6.85 | 6.85 |
| 16/16 | 13.70 | 13.7 | 13.70 | 13.70 | 13.70 |
| 32/16 | 27.40 | 27.4 | 27.40 | 27.40 | 27.40 |
| 80/16 | 68.50 | 68.5 | 68.50 | 68.50 | 68.50 |
| 160/16 | 137.00 | 137 | 137.00 | 137.00 | 137.00 |

**A-row correction from Claude §136:** A row 4's printed +0.14% is compatible with truncating the computed +0.145985…%, but not rounding it half-up. The earlier Run 329 phrase "rows 4–6 do not reproduce" was true only under the named half-up convention; do not generalize it to truncation. Rows 5 and 6 differ more substantially and remain review flags. The printed percentages are not necessarily exact points; their uncertainty is not independently established.

## Editorial acceptance / next action

- **Claude:** independently review this v331 wording for faithful representation of Dataset A row 6 inequality and placement; do not edit GPT file, reply in shared coordination records. The current CSV builder's output issues are separately documented in [CSV acceptance specification v331](F-001-CSV-REVIEW-331.md).
- **Timothy:** resolve A1–A6, B6, A rows 6/7 dispositions, *Gerah* terminology, the optional precision note and claims, source/license/credit and explicit publication. No default or assistant preference substitutes for author approval.
- **GPT:** after source and editorial decisions, check real EPUB/PDF and both CSVs against independently held source pins and a single reconciled receipt, with a prospective pre-test Issue. **No actual final files, checksum receipt, publication, paid API or storefront action is claimed here.**
