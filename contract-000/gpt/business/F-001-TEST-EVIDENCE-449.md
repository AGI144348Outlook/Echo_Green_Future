# F-001 — Article 1 grid fairness / editorial arithmetic, Run449 actual evidence

**Sole product:** TAM Protocol ebook F-001. **HOLD / NOT LAUNCH-READY.** This is a reversible source-bound research note, not historical authentication, approved editorial copy, or a release gate.

**Prospective registration:** [Issue #129 PRE](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/129) was published before numerical testing. The six-fraction scaling observation arose *after* the first results; a separate [prospective amendment](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/129#issuecomment-6504493206) was posted before its exact-rational follow-up.

**Source custody:** `The-TAM-protocol@d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`; Dataset A exact Git blob `b62c970a660e0a6685b58db1ef121690daa4fce7`, Article 1 `237bd3335abdcc0f0465817dffe01ad6eaa86055`. Dataset A explicitly calls its numbers **“Re-calculated for 13.7g Invariant”**; original excavated weights, uncertainties, selection rule and independent historical source were not provided.

**Declared model targets:** 13.7g × [10, 5, 1, 1/2, 1/4, 1/8]; hypothetical 11.4g × [12, 6, 6/5, 3/5, 3/10, 3/20]. The controlled sensitivity case uses the *same* first menu with 11.4g; it is intentionally restrictive and **not** a fair historical rejection of 11.4g. Each measured mass is matched to its nearest declared target by absolute mass difference; percent is relative to target.

| Original Dataset A row | Mass (g) | 13.7g target (g) | 13.7g absolute error % | Hypothetical 11.4g target (g) | 11.4g absolute error % |
|---|---:|---:|---:|---:|---:|
| Ingot Slice (Heavy) | 136.98 | 137.0000 | 0.01460 | 136.8000 | 0.13158 |
| Coiled Wire (Large) | 68.52 | 68.5000 | 0.02920 | 68.4000 | 0.17544 |
| Hacksilber Scraps (x3) | 13.71 | 13.7000 | 0.07299 | 13.6800 | 0.21930 |
| Flattened Foil | 6.86 | 6.8500 | 0.14599 | 6.8400 | 0.29240 |
| Silver Droplet | 3.42 | 3.4250 | 0.14599 | 3.4200 | 0.00000 |
| Small Scrap | 1.71 | 1.7125 | 0.14599 | 1.7100 | 0.00000 |

**Observed arithmetic:** Maximum absolute error 0.1459854% / mean 0.0924574% for 13.7g, and 0.2923977% / mean 0.1364522% for the hypothetical 11.4g grid. Leave-one-out maximum is unchanged at 0.1459854% for all six 13.7g omissions (three rows tie at the maximum); for 11.4g, omitting the foil reduces maximum to 0.2192982%, while the other five omissions leave 0.2923977%. The common fraction menu gives the 11.4g model a maximum 20.3508772% and mean 20.1637427% error, **because the menu is anchored to 13.7g**. This controlled case exposes menu sensitivity; it is not a historically neutral comparison.

**New algebraic observation (tested only after the pre-amendment):** Every proposed alternative fraction is exactly **6/5** times the corresponding 13.7g fraction: 12/10 = 6/5 = (6/5)/1 = (3/5)/(1/2) = (3/10)/(1/4) = (3/20)/(1/8). Thus 11.4g × (6/5) = **13.68g**, only 0.02g below 13.7g. The six target pairs differ by 0.20, 0.10, 0.02, 0.01, 0.005 and 0.0025g. This is a **rescaling of the same six-position pattern**, not independent evidence that historical accountants used either base. The model menus are constructed from the same six printed values, so comparing their small residuals cannot establish historical uniqueness.

**Additional source-text discrepancies, directly computed:** Dataset A prints Silver Droplet 3.42g as **−0.03%** from 3.425g, but the calculated deviation is **−0.1459854%**. It prints Small Scrap 1.71g as **<0.01%** from 1.7125g, but the calculated deviation is **−0.1459854%**. The printed percentages need a rounding or denominator explanation, or correction, before any release. This is a text/arithmetic discrepancy, not evidence about the hoard's actual measured values.

**Actual tests and deviations:** First predeclared V8 arithmetic run on the pinned Dataset A passed **7/7** assertions (source pin, six rows, both model bounds, common-grid change, missing-row rejection, foil perturbation to 7.11g detected). The post-amendment exact-rational cross-multiplication found **6/6** fractions equal to 6/5 of the original. Committed script `F-001-ARTICLE1-GRID-AUDIT-449.js` Git blob `33cad9d5df8128690d6adb8b28274eee79960f68` was fetched back and its **exact committed functions** executed in V8 against the pinned Dataset A: **10/10** checks passed, including missing and duplicate rows, source pin, exact scaling, effective base and perturbation. No failures or code corrections in these final checks. This was **not** a Node CLI process execution, original Python claim scanner replay, Genesis test, or independent archaeology review. No CI triggered.

**Proposed editorial handling (NOT APPROVED):** Keep S16–S18 in CLAIMED / UNSUPPORTED-AS-PHYSICAL-PROOF state. Add an explicit data-provenance notice and correct both printed deviation percentages (subject to verifying intended rounding/denominator). Do not treat the proposed 11.4g grid as historical fact. Next scientific step is a published independent inventory of original measured masses, explicit uncertainties, an advance-selected set of competing units and allowed fractions, and a held-out validation sample. Obtain Timothy's A1–A6/B1/B4/B6/C1, rights, editorial and release decisions separately.
