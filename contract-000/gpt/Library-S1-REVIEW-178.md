# GPT Library-first review — Run 178 (2026-10-18)

GitHub recursive tree `library-shared@b35f1eca60eda49f09197e2597ffa329660165dd`, not truncated: **36 blobs**, **29 KEEP / 7 DEFER / 0 PRUNE**. Compared to Run 177: 33 unchanged, one updated F-001 plan (§51→§53), two new entries (`PROPOSED-PATCHSET-52.diff`, `ledger_merge.py`). Prior decisions for unchanged entries inherited; new entries and §53 source-inspected. This is a metadata inventory and targeted review, not 36 complete semantic audits. No deletions. DEFER means preserved but excluded from active work. No project other than F-001 started.

| Decision | Path | Git blob SHA prefix | Bytes | Evidence/reason |
|---|---|---|---:|---|
| KEEP | `Business/README.md` | `99feb4684bbf` | 1354 | Library/Workshop documentation or index retained as an inert dataset. |
| DEFER | `Business/ideas/F-001-candidate-B-dataset-watch-digest.md` | `3283f9c65189` | 27038 | Alternative income candidate; keep inert while F-001 TAM ebook is the only project. |
| DEFER | `Business/ideas/F-001-candidate-C-provenance-kit.md` | `b35f6be7e9c5` | 13788 | Alternative income candidate; keep inert while F-001 TAM ebook is the only project. |
| KEEP | `Business/ideas/F-001-candidate-ebook-gumroad.md` | `9f558c1406bb` | 125188 | Single active F-001 draft, updated to §53; release HOLD pending A1–A6. |
| KEEP | `Business/ideas/F-001-decision-sheet.md` | `9b6280a760be` | 6846 | A1–A6 decision/approval gate; no default is an authorization. |
| KEEP | `Business/ideas/F-001-gpt-checklist.md` | `69449fceac9d` | 236 | GPT/Claude task split reference. |
| KEEP | `Business/ideas/F-001-tam-build/PROPOSED-PATCHSET-52.diff` | `26a22c767550` | 6581 | New Claude-tested draft patch for no-clobber, listing and ledger parsing; not applied to source. |
| DEFER | `Business/ideas/F-001-tam-build/__pycache__/layout_map.cpython-313.pyc` | `283bfb2e2b41` | 4527 | Generated Python bytecode; non-portable, preserved as a dataset but not executed. |
| KEEP | `Business/ideas/F-001-tam-build/build.py` | `ede8da6f9e33` | 12127 | F-001 offline development utility; retains source fingerprint and requires independent review. |
| KEEP | `Business/ideas/F-001-tam-build/build_pdf.py` | `c029cd67c81c` | 2391 | F-001 offline development utility; retains source fingerprint and requires independent review. |
| KEEP | `Business/ideas/F-001-tam-build/claim_scan.py` | `31f3dcff486c` | 3092 | F-001 offline development utility; retains source fingerprint and requires independent review. |
| KEEP | `Business/ideas/F-001-tam-build/epub_check.py` | `176d42ee19f8` | 7122 | F-001 offline development utility; retains source fingerprint and requires independent review. |
| KEEP | `Business/ideas/F-001-tam-build/layout_map.py` | `07167e3266c5` | 2920 | F-001 offline development utility; retains source fingerprint and requires independent review. |
| KEEP | `Business/ideas/F-001-tam-build/ledger_map.py` | `5fbad4c38139` | 9037 | F-001 offline development utility; retains source fingerprint and requires independent review. |
| KEEP | `Business/ideas/F-001-tam-build/ledger_merge.py` | `0f706be42294` | 4052 | New offline private ledger merge draft; all-time export completeness remains unverified. |
| KEEP | `Business/ideas/F-001-tam-build/listing_check.py` | `adc3123c3031` | 3621 | F-001 offline development utility; retains source fingerprint and requires independent review. |
| KEEP | `Business/ideas/F-001-tam-build/rebuild_datasets.py` | `fa3a62f76549` | 4466 | F-001 offline development utility; retains source fingerprint and requires independent review. |
| KEEP | `Business/ideas/README.md` | `af4a5fdf2634` | 624 | Library/Workshop documentation or index retained as an inert dataset. |
| KEEP | `Business/law-watch/README.md` | `97534cbe0ffc` | 69 | Library/Workshop documentation or index retained as an inert dataset. |
| KEEP | `Business/ledger/CATEGORIES.md` | `9dc5994404b2` | 485 | Public financial schema only; no customer records. |
| KEEP | `Business/ledger/SCHEMA.md` | `1a330a172d62` | 1069 | Public financial schema only; no customer records. |
| KEEP | `Business/records/RETENTION.md` | `a303c78e739c` | 434 | Library/Workshop documentation or index retained as an inert dataset. |
| KEEP | `Business/reports/README.md` | `d5f020432cf9` | 67 | Library/Workshop documentation or index retained as an inert dataset. |
| DEFER | `Business/tax/CALENDAR.md` | `44dac4a98193` | 1228 | Tax dates require current jurisdiction-specific verification; do not rely on for filing. |
| KEEP | `Formulas/F-0001-Echo-Harness-Usability-Criterion.md` | `09e5c0ec7e5b` | 2103 | Formula provenance retained; interpretation not canon. |
| KEEP | `README.md` | `59be277fef1c` | 762 | Library/Workshop documentation or index retained as an inert dataset. |
| KEEP | `Workshop/README.md` | `d39dcb35cb4e` | 187 | Library/Workshop documentation or index retained as an inert dataset. |
| KEEP | `Workshop/fallbacks/README.md` | `d9fe3e458a5d` | 69 | Library/Workshop documentation or index retained as an inert dataset. |
| KEEP | `Workshop/pipelines/P-001-budgeted-inference/README.md` | `cae451754258` | 4646 | Library/Workshop documentation or index retained as an inert dataset. |
| DEFER | `Workshop/pipelines/P-001-budgeted-inference/reference-bot-run.yml` | `1d643ee021cd` | 3564 | Executable workflow/Worker/deployment path; no activation or paid inference authorized. |
| DEFER | `Workshop/pipelines/P-001-budgeted-inference/reference-worker.mjs` | `e912294e5344` | 6378 | Executable workflow/Worker/deployment path; no activation or paid inference authorized. |
| KEEP | `Workshop/pipelines/P-001-budgeted-inference/test-worker.mjs` | `e430c4bf9538` | 2553 | Offline test fixture only; no deployment. |
| KEEP | `Workshop/pipelines/README.md` | `6c0e3e590b69` | 69 | Library/Workshop documentation or index retained as an inert dataset. |
| KEEP | `Workshop/solutions/README.md` | `d0748f7ebb` | 69 | Library/Workshop documentation or index retained as an inert dataset. |
| KEEP | `Workshop/solutions/S-001-cloudflare-deploy-without-github-app/README.md` | `54c7280741d9` | 4413 | Library/Workshop documentation or index retained as an inert dataset. |
| DEFER | `Workshop/solutions/S-001-cloudflare-deploy-without-github-app/reference-deploy.yml` | `a33d0202daf5` | 2780 | Executable workflow/Worker/deployment path; no activation or paid inference authorized. |

**New evidence:** §52 patch is proposed only; source scripts unchanged. §53 ledger merge is idempotent for duplicate refs but cannot recover a refund absent from a month-only export. GPT's new private pre-merge relative-coverage gate is in the Run 178 handoff. It does not change the shared Library. R3 and branch protections preserved.
