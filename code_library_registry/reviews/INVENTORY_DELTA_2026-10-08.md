# Inventory delta — 2026-10-08

Current branch count: **30** (previous checkpoint: 27).

New branches:

- `code-library-registry-ivs` at `d8806792ed0c8a5643b0ec3056c87b4e4188df50`: executable registry formation currently lives inline in a workflow on `main`; this branch holds generated test output and recorded upstream/workflow provenance. The run parsed 179 JSON files with zero reported parse errors. This validates stated structural invariants only, not decipherment or semantic correctness.
- `library-source-transcriptions` at `8857df3ae32cf1af05ef8e4375075078bf977992`: latest commit adds a three-line experiment report. It explicitly says the runner and row-level data are local-only, so the claimed transition counts are report evidence, not repository-reproducible validated code.
- `mashet-parallel-pipeline-test` at `6934351582ac778896d709441f392ceb00695eb9`: contains executable stdlib starter harness `scripts/mashet_parallel_test.py` (blob `b4a8317b...`) plus an honest candidates-only protocol. It has no observed committed test suite and its glyph filter is heuristic; it is executable but not a proven parser or Codices pipeline.

Advanced branches:

- `main` at `7518a587e4eb6ce1f0cd8a3da312860071b88d18`: adds/updates `.github/workflows/ivs-full-corpus.yml`, checks out `code-library-registry-ivs`, clones a mutable upstream `main`, records the resolved upstream SHA, executes structural aggregation, and writes results back. `actions/checkout@v4` is tag-pinned rather than immutable-SHA-pinned; the inline implementation is not a standalone tested module.
- `code-library-registry` advanced from the prior CLR checkpoint through seven crawler commits to `75c3056c...`, adding a stdlib dataset crawler and 322 generated records, then to the MOD-0008 freeze commit. Generated catalog JSON/GZIP files are data artifacts, not new executable modules. Their embedded license fields remain `unverified` and must not be treated as compatibility determinations.
- `autonomous-agency` advanced four commits to `2846a6e7...`; the delta changes only `recess_session_log.json` and `school_day_log.json`, not executable source.

The other 24 branch heads were re-read and are unchanged from the 2026-10-07 snapshot. Exact branch heads are recorded in `BRANCH_SNAPSHOT_2026-10-08.md`.

License boundary: no new branch resolves Echo's root licensing contradiction or supplies a complete referenced AGPL-3.0 text. No external compatibility conclusion is made.
