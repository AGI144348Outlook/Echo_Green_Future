# F-001 — Run 306 receipt verifier v3 test evidence (2026-10-23)

**Pre-test notice:** [Issue #25 comment 6373655780](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/25#issuecomment-6373655780), posted before local execution. No GitHub Actions or CI triggered. This is an unintegrated, read-only synthetic characterization, **not** a book release test.

## Reproducibility

- Linux 6.18.55 x86_64, Python **3.13.5**; `python3 -I -B PROPOSED-f001-test-receipt-v3.py`; subprocesses isolated with `tempfile.TemporaryDirectory`, 4-second timeout, no network, no paid inference.
- Source `PROPOSED-f001-receipt-verify-v3.py`: **Git blob `4aafb14298e901079428864bb57be28810bb226c`**, SHA-256 `fdae1cfba4e1238bb048d060388b9967c72d4273230ed7675ecaf3563dc55858`, 10,723 bytes.
- Harness `PROPOSED-f001-test-receipt-v3.py`: **Git blob `b67c8debf301e7f9019d8ef55b2f4cae2f296026`**, SHA-256 `2dd379f94b4c67e2f328abbb0f27855c67c52a83ab78921429b9fe0613b68bbb`, 2,414 bytes.
- Archived v2 regression harness Git blob `87c22119b884556fa08d918cc315936da0ceae49`; v2 editorial harness Git blob `0411e59ab8f788c244763d202cdfb0ea25c04afe`. Local `git hash-object` matched **all four** committed Git blobs exactly. Previous Run 305 handoff ZIP provided the archived v2 files; v3 was reconstructed from exact v2 blob and the committed six textual modifications, then blob-verified before execution.
- Fixtures: four synthetic placeholders, **not real PDF/EPUB**; temporary pin manifest and receipt; each case verifies before/after input SHA-256 equality, no stderr, no timeout, HOLD, both authentication flags false, `publication_authorization=ABSENT`, `format_accessibility_rights_verified=false`.

## Observations — EXECUTION-VERIFIED

**24/24 expected outcomes**, grouped as **10/10 regression**, **7/7 editorial**, **7/7 new strictness**. Two positive controls (`consistent`, `baseline_pending`) returned exit 0 / integrity PASS / **release HOLD**, measuring four synthetic artifacts each. All 22 negative cases returned exit 1 / integrity FAIL / **release HOLD**. No unexpected exceptions, timeouts, input mutation or stderr.

| Group | Cases and actual outcomes |
|---|---|
| v2 regression (10) | `consistent` PASS/HOLD; `missing_pdf`, `stale_a`, `wrong_commit`, `missing_script`, `false_approval`, `traversal`, `symlink`, `duplicate_json`, `forged_hash` all FAIL/HOLD as expected. |
| v2 editorial (7) | `baseline_pending` PASS/HOLD; `contradiction_no_flagged`, `unsupported_recorded`, `unsupported_claim`, `wrong_flagged_lines`, `false_editorial_auth`, `false_release` all FAIL/HOLD. |
| v3 strictness (7) | `Q1_float_lines`, `Q2_float_size`, `Q4_unknown_top`, `Q5_wrong_root`, `Q6_bool_size`, `Q7_duplicate_lines`, `Q8_unsorted_lines` all exit 1 / FAIL / HOLD as pre-registered. |

**Interpretation:** v3 closes Claude's §113 Q1/Q2/Q4/Q5 schema-hygiene gaps in these Linux synthetic cases. A PASS means byte consistency with **caller-supplied** pins, never independent source authentication or release approval.

**Limitations:** The synthetic Dataset A has only three lines, yet the receipt flags [6,7]; v3 still does not re-parse the actual CSV with the v5 parser or bind a source-pinned v5 report. The tests did not verify final EPUB/PDF, accessibility, manuscript rights, editorial dispositions, race/symlink-parent attacks or Windows portability. `Path.resolve(strict=True)` and path checks are not an atomic defense against concurrent filesystem swaps. No final source-pin trust anchor exists.

**Next:** Claude independently reviews v3 and proposes a source-pinned v5 report interface; GPT designs and tests that integration in a later prospectively noticed run. **F-001 remains HOLD**, pending Timothy A1–A6/B6, CSV lines 6/7 editorial decisions, rights/credit/terms and explicit publication approval.
