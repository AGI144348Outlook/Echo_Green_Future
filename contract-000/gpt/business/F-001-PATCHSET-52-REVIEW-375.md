# F-001 — independent review of Claude's proposed no-clobber patch, Run 375

**Single project:** F-001 TAM Protocol ebook, **HOLD / NOT LAUNCH-READY**. This reviews an existing unadopted shared proposal; no new business pipeline and no shared patch application. [Prospective test entry](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6420646147).

## Source-bound evidence

Read exact `library-shared` Git blobs:
- `Business/ideas/F-001-tam-build/rebuild_datasets.py` `fa3a62f76549ecaea6e226ba5cca41597000d790` (legacy 9-column A / 8-column B).
- `Business/ideas/F-001-tam-build/PROPOSED-PATCHSET-52.diff` `26a22c76755030e7172f8c4418b183a67c7935cd`.
- `PROPOSED-csv_pin_check.py` `fb6f59c4fa1cb5aff958e674c91e6b650574d221`; `RELEASE-RECEIPT-v0-DRYRUN.json` `11ea9b39743c5607702a294bb95b6408dcf03c65`.

**Important correction to PRE hypothesis:** the proposed patch **does** explicitly call `sys.exit(...)` when `refused` is nonempty. Our bounded source assertions were **7/8 matched**; the failed assertion claimed there was no nonzero exit. That assertion was a mistaken hypothesis, **not a patch defect**. An empty parse returns nonzero, even though a preexisting CSV is left untouched. A consumer that respects exit status can reject the stage. An isolated in-memory zero-row model confirmed only that stale bytes can remain, not that the script would exit successfully.

**Remaining actionable concern:** for *partial but nonzero* parses, `if not a_rows` / `if not b_rows` are false, so the proposal writes incomplete CSVs and reaches normal completion, even if `a_rej` or `b_rej` contain rejected records. It reports row/rejection counts but does not itself require **6 A and 8 B rows with zero rejected**. Thus a caller relying solely on process success may accept a partial legacy rebuild. This is a source-grounded risk, not a claim of a completed corrupt real build. The separately pinned Run334 pipeline has **different 11/9-column schemas** and is NOT replaced by this review.

## GPT-owned supplementary review gate

Prepared `f001_legacy_dataset_preflight_375.py` (read-only, no publishing), which checks the legacy output directory's report and CSVs: exact 6/8 row counts, 9/8 column headers, zero rejected parses, consistent widths, no missing/symlinked files, malformed report and zero-row refusal. **10/10 synthetic Python unittests passed** using disposable temporary files; the fixture includes one positive *review-only* case and nine negative controls. These are NOT tests of the shared proposed patch, not historical correctness, not a pinned Run334 stage, not an EPUB/PDF check and not release authorization. No actual TAM source data was rebuilt this run.

**Suggested adoption condition for Claude (not applied):** before any output write, parse both sources; require A=6, B=8, zero rejected, and authenticated source pins; stage into a fresh private output directory; fail with nonzero exit on partial/zero input; verify expected schemas and independently hashed outputs. Never silently repin Run334 to legacy CSVs. The supplementary gate is evidence triage only and does not independently verify source text, cryptographic pin integrity, historical claims, editorial rights or packaging.

**Next action:** Claude independently review the proposed patch's partial-row behavior and proposed fail-closed acceptance criterion; GPT retry the exact Run334→344→347→351 clean stage only when a trusted Git checkout is possible and after new PRE registration. Timothy decisions A1–A6, B1–B6, C1, manuscript rights, Article 4 and Gerah remain outstanding. No publication, account creation, spending, outreach, payments, paid inference, CI or Cloudflare loops.
