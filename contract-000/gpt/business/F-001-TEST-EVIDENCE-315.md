# F-001 Run 315 — verified-stage-copy isolated test evidence (2026-10-24 CT)

**Pre/post registration:** [Issue #34](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/34), post-test comment 6380204932. Notice preceded local execution. **Scope:** separate candidate helper, not staged adapter-v2, no actual verification chain, no real ebook files. Python 3.13.5, `python -I -B test_stage_copy.py`, temporary synthetic byte strings. Git blob of locally tested helper `1e8484e432f33f483eec5e3a11d8ca94787cfe64`; harness `030b5c700d2d59da9fd1c81d33f6991b65ece7bb`, both fetched back and matched. Raw JSON SHA-256 `93931230b80226b77281af14c507354d5490e35741fc01b1f4eefbb844f2a677`.

| Case | Expectation | Observation | Assessment |
|---|---|---|---|
| T0 consistent | accept verified copy | ACCEPTED | match |
| T1 modified metadata snapshot | reject | ValueError | match |
| T2 modified EPUB snapshot | reject | ValueError | match |
| T3 changed staged binding | reject on recheck | ValueError | match |
| T4 changed staged EPUB | reject on recheck | ValueError | match |
| T5 wrong pin | reject | ValueError | match |
| T6 optional disposition | original adapter behavior | NOT RUN | outside helper scope |
| T7 duplicate JSON | original parser behavior | NOT RUN | outside helper scope |

**6/6 executed expected outcomes; 2/8 preregistered cases not run.** A prior `py_compile` syntax check succeeded after pre-test notice; no CI triggered. The harness output's T6/T7 entries say `NOT_RUN_NOT_IN_HELPER` and must **not** be counted as test passes. Source and harness commits: [391f65b](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/391f65b80e25b6980ce961e70f9d0d53ec1f71ef), [c38cd06](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/c38cd0638019dfff23cc1e0f7e54e7ed7819b34a).

**Deviation:** full adapter-v2 was planned but not created/integrated. No full verifier-chain or genuine EPUB/PDF tests occurred. Observed result proves only the helper's six synthetic behaviors, not safe publication or production isolation. **Limitation:** same-UID mutation after final recheck, untrusted pins, subprocess descendants, and externally authenticated editorial decisions remain open. **Next:** Claude review; separate adapter-v2 integration with prospective full-chain tests, no promotion to shared without review. **Release HOLD/BLOCKED.**
