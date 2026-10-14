# Contract-000 — ChatGPT Library-first review, Run 072

Source: `library-shared` @ `f6ecce6f75ab649a4870a306cf761bd3b7a2148e` (2026-10-13 America/Chicago). Each row's SHA is a Git blob fingerprint from `fetch_file`, not a calculated SHA256. Classification means registration/working-set selection, **not permission to execute**. R3: no deletions; all shared source files untouched. All decisions independently reasoned by ChatGPT. Evidence state: SOURCE-OBSERVED; no runtime tests in this review.

| Source path | Blob SHA | Decision | Evidence and reason |
|---|---|---|---|
| `Business/ideas/F-001-tam-build/build.py` | `96e4ef3b47f0f4be692337650e61c4596f58ce09` | **KEEP** | Draft assembler; read-only TAM input, writes outside repository; reproducibility and publication still gated. |
| `Business/ideas/F-001-tam-build/build_pdf.py` | `c029cd67c81c375a34d74ac77baaaf9fdd762524` | **KEEP** | PDF builder and report; page count uses raw PDF regex, requires independent page verification before release. |
| `Business/ideas/F-001-tam-build/claim_scan.py` | `31f3dcff486c4c8cc96d514eb425da86834d00c3` | **KEEP** | Regex flags strong claims and emits blank-status worksheet; cannot itself establish evidentiary truth. |
| `Business/ideas/F-001-tam-build/epub_check.py` | `176d42ee19f82580702a0bfc1941b0d28932ec31` | **KEEP** | Offline structural EPUB checks; explicitly not EPUBCheck or full accessibility audit. |
| `Business/ideas/F-001-tam-build/ledger_map.py` | `8dd95e339b98acbce6816b9e0515d29ccdc8acc9` | **DEFER** | Preserve as dataset; export CSV columns and private ledger destination not verified; never process customer data publicly. |
| `Business/ideas/F-001-tam-build/listing_check.py` | `e329b64d2768deb8fe896a0ed383160c29d7481b` | **KEEP** | Offline listing-vs-build and unresolved-claims checks; source contents do not authorize listing publication. |
| `Business/ideas/F-001-tam-build/rebuild_datasets.py` | `fa3a62f76549ecaea6e226ba5cca41597000d790` | **KEEP** | Parser reconstructs A/B from copied text and reports numeric recomputations; source percentages require editorial sign-off. |
| `Workshop/pipelines/P-001-budgeted-inference/README.md` | `cae451754258a855ea914be8e0cbcec316bb246d` | **KEEP** | Documents budgeted-inference pipeline, inputs, outputs, limits and audit checklist; historical deployment claims not rerun. |
| `Workshop/pipelines/P-001-budgeted-inference/reference-bot-run.yml` | `1d643ee021cd395e509aecc35a66a46b8b0448bd` | **DEFER** | Workflow has contents:write and external /think invocation; retain evidence but do not execute or deploy. |
| `Workshop/pipelines/P-001-budgeted-inference/reference-worker.mjs` | `e912294e5344f442de8b39f39e28930ef5092eea` | **DEFER** | Contains live model-inference path and cost assumptions; no inference permitted this run. |
| `Workshop/pipelines/P-001-budgeted-inference/test-worker.mjs` | `e430c4bf9538eb634103d2e0f3af9ff3c196a721` | **KEEP** | Mocked offline worker test; useful as nonproduction test reference, not a live budget proof. |

Totals: 8 KEEP, 3 DEFER, 0 PRUNE. This pass samples 11 current shared Library entries, not the entire Library. `DEFER` means promotion/execution unresolved; source remains intact and referenceable. Restore path: revisit source tuple and resolve stated concern, then add a new dated decision (do not erase this record).
