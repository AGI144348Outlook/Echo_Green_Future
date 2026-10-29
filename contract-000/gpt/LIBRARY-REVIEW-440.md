# Run440 — Library-first reversible review (2026-10-29 ~03:55 CT)

Read before work: Contract-000 `0fbc794`, TJ R1–R7 `3ce87eb`, Claude's latest DISC-002 `ee443fb`, shared Library README `59be277`, Run439 checkpoint `e5851d0`, and the full 89-row [Run436 ledger](LIBRARY-REVIEW-436.md).

**89 inherited source-bound candidate decisions reassessed by documentary evidence:** **31 KEEP / 57 DEFER / 1 PRUNE**. The 89 individual path/blob/size/rationale records remain in the Run436 ledger; no decision was silently changed. This is **not** a fresh 89-entry tree enumeration or 89 independent body reads. Under TJ R3, PRUNE is reversible removal from an active set, never file deletion.

**Four fresh public source-body reads on `library-shared`, connector blob IDs compared to ledger:**

| Path | Current Git blob | Decision | Evidence / reason |
| --- | --- | --- | --- |
| `Business/ideas/F-001-tam-build/build.py` | `ede8da6f9e33631bd7d329f0ace5a880258fac18` | KEEP | Source says draft-only offline manuscript/CSV/optional EPUB build, explicitly not editorial approval or release. Preserve build provenance. |
| `Business/ideas/F-001-tam-build/epub_check.py` | `176d42ee19f82580702a0bfc1941b0d28932ec31` | KEEP | Proposed stdlib structural checker; its own documentation says it cannot replace independent EPUBCheck or store validation. |
| `Business/ideas/F-001-decision-sheet.md` | `2975edcc4cae8a17499e873b68ba75f5c39ea527` | KEEP | Single F-001 project, A1–A6 decisions open; historical build evidence is not authorization. |
| `Workshop/pipelines/P-001-budgeted-inference/README.md` | `cae451754258a855ea914be8e0cbcec316bb246d` | KEEP | Budgeted-inference historical reference only; not invoked, no new paid inference or Cloudflare loop. |

**Result:** all four pins match inherited ledger; zero reclassifications; zero deletions. The new Run440 source-custody wrapper is GPT-only and is **not** an automatically accepted shared Library entry. Preserve provenance and alternate versions.
