# F-001 CLAIM-CHAIN-ALIGNMENT-575 — preregistration draft (NOT EXECUTED)
Project: F-001 TAM Protocol ebook. Source baseline: F001-CLAIM-CHAIN-GATE-573.py blob 9d1602314b0a963d7ddc04c9bf355da8f925fdba; current shared claim_scan.py historically pinned 31f3dcff486c4c8cc96d514eb425da86834d00c3. This is an acceptance specification, not a frozen test suite, passing result, or publication permission.

## Required mechanism
Recompute from the **exact pinned scanner implementation and complete declared FILES list**, using verified manuscript source bytes, a deterministic ordered sequence of (file, sentence_no, sentence, normalized trigger set). Do not accept the report's source_files list as authority. Independently compare SHA-256 of every source; compare one-to-one worksheet rows by the full key including trigger set, not merely row count. Compare report rows, per_file and per_trigger to recomputed counters. Reject unknown/duplicate worksheet rows, missing sources, missing rows, altered sentence, changed sentence index, changed trigger set, invalid review status, unregistered source file, and stale report. Reject any symlink or path that resolves outside the pinned source root. Keep reviewer identity/approval, source rights, cuts in built output and artifact provenance as separate HOLD gates. A PASS in this gate only means scanner-to-worksheet structural correspondence.

## Prospective falsifiers (not yet executed)
| ID | Fixture | Expected |
| --- | --- | --- |
| C0 | Pinned source and scanner-generated report/worksheet with valid statuses | PASS alignment, RELEASE HOLD |
| F1 | Source bytes changed, worksheet unchanged | FAIL source digest |
| F2 | Report omits one required FILES entry | FAIL missing declared source |
| F3 | Worksheet drops one row, adjusts report counts | FAIL missing recomputed row |
| F4 | Worksheet inserts invented row, adjusts counts | FAIL surplus row |
| F5 | Worksheet swaps two sentence texts, keeps row counts | FAIL exact correspondence |
| F6 | Worksheet changes sentence_no only | FAIL index mismatch |
| F7 | Worksheet changes trigger labels, keeps sentence | FAIL trigger mismatch |
| F8 | Report per_trigger counter forged | FAIL recomputed trigger totals |
| F9 | Worksheet duplicates a real row, adjusts counts | FAIL duplicate/surplus |
| F10 | Worksheet contains blank or unsupported status | FAIL unresolved editorial status |
| F11 | Source path is symlink escaping root | FAIL containment |
| F12 | Worksheet matches scanner but reviewer evidence absent | PASS alignment ONLY; RELEASE HOLD |
| F13 | Worksheet status CUT but excluded passage remains in EPUB | PASS alignment ONLY; downstream artifact gate FAIL/HOLD |

## Execution protocol
Before execution, post a prospective entry in the relevant GitHub Issue/Discussion explaining Timothy's concern, problem, hypothesis, proposed fix, exact pinned inputs, command, acceptance and falsifiers. Pin test fixture SHA and code SHA *before* running. Then run unmodified tests, record actual stdout/stderr, exit codes, interpreter, time, hashes, deviations, and respond in the SAME thread. Do not count this document as a retrospective pre-test. Frozen VER-15 in Issue #229 has priority; its source bytes must be verified before execution.

## Collaboration / release
GPT owns alignment implementation and reproducible test evidence. Claude owns editorial semantics, quotation-rights and claim interpretation; request review of sentence segmentation and trigger normalization. Timothy owns A1–A6 and commercial publication authority. HOLD until VER-15, REG-9, H2, REPLAY-6, editorial provenance, EPUB/PDF accessibility and Android checks pass and authorization is explicit.
