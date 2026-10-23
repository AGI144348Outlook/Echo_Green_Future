# F-001 Run 307 — v5 report-binding gate evidence (2026-10-23)

**Pre-test prospectively published:** [Issue #26](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/26) before local execution. **Sole continuing business project:** F-001 TAM Protocol ebook; this is a read-only, unintegrated integrity proposal. Publication remains HOLD.

## Sources and exact tested bytes

- GitHub [GPT-owned proposed gate](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/23d8070dbeb2b9894195e2c1d00147a631cdb561), Git blob `7556a83ff3923528b0be5d6c419a231285cee1d3`, SHA-256 `5bc5ecc2c2bd8e3b4e7da2aedc300a98f8c8f73b7538219aa1a2500eb6378219`. Retrieved GitHub blob matched locally tested bytes exactly.
- Existing v5 parser `contract-000/gpt/business/PROPOSED-f001-disposition-binding-v5.py`, Git blob `f8c2b4b29f9fffb1bc3d65f4f1fdf56954b7a4f0`, SHA-256 `5bddfd4a4792a2fdf29d41236f5f0284d40763873cc5aaef90722719198f3372`.
- Archived public-derived Dataset A: **584 bytes**, SHA-256 `d3c176b9d2ff8041b093f46f28c7b56619d1e1cc3b3ea4841b12027e5ec826f2`, flagged CSV lines 6 and 7 (not editorial decisions).
- [GPT-owned 15-case test harness](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/588f52279a635c001ce1335d6823c4da94696d79) is now committed and also included in the Run 307 handoff archive. Verified Git blob: `60acab52956502169506a58a99293fae71ac96aa`, SHA-256 `4926deba262a8215cfc991790a86dcc87105bf577ad38d17a74c19b7f0411fd9`. The [archived public Dataset A fixture](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/28eb3a94cd4488f962d3a2cc5e40e29a67f102c7) was committed with exact original CRLF bytes (Git blob `8ef7fa41ef0229ce9a2754737f0aa0e774fd3b7b`). Local JSON results SHA-256 `4db8efda9ebebc26ccd1d23546d124064e0bbefef0d4f823c7d0c0fb825ad243`. Do not describe the harness as a repository commit.

## Method and observed outcomes (EXECUTION-VERIFIED locally)

Linux / Python 3.13.5, `python3 -I -B`, temporary directories, 5-second v5 subprocess limit and 7-second harness subprocess limit, no GitHub Actions or paid inference. Every case used a copied, hash-checked v5 source and archived public Dataset A; editorial record in the second control was **synthetic and explicitly not Timothy's decision**. The harness recorded exit code, integrity state, HOLD state, no authentication, and before/after hashes of all ordinary inputs.

**15/15 expected outcomes:**

| Case | Observation |
|---|---|
| PENDING, no editorial record | PASS / HOLD, v5 PENDING |
| Synthetic recorded dispositions | PASS / HOLD, v5 RECORDED_UNAUTHENTICATED |
| Changed Dataset A bytes | FAIL / HOLD |
| Changed v5 script bytes | FAIL / HOLD |
| Incorrect report pin | FAIL / HOLD |
| Missing report | FAIL / HOLD |
| Forged report line numbers | FAIL / HOLD |
| False report authentication claim | FAIL / HOLD |
| Three-line CSV with re-pinned report | FAIL / HOLD; actual [6,7] absent |
| Stale report after re-pinned CSV change | FAIL / HOLD |
| Duplicate JSON report key | FAIL / HOLD |
| Symlinked report | FAIL / HOLD |
| Oversized report (>1 MiB) | FAIL / HOLD |
| FIFO report without writer | FAIL / HOLD, no hang |
| Changed editorial record after report generation | FAIL / HOLD |

No unexpected exception, timeout, input modification, READY output or authenticated approval was observed. **Interpretation:** binding a stored report to fresh execution of a *fixed audited v5 script* removes the specific three-line CSV false positive from the previous receipt v3 fixture, and catches report/record drift in these local cases. This does not make the source pin independent or authorize a publication.

## Limitations / next steps

- Source and report SHA-256 are caller-supplied; an independent witness or Timothy source approval remains missing. The fixed script Git blob prevents arbitrary caller-chosen code in this proposal but does not protect against filesystem races or symlinked parent directories. This is not a security sandbox.
- No real EPUB/PDF, final Dataset B, signed editorial decisions, cross-platform run, concurrency probe or integrated four-artifact receipt was tested. The synthetic dispositions must never be treated as Timothy's.
- Claude should independently review this proposed gate and the contract for merging its output into receipt v3/v4; no GPT modification to Claude files. GPT's next step is a separately reviewed four-artifact integration, still HOLD.
- Timothy decisions remain: F-001 A1–A6/B6, lines 6/7 dispositions, licensing/credit/terms, explicit publication permission; A-000 first-anchor witness/update/recovery semantics.
