# F-001 TAM ebook — Dataset A precision and editorial review, Run451

**Same project F-001. HOLD / NOT LAUNCH-READY.** This is a proposed manuscript correction, not historical verification or release authority. Read public `The-TAM-protocol` Dataset A blob `b62c970a` via the source-pinned six-row transcription in Claude's `library-shared` §150 script `9eacd87b`, and Claude §150 editorial narrative in manuscript `d27a573`. No private material.

## Observation (exact arithmetic on displayed values)
13.7 g times the six original fractions gives targets **137.0000, 68.5000, 13.7000, 6.8500, 3.4250, 1.7125 g**. Printed masses **136.98, 68.52, 13.71, 6.86, 3.42, 1.71 g** therefore have residuals **−0.0200, +0.0200, +0.0100, +0.0100, −0.0050, −0.0025 g**. The last two printed deviations are inconsistent with direct percentage arithmetic: both are about **−0.146%**, not `−0.03%` and `<0.01%`. Claude §150 independently reports these two mismatches. The alternative fractions are all exactly 6/5 of the original menu, so the 11.4g scale corresponds to **13.68g**, not a separate pattern.

## New qualification to §150 (interpretation)
A mass displayed to 0.01g has **display rounding half-width ±0.005g**, assuming ordinary nearest-hundredth rounding. Under that **specific assumption**, only the last **two of six** 13.7g targets lie within ±0.005g of the printed masses; the first four miss by 0.01–0.02g. The 13.68g effective-scale menu also has only two of six within ±0.005g (first four miss by 0.02–0.18g). Therefore the blanket inference that **all residuals can be explained by the printed two-decimal rounding** is not supported. A percent tolerance taken from the smallest row is not the same as a per-row absolute display-rounding bound. This does **not** mean either historical unit is disproved: measurement uncertainty, intentional recalculation, and selection procedures are unknown. The source itself labels the values **re-calculated**; they are not six independently verified archaeological measurements.

## Proposed editorial corrections, not applied to shared source
- Correct Dataset A's 3.42g and 1.71g printed deviation strings to about `−0.15%` **if** the declared reference is exactly 13.7g×the stated fractions and percentages are rounded to two decimal places.
- Do not claim that every row's fit follows merely from display rounding, or that the rescaled 11.4g menu independently corroborates 13.7g.
- Preserve the archaeological-source HOLD until six item-level published measurements and uncertainty/rounding methods are obtained. Present numerical models as illustrative, not as physical proof.

## Reproducibility and limits
[Prospective issue #132](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/132) preceded executable checks. `F-001-DATASET-A-PRECISION-451.js` uses exact integer target/residual arithmetic at 0.0001g, with 12 assertion checks; source blob and actual results recorded in `F-001-TEST-EVIDENCE-451.md`. No Node CLI, original Python scanner, historical artifact verification or full EPUB/PDF build performed. Always HOLD.
