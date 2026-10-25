# F-001 — real pinned-source dataset rebuild, ChatGPT Run 358 (2026-10-25 ~18 CT)

**One product:** F-001 TAM Protocol ebook. **HOLD / NOT LAUNCH-READY**. Continued [Run 357 source audit](../business/F-001-SOURCE-AUDIT-357.md) and the shared [F-001 decision sheet](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-decision-sheet.md). **Pre-test registered before execution:** [Issue #56](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56). No shared branch, source repository, main or Claude edits.

## Exact source and script evidence

Three files were transcribed from authenticated GitHub connector `fetch_file` results into an **isolated local scratch directory** because the container cannot resolve GitHub DNS. **Every resulting Git blob SHA-1 was computed from the actual local bytes and matched the separately fetched GitHub blob SHA** before executing:

| Local file / GitHub origin | Bytes | Git blob SHA-1 verified | Raw SHA-256 |
| --- | ---: | --- | --- |
| TAM `Dataset A: The Eshtemoa Inventory (Forensic Weight Distribution)` | 610 | `b62c970a660e0a6685b58db1ef121690daa4fce7` | `48437f58ee74a9a0226d901d1291b6c104764648fe7760ebbc91b74b6ba6a302` |
| TAM `Dataset_B_Binary_Matrix.md` | 646 | `12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4` | `bc16da657b19317e110cdcf4159a9118aa89f2cfc4f8183e7e3f1d94f2eb3b81` |
| Shared `Business/ideas/F-001-tam-build/rebuild_datasets.py` | 4466 | `fa3a62f76549ecaea6e226ba5cca41597000d790` | `77d4c8a20a1b627336552e3e1e7c85da5fd37c916d9ac3ee1d4fdf0ef73c9dbc` |

TAM commit: [`d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`](https://github.com/AGI144348Outlook/The-TAM-protocol/commit/d46456a18fe412398d0ae37ec5a8c4eebb44e0c9); Git commit tree: `5dfabe3a978e05e26528f0cb90101dd7de943f3a`. The public TAM repo was **not cloned**; the isolated snapshot consists of the two exact verified source blobs needed by this builder. The script was run as source, not imported from a modified wrapper.

## Execution and observed results

Commands (local isolated paths; no GitHub writes during execution):

```sh
python3 -I /mnt/data/contract358/rebuild_datasets.py /mnt/data/contract358/tam-source /mnt/data/contract358/run
python3 -I -B /mnt/data/contract358/rebuild_datasets.py /mnt/data/contract358/tam-source /mnt/data/contract358/run-repeat
```

Both commands exited successfully and printed `{"A": {"rows": 6, "rejected": 0}, "B": {"rows": 8, "rejected": 0}}`. Outputs from the two distinct directories were byte-identical.

| Actual generated output | Bytes | Raw SHA-256 | Git blob SHA-1 (re-fetched from GPT branch) |
| --- | ---: | --- | --- |
| [dataset-a.csv](F-001-DATASET-358/dataset-a.csv) | 584 | `d3c176b9d2ff8041b093f46f28c7b56619d1e1cc3b3ea4841b12027e5ec826f2` | `8ef7fa41ef0229ce9a2754737f0aa0e774fd3b7b` |
| [dataset-b.csv](F-001-DATASET-358/dataset-b.csv) | 588 | `fecd151b5b7393fc69975a0b323e02c5f306eb1fd49bedc2901f849001e8afc5` | `0df0e4153cf2ae9c292dd05588485e13bfd999f3` |
| [dataset-check.json](F-001-DATASET-358/dataset-check.json) | 326 | `036a85e5fe3b372c6ada0e0851f3463fd6da3e5d6ab825972cb454085f85dde4` | `0f333dd8d9a86dff947883bd41d46a585dc83c59` |

**Observed Dataset A:** four rows `stated_matches_recomputed=True`; **Silver Droplet** (`-0.03` stated versus `-0.146` computed) and **Small Scrap** (`<0.01` stated versus `-0.146` computed) are `False`. The original claims remain untouched in a separate CSV column.

**Observed Dataset B:** eight `ratio_over_16_equals_units=True`. Its `deviation_pct` includes `-0.73` for ratio 1 and `-0.146` for ratios 2 and 4. The builder **does not enforce a B mass-deviation acceptance threshold**; a true ratio/unit relationship is not proof of mass agreement or historical validity. This is a newly visible product quality boundary, not a decision to correct source data.

**Hypothesis result:** expected 6/8 parsed rows, zero rejects and two flagged A mismatches confirmed; byte reproducibility confirmed in two runs. No challenge to the narrow parsing hypothesis was observed. Wider provenance, scientific/historical claims and release remain unresolved.

## Limits and follow-up

This is execution of **the exact shared Python builder** on **the two exact public TAM source blobs**, not execution of the three-script stage coordinator, a full TAM checkout, manuscript editor, EPUBCheck/Ace, PDF verification, or independently witnessed release. Git blob matching establishes byte identity to the fetched GitHub objects, not the source's scientific truth or Timothy's publication authorization. The generated CSVs are **draft research evidence only**, not a saleable product or independently signed attestation.

**Next GPT task:** integrate these actual CSV bytes into the previously developed HOLD staging/manifest checks, with a new prospective test entry before executing any additional diagnostics; independently review whether B mass-deviation should be reported as a separate warning without inventing a threshold. **Claude complementary task:** editorial disposition for the two A deviations, Gerah ambiguity, rights, ~35 claims and listing; challenge any conflation of B ratio checks with measured mass. **Timothy blockers:** A1–A6, B6/C1, editorial corrections, credit/licence, book ID and publication approval. No outreach, account creation, spending, payment, paid inference or Cloudflare loops.
