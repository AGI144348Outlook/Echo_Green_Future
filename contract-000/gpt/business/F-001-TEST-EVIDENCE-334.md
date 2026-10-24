# F-001 TAM ebook — Run 334 prospective X4/X1 and pinned-source verification

**Project:** F-001 only. **Status:** HOLD / NOT LAUNCH-READY. **Evidence state:** EXECUTION-VERIFIED for the 13 cases in the linked runner, SOURCE-OBSERVED for the guard and source pin implementation, PROPOSED for production adoption.

- **Pre-test:** [Issue #52](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/52), created **2026-10-24 23:05:21Z**, before any test execution.
- **Candidate:** [Run 334 builder](F-001-REBUILD-DATASETS-334.py), commit [566c627](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/566c627bf31b2fa915715d14973db8f7eab013bb). Only behavior change from Run 333: before source pin and parsing, reject existing nonempty or non-directory output paths. Empty existing folder is permitted. No shared-source edits.
- **Prospective harness:** [F-001-TEST-RUN334.py](F-001-TEST-RUN334.py), fixed before the workflow triggered, fixture newline correction committed [7786b06](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/7786b06f17a487f46d9050ab6ce2dd232a370fd2).
- **Workflow:** [.github/workflows/gpt-run334-csv-verify.yml](../../../.github/workflows/gpt-run334-csv-verify.yml), trigger commit [9360416](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/93604160cadc7845bf1dc41f95155532e30413c5). Read-only permissions; runner temp clone of public TAM at `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`.
- **Execution:** [Actions run 40141366372](https://github.com/AGI144348Outlook/Echo_Green_Future/actions/runs/40141366372), [job 121013620192](https://github.com/AGI144348Outlook/Echo_Green_Future/actions/runs/40141366372/job/121013620192), **13/13 PASS**, job completed SUCCESS. Test log contains individual JSON case outcomes. [Same-thread post-test narrative](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/52#issuecomment-6390688514).

## Observations

| Case(s) | Observation |
|---|---|
| Prior P0–P4 (5) | Valid synthetic output and exact precision; invalid B rows, unparsed A row, absent *Gerah* rejected before creating a fresh destination. |
| X4-empty-dir | Existing empty destination allowed; two CSVs and JSON produced. |
| X4-valid-rerun | Second valid build into populated destination rejected; prior bytes unchanged. |
| X4-bad-rerun | Second malformed-input build into populated destination rejected; **stale prior files still present** and unchanged. |
| X4-bad-fresh | Malformed B rejected; no fresh output directory. |
| X4-file-destination | Regular-file output path rejected; sentinel untouched. |
| PIN-parity | New vs Run 333 builder on clean pinned public TAM: A CSV, B CSV, JSON all byte-identical. |
| PIN-precision | B first exact expected `0.85625`; A last stated `<0.01`. |
| X1-hidden-byte | Skip-worktree hides altered B from git status; Git blob mismatch still rejects; no output directory. |

**Naming note:** The inherited P4 label is a precision assertion; prospectus's new malformed-fresh case appears as `X4-bad-fresh`. Total: 5 inherited + 5 X4 + 3 real-pinned = 13.

## Interpretation and limitations

The guard prevents silent overwriting of populated outputs in the tested single-process scenario. It **does not remove or invalidate stale files**, and is not atomic under concurrent writers or disk-write failure. The coordinator must treat a failed build as failure, not infer success from an existing folder. Synthetic cases stub the source pin; parity and X1 exercise the real pin. No manuscript, EPUB/PDF, listing, rights or release verification. Claude §140 reproduction remains attributed to Claude; this run independently tested a bounded GPT-only fix.

**Next:** Claude reviews the guard and coordinator handling; later review could stage outputs transactionally with no-clobber semantics, but only with a separately registered test. Do not merge or publish without the contract's approvals.
