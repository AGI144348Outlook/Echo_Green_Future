# F-001 Run 376 — 14-row editorial reconciliation (HOLD)

**PRE-TEST:** [Issue #56](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6422091548). **Continuing project:** F-001 TAM Protocol ebook only. **Inputs:** [Run371 actual-source legacy CSV A/B](https://github.com/AGI144348Outlook/Echo_Green_Future/tree/contract-000-gpt-run371-20261026-0700/contract-000/gpt/business/F-001-DATASET-STAGE-371), blob A `8ef7fa41ef0229ce9a2754737f0aa0e774fd3b7b`, B `0df0e4153cf2ae9c292dd05588485e13bfd999f3`. These are derived CSVs, not the original historical records or pinned Run334 schema.

**Executable:** [read-only Node/V8 reconciler](f001_editorial_reconcile_376.js), Git blob `809b07d370ce74c157bc14dd60dadb6808bb1187`. **Output:** [14-row JSON worksheet](F-001-EDITORIAL-RECONCILIATION-376.json), including CSV line numbers, values, calculated percent deviations, source flag statuses and human review questions.

**Observed:** positive run **45/45 assertions matched** (six A expected/deviation pairs, eight B ratio/expected/deviation triples, schema/count and source-specific flags). Five replay controls using the exact committed JS source yielded **5/5 expected verdicts**, including four intentional corruptions/reductions. Controls:
- baseline: expected `true`, observed `true` (45/45 checks), matched.
- A expected mass corrupted: expected `false`, observed `false` (44/45 checks), matched.
- B ratio/unit inconsistency: expected `false`, observed `false` (41/45 checks), matched.
- B first displayed mass tampered: expected `false`, observed `false` (43/45 checks), matched.
- A Silver Droplet row removed: expected `false`, observed `false` (40/43 checks), matched.

**Editorial observations:** A Silver Droplet and Small Scrap have `stated_matches_recomputed=False` in the derived dataset. Dataset A calls 1/8 U *Gerah* while Dataset B labels 1/16 U as *Trace/Gerah Base*. Dataset B 1/16 U displays 0.85 g against the 13.7×unit model of 0.85625 g; truncation is one possible explanation, not established. Four B rows with the same units as A rows have displayed masses differing by 0.01–0.02 g (ratios 8,16,80,160); these can reflect distinct objects or measurement/rounding choices and are not declared errors.

**Interpretation:** This is a reproducible *editorial decision packet*, not a scientific validation of historical measurements. Keep both sources intact; ask Claude to review claims, Gerah, Article 4, and measurement precision before Timothy resolves manuscript language. **No automated correction.** `release_authorized=false` and status HOLD.

**Limits:** no original precision metadata, no independent primary-source authentication, no rights/license check, no full Run334→344→347→351 staging, EPUB/PDF/a11y/listing or publication. Tests are V8 assertions over committed legacy CSVs and synthetic corruptions, not Python builder or CI execution.

**Next:** Claude independent editorial crosscheck, Timothy decisions A1–A6/B6/C1; GPT integrate approved wording into review build only after explicit authority. No new product or commercial action.
