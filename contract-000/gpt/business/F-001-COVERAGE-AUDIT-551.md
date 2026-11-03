# Run551 — F-001 preregistered harness coverage audit (2026-11-02 CST)

**Project F-001: TAM Protocol ebook only. Status: HOLD / NOT LAUNCH-READY.** Source: Run550 `f001_verifier_cases_550.py` blob `325628adb168f5d012f115445a68bb4bd83fbc3d`, verifier547 blob `ecb88e250e05d0d4c1378b04b1864cc9af776b44`, prospective Issue #224.

## Static review finding, NOT a test result
The 15-case harness catches `(OSError, NotImplementedError)` during mutation and prints `SKIP platform unsupported`, then continues; its final `failures=0` and exit 0 can occur with fewer than 15 cases executed. In particular `extra_fifo` relies on `os.mkfifo`, and symlink creation can fail on some platforms. This is an evidence-coverage gap, not evidence of a verifier vulnerability.

## Proposed correction (not executed)
Track `executed`, `skipped`, and `failures` separately. For the preregistered full 15-case claim, require `executed==15 and skipped==0 and failures==0`; otherwise exit nonzero and retain HOLD. Platform-incompatible cases may be reported individually as NOT RUN, never PASS. Keep original 15-case list and frozen expected outcomes. Include raw stdout/stderr and environment in same-thread Issue #224 results. A co-modified artifact+manifest is expected to pass *internal consistency* while demonstrating that it cannot prove provenance.

## Execution limitation
GitHub source reads succeeded but the container could not resolve github.com for a clean pinned checkout; no repository tests, CI or diagnostics were run. No retrospective test claims. Next: implement coverage accounting on GPT branch, prospectively note any substantive test protocol change in #224 before executing, then run in disposable checkout and post observations there.

## Acceptance criteria (unchanged)
[ ] #224 15 cases fully executed with evidence and coverage; [ ] #220 custody negative cases; [ ] #197 nine-case regression; [ ] H2; [ ] six-file replay; [ ] 82 editorial decisions; [ ] 69 rights units / 77 passages; [ ] history review; [ ] accessible EPUB/PDF; [ ] Android review; [ ] Timothy A1–A6 and explicit publication approval.

Claude: please continue editorial/history/rights review and identify latest DISC-002 contribution. No alternate income project, release, payment, outreach or private data.
