# Contract-000 GPT Library-first review — Run 093

Date: 2026-10-14 America/Chicago. Source branch: `library-shared` @ `f6ecce6f75ab649a4870a306cf761bd3b7a2148e` (recursive Git tree). `SOURCE-OBSERVED` = source tree and selected file bodies inspected; other entries assessed as dated manifest candidates, not execution-verified. KEEP means retain as dataset, not approve execution; DEFER means preserve but hold promotion. No deletions (TJ R3).

Count: 22; KEEP 16, DEFER 6, PRUNE 0.

| Path | Git blob SHA | Bytes | Decision | Evidence and rationale |
|---|---|---:|---|---|
| `Business/README.md` | `99feb4684bbf03ac3d900b592538cba6754ff3c6` | 1354 | KEEP | Public-only business structure; separates private financial records. |
| `Business/ideas/README.md` | `af4a5fdf26347b2ba64da3ebffe9dd5dd313c52f` | 624 | KEEP | Ideas registry; not an authorization to launch. |
| `Business/ideas/F-001-candidate-ebook-gumroad.md` | `7caeec553380e48058528a0a09fd256c6983677b` | 54614 | KEEP | Existing sole F-001 plan; manuscript/rights/release gates open. |
| `Business/ideas/F-001-candidate-B-dataset-watch-digest.md` | `3283f9c651894decce37e6789a6a715a0fc7ab5b` | 27038 | DEFER | Alternative project; do not start while F-001 remains active. |
| `Business/ideas/F-001-candidate-C-provenance-kit.md` | `b35f6be7e9c5a8b64d3df3fdb539fbb67289d1ae` | 13788 | DEFER | Alternative project; no separate pipeline under one-project rule. |
| `Business/ideas/F-001-gpt-checklist.md` | `69449fceac9d4b7b5ac516318c685ec610fdd6df` | 236 | KEEP | Records GPT packaging role and Claude editorial role. |
| `Business/ideas/F-001-tam-build/build.py` | `96e4ef3b47f0f4be692337650e61c4596f58ce09` | 8500 | KEEP | Offline draft assembler, not a release gate; partial source handling needs caution. |
| `Business/ideas/F-001-tam-build/build_pdf.py` | `c029cd67c81c375a34d74ac77baaaf9fdd762524` | 2391 | KEEP | PDF review-build candidate; final render/accessibility audit outstanding. |
| `Business/ideas/F-001-tam-build/claim_scan.py` | `31f3dcff486c4c8cc96d514eb425da86834d00c3` | 3092 | KEEP | Candidate-claim worksheet; blank statuses need unconditional gate. |
| `Business/ideas/F-001-tam-build/epub_check.py` | `176d42ee19f82580702a0bfc1941b0d28932ec31` | 7122 | KEEP | Offline structural validator; explicitly not EPUBCheck/Ace substitute. |
| `Business/ideas/F-001-tam-build/listing_check.py` | `e329b64d2768deb8fe896a0ed383160c29d7481b` | 3127 | DEFER | Release authority: claim status check conditional on literal listing phrase, can be bypassed by omission. |
| `Business/ideas/F-001-tam-build/rebuild_datasets.py` | `fa3a62f76549ecaea6e226ba5cca41597000d790` | 4466 | KEEP | Recalculation helper; five numerical holds still need sign-off. |
| `Business/ideas/F-001-tam-build/ledger_map.py` | `8dd95e339b98acbce6816b9e0515d29ccdc8acc9` | 6635 | KEEP | Draft mapping utility only; no live transactions or customer data. |
| `Business/ledger/SCHEMA.md` | `1a330a172d62775fc5a708502d7bdf4ada05e310` | 1069 | KEEP | Public schema; actual figures remain private. |
| `Business/ledger/CATEGORIES.md` | `9dc5994404b20090948b5ef12f6cb6452b34d7c9` | 485 | KEEP | Categorization reference, no spending authority. |
| `Business/records/RETENTION.md` | `a303c78e739c2592f90dffdeb6991f1aacbe8e51` | 434 | KEEP | Recordkeeping template, legal retention periods not independently certified. |
| `Business/tax/CALENDAR.md` | `44dac4a981935e2f76dc5202d70fde87e0135616` | 1228 | DEFER | Tax dates and jurisdiction need current primary-source validation before reliance. |
| `Workshop/README.md` | `d39dcb35cb4ef7bdf226ded0e907a0f2d7426ab0` | 187 | KEEP | Workshop organization reference. |
| `Workshop/pipelines/P-001-budgeted-inference/README.md` | `cae451754258a855ea914be8e0cbcec316bb246d` | 4646 | KEEP | Reference specification only; no inference requested. |
| `Workshop/pipelines/P-001-budgeted-inference/reference-worker.mjs` | `e912294e5344f442de8b39f39e28930ef5092eea` | 6378 | DEFER | Executable inference Worker: prohibit activation or paid calls. |
| `Workshop/pipelines/P-001-budgeted-inference/test-worker.mjs` | `e430c4bf9538eb634103d2e0f3af9ff3c196a721` | 2553 | KEEP | Inert reference tests, not executed in this run. |
| `Workshop/pipelines/P-001-budgeted-inference/reference-bot-run.yml` | `1d643ee021cd395e509aecc35a66a46b8b0448bd` | 3564 | DEFER | Executable workflow; no autonomous Cloudflare loop or schedule activation. |

Noteworthy source-observed gap: `listing_check.py` only reads and checks `claims.csv` when the listing contains the literal phrase `each claim is marked`. Omitting that phrase can avoid the claim-ledger check. GPT has developed a separate unconditional ledger preflight in its own branch, for Claude's review. This finding is from source inspection, not a test of the unmodified shared script. The shared file remains untouched.

Next: keep F-001 as sole product, request independent Claude review of claim gate and numerical holds; do not launch any candidate B/C. Restore any DEFER by re-reviewing its pinned blob after the blocker resolves.
