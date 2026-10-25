# F-001 Run 348 — pre-registered integration evidence (2026-10-25 CT)

**Single project:** F-001 TAM Protocol ebook. **HOLD / NOT LAUNCH-READY.**

**Prospective record:** [Issue #53 PRE-TEST](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6398028172) was published before the code checks and attempted execution. **Actual follow-up:** [Issue #53 POST-TEST](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6398036642).

**Input refs:** prior GPT Run 347 `0270f121f1a710dde6f5eccee28410230005283f`; caller 346 blob `95070b6e4de93974cf263353aec2d7d2a65e30cd`; consumer 347 blob `b2a97390ba39959cd2f86a5e51ea186348f31fb2`; gate 344 blob `5d5bb8f85db7f21c50ca71625e82c51102fed088`.

**Changed artifact:** [F-001-STAGE-SESSION-348.py](F-001-STAGE-SESSION-348.py), blob `19942fc04c46d3caf5a68f6ebf7fb9a52dbfc21b`, commit [b1e14c6](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/b1e14c6b776712467d6f9606c4371de0fd2f2668). Three lines changed from Run 346: two documentation lines and the consumer pin.

| Prospectively specified check | Observed result | Method / limit |
| --- | --- | --- |
| P61 exact expected delta | **PASS** | GitHub-connected fetch of both committed callers, JS line-by-line comparison; exactly 3 expected lines differ. |
| P62 consumer blob pin | **PASS** | Pin equals GitHub-connected Run 347 consumer blob SHA exactly. |
| P63 gate pin / caller logic / HOLD / resource bounds | **PASS (6 source assertions)** | Connected gate blob match, byte-identical `main()` and `run_checked()`, fresh stage, HOLD, timeouts and bounded consumer helper. |
| P64 Python syntax / full fail-closed synthetic smoke | **NOT RUN** | Execution container `urllib.request.urlopen(raw.githubusercontent.com)` failed: `URLError [Errno -3] Temporary failure in name resolution`. No executable source obtained. |
| P65 real pinned TAM integration | **NOT RUN** | Same DNS blockage; no verified real stage fixture available. |

**Total actual checks:** **8/8 source-level assertions PASS**; **zero Python runtime tests**. A static match is not a valid end-to-end result.

**Remaining risks:** Run 347 consumer has not passed a complete positive-path stage; `pin_script()` in caller checks file bytes before invoking the same pathname, leaving a potential time-of-check/time-of-use swap in a writable directory; the descriptor-based consumer still relies on a private stable staging root and cannot prevent hostile ancestor replacement or same-metadata in-place tampering. No production/shared promotion or release permission is implied.

**Next independent check (requires its own PRE-TEST):** execute full consumer with pinned real or deterministically built valid stage, negative swapped/malformed stage, and exact caller gate/consumer subprocess binding; verify release stays HOLD and the receipt cannot be replayed. Ask Claude to review the pin transition and its own F-001 §140 X4 stale-output observation. No CI, publication, account, spending, paid inference or autonomous Cloudflare loops occurred.
