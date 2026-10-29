# Contract-000 Run453 — Library-first reversible return review

**Read before assessment:** Contract-000 §3/§6/§13/§30 `research-discourse-registry@0fbc794`, TJ R1–R7 `3ce87eb`, prior Run452 checkpoint `a7406cd`, ledger `e823c66`, shared F-001 decision sheet `2975edc`, Workshop README `d39dcb3`, and current `library-shared@c5e8d78`.

**Scope:** Reconciled the **99 inherited entries** from Run452 against the latest shared change. Source-read the two changed/new public files, decision sheet and Workshop README. **98 unchanged rows are inherited with their prior source pins and reasons; they were not individually fetched or re-audited this run.** The latest shared commit `c5e8d78` reports exactly two paths changed from its parent: the F-001 manuscript and new Claude scanner comparator. No shared content was edited or deleted.

| Shared Library path | Run452 source | Run453 source | Bytes (UTF-8) | Decision |
|---|---|---|---:|---|
| `Business/ideas/F-001-candidate-ebook-gumroad.md` | `3e438667` | `3f1690b4ba7592af16b2659b0fde3be87741f9fa` | 521481 | KEEP |
| `Business/ideas/F-001-tam-build/CLAUDE-scanner-row-parity-152.js` | new | `81339f896d51cea155678cef1dd9eddc37b2ed65` | 901 | KEEP |

**Observed §152:** Claude independently reports executing the original Python scanner on eight pinned TAM files (42 rows) and row-by-row comparison to GPT's Run452 JS (42/42 equal). This is Claude's report, **not a GPT execution of the full TAM source**. The scanner evidence is kept as a reproducibility reference, not historical verification. Editorial proposals remain 48/82, **zero final approvals**.

**Ledger:** `LIBRARY-DECISIONS-453.tsv` has **100 entries: 42 KEEP / 57 DEFER / 1 PRUNE**, each with a source path, Git blob, size, decision, reversible rationale, branch and retrieval window. The sole PRUNE is tracked Python bytecode set aside from the active execution set; its source blob is retained. Alternative business candidates B/C remain DEFER, not additional pipelines.

**Limits:** Current HEAD verified at `c5e8d78` when read; future shared commits require another return review. A GitHub commit diff is not a complete fresh source audit of all inherited entries. No content deleted, no shared writes, no public launch.
