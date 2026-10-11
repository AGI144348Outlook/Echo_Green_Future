# CHECKPOINT — mirror-claude (Contract 000 §15.6)

**Last run:** 2026-10-11T15:00Z (scheduled hourly run, Claude)
**Stage:** S1 — Library inventory and pick/prune (three sources as equals, §13). **All INERT rows in the three Library manifests are now decided (batch 14).** S1 is not closed: 51 DEFERRED rows and the batch-8 double registrations (below) remain.

## Position

| Source manifest | Rows | Decided | Next |
|---|---|---|---|
| `code-library-registry` | 872 | 872 (845 KEPT, 7 PRUNED, 20 DEFERRED) | done; 20 DEFERRED rows await a re-listed manifest or a ruling |
| `code-library-registry-ivs` | 212 | 212 (192 KEPT, 8 PRUNED, 12 DEFERRED) | done |
| `library-source-transcriptions` | 901 | 901 (875 KEPT, 7 PRUNED, 19 DEFERRED) | done |

Batch 1 covered `code_library_registry/` except `modules/`. Batch 2 covered `modules/`, `Algorithms/Stress-Test-001/002` and top-level files. Batch 3 covered `Datasets/` non-catalog files (INDEX, crawler/*, state/*: 12) and the first 138 `catalog/datagov` rows (69 record pairs, ordered as in the manifest, last one `datagov/neh-grants-2010s/`; continue at the first INERT datagov row). For all 69 pairs the sha256 of the decompressed raw response equals the checksum in `record.json` (EXECUTION-VERIFIED). 4 batch-3 blobs (INDEX.md, state/runs.json, seen.json, skipped.json) differ at 86785a0: the manifest (listed at 032606a) is stale for crawler-written files; catalog record blobs matched.

Batch 4 (2026-10-11T05Z) covered the last 3 datagov record pairs and the first 72 huggingface pairs (150 rows, ending at `huggingface/salim-ingram_philosophy_quotes/record.raw.json.gz`). 75/75 raw checksums match (EXECUTION-VERIFIED). `huggingface/SciAILab_OSWorld-Science-data` (2 rows) DEFERRED: both blobs differ at 86785a0 from the manifest (record re-fetched by the crawler).

Batch 5 (2026-10-11T06Z) covered the last 9 huggingface pairs and the first 66 zenodo pairs (150 rows, ending at `zenodo/19615720/record.raw.json.gz`). All 150 blobs match the manifest at 86785a0; 75/75 raw checksums match (EXECUTION-VERIFIED); all KEPT. Zenodo keyword relevance is poor (13/66 strict, 39/66 any-word), recorded as evidence in F-001 candidate B §11; nothing pruned (Timothy has not ruled on off-topic pruning).

Batch 6 (2026-10-11T07Z) covered the next 75 zenodo pairs (150 rows, ending at `zenodo/546302/record.raw.json.gz`). All 150 blobs match the manifest at 86785a0; 75/75 raw checksums match (EXECUTION-VERIFIED); all KEPT. Relevance evidence (31 auto / 26 review / 18 drop under the §11 tiers) recorded in F-001 candidate B §12.

Batch 7 (2026-10-11T08Z) covered the last 28 zenodo pairs of `code-library-registry` (56 rows, all KEPT; 28/28 raw checksums match, EXECUTION-VERIFIED) and the first 94 rows of `code-library-registry-ivs` @ d880679 (all 94 blobs match the manifest). 80 IVS rows are blobs identical to `code-library-registry` rows and mirror that decision (same path preferred when a blob appears at several paths); `code_library_registry/INDEX.md` is KEPT here because its blob is current at d880679 (it was DEFERRED in `code-library-registry` only for a stale listing). 14 IVS-only blobs: 12 KEPT (IVS README/SOURCES, registry-formation tests 001/002 reports, inputs, outputs and `registry_former.py`; IVS variants of crawler README/keywords/schedule and WORK_QUEUE), `IVS/.gitignore` PRUNED, `IVS/bootstrap.sh` DEFERRED (clones six third-party repos). Relevance evidence in F-001 candidate B §13.

Batch 8 (2026-10-11T09Z) covered the last 118 rows of `code-library-registry-ivs` (109 KEPT, 6 PRUNED, 3 DEFERRED) and the first 32 rows of `library-source-transcriptions` (27 KEPT, 1 PRUNED, 4 DEFERRED). Every one of the 150 blobs is identical to a row decided in an earlier batch, and each mirrors that decision (same path preferred, so the MOD-0004/6/7 license snapshots stay PRUNED as in `code-library-registry` even though their blob equals root `LICENSE`). IVS blobs verified at d880679; transcriptions blobs verified at 43612d0 (manifest was listed at 4391ddc; all 32 match). KEPT rows registered in the same sub-libraries as their source rows (Registries 84, Algorithms 46, Indices 44, Codices 11, Formulas 2, Logics 1).

Batch 9 (2026-10-11T10Z) covered the next 150 rows of `library-source-transcriptions` (datagov `FEMA-0614` through huggingface `Maithili-Computational-Linguistics-Lab_maithili_poem`): all 150 KEPT. Every blob is identical to a row decided in `code-library-registry` (and verified there by raw checksum in batches 3–4); all 150 match the branch at 43612d0 (manifest listed at 4391ddc). Registered in Registries (150).

Batch 10 (2026-10-11T11Z) covered the next 150 rows of `library-source-transcriptions` (huggingface `Manojkl_Tulu-Dictionary` through `zenodo/10289404`): 148 KEPT, 2 DEFERRED. Every blob is identical to a row decided in `code-library-registry` and all 150 match the branch at 43612d0. 75/75 record pairs: raw checksum matches `record.json` on this branch (EXECUTION-VERIFIED). The 2 DEFERRED rows are `huggingface/SciAILab_OSWorld-Science-data` (record.json + raw): this branch holds the older blob that `code-library-registry` re-fetched; mirrored DEFERRED. KEPT rows registered in Registries (148).

Batch 11 (2026-10-11T12Z) covered the next 150 rows of `library-source-transcriptions` (`zenodo/10307420` through `zenodo/21645640`): all 150 KEPT. Every blob is identical to a KEPT row at the same path in `code-library-registry`; all 150 match the branch at 43612d0. 75/75 record pairs: raw checksum matches `record.json` on this branch (EXECUTION-VERIFIED). Registered in Registries (150).

Batch 12 (2026-10-11T13Z) covered the next 150 rows of `library-source-transcriptions` (`zenodo/22031681` through `zenodo/6841010`): all 150 KEPT. Every blob is identical to a KEPT row at the same path in `code-library-registry`; all 150 match the branch at 43612d0. 75/75 record pairs: raw checksum matches `record.json` on this branch (EXECUTION-VERIFIED). Registered in Registries (150).

Batch 13 (2026-10-11T14Z) covered the next 150 rows of `library-source-transcriptions` (the last 14 zenodo pairs from `zenodo/7019859`, then `Datasets/crawler|state`, root files, `code_library_registry/` assessments, artifacts and modules MOD-0001 to MOD-0005 `provenance.json`): 137 KEPT, 4 PRUNED, 9 DEFERRED. Every blob is identical to a row decided in `code-library-registry` or `code-library-registry-ivs` and all 150 match the branch at 43612d0. 14/14 record pairs: raw checksum matches `record.json` (EXECUTION-VERIFIED). Mirrored decisions; one exception by batch-7 precedent: `code_library_registry/INDEX.md` KEPT (DEFERRED in code-library-registry only for a stale listing; blob current here). PRUNED: MOD-0002..0005 license snapshots (as in code-library-registry). DEFERRED: crawler state files (5), `ECHO_Autonomous_Agency_Branch.zip`, CLR-0002/0009/0010 HTML artifacts. Registered: Registries 113, Algorithms 11, Indices 7, Codices 3, Formulas 2, Logics 1.

Batch 14 (2026-10-11T15Z) covered the last 119 rows of `library-source-transcriptions`: 113 KEPT, 2 PRUNED, 4 DEFERRED. 73 rows are blobs identical to rows decided earlier and mirror those decisions (MOD-0005 validation, MOD-0006/0007, research_papers, 35 `reviews/`; PRUNED: MOD-0006/0007 license snapshots; DEFERRED: `echo-dataset-crawler.zip`, `src/a159_cloudflare_migrator.py`, `src/index.js`, `wrangler.toml`). The 46 rows unique to this branch were read (in full or sampled, plus a keyword scan for personal or secret material: none found; all technical/research text) and KEPT: `source-transcriptions/` (TEMA spec, Mashet control surface parts 1-8) in Codices; `experiments/nve-d/` specs in Logics/Formulas, code in Algorithms, trial records in Registries; `registries/mashet-candidates/` in Registries, with the NVE-C reconciliation table as the first Matrices entry; `docs/` in Logics; `source-index/` and READMEs in Indices. All 119 blobs match the branch at 43612d0. EXECUTION-VERIFIED: `scripts/registry_former/mashet_candidate_registry.py` runs offline (stdlib, `python3 -I`, scratch copy): 93 candidates vs 96 claimed, 12 duplicate glyphs, matching NVE-C `observed_total` 93; output not committed. Registered: Registries 45, Indices 25, Algorithms 20, Codices 14, Logics 5, Formulas 3, Matrices 1.

Totals (EXECUTION-VERIFIED from the three manifests): 1,985 rows; 1,912 KEPT, 22 PRUNED, 51 DEFERRED; 0 INERT.

**Defect found this run (not yet fixed):** 51 (branch, path) pairs from batch 8 (09Z; 42 `code-library-registry-ivs`, 9 `library-source-transcriptions` Stress-Test rows) are registered as a primary row in two sub-libraries each, instead of one primary plus an `xref-from:` row. Next step: a correction pass that keeps the sub-library of the source row as primary and re-tags the other row `xref-from:` (append-only note in PRUNE-LOG; no row deleted).

Next S1 work: (1) the batch-8 correction above; (2) the 51 DEFERRED rows, which wait on Timothy's rulings (re-listing stale manifests, Worker/deploy code, crawler state, third-party clone script, licence-unresolved modules). Moving to S2 (Mirroring Sub-Repository) needs S1 judged complete; whether DEFERRED rows block that is a question for Timothy.

Look-ahead (corrected): the earlier "28 zenodo pairs left" was wrong; only 14 pairs remained and are now done. The 119 INERT rows left are non-catalog rows; the 46 unique to this branch (`source-transcriptions/`, `experiments/nve-d/`, `registries/mashet-candidates/`, `docs/`, `scripts/`, `source-index/`) are among them and need a real read. Tip: use `git ls-tree -r` without `-l` on this partial clone (`-l` fetches every blob and timed out).

Earlier look-ahead (EXECUTION-VERIFIED against the three manifests): of the 569 INERT rows left in `library-source-transcriptions`, 523 are blobs identical to rows already decided elsewhere (328 zenodo catalog, 176 `code_library_registry/`, 19 other); **46 are unique to this branch** (`source-transcriptions/` 10, `experiments/nve-d/` 28, `registries/mashet-candidates/` 4, `docs/` 2, `scripts/` 1, `source-index/` 1). Those 46 need a real read, not mirroring; read each before deciding, and check none is private Testament or personal material before registering.

## Source refs read this run

| Ref | Commit |
|---|---|
| research-discourse-registry | 520f61c before this run's commit (contract files unchanged; §3, §13, §19 re-read) |
| mirror-claude | 1db4243 (before this run's commit) |
| library-shared | a78db19 (before this run's commit) |
| code-library-registry | 86785a0 (unchanged) |
| code-library-registry-ivs | d880679 (unchanged) |
| library-source-transcriptions | 43612d0 (unchanged) |
| genesis-documentary | f888091 (unchanged) |
| mirror-chatgpt | 2fcac0e (unchanged) |
| mirror-chatgpt-root | f5c8c1b (first recorded here; GPT run-011 checkpoint, 2026-10-11 12:02Z; cites DISC-002 companion 5c94ccb, already answered) |
| contract-000-gpt-team | 358818e (unchanged; read only) |
| super-duper-octo-winner (ChatGPT, read only, via git ls-remote) | main e267982, gpt-worker-output 713fce1, echo-upstream-mirror d38d7ee, echo-governor-snapshot 561c1a0 (unchanged) |

## Commits made this run

| Branch | Commit |
|---|---|
| mirror-claude | (this commit; see RUN-LOG) |
| research-discourse-registry | 073f604 (DISC-002 short note) |
| library-shared | d96a888 (F-001 candidate C §11) |
