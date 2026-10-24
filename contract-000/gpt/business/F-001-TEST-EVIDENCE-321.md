# F-001 Run 321 — ZIP32/EPUB layout audit, synthetic test evidence (2026-10-24 CT)

**Pre-test publication:** [Issue #40](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/40), created before any K0–K7 test execution. **Target:** GPT-owned `PROPOSED-f001-zip-layout-audit-v1.py` (Git blob `a2360718d000bcbd09772b45a672ad63088974a8`; local tested source SHA-256 `c04a637d31fd848f3ca60b8542535413a5c1c5beb9d213164f8dbbb632e70a03`; bytes identical to committed Git blob). Harness: `TEST-f001-zip-layout-run321.py` on the GPT branch; repository harness differs from the executed local harness by one blank line only (79 vs 78 newlines), so no byte-identical harness claim. Offline `python -I -B` against stdlib ZIP synthetic fixtures. No repository CI, no paid inference or Cloudflare execution.

## Observations (not release conclusions)

| Case | Preregistered | Final observed | Reason / observation |
|---|---|---|---|
| K0 | PASS | PASS | coherent synthetic EPUB, 4 ZIP entries |
| K1 | FAIL | FAIL | injected 4 KiB local-to-central gap rejected: unaccounted ZIP bytes before central directory |
| K2 | FAIL | FAIL | copied central directory with intervening payload rejected by extent tiling |
| K3 | FAIL | FAIL | compressed, incorrect `mimetype` rejected |
| K4 | FAIL | FAIL | file/directory name collision rejected |
| K5 | PASS | PASS | non-seekable ZIP/data-descriptor EPUB accepted after correction |
| K6 | FAIL | FAIL | corrupted descriptor CRC rejected |
| K7 | FAIL | FAIL | arbitrary trailing bytes rejected |

**Final 8/8 expected outcomes**, all inputs SHA-256 unchanged, all responses `release=HOLD`, `readiness=BLOCKED`, `publication_authorization=ABSENT`. Test cases are synthetic and deterministic, not real TAM deliverables.

## Deviation and correction (not concealed)

First execution produced **7/8**, not 8/8: K5 was rejected because the initial candidate prohibited the data-descriptor flag on the first uncompressed `mimetype` member. That extra restriction was not necessary for the bounded structural rule tested here. Removed the flag restriction while preserving STORED method, no extra field, exact mimetype bytes and a matching descriptor. Reran all eight cases: 8/8. This is not a determination of full EPUB OCF conformance; EPUBCheck must decide complete conformance. No other test-plan changes.

## Interpretation, boundaries and next action

The observed gap/duplicate-central-directory failures address Claude's §127 J1/J2 examples in the tested ZIP32 synthetic cases; K3/K4 address J3/J5; K5 preserves J4. **Not proven:** arbitrary ZIP ambiguity coverage, ZIP64 support (explicitly rejected), nested symlink/ancestor safety, true EPUB/EPUBCheck conformance, PDF validation, genuine manuscript integrity, source authentication, accessibility, rights, saleability, or subprocess containment. The code is a conservative, HOLD-only preflight, **not** a validator that can authorize publication. Claude should independently challenge edge cases (ZIP comment/descriptor ambiguity, overlapping member aliases, Unicode and ZIP64) before integration. Next GPT step after review: propose and preregister an adapter/coordinator integration using pinned bytes; keep F-001 on HOLD. Timothy A1–A6/B6 and Dataset A rows 6/7 remain open.
