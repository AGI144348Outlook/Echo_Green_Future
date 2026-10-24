# F-001 TAM Protocol ebook — numerical consistency evidence and editorial disclosure draft, Run 327 (2026-10-24 CT)

**ONE active project:** F-001 TAM Protocol ebook. **DRAFT / HOLD / BLOCKED / NOT LAUNCH-READY.** This is an independent, source-pinned arithmetic review of the public TAM notes, not a historical or archaeological validation, product release, or correction to shared sources.

## Provenance, preregistration and method

- **Pre-test:** [Issue #46](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/46) published before the first execution; method and falsifiers recorded there. No CI or paid inference.
- Source repository `AGI144348Outlook/The-TAM-protocol`, pinned `main` commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`; Dataset A Git blob `b62c970a660e0a6685b58db1ef121690daa4fce7` (six source rows), Dataset B Git blob `12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4` (eight rows).
- Python `Decimal` script: [F-001-NUMERIC-AUDIT-327.py](F-001-NUMERIC-AUDIT-327.py). Local final script SHA-256 `acfd21df57f5b25917e2835ad3c8d11c648532f6b7544f2f383f54c3547647c5`; output JSON SHA-256 `c283fb89c7a70d94b3391b8413072e2cb49bbecc09d748a3d4dfa5495633c07b`. The script transcribes the public source rows into constants; **it does not independently fetch/authenticate source bytes at runtime**. Each displayed row was compared against the fetched GitHub source before execution.
- Equation: `expected_g = 13.7 × stated_unit_fraction`; `deviation_% = 100 × (displayed_g - expected_g) / expected_g`. Comparison uses nearest hundredth of a percentage point, half-up. Hypothetical rounding interval for each displayed two-decimal gram mass is `[displayed - 0.005, displayed + 0.005)` grams; this is an analytical assumption, **not a measurement-precision claim made by the source**.

## T1–T3: Dataset A observed results

| Source object | Displayed mass (g) | Stated unit | Printed deviation | Recomputed from displayed mass | Printed deviation reproduced? | Compatible with a hypothetical 0.01g rounding interval? |
|---|---:|---:|---:|---:|---|---|
| Ingot Slice (Heavy) | 136.98 | 10 | -0.01% | -0.014599% | YES | YES |
| Coiled Wire (Large) | 68.52 | 5 | +0.03% | +0.029197% | YES | YES |
| Hacksilber Scraps (x3) | 13.71 | 1 | +0.07% | +0.072993% | YES | YES |
| Flattened Foil | 6.86 | 1/2 | +0.14% | +0.145985% | **NO** (rounds +0.15%) | YES |
| Silver Droplet | 3.42 | 1/4 | -0.03% | -0.145985% | **NO** (rounds -0.15%) | YES |
| Small Scrap | 1.71 | 1/8 | <0.01% | -0.145985% | **NO** | YES |

**Observation:** Three of six printed deviations reproduce directly from displayed masses, three do not. **Interpretation:** all six could be compatible with unseen, higher-precision measurements subsequently rounded to 0.01g, but those raw measurements are **not present** in the inspected source. Do not silently substitute calculated deviations for the original figures; request measurement provenance, original denominator/rounding rule and Timothy's editorial disposition.

## T4–T5: Dataset B and cross-dataset terms

| B ratio | Displayed mass (g) | Expected mass (g) | Deviation from exact fraction | Exact fraction within ±0.005g of displayed? |
|---:|---:|---:|---:|---|
| 1 | 0.85 | 0.856250 | -0.729927% | **NO** |
| 2 | 1.71 | 1.712500 | -0.145985% | YES |
| 4 | 3.42 | 3.425000 | -0.145985% | YES |
| 8 | 6.85 | 6.850000 | 0.000000% | YES |
| 16 | 13.70 | 13.700000 | 0.000000% | YES |
| 32 | 27.40 | 27.400000 | 0.000000% | YES |
| 80 | 68.50 | 68.500000 | 0.000000% | YES |
| 160 | 137.00 | 137.000000 | 0.000000% | YES |

**Observation:** Seven of eight Dataset B displayed masses lie within ±0.005g of their exact 13.7g fractions. The 1/16 unit is 0.85625g, which would ordinarily display as 0.86g when rounded to two decimals, whereas B prints 0.85g. **Interpretation:** it might reflect truncation, a different precision policy, or source error; the audit cannot decide which. Dataset A labels the 1/8 unit *Gerah*; Dataset B labels the 1/16 unit *Trace/Gerah Base*. This is a terminology conflict, not permission to standardize silently.

## Execution history and deviations (not concealed)

1. First local script attempt failed with `TypeError`: a string variable `f` was multiplied by `Decimal` when generating expected masses; no results file was produced.
2. Second attempt corrected expected-mass calculation but failed at the analogous difference calculation in B; no results file was produced.
3. Third attempt produced the expected summary, but source inspection of the harness revealed that `pdev(m,f)` improperly captured the loop's `fraction` variable instead of using its parameter. This was a harness defect even though its output happened to agree for this call sequence.
4. Final corrected run uses `pdev(m,f)` with the function parameter, all six declared assertions completed, no exceptions; final summary: **A 3 reproduced / 3 not reproduced / 6 interval-compatible; B 7 interval-compatible / 1 outside; Gerah wording conflict present.** The final JSON is archived in the run's local handoff package; only the tested script and researcher-readable results are committed here.

No deviation from the prospectively registered *research question* or dataset scope. The first three implementation defects and corrections are part of the record; this is not presented as a first-try pass. No source file, shared branch, or published product was changed.

## Draft disclosure for editorial consideration (NOT approved book copy)

> The weight tables reproduce values from the author's research notes. When deviations are recalculated using the masses as displayed and a 13.7g reference unit, three Dataset A percentages differ from the printed deviations. Those differences might reflect rounding from measurements of greater precision, but original measurements and their calculation method have not been supplied. Dataset B also displays 0.85g for a theoretical 1/16 unit of 0.85625g, and the term *Gerah* is applied differently across the two datasets. These are open editorial and source-verification questions; the tables do not independently establish historical standards, trade networks or predictive accuracy.

## Continuing acceptance, blockers and next action

**Project identifier:** F-001 (unchanged). **Deliverables:** [ ] author-approved manuscript and claims sheet; [ ] real source-pinned EPUB with EPUBCheck/accessibility; [ ] real PDF with rendering/accessibility; [ ] reviewed Dataset A CSV with rows 6/7 disposition; [ ] reviewed Dataset B CSV with terminology and precision policy; [ ] approved rights/credit/listing and independent release receipt. **Acceptance:** no unverified measurement promoted to historical fact, exact source/rights approved, all four genuine output files independently verified, and Timothy explicitly authorizes release. **Current publication gate: HOLD/BLOCKED.**

**Complementary Claude action requested:** independently check this arithmetic and the three non-reproducing A deviations; ask Timothy for original mass precision/rounding, Dataset A row dispositions and B's 1/16 value; incorporate a truthful table note or annotated appendix in Claude's manuscript workflow. **GPT next:** independently verify genuine EPUB/PDF/CSV bytes against the pinned source only after the editorial decisions and real artifacts exist. No new income pipeline, ZIP checker version, paid inference, outreach, spending or publication.
