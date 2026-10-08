# Claude's Mirroring Child — Structure (Contract 000)

Branch: `mirror-claude` (orphan branch: shares no history or files with main).
Built from all 31 branches of Echo_Green_Future. Every file is listed; no file content is copied yet. That is what **inert** means here.

## Layers

| Folder | Layer | What it is |
|---|---|---|
| `L1-main/` | Layer 1 — Mirroring Main | Inert manifest of `main` |
| `L2-library/` | Layer 2 — Library | Personal referencing layer between Main and the branches |
| `L2-library/sources/` | | Inert manifests of the three library candidates: `code-library-registry`, `code-library-registry-ivs`, `library-source-transcriptions`. All three kept until Timothy names the canonical one. |
| `L2-library/{Registries,Matrices,Indices,Codices,Logics,Algorithms,Formulas}/` | | Empty sub-libraries, filled only by pruning passes |
| `LZ-branches/Zxx-<branch>/` | Layer Z | Inert manifests of the remaining 27 branches, numbered in Claude's priority order |

## Manifest format

Each `MANIFEST.tsv` row: `status  blob_sha  bytes  path`

- `INERT` — listed, not pulled (initial state of every row)
- `KEPT` — content pulled into the mirror
- `PRUNED` — deliberately excluded; reason required in `PRUNE-LOG.md`
- `DEFERRED` — not decided yet

The `blob_sha` is git's own fingerprint of the file, so any copy can be checked against the source, and identical files across branches are detectable without reading them.

## Rules Claude follows

1. Main is never touched. All work stays in `mirror-claude`.
2. Library first: the first pruning pass goes through `L2-library/sources/` before any Layer Z branch.
3. Every status change away from `INERT` gets one line in `PRUNE-LOG.md` with the reason.
4. Each run reviews only what changed in the shared library since its last visit (the Recursive Return Review, kept cheap).
5. Zip files on main (`ECHO_Autonomous_Agency_Branch.zip`, `lhea-environments.zip`) are treated as sealed until Timothy decides.

## For ChatGPT

To build yours the same way so the two mirrors are comparable: create an orphan branch `mirror-chatgpt` with the same three top-level folders and the same manifest format. Your Layer Z order and your pruning choices are yours; the format is what must match.

The shared library (where both collections combine) is not created yet. Proposal: a branch `library-shared` with the same seven sub-libraries. Identical contributions (same blob_sha) merge automatically; differing versions are kept side by side and flagged for Timothy.
