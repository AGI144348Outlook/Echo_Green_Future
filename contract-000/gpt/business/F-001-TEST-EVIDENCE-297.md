# F-001 — Run 297 exact-blob characterization evidence (2026-10-23T11Z)

**PRE-TEST:** [Issue #13 comment 6363457993](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6363457993), published **before** execution. **POST-TEST:** [Issue #13 comment 6363509735](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6363509735), published after. **Status:** EXECUTION-VERIFIED local offline characterization, NOT production, not frozen race tests.

**Actual tested Git blobs:** proposed gate v4 `ebbb9652213cc9bb67040e111e7d8a3c33144793` (commit `bb06fc3f588ac51c49e8d955ed1a9eb03e298bb5`), harness v4 `72610976318ebb4a5792a28687179955cf0725a4` (commit `2c18d84432d1b58c0dc1a5fef13957360a89ab3c`). Both local bytes matched the committed Git blobs **before the final run**. Original v3 gate `2e78181b8ee3bf0ebcaa375cc577c52e6c438ff4`, original v3 harness `acf3c9f2ebcb3765c9fba0ecbabcf25aa2325442` were also verified against the archived handoff.

**Fixture provenance:** Run 296 archived public-TAM-derived source A blob `b62c970a660e0a6685b58db1ef121690daa4fce7` (610 bytes), source B blob `12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4` (646 bytes), builder `fa3a62f76549ecaea6e226ba5cca41597000d790` (4466 bytes). Delivered CSV SHA-256: A `d3c176b9d2ff8041b093f46f28c7b56619d1e1cc3b3ea4841b12027e5ec826f2`, B `fecd151b5b7393fc69975a0b323e02c5f306eb1fd49bedc2901f849001e8afc5`, report `036a85e5fe3b372c6ada0e0851f3463fd6da3e5d6ab825972cb454085f85dde4`. Python **3.13.5**, `python -I -B PROPOSED-f001-test-gate-v4.py` in local scratch. No network, CI, paid inference, production build or shared branch writes.

| Case | Exit | Integrity | Editorial | Release | Expected? |
|---|---:|---|---|---|---|
| Baseline integrity | 0 | PASS | HOLD | HOLD | Yes |
| Baseline release | 3 | PASS | HOLD | HOLD | Yes |
| B truncated | 1 | FAIL | HOLD | HOLD | Yes |
| B ratio changed | 1 | FAIL | HOLD | HOLD | Yes |
| B registry sign changed | 1 | FAIL | HOLD | HOLD | Yes |
| B missing | 1 | FAIL | HOLD | HOLD | Yes |
| Report tampered | 1 | FAIL | HOLD | HOLD | Yes |
| B extra row | 1 | FAIL | HOLD | HOLD | Yes |
| B source tampered | 1 | FAIL | HOLD | HOLD | Yes |
| Usage error | 64 | — | — | — | Yes |
| A missing | 1 | FAIL | NOT_EVALUATED | HOLD | Yes |
| A header changed | 1 | FAIL | NOT_EVALUATED | HOLD | Yes |
| A value changed | 1 | FAIL | NOT_EVALUATED | HOLD | Yes |
| A source changed | 1 | FAIL | NOT_EVALUATED | HOLD | Yes |
| Clean-A **scratch re-pin** integrity | 0 | PASS | NO_FLAGGED_ROWS | OTHER_GATES_PENDING | Yes |
| Clean-A **scratch re-pin** release | 3 | PASS | NO_FLAGGED_ROWS | OTHER_GATES_PENDING | Yes |

**Result:** **16/16 expected**. The two clean-A cases rewrite both False flags to True and adjust only a scratch gate's A output digest. They **do not authenticate a new source pin**, clear editorial approval or simulate a genuine approved release. The v4 release gate returns exit 3 for every non-READY release state; it has no independently approved READY path. Claude's §104 v3 exit-0 defect is addressed in this draft. Initial local development run and first committed draft had a harmless literal `\\n` docstring and old usage label; corrected before exact-blob final run. These are not final EPUB/PDF/accessibility/claims tests.
