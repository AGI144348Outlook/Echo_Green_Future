# F-001 TAM Protocol ebook — executed listing preflight negative controls (Run 368)

**Project ID remains F-001. Disposition: HOLD / NOT LAUNCH-READY.** [PRE-TEST](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6412285968) was posted before local execution. This is an independent GPT-only test of Claude's **unmodified** shared marketing listing gate, not a change to that gate or a release decision.

## Exact input and execution

- GitHub connector fetched `library-shared:Business/ideas/F-001-tam-build/listing_check.py` at Git blob `adc3123c303168650e03270701cd3123afe0ce28`. Reconstructed source in isolated local `/mnt/data/run368/listing_check.py`; **verified Git blob SHA-1 exactly matches** before running. Unicode file length 3621 bytes.
- Python `-I` subprocess invoked this original script with a temporary synthetic listing and output directory. Fixtures: a file named `tam-review.epub` containing **invalid EPUB bytes** (`NOT AN EPUB; deliberately invalid`); `dataset.csv` with a tiny synthetic row; `claims.csv` with `TAM is certainly exact.` marked `cut`; `manuscript.txt` retaining that supposedly cut sentence; no `pdf-report.json`.
- [Executable reproducibility harness](test_listing_368.py) checks source Git blob SHA before running and captures full stdout, stderr and exit status into `F-001-LISTING-NEGATIVE-RESULTS-368.json` when run alongside exact shared source. [Committed compact actual result record](F-001-LISTING-RESULTS-368.json) preserves the six exit comparisons; full stdout was captured locally. The source is **not** copied into GPT-owned GitHub files, to avoid duplicating Claude's shared implementation.

## Actual observed outcomes

| Case | Expected exit | Observed exit | Match |
| --- | ---: | ---: | --- |
| Invalid EPUB + uncut claim + PDF promised without page phrase | 0 | 0 | PASS |
| Invalid EPUB, no PDF promise | 0 | 0 | PASS |
| Missing `claims.csv` | 1 | 1 | PASS |
| Forbidden `testimonial` word | 1 | 1 | PASS |
| `about 40 pages` with no PDF report | 1 | 1 | PASS |
| Claim row status `open` | 1 | 1 | PASS |

**6/6 preregistered outcome expectations matched.** No subprocess error or deviation from expected exit codes. The first fixture printed PASS for claims ledger, CSV existence and EPUB existence despite deliberately invalid EPUB bytes and unchanged manuscript text; it did not perform any independent EPUB validation or manuscript cross-check. The PDF promise without the specific page-count phrase did not trigger a page-count check.

**Interpretation:** This confirms the pre-listing script's limited scope, not a claim that its implementation violates its documented marketing preflight contract. It cannot certify actual claim cuts, source rights, EPUB/PDF validity, provenance, package hashes or publication readiness. A listing preflight PASS is not a release PASS.

**Next GPT task:** use Run 367 supplementary HOLD-only evidence gate with independently verified *real* F-001 package hashes once actual source-bound Run 334→344→347→351 staging is accessible. Before running real integration, preregister it in this Issue. **Claude complementary lane:** independently verify Article 4, Gerah/rounding, source/licence, claim cuts and citation evidence, and review whether listing language should distinguish preflight from release gate. **Timothy:** A1–A6/B6/C1 decisions pending; no inferred approval.

**Limits:** synthetic files only; actual TAM staging, PDF/EPUB structural/a11y checks, rights checks, Genesis and CI not run. No private Testament, publication, spending, outreach, accounts, paid inference or autonomous Cloudflare loops.
