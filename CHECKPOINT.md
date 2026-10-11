# CHECKPOINT — mirror-claude (Contract 000 §15.6)

**Last run:** 2026-10-11T07:00Z (scheduled hourly run, Claude)
**Stage:** S1 — Library inventory and pick/prune (three sources as equals, §13)

## Position

| Source manifest | Rows | Decided | Next |
|---|---|---|---|
| `code-library-registry` | 872 | 816 (789 KEPT, 7 PRUNED, 20 DEFERRED) | `zenodo` done through `546302`; continue at the first INERT row (56 zenodo rows = 28 pairs left; the last INERT rows of this manifest), then `code-library-registry-ivs` |
| `code-library-registry-ivs` | 212 | 0 | after code-library-registry pass, or interleave by shared blob |
| `library-source-transcriptions` | 901 | 0 | — |

Batch 1 covered `code_library_registry/` except `modules/`. Batch 2 covered `modules/`, `Algorithms/Stress-Test-001/002` and top-level files. Batch 3 covered `Datasets/` non-catalog files (INDEX, crawler/*, state/*: 12) and the first 138 `catalog/datagov` rows (69 record pairs, ordered as in the manifest, last one `datagov/neh-grants-2010s/`; continue at the first INERT datagov row). For all 69 pairs the sha256 of the decompressed raw response equals the checksum in `record.json` (EXECUTION-VERIFIED). 4 batch-3 blobs (INDEX.md, state/runs.json, seen.json, skipped.json) differ at 86785a0: the manifest (listed at 032606a) is stale for crawler-written files; catalog record blobs matched.

Batch 4 (2026-10-11T05Z) covered the last 3 datagov record pairs and the first 72 huggingface pairs (150 rows, ending at `huggingface/salim-ingram_philosophy_quotes/record.raw.json.gz`). 75/75 raw checksums match (EXECUTION-VERIFIED). `huggingface/SciAILab_OSWorld-Science-data` (2 rows) DEFERRED: both blobs differ at 86785a0 from the manifest (record re-fetched by the crawler).

Batch 5 (2026-10-11T06Z) covered the last 9 huggingface pairs and the first 66 zenodo pairs (150 rows, ending at `zenodo/19615720/record.raw.json.gz`). All 150 blobs match the manifest at 86785a0; 75/75 raw checksums match (EXECUTION-VERIFIED); all KEPT. Zenodo keyword relevance is poor (13/66 strict, 39/66 any-word), recorded as evidence in F-001 candidate B §11; nothing pruned (Timothy has not ruled on off-topic pruning).

Batch 6 (2026-10-11T07Z) covered the next 75 zenodo pairs (150 rows, ending at `zenodo/546302/record.raw.json.gz`). All 150 blobs match the manifest at 86785a0; 75/75 raw checksums match (EXECUTION-VERIFIED); all KEPT. Relevance evidence (31 auto / 26 review / 18 drop under the §11 tiers) recorded in F-001 candidate B §12.

## Source refs read this run

| Ref | Commit |
|---|---|
| research-discourse-registry | 520f61c (unchanged since 03Z; no ChatGPT reply) |
| mirror-claude | 0364bd5 (before this run's commit) |
| library-shared | 24b8811 (before this run's commit) |
| code-library-registry | 86785a0 (unchanged) |
| code-library-registry-ivs | d880679 (unchanged) |
| library-source-transcriptions | 43612d0 (unchanged) |
| genesis-documentary | f888091 (unchanged) |
| mirror-chatgpt | 2fcac0e (unchanged) |
| contract-000-gpt-team | 358818e (unchanged; read only) |
| super-duper-octo-winner (ChatGPT, read only) | e267982 (unchanged) |

## Commits made this run

| Branch | Commit |
|---|---|
| library-shared | 7854dfd |
| research-discourse-registry | none (skipped: no ChatGPT reply since 520f61c) |
| mirror-claude | (this commit; see RUN-LOG) |
