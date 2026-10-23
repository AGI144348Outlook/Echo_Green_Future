# F-001 — GPT Run 303 v5 test evidence (2026-10-23)

**Scope:** Continuing sole project F-001 TAM Protocol ebook. Proposal v5 is unintegrated and read-only; **release HOLD**. This is an offline characterization, **not** final EPUB/PDF verification, editorial approval, production release or Contract-000 frozen race test.

**Prospective notices (published before execution):** Issue #13 [6370393355](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6370393355) for synthetic tests; [6370433489](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6370433489) for archived public-source-derived CSV test. No tests preceded the relevant notice.

## Inputs / method

- GPT v4 Git blob `c267639e5dbbf078a6af11e172f42965837582af`, extracted from Run 302 handoff, checked by `git hash-object` against GitHub.
- GPT v5 proposed file `contract-000/gpt/business/PROPOSED-f001-disposition-binding-v5.py`, Git blob `f8c2b4b29f9fffb1bc3d65f4f1fdf56954b7a4f0`, SHA-256 `5bddfd4a4792a2fdf29d41236f5f0284d40763873cc5aaef90722719198f3372`. GitHub blob and local reconstructed file matched before execution. v4 preserved unchanged.
- Changes: descriptor-checked nonblocking/no-follow (where available), 1 MiB+1 bounded read for CSV, `lexists` for editorial-record presence, v5 usage correction. Adapted Claude §110 proposed patch to GPT-owned new file; Claude/shared files unchanged.
- Linux Python **3.13.5**, `python -I -B`, temporary synthetic CSV/JSON and 4-second subprocess timeouts, checks for structured JSON, expected exit/status, `release=HOLD`, both authentication booleans `false`, no unexpected stderr, and input immutability. `py_compile` succeeded. No CI, network, paid inference or Cloudflare execution.
- New committed nine-case harness: `contract-000/gpt/business/PROPOSED-f001-test-v5-csv.py`, Git blob `de2aa01dd3772949ede8863f8fe5f9d2445adcc0`. The earlier v4 16-case and 7-case harnesses were copied into scratch and pointed at v5, with no test expectation changes.
- Archived public-source-derived Dataset A from Run 299 handoff: **584 bytes**, SHA-256 `d3c176b9d2ff8041b093f46f28c7b56619d1e1cc3b3ea4841b12027e5ec826f2`, previously reconstructed from TAM source commit `d46456a`; source was not independently fetched/rebuilt this run. Editorial JSON was synthetic and explicitly unauthenticated.

## Observations (EXECUTION-VERIFIED locally)

| Test family | Expected / observed | Details |
|---|---:|---|
| Adapted v4 general synthetic regression | **16/16** | valid, missing, clean, wrong pin, malformed/deep, 1 MiB boundary, record FIFO/symlink/directory/device, duplicate key, incorrect row bindings; all expected outcomes |
| Adapted v4 record IO harness | **7/7** | overlapping cases (not seven new independent cases), including record FIFO no writer, no hangs |
| New v5 CSV / symlink harness | **9/9** | baseline valid; wrong pin; CSV FIFO, directory, symlink, broken symlink, >1 MiB CSV, /dev/zero; dangling record symlink now INVALID, not PENDING |
| Archived public-source Dataset A | **3/3** | absent record → `3/PENDING/HOLD`; synthetic bound record for CSV lines **[6,7]** → `0/RECORDED_UNAUTHENTICATED/HOLD`; stale pin → `1/INVALID/HOLD` |

**Total executions:** 16 + 7 + 9 + 3 = **35/35 expected outcomes**, with overlapping scenarios across families; do not interpret as 35 distinct cases. No observed hang, unexpected traceback, stderr, input mutation, READY or authenticated result. Archived Dataset A digest remained unchanged.

**Interpretation:** The v5 proposal closes the specific §110 CSV FIFO/unbounded-read and dangling-record-symlink cases on this Linux runtime; this is robustness characterization, not a security proof. The record-file and CSV-file path policy is now consistent at the last path component. The changed behavior **rejects symlinked CSV files** even when the target bytes match a digest.

**Limits / deviations:** No deviations from the stated expectations. `O_NONBLOCK` and `O_NOFOLLOW` are platform-dependent; no Windows or concurrent rename test. `O_NOFOLLOW` does not protect symlinked parent directories. The 1 MiB Dataset A limit is F-001-specific and still a proposal, not a general-purpose CSV policy. The expected SHA-256 is caller-supplied and **not authenticated**. Archived CSV provenance was checked against prior handoff, not a fresh remote source. A passing disposition parser does not authorize publication or authenticate Timothy.

**Next:** Claude independently review v5 and the symlink policy; GPT define a separate source-pinned, four-artifact receipt integration that refuses to elevate parser exit 0 to release READY. Editorial rows 6 and 7, A1–A6/B6 and explicit publication permission remain Timothy's decisions. No shared/main edits.
