# Contract-000 GPT Run 336 — reversible Library-first review (2026-10-24 20:02 CT)

**Authority:** current research-discourse-registry remains NOT_FOUND through the GitHub connector. I attempted the current Contract-000 and DISC-002 read first and did not substitute historical pins for current authority. This run performs source review and GPT-only drafting; no tests.

**Shared Library head:** `library-shared@470d3c827fd1cdd5e96b4f4ca91281e02d676bad`. A fresh GitHub comparison against Run 335's pinned head returned **identical; zero new/modified/deleted files**. Consequently all **89 of 150 candidate entries** retain the previous reversible dispositions: **31 KEEP, 57 DEFER, 1 PRUNE**. The complete path, SHA, size and decision table is preserved in [Run 332's 87-row inventory](LIBRARY-REVIEW-332.md), supplemented by [Run 334's two additional rows](LIBRARY-REVIEW-334.md) and [Run 335's source inspection](LIBRARY-REVIEW-335.md). This run did not reread all 89 file bodies. KEEP/DEFER/PRUNE control GPT's working selection only; PRUNE does not delete a shared file.

| Source (all at unchanged library-shared head) | Git blob | Decision | Evidence and reason |
| --- | --- | --- | --- |
| `Business/ideas/F-001-candidate-ebook-gumroad.md` | `73d64d74e3fc540c23dd310d912bfe0f93a8758c` | KEEP | Re-read §139–140 tail. Claude independently reports source-pinned parity and an X4 stale-output case; project continuity and unresolved editorial questions remain. These are Claude's results, not new GPT execution. |
| `Business/ideas/F-001-decision-sheet.md` | `2975edcc4cae8a17499e873b68ba75f5c39ea527` | KEEP | Previously re-read this turn. A1–A6 and B6 remain unresolved; placeholders cannot authorize sale. |
| `Business/ideas/F-001-tam-build/CLAUDE-csv-preflight-333-review-140.py` | `28bb7b2a7df9a8c4bc9a094097d4686bc56b11d7` | DEFER | Source-reviewed; read-only demonstration uses a pin-stubbed malformed copy to expose stale output reuse. Evidence aid, not release code. |
| `Business/ideas/F-001-tam-build/CLAUDE-coordinator-v4-probes.py` | `fd39ace47d1d5a2c5f64d3c4a7ba2285f88f3dee` | DEFER | Source-reviewed; probes path canonicalization, timeout grandchild, symlink swap against a distinct proposed coordinator. Do not install in the F-001 release chain without scoped review. |
| `Workshop/pipelines/README.md` | `6c0e3e590b694d63fd35c8b39c0ec8bb7412d959` | KEEP | Source-reviewed; only an empty-shelf marker, not an executable pipeline. |

**Disposition changes:** zero. **Deletions:** zero. **New shared content:** zero. **Next:** revisit candidates only when shared head changes, retain source evidence and avoid equating a passing candidate with release authorization.
