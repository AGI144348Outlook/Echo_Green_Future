# Mashet simultaneous pipeline test
Branch: `mashet-parallel-pipeline-test` (from `dev-suite-datasets`).
Two isolated runs are launched concurrently; reconciliation runs after both finish.
A: glyph-only heuristic structural extraction, no meanings.
B: source-line preservation with category context; candidate status only.
C: provenance and comparison metadata; **no promotion** to DSL, matrices, or codices.
Run: `python scripts/mashet_parallel_test.py mashet_source.txt`
The original PDF should be retained unchanged. Extract a UTF-8 text copy separately.
Important: the harness is a starter, **not** the existing IVS registry former or a proven full Datasets→Codices implementation. Verify the glyph extraction before trusting results. Keep §DSL§ inversion separate.
