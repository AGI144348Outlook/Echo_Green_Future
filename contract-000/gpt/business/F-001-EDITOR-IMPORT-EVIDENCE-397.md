# F-001 — Run397 offline editor import hardening and limits

**Sole project:** F-001 TAM Protocol ebook. **Status:** HOLD / NOT LAUNCH-READY. **Pre-test and post-test:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/70. **Parent:** [Run396 editor](F-001-OFFLINE-EDITOR-396.html) (unchanged). **New draft:** [F-001-OFFLINE-EDITOR-397.html](F-001-OFFLINE-EDITOR-397.html).

## Problem and change

The Run396 45-card worksheet checked project, source commit, release_authorized=false, card count and occurrence id/blob/number, but accepted arbitrary schema/release-status strings, did not verify the `source_file` field, and silently normalized invalid decision/rights values on import. An import could also overwrite existing local draft entries without an explicit warning. None of these was a release authorization bypass (exports still say HOLD), but they are integrity and user-work preservation gaps.

Run397 keeps the same 45 source-bound occurrences and v396 JSON schema for backward compatibility. It **rejects** imports with wrong schema, non-HOLD status, release authorization, wrong source commit, mismatched source file/blob/sentence number, duplicate/missing IDs, unknown decision/rights, non-string or extra draft fields. It warns before replacing nonempty local drafts and allows cancellation. **The v396 localStorage key is preserved** so saved local drafts are not silently stranded by upgrading the worksheet. No new rights or editorial status is conferred; export remains `release_authorized:false`, `release_status:HOLD`.

## Executed checks

Connector-side V8 evaluation of the embedded committed JavaScript, with `document` absent (no browser rendering), verified **16/16** controls on final blob `7da6d43f42618ae915adb9f1fda216890a635674`: 45-card baseline, full export/import roundtrip, 13 tamper-negative cases (schema, release status, release flag, source commit, source filename, blob, sentence number, duplicate ID, invalid decision, invalid rights, non-string reviewer, extra draft field, missing card), and preservation of v396 draft key/import warning. Original initial edit passed 15 controls; during review, an overbroad import-warning predicate was corrected and a mistaken v397 storage-key change was reverted; final committed version was re-fetched and rechecked. **No actual Android browser test, user draft import, or release packaging was performed.**

## Actual-source Python scanner blockage

Attempted read-only HTTPS retrieval of the public TAM README from `raw.githubusercontent.com` in the isolated local Python environment; `urllib.request.urlopen` failed with `URLError: [Errno -3] Temporary failure in name resolution`. A separate download route was unavailable. Therefore the original `claim_scan.py` was **NOT** executed against the eight actual TAM files. The prior Run393 eight-file connector-side JS parity result (42 baseline occurrences) remains separately evidenced; do not re-label it as Python execution.

## Acceptance, next owner and limitations

All **45 editorial cards remain UNREVIEWED**, including 18 P1 proposals. The HTML tool is a HOLD-only preparatory draft aid, not a rights, evidence, accuracy, citation or publication checker. A synthetic validation success cannot certify content. Next GPT action: materialize all eight pinned source files in a Python-accessible environment, run exact original `claim_scan.py` via the Run395 pinned runner and verify all 42 baseline rows and source SHA-256 digests; then complete the 334→344→347→351 staging with positive and tamper-negative HOLD-only cases. Next Claude action: independent P1 evidence/rights review and duplicate-occurrence reconciliation. Timothy still decides A1–A5/B1/B4/B6/C1, rights/editorial disposition and publication authority. No second income project, account, outreach, spending, payment or release.
