# CHECKPOINT — mirror-claude (Contract 000 §15.6)

**Last run:** 2026-10-11T22:00Z (scheduled hourly run, Claude)
**Stage:** S2 done (first pass) and S3 started, under TJ-RULINGS R3 (S2/S3 may start with DEFERRED rows open; no deletions; PRUNED = set aside, fingerprint kept). S1 stays complete at the three unchanged Library heads (e104608, d880679, 43612d0; coverage gap 0); its 110 DEFERRED rows remain open. **S2:** all 20 `L1-main` rows decided at main e28421a (19 listed + 1 new path in `L1-main/MANIFEST-ADDENDUM-1.tsv`): 7 KEPT, 1 PRUNED, 12 DEFERRED. **S3:** Z01 `genesis-documentary` @ f888091 done (44 rows: 33 KEPT, 2 PRUNED, 9 DEFERRED), Library registration first, then the mirror manifest. 64 rows decided this run (limit 150). Next: Z02 `resh-lattice-agency`.

**Earlier stage note (21Z, superseded by R3):** S1 — Library inventory and pick/prune (three sources as equals, §13). **No INERT rows remain**, and every path at the three branch heads (e104608, d880679, 43612d0) is listed in a manifest or addendum (coverage gap 0, EXECUTION-VERIFIED). Batch 16 (18Z) decided the last 89 `Datasets/files/` rows: 30 KEPT, 59 DEFERRED. **110 DEFERRED rows remain**, all waiting on Timothy's rulings.

## Position

| Source manifest | Rows | Decided | Next |
|---|---|---|---|
| `code-library-registry` | 872 | 872 (845 KEPT, 7 PRUNED, 20 DEFERRED) | done; 20 DEFERRED rows await a re-listed manifest or a ruling |
| `code-library-registry` ADDENDUM-1 @ e104608 | 144 | 144 (85 KEPT, 59 DEFERRED) | done; 59 DEFERRED = Rapidata AI-video `.mp4` files (308 MB, integrity not re-hashed) |
| `code-library-registry-ivs` | 212 | 212 (192 KEPT, 8 PRUNED, 12 DEFERRED) | done |
| `library-source-transcriptions` | 901 | 901 (875 KEPT, 7 PRUNED, 19 DEFERRED) | done |
| `library-source-transcriptions` ADDENDUM-1 @ 43612d0 | 78 | 78 (78 KEPT) | done |
| **S2** `L1-main` MANIFEST @ 7518a58 (blobs re-checked at e28421a) + ADDENDUM-1 @ e28421a | 19 + 1 | 20 (7 KEPT, 1 PRUNED, 12 DEFERRED) | done; KEPT rows registered (6 as `main` cross-refs to Library primaries, 1 new Logics primary) |
| **S3** Z01 `genesis-documentary` @ f888091 | 44 | 44 (33 KEPT, 2 PRUNED, 9 DEFERRED) | done; registered Algorithms 12, Matrices 9, Codices 6, Logics 3, Registries 2, Indices 1 |
| S3 Z02 `resh-lattice-agency` | see its manifest | 0 | next |

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

Batch 15 (2026-10-11T17Z): compared each branch tree with its manifest (`code-library-registry-ivs` 0 new paths; the other two 144 and 78) and wrote `MANIFEST-ADDENDUM-1.tsv` (existing manifest rows unchanged). Decided 133, all KEPT: CLR-0043 Lexicon Registry (README, assessment, grammar.js, template, starter.json, build/), `symbol_registries/` (README, hebrew-index, rules snapshot), neuroplasticity design notes, 21 new catalog record pairs (21/21 raw checksums match `provenance.checksum`, EXECUTION-VERIFIED), NVE-D trials 011–063 (71 files), configuration lab + tests (9/9 unit tests pass offline, EXECUTION-VERIFIED), lab status, 3 docs/assessments, and the `nve-d-configuration-checks.yml` workflow (read in full: contents:read, tests only, no secrets or deploy, so KEPT, unlike the batch-1 DEFERRED deploy workflows). Keyword scan for personal/secret material: none. Registered: Registries 116, Algorithms 10, Logics 4, Indices 2, Codices 1. ChatGPT's run-015 eight KEEP decisions (mirror-chatgpt-root a51dca1) agree with Claude's on all eight blobs (7 decided in batch 1, `rules-snapshot` in this batch).

Batch 16 (2026-10-11T18Z) covered the 89 `Datasets/files/` rows of the code-library-registry addendum (crawler-downloaded third-party data files for 8 catalog records). Rule: KEPT when the blob is current, the catalog record declares a licence (cc-by-4.0 / apache-2.0, SOURCE-OBSERVED) and the recomputed sha256 equals the record's sha256 and any source-declared checksum (30/30 sha256 and 26/26 declared checksums match, EXECUTION-VERIFIED). 59 `.mp4` files (308 MB AI-generated video, Rapidata Sora physics set) DEFERRED: not re-hashed (crawler's own match is SOURCE-OBSERVED), pending the data-files ruling. Off-topic keyword false hits (zenodo 10357138 fort 3D model, 5408613 chromium isotopes) KEPT and flagged under the standing no-relevance-prune rule. Registered: Registries 30. ChatGPT run 016 cross-check logged: NVE-C hidden surplus (F 17 vs 16, `missing 0`) confirmed; disagreement on `mashet_candidate_registry.py` (Claude KEPT, ChatGPT DEFER) preserved.

Totals (EXECUTION-VERIFIED from manifests + addenda, 18Z): 2,207 rows; 2,075 KEPT, 22 PRUNED, 110 DEFERRED, 0 INERT. Register: 2,193 rows, 2,075 distinct primaries = 2,075 KEPT, 0 double primaries. Coverage at heads: 1,016 / 212 / 979 tree paths, all listed, none gone.

Superseded 17Z totals: : 2,207 rows; 2,045 KEPT, 22 PRUNED, 51 DEFERRED, 89 INERT. Register: 2,163 rows, 2,045 distinct primaries = 2,045 KEPT, 0 double primaries.

**Batch-8 double registrations — corrected 2026-10-11T16Z.** 51 (branch, path) pairs (42 `code-library-registry-ivs`, 9 `library-source-transcriptions`) were primary in two sub-libraries (one pair in three). The sub-library where the matching `code-library-registry` row is primary stayed primary; 52 other rows re-tagged `xref-from:<primary>` (old cross_ref kept in PRUNE-LOG, append-only; no row deleted, no decision changed). Check (EXECUTION-VERIFIED): 2,030 register rows, 1,912 distinct primaries = 1,912 KEPT, 0 double primaries.

Next S1 work (18Z): no INERT rows left. Each run: re-check coverage against the three branch heads (`code-library-registry` changes with every crawler run), list new paths in a new append-only addendum and decide them; otherwise wait on Timothy's rulings for the 110 DEFERRED rows (stale listings, Worker/deploy code, crawler state, third-party clone script, licence-unresolved modules, the 59 downloaded videos). Moving to S2 needs Timothy's call on whether open DEFERRED rows block it.

Look-ahead (corrected): the earlier "28 zenodo pairs left" was wrong; only 14 pairs remained and are now done. The 119 INERT rows left are non-catalog rows; the 46 unique to this branch (`source-transcriptions/`, `experiments/nve-d/`, `registries/mashet-candidates/`, `docs/`, `scripts/`, `source-index/`) are among them and need a real read. Tip: use `git ls-tree -r` without `-l` on this partial clone (`-l` fetches every blob and timed out).

Earlier look-ahead (EXECUTION-VERIFIED against the three manifests): of the 569 INERT rows left in `library-source-transcriptions`, 523 are blobs identical to rows already decided elsewhere (328 zenodo catalog, 176 `code_library_registry/`, 19 other); **46 are unique to this branch** (`source-transcriptions/` 10, `experiments/nve-d/` 28, `registries/mashet-candidates/` 4, `docs/` 2, `scripts/` 1, `source-index/` 1). Those 46 need a real read, not mirroring; read each before deciding, and check none is private Testament or personal material before registering.

## Source refs read this run

22Z: Library heads unchanged (git ls-remote, EXECUTION-VERIFIED); coverage gap stays 0. New since 21Z: TJ-RULINGS R1–R7 and Contract §30 (research-discourse-registry b7cbda2, 25588a8), then another Claude session's SPEC-DRAFT-001 review (fda6aee) and self-update 1/4 (a860a25), which landed while this run was working; `contract-000-gpt-team` 358818e → 2f26898 (independent income automation proposal, read only). dual-order-os 2d92938 and The-TAM-protocol d46456a read (public, read only).

Totals after this run (EXECUTION-VERIFIED): register 2,233 rows (2,193 + 7 main + 33 Z01); 0 double primaries.

| Ref | Commit |
|---|---|
| research-discourse-registry | 25588a8 at start; a860a25 before this run's commit |
| mirror-claude | 5986eef (before this run's commit) |
| library-shared | fe3edeb (before this run's commit) |
| main | e28421a (unchanged; read only) |
| code-library-registry / -ivs / library-source-transcriptions | e104608 / d880679 / 43612d0 (unchanged) |
| genesis-documentary | f888091 (unchanged; S3 Z01) |
| mirror-chatgpt / mirror-chatgpt-root | 2fcac0e / 2becf76 (unchanged) |
| contract-000-gpt-team | 2f26898 (new; read only) |
| super-duper-octo-winner (read only) | main e267982, gpt-worker-output 713fce1, echo-upstream-mirror d38d7ee, echo-governor-snapshot 561c1a0 (unchanged) |
| dual-order-os (read only) | 2d92938 |
| The-TAM-protocol (read only) | d46456a |

## Commits made this run

| Branch | Commit |
|---|---|
| research-discourse-registry | a59f64c (DISC-002 22Z: R5 scoped as race contract RC-R5) |
| library-shared | 4690539 (F-001 §15: TAM Protocol source measured; product shape) |
| mirror-claude | this commit (S2 batch 1, S3 batch 1 Z01, DUAL-ORDER-FIT.md, CHECKPOINT/RUN-LOG) |

Pending for later runs: S3 Z02 onward; DUAL-ORDER-FIT next steps (framework column, derived indices). SPEC-DRAFT-001 was reviewed by another Claude session (fda6aee).
