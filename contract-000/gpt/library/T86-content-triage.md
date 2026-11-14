# T86 Library-first content review — 2026-11-14

Source branch `code-library-registry`; read-only. Previous T85 metadata inventory: 150 provisional candidates (75 KEEP,75 DEFER); this pass reviews **four content-bearing candidates**, not 150 new files. All decisions non-destructive and subject to rights/provenance.

| Source | Blob SHA | Decision | Content evidence and reason |
|---|---|---|---|
| `Algorithms/Stress-Test-001/README.md` | fetched in T86 | KEEP | Explicitly distinguishes definitions from authority and registration from execution; essential safe registry test specification. |
| `Algorithms/Stress-Test-001/MANIFEST.txt` | `271c660294a8dc70d45f4e34eeec2347c3db6d32` | KEEP | Enumerates glyph and neuroplasticity inputs and excludes benchmark from ingestion; retain as provenance gate. |
| `Algorithms/Stress-Test-001/benchmark/EXPECTED.md` | `5ceb8cbfc37ab5c251e2a4753df257e962a44889` | DEFER | Useful sealed evaluation criteria, but MUST remain out of ingestion and training material; not eligible for live registry promotion. |
| `Algorithms/Stress-Test-002/EXPECTED.md` | `1739dc7ec3c062b279cb0e93a528c03af80c4bb8` | DEFER | Losslessness/uncertainty benchmarks; evaluation-only to prevent answer contamination; requires rights and scope review. |

**Totals 2 KEEP / 2 DEFER / 0 PRUNE.** Shared Library README blob `59be277fef1c9fc830c23de1a3fe3fe0b72ec7ce` read; it says the shared Library is inert until authorized population. No shared content deleted or copied into it. T85 150-row inventory overlaps these four and must be deduplicated; do not count as four distinct additional candidates.

Gates: complete original inventory, content-level reviews, source/license provenance, deduplication and seven-sub-library classification. The full governing Contract-000 and canonical DISC-002 files were not freshly located by path in this pass; T85 checkpoint and current issue discussion were read. No claim of complete Library gate.
