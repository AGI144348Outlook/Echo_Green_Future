# F-001 Run526 — nine-case replay acceptance and evidence integrity (DRAFT; NOT EXECUTED)

Project: **F-001 TAM Protocol ebook**, sole active income project. Status: **HOLD / NOT LAUNCH-READY**.

## Source-verified gap in Run524 runner
Read exact `f001_exact_source_nine_case_524.sh` (Git blob `4df5aaed094fcdcb14d27530564b05d115abe03d`), six-case harness (blob `d02a1ff4147f37db9b09b5145d69768d4e568066`), and three-case supplement (blob `081337219f4955f44a5441b7b9dbb34ab5cfd6ee`). The runner checks **two process exit codes**, but does **not independently check that six and three named cases actually executed**. Thus an inadvertently truncated harness exiting 0 would be counted as successful. This is a static source observation, **not a demonstrated exploit or runtime failure**.

## Acceptance refinement for existing Issue #197 (not a new test protocol)
Keep the frozen scenario set and source pins unchanged. A future execution report must capture the complete unmodified stdout/stderr, source Git blob hashes, SHA-256 fingerprints, Node version, OS, two exit codes and the following independent checks:
1. Original harness emits exactly six distinct `PASS <case name>` lines, no `FAIL`, and JSON summary `{"planned":6,"failures":0,...}`.
2. Supplemental harness emits exactly three distinct `PASS <case name>` lines, no `FAIL`, and JSON summary `{"planned":3,"pass":3,"fail":0,...}`.
3. Every expected case name matches the nine names in the pinned harness files; unexpected or duplicate names are failures. Both process exit codes must be zero; timeouts are failures.
4. Do not infer parent-directory race safety, historical correctness, quotation rights, or publication authority from synthetic fixture results.
5. If any result differs, preserve raw output, mark FAIL/INCONCLUSIVE, and report the deviation in **Issue #197**, without rewriting frozen tests.

## Practical blocker
Local execution environment cannot resolve `github.com` for a Git checkout; GitHub connector can read source but does not place a checkout in the local process. No execution was attempted after this failure. Do not report any case as passed in Run526.

## Deliverables and acceptance remaining
- [ ] Exact-source nine-case replay and same-thread actual results (#197).
- [ ] H2 evidence verification (#174).
- [ ] Six-file replay (#161).
- [ ] 82 editorial decisions and 69 quotation-rights units (77 passages), historical review.
- [ ] Accessible PDF/EPUB builds and Android checks.
- [ ] Explicit Timothy approval before publication or payments.

**Next GPT action:** run pinned sources only when an accessible local checkout and Issue #197 posting access are confirmed. **Claude:** continue independent editorial, provenance, historical and rights review; review this acceptance gap without modifying GPT files. No storefront, outreach, paid API inference or Cloudflare loops.
