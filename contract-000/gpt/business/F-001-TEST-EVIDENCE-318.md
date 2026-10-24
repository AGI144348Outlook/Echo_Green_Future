# F-001 Run 318 — prospective supplemental format tests, observed evidence

**Scope:** Sole income project **F-001 TAM Protocol ebook**. This is a synthetic, offline, read-only structural *supplement* to Run 317's smoke gate; not integrated into coordinator, not a full EPUB/PDF validator and not a release gate. Status remains **HOLD / BLOCKED**.

**Prospective notice:** [GitHub Issue #37](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/37) was created **before** local execution. Its S0–S5 predictions were not modified. Claude's G1–G6 remain independent and were prospective at the time of this run.

**Exact tested bytes:** `PROPOSED-f001-format-supplement-v1.py` Git blob `eeccb2d50b44b6075949ecf0f118263b0cf68381`, SHA-256 `7ad3417e5bb14f9e096469ff8f5545ba7e32d721380e2e23df6b696266a8fa0a`; `PROPOSED-f001-test-format-supplement-v1.py` Git blob `b5897d4d94f59ef99b082ed8c6a6b1ec2b2e56dd`, SHA-256 `4db10ae80a94980eebaf6df36b303cb4e37a98d659cfc614f30277c7a496cd8a`. GitHub `fetch_file` confirmed both blob IDs match local `git hash-object`. Python **3.13.5**, Linux, `python3 -I -B`, temporary directory, no network/CI/paid inference. No actual book artifacts.

## Observations (execution-verified locally)

| Case | Predicted | Observed | Diagnostic |
|---|---|---|---|
| S0 minimal coherent synthetic EPUB+PDF | PASS | PASS | 5 EPUB members CRC checked; PDF object markers present |
| S1 corrupt unused ZIP cover member | FAIL | FAIL | `Bad CRC-32 for file 'images/cover.jpg'` |
| S2 two casefold-colliding ZIP names | FAIL | FAIL | `casefold-colliding EPUB members` |
| S3 Unix symlink ZIP member | FAIL | FAIL | `Unix symlink EPUB member` |
| S4 fake PDF header/xref with no objects | FAIL | FAIL | `PDF has too few object declarations` |
| S5 valid synthetic PDF with 12 trailing NULs | PASS | PASS | tolerant EOF tail heuristic accepted |

**Result:** **6/6 expected outcomes**, 2 PASS controls and 4 correctly rejected malformed cases. Every output contained `release=HOLD`, `readiness=BLOCKED`, `publication_authorization=ABSENT`, `full_conformance_verified=false`. SHA-256 of both input files was unchanged before/after every check. Exit status **0**. No observed unexpected exception, timeout, or deviation from the preregistered S0–S5 cases.

**Interpretation:** This candidate detects the four tested failure classes. The CRC check covers unused assets that the earlier gate never decompressed. Rejecting casefold collisions/symlink ZIP members prevents certain unsafe extraction scenarios even though the checker never extracts. The PDF object markers prevent one trivial false-positive but **are not a trustworthy PDF parser**; forged markers, broken references, malformed content, accessibility errors, unsafe PDFs and legitimate variants remain outside this test. The EOF NUL tolerance is a documented heuristic, not a conformance ruling.

**Limits:** Synthetic fixtures only; no real TAM EPUB/PDF, no independent source pins, no signed editorial decisions, no subprocess isolation, no full EPUBCheck/PDF rendering, no rights/claims/accessibility review. The checker is not wired into coordinator-v4, and its separate PASS does not override any earlier FAIL or HOLD. No claims about malicious same-UID actors, cryptographic identity or production readiness.

**Next:** Claude independently reviews the candidate against its G1–G6 plan; if useful, a separate prospective integration test may compose it with the existing HOLD-only coordinator. Product readiness still blocked on A1–A6/B6, Dataset A rows 6/7, source/rights/credit/price, genuine deliverables, independent signoff and Timothy's explicit publication authorization. No private Testament content, shared deletions, account creation, outreach, spending or publication.
