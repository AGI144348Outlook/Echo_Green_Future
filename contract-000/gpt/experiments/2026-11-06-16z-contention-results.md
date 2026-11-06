# GPT-only experimental results — 2026-11-06 16Z
Prospective Issue #327 created before test; post-test comment https://github.com/AGI144348Outlook/Echo_Green_Future/issues/327#issuecomment-6689302280.
Source commit 9ddcd0d9acf2d163e2f419c07ca51035887edebf; fetched exact blob f5c42b480dee193f758134e09a06fc96e8182cc4; JS Function execution of fetched source; fixed seeds 1106, 1116, 1124; 270 steps; two draws/step p=0.54, age<=8, dwell=3.
T1..T10 all true (10/10). Seed 1106: 297 arrivals, 269 accepted, 20 expired, 8 terminal, 260 accepted with wait, max age 8. Seed 1116: 291/269/9/13, 266 waited, max age 8. Seed 1124: 305/268/28/9, 263 waited, max age 8. All baseline max one admission per step and zero observed seat overlap.
Mutants: expiry_off accepted max age 27; admit_two admitted 2/step. Ledger conserved in all tested runs.
Synthetic independent circular target loss (lower better): coupled 6.8395061728, uncoupled 6.7407407407, shuffled 6.5802469136. Coupling loses. T10 tests difference and finite loss, not superiority.
Limitations: event ledger and generator still in same code file, verifier logically distinct but not independent implementation; target artificial; 3 seeds; no real glyph semantics, A-000 authority, or 27-node cognitive learning; no production execution. No CI, paid inference, external effects.
Next: independently implement event verifier, inspect terminal expiration semantics, increase seeds, and add genuine multiring glyph composition separately after prospective registration.
