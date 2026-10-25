# F-001 — Run 346 prospective test and observations (2026-10-25 ~06 CT)

**Pre-test published BEFORE execution:** [Echo_Green_Future Issue #53, PRE comment 6396820036](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6396820036). This is one bounded development iteration of **F-001 TAM Protocol ebook**, not a new project. Release status **HOLD**.

**Actual source:** GPT-only `F-001-STAGE-SESSION-346.py` Git blob `95070b6e4de93974cf263353aec2d7d2a65e30cd`, committed at [a91161b](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/a91161b4bd58b9f87f4fd66f170a4c117f7964b8). Inherits Run 345 gate pin `5d5bb8f`, consumer pin `ebbef36` and unchanged `main()`. Replaces unbounded temporary-file child output spooling with `selectors.DefaultSelector()` + `subprocess.PIPE` + incremental `os.read` with `MAX_CAPTURE=16384` bytes per stream. On any over-limit, timeout or error, finally kills the same POSIX process group.

**P49 committed-source static observations:** Connected GitHub read fetched the committed Run 345 and Run 346 blobs. **10/10 PASS**: 40-hex committed blob; identical `main()` bodies; unchanged exact gate/consumer pins; selector+pipe and no `TemporaryFile` in helper; cap checked during read; finally cleanup; unchanged `release=HOLD` and `CONSISTENT_CURRENT_INVOCATION` fields; new imports; helper text matches synthetic test copy by FNV-1a 32-bit `0x9c31e568` over 2313 trimmed characters. FNV here is an accidental-mismatch check, not a cryptographic signature. No entire caller integration was executed.

**P50–P54 synthetic helper-only execution:** Local disposable `/mnt/data/f001_run346_helper_probe.py`, invoked `python3 -I -B /mnt/data/f001_run346_helper_probe.py` (Linux, Python 3.13.5). The test contains the exact extracted `run_checked()` helper text (FNV matched) plus `reject` and `kill_process_group` helpers and synthetic `python -c` children. It does **not** run the committed caller `main()`, real TAM builder, gate or consumer. No CI triggered.

| Prospective case | Observed result | Outcome |
| --- | --- | --- |
| P50 normal output | exit 0; stdout `hello`, stderr `warn`; ~0.923s | PASS |
| P51 stdout flood | 2,000,000-byte writer rejected `ValueError: child output exceeds per-stream capture bound` at ~0.541s, before 3s sleep | PASS |
| P51 stderr flood | same rejection at ~0.737s | PASS |
| P52 nonzero child | exit 7 preserved; ~0.676s | PASS |
| P53 timeout | 2s sleeper, deadline 0.2s; `TimeoutExpired` at ~0.204s | PASS |
| P54 inherited pipe | same-session grandchild; leader exit 0, helper returns ~0.803s; delayed marker absent after 1.4s | PASS |

**Observation vs interpretation:** 10 static assertions and 6 synthetic helper checks passed. This supports only the *specific* output-capture boundary and same-session cleanup in this environment. It does **not** prove full Run 346 caller integration, the gate's nested builder, final CSV hashes, stage-file disk quotas, detached grandchildren, race-free source reads, hostile filesystem handling, accessibility or publication readiness. The earlier P46–P48 actual pinned-TAM integration cases remain **NOT RUN** because the local shell cannot resolve `raw.githubusercontent.com`/GitHub; a direct download attempt returned `Temporary failure in name resolution`. No synthetic substitute was presented as full integration.

**Next:** Claude independent review of the new capture helper and any diagnostic loss; then a separate disposable real pinned TAM clone/gate/consumer integration under the already prospective P46–P48 or an Issue amendment if the method changes. Post actual results in the same Issue. F-001 rights, manuscript, claims, EPUB/PDF, receipts and Timothy publication decisions remain HOLD. No paid API inference, Cloudflare loops, main/shared writes, spending or outreach.
