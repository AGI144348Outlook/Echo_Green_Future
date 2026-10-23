# F-001 synthetic disposition v3 test evidence — GPT Run 301 (2026-10-23)

**Status:** EXECUTION-VERIFIED offline characterization; NOT a production build, editorial approval or release gate. **Pre-test:** [Issue #13 comment 6367846503](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6367846503) posted before execution. **Post-test:** [comment 6367896126](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6367896126) posted after execution.

**Tested source:** `contract-000/gpt/business/PROPOSED-f001-disposition-binding-v3.py`, commit `f6f09f4120c4781b454f364ef3ee2022d7f6d48b`, Git blob `aa632bf3c8144a2c8fa0308ba7fc88c8fe9a1102`. Local `git hash-object` matched this exact blob. Python 3.13.5 / Linux; local command `python3 -I -B test_f001_v3.py`; synthetic CSV and JSON in temporary folders, parser invoked as subprocess, all inputs re-read afterward for immutability. Local harness and JSON output are available in Run 301 handoff (not a committed GitHub test suite).

| Case | Expected / observed exit | Expected / observed status | Release |
|---|---:|---|---|
| Two flagged synthetic rows, complete unauthenticated record | 0 | RECORDED_UNAUTHENTICATED | HOLD |
| Two flagged rows, missing record | 3 | PENDING | HOLD |
| No flagged rows, missing record | 0 | NO_FLAGGED_ROWS | HOLD |
| 100,000 nested `[` in editorial record | 1 | INVALID (structured RecursionError) | HOLD |
| 1,048,577-byte editorial record | 1 | INVALID (size bound) | HOLD |
| Malformed JSON record | 1 | INVALID | HOLD |
| Incorrect expected Dataset A SHA-256 | 1 | INVALID | HOLD |
| Changed CSV with old expected digest | 1 | INVALID | HOLD |

**Observations:** **8/8** expected outcomes. All emitted parseable JSON; `source_pin_authenticated=false`, `decision_reference_authenticated=false`, `release=HOLD`; no stderr and no input mutation. Deep input no longer causes an uncaught exception; oversize record is rejected. No unexpected test failures. Synthetic fixture values do not represent editorial decisions.

**Interpretation and limits:** These results characterize only the above cases. Proposed 1 MiB record limit is not yet agreed by Claude/Timothy; CSV input size remains unbounded; `record_path.stat()` and `read_bytes()` are not atomic (a second length check mitigates oversize after read, not memory cost); expected digest comes from caller and is not independently authenticated. Exit 0 can mean either `NO_FLAGGED_ROWS` or `RECORDED_UNAUTHENTICATED`; consumers must check status. No final EPUB/PDF/CSV artifacts, private material, paid inference, GitHub CI or Cloudflare loops were executed. F-001 remains ON HOLD.

**Next:** Claude independently review v3, size bound and JSON error reporting. Preserve v2; agree on a separate source-pinned receipt integration before adoption. Timothy's A1–A6/B6 and two Dataset A dispositions remain open.
