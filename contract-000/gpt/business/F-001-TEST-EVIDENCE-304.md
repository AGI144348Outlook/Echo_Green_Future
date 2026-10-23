# F-001 — GPT Run 304 read-only receipt verifier v1 test evidence (2026-10-23)

**Scope:** Sole active income project `F-001` TAM Protocol ebook; **HOLD**. This is a PROPOSED unintegrated receipt verifier, not a release. Pre-test notice posted first in [Issue #13 comment 6371503772](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6371503772). Actual results subsequently posted in [comment 6371582617](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6371582617).

## Exact tested source and environment

- `contract-000/gpt/business/PROPOSED-f001-receipt-verify-v1.py` commit `d3bb5e1dd9406e1aeb4f55c0e5ceb835babf81a4`, Git blob `696e66f79376abee6f5efed596a6c149f3c75909`, SHA-256 `36ff7d71bee3aa8a601966fdf554390bb681caf766ab27b8a8df7429493eac88`, 9,216 bytes.
- `contract-000/gpt/business/PROPOSED-f001-test-receipt-v1.py` commit `626e91f32a648af85ea585368b5c9fa75c91fad1`, Git blob `040e6b75e63df7a14d69e3c8d23ab152399f6ebe`, SHA-256 `6df22aa07a8910523273aabcc57d91acfb1a65fad8a318de4500f84837390087`, 5,398 bytes.
- Git blob IDs computed locally with `git hash-object` and independently fetched from GitHub after commit; **both match**. Linux, Python 3.13.5, `python3 -I -B PROPOSED-f001-test-receipt-v1.py`. Isolated temporary synthetic data; each verifier subprocess had a four-second timeout. No CI or paid services.

## Case-level observations (EXECUTION-VERIFIED)

| Case | Expected exit | Actual exit | Integrity | Release | Result |
|---|---:|---:|---|---|---|
| consistent four-file synthetic fixture | 0 | 0 | PASS | HOLD | PASS |
| missing PDF | 1 | 1 | FAIL | HOLD | PASS |
| altered Dataset A bytes with old digest | 1 | 1 | FAIL | HOLD | PASS |
| receipt source commit differs from manifest | 1 | 1 | FAIL | HOLD | PASS |
| missing required `build_pdf.py` pin | 1 | 1 | FAIL | HOLD | PASS |
| self-asserted `approved:true` and `release:READY` | 1 | 1 | FAIL | HOLD | PASS |
| artifact path traversal `../` | 1 | 1 | FAIL | HOLD | PASS |
| symlinked PDF artifact | 1 | 1 | FAIL | HOLD | PASS |
| duplicate-key JSON receipt | 1 | 1 | FAIL | HOLD | PASS |
| forged receipt EPUB hash | 1 | 1 | FAIL | HOLD | PASS |

**Total: 10/10 expected outcomes**, no deviation. All reports `source_pin_authenticated=false`, `approval_authenticated=false`, `publication_authorization=ABSENT`, `format_accessibility_rights_verified=false`; no unexpected stderr, tracebacks, timeouts or input mutations. The successful synthetic fixture measured four artifact hashes but its EPUB/PDF are placeholder bytes, **not valid book formats**.

## Interpretation, limitations and next action

The checker validates *consistency* of separately supplied pin and receipt records and actual file bytes, not independent authenticity of the source-pin manifest, Timothy's editorial decision or approval. A malicious actor controlling both JSON files and artifact bytes could manufacture an internally consistent PASS. No real TAM EPUB/PDF build, EPUBCheck, accessibility, PDF layout, claims, rights, source signature, Windows portability, concurrent filesystem race or final release test was performed. A nonzero result means integrity FAIL; zero still means **HOLD**, never READY.

**Next:** Claude independently review schema, parser v1 and the separation of source authority from byte consistency; agree a trusted pin witness and final receipt source map, then build and validate four genuine deliverables on an authorized non-main candidate branch. Keep GPT v5 and Claude patch stack unchanged pending review. Timothy's Dataset A lines 6/7 editorial dispositions and F-001 A1–A6/B6 and explicit publication authorization remain blockers.
