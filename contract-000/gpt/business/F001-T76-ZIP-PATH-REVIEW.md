# F-001 T76 — ZIP preflight correction proposal (not executed)

Project: **F-001 TAM Protocol ebook**, sole income project; status **HOLD / NOT LAUNCH-READY**.
Owner: GPT packaging; Claude editorial/rights. No release authorization.

## Source observation
`contract-000/gpt/business/f001_epub_zip_preflight_t74.py` blob `561f5f3ce11edb0c64042063d4fcb5a33a15ccd3` contains the condition `"\\\\" in name` in the ZIP path check. This tests for **two consecutive backslashes**, not any backslash. A single backslash could therefore be admitted if the other checks pass. This is source inspection only, not an executed exploit or validated defect.

## Proposed minimal patch (not applied to original)
Replace the double-backslash substring check with a single-backslash membership check, i.e. Python source `"\\" in name`, and preserve other rejection logic. Also add an explicit archive member count/size budget and directory-name cases to exact-source fixtures already preregistered in Issue #465.

## Prospective test requirements before execution
Post an amendment to Issue #465 **before** any diagnostic, benchmark or fixture execution. Run exact fetched source (pinned blob), a patched candidate on a GPT-owned path, and at least: valid minimal EPUB, one-backslash name, two-backslash name, ../ traversal, duplicate, directory, oversize member, compression ratio, wrong mimetype, and nonfirst mimetype. Record Python version, SHA-256 of executed bytes, expected vs observed outcomes, exception types, limitations and any divergence. Do not equate ZIP preflight with EPUB 3.3 conformance or security certification.

## Release acceptance
Integrate independent container/OPF/spine validator, inspect delivered PDF, accessibility and Android reader QA, confirm manuscript/editorial and licensing/rights A6, and obtain explicit Timothy publication admission. Remain HOLD until all pass.
