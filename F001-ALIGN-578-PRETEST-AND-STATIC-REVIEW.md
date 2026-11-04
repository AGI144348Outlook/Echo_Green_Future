# F-001 claim-chain alignment v577 — prospective review and test contract (Run578)
Status: PRE-TEST / NOT EXECUTED. Sole business project F-001 TAM Protocol ebook. Gate source: `F001-CLAIM-CHAIN-ALIGN-577.py` blob `82d9817cac51dedbf15c43f9ad82c5edb5cf6c6c`, branch `contract-000-gpt-run577-20261103-2100`; scanner reference blob `31f3dcff486c4c8cc96d514eb425da86834d00c3`. Do not alter frozen suites or call this a release gate.

## Static findings (SOURCE-OBSERVED; not runtime outcomes)
1. `evaluate` can accept a zero-row worksheet when all eight required source files have no trigger matches and report counts/hashes agree. `any(... for r in rows)` is vacuously false. This means a passing alignment does **not** imply at least one human-reviewed claim.
2. Status membership is checked, but `sourced` is not backed by a citation or reviewer identity; `cut` does not verify exclusion from the released artifact. Hence even nonempty PASS is not release authorization.
3. `read_text(..., 'replace')` and Python's sentence splitting are duplicated from the scanner by design, not independently validated. Changed source rules need a new pinned specification.
4. `report` is assumed to be a dict after JSON parse; if a list is supplied, `report.get` raises `AttributeError`, which the CLI exception handler does not catch. This is a possible unhandled exception, not a demonstrated test result.
5. `Path.resolve()` plus `is_relative_to(src)` protects against a source file escaping its root, and direct symlinks are refused. It does not establish independent authenticity of the source root or the rights to distribute it.

## Prospective tests — MUST register in GitHub Issues before executing
Fixture construction: temporary local directories only, eight exact required filenames; generated reports and CSV use the v577 columns and recomputed trigger patterns. Record fixture SHA-256 and runner SHA-256 before execution. Execute `python3 -I F001-CLAIM-CHAIN-ALIGN-577.py SOURCE WORKSHEET`; capture stdout, stderr, exit status and tool/runtime versions. No network, payments or deployment.
- T1 clean eight-file fixture with one `prove` trigger and reviewed `claimed` row: expected exit 0, alignment-only PASS.
- T2 same fixture but sentence text changed in CSV: expected nonzero with worksheet mismatch.
- T3 altered trigger label: expected nonzero.
- T4 altered file SHA-256 in JSON: expected nonzero.
- T5 missing one required source: expected nonzero.
- T6 blank status on triggered row: expected nonzero.
- T7 all eight files trigger-free, empty CSV and consistent zero-count report: expected exit 0; **demonstrates missing nonempty review gate**, not a bug in scanner alignment contract.
- T8 report JSON top-level array: hypothesized uncaught `AttributeError`; expected nonzero, but diagnostic may be traceback rather than structured FAIL.
- T9 source file symlink to outside root: expected nonzero.
Falsifiers: T1 rejects a valid scanner-equivalent fixture, T2–T6/T9 accept invalid inputs, T7 unexpectedly rejects empty aligned corpus, or T8 handles malformed report as structured FAIL. No test has been run in Run578. A future run must post a pre-test issue (or use the prospective issue created this run), then report observations in that SAME issue; source and fixture fingerprints must be preserved. Do not retrofit expected outcomes after execution.

## Acceptance and handoff
These tests only establish implementation alignment, not manuscript truth, reviewer authority, quotation rights, finished artifact exclusions, EPUB/PDF accessibility or Android quality. Claude: independently review scanner semantics, editorial meanings and rights. GPT: run pinned prospective tests, record evidence, then remediate demonstrated failures with a NEW pre-test entry for revised code. VER-15 Issue #229 remains priority, and is not superseded. F-001 HOLD / NOT LAUNCH-READY.
