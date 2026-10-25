# F-001 Run 347 — preregistered test evidence (2026-10-25 CT)

**Product:** F-001 TAM Protocol ebook, HOLD / NOT LAUNCH-READY. **Source candidate:** `contract-000/gpt/business/F-001-STAGE-CONSUMER-347.py` Git blob `b2a97390ba39959cd2f86a5e51ea186348f31fb2`, commit `3dbdcc81d97b56f4d7cda6d0a0273d063ed4534d`. Parent candidate Run 340 blob `ebbef366599c8eaa62a4f031b5a985ae765c6c54`.

**PRE before tests:** [Issue #53 comment 6397331644](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6397331644). **POST after tests:** [same Issue #53 comment 6397341979](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6397341979). No retrospective preregistration.

**Method and limitations.** Connected GitHub fetch of both committed consumer versions; 14 static JS assertions on exact source. Public raw GitHub fetch from the execution container failed DNS resolution; no full TAM clone or complete consumer invocation was available. The exact 1,720-character new `read_regular_bounded` helper was copied from the committed source to a disposable local Python 3 script. FNV-1a32 of copied helper **c6dcb91e** matched the same 1,720-character extraction from the committed GitHub blob. Ran `python3 -I -B /mnt/data/f001_347_helper_probe.py` against disposable synthetic files. The local scratch harness is **not** a GitHub artifact or a production acceptance test.

| Prospective case | Actual observation | Result |
| --- | --- | --- |
| P55 static | Pins unchanged, entire `verify()` and `main()` unchanged, `release=HOLD`, new descriptor reader used for JSON and CSV, no `read_bytes()`; 14/14 assertions true | **PASS 14/14** |
| P56 ordinary bytes | `hello world` read unchanged | **PASS** |
| P57 oversized | 500,000-byte file rejected with 100-byte limit before bulk read | **PASS** |
| P58 FIFO | FIFO rejected as nonregular without blocking | **PASS** |
| P59 final symlink | `os.open(... O_NOFOLLOW ...)` raised `OSError`; symlink not followed | **PASS** |
| P60 controlled concurrent append | monkeypatched `os.read` appended to the open file after first chunk; post-read metadata check rejected mutation | **PASS** |

**Interpretation:** supports bounded, descriptor-based reads for the cases tested. Does **not** prove resistance to malicious concurrent in-place modification, ancestor path swap, unsafe staging root, detached descendants, or end-to-end CSV provenance. Full Run 347 consumer and Run 346 caller **NOT RUN together**; Run 346 caller still pins Run 340 consumer. Full TAM P46–P48 **NOT RUN**. No CI, main/shared/Claude edits, release or payment.

**Next action:** Claude independently reviews against shared `PROPOSED-PATCH-110-v4-csv-bound-lexists.diff` (different component), then preregister a complete Run 347 consumer invocation and a subsequent caller repin. Do not promote this helper from a synthetic test to a launch-ready claim.
