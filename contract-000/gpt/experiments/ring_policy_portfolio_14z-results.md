# Issue #325 — 14Z experimental observations (POST)
Prospective issue: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/325. POST comment ID 6686582788. Source commit 3a1d9e029b292de9c5d757ed3610917d824bf901, Git blob 686daa62b71739662c1ebce639a9ac2104f3cba3. Fetched source and evaluated twice in V8, identical JSON; no CI.

| Type | Outcome | Observation |
|---|---|---|
| T1 27-tick circular closure | PASS | modular distance at 27*n ≈ 0 |
| T2 26-tick nonclosure | PASS | angular difference > 1° |
| T3 doubled step mutant | PASS | intermediate angle differs; closure alone would miss |
| T4 expiry sweep mutant | FAIL | no-expiry still records terminal expiry (41), base 42; accepted 113 vs 112 |
| T5 two-per-step queue mutant | FAIL | accepted both 112; admission timing differs |
| T6 retry-limit mutant | PASS | accepted 109 vs 110 |
| T7 drop/retry signature | PASS | drop 87 vs retry 109 |
| T8 seat assignment bias | PASS (weak) | seat-0 135/270 vs 270/270 in assignment vector only |
| T9 three-ring intervention | PASS | coupled trace differs; alignments uncoupled 0, coupled 0, shuffled 11 |
| T10 independent target | PASS (weak) | loss uncoupled 6.6875, coupled 6.75, shuffled 6.84375; no advantage |

154 synthetic grants; queue accepted 112/expired 42, retry accepted 109/dropped 45, drop accepted 87/dropped 67. Seeds 1106,1116,1124 recorded in source; only 1106 affects the shown ring trace. Not a 30-seed test. T4 and T5 oracle defects must be fixed in a prospective amendment, not retroactively counted as passes. Method deviation: JS instead of Python. No semantic learning, real gematria, external task advantage, independently measured entropy or physical precession established.
