# F-001 — Listing preflight versus release evidence (ChatGPT Run 366)

**Project:** F-001 TAM Protocol ebook, unchanged. **Disposition: HOLD / NOT LAUNCH-READY.** This is a GPT-only static source review; it does not change the shared Library or approve a listing. [Pretest Issue #56](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6410326795); [prospective refinement](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6410351611).

## Exact public evidence

- Shared `Business/ideas/F-001-tam-build/listing_check.py`, Git blob `adc3123c303168650e03270701cd3123afe0ce28`, current `library-shared`.
- Shared `Business/ideas/F-001-tam-build/RELEASE-RECEIPT-v0-DRYRUN.json`, Git blob `11ea9b39743c5607702a294bb95b6408dcf03c65`.
- Pinned HOLD stage coordinator Run 351 and previous Run 365 checkpoint; current public F-001 decision sheet. Actual TAM checkout attempted read-only on 2026-10-26 ~02 CT: `Could not resolve host: github.com`, exit 128. No real stage run.

## Source assertions — 14/14 matched (STATIC ONLY)

- MATCH: status includes claimed
- MATCH: status includes cut
- MATCH: claim gate tests status membership, not source
- MATCH: CSV advertised gate checks file names
- MATCH: EPUB advertised gate checks glob existence
- MATCH: PDF page verification conditional
- MATCH: no import hashlib
- MATCH: no explicit receipt read
- MATCH: dry-run status non-release
- MATCH: dry-run claims signoff null
- MATCH: dry-run EPUB hash null
- MATCH: dry-run PDF hash null
- MATCH: dry-run dataset hash null
- MATCH: dry-run explicitly fail-closed

**Observation:** `listing_check.py` accepts `claimed`, `inferred`, `test`, `cut`, and `sourced` as completed *labels*. It checks whether a claims CSV exists and rows carry one of those labels, but does not authenticate evidence behind `sourced` or independently verify that text labeled `cut` is absent from the final book. It checks the *presence* of a CSV/EPUB when those terms appear in listing text, not package bytes, hashes, structural validity or provenance. The PDF page count check is conditional on a listing phrase matching `about <number> pages`; the code does not unconditionally require a verified PDF. These are legitimate **marketing-text preflight** checks, not a release certification. The separate dry-run receipt itself declares it is not a release, contains null claims-signoff, EPUB, PDF and dataset hash fields, and states any null hash blocks release.

**Interpretation, not an executed false-positive test:** a listing with no bracket placeholders or forbidden words, a `claims.csv` row marked `cut` (regardless of whether the manuscript actually removed it), and a dummy file named `tam-draft.epub` could satisfy the listed predicates. This is a prospective adversarial fixture, **NOT RUN**. Do not interpret `listing_check.py` exit 0 as rights, editorial accuracy, release approval or package authenticity.

## Acceptance gap and complementary work

| Requirement | Evidence currently available | Release acceptance still required |
| --- | --- | --- |
| Claims | Marked status is syntactically checked | Human disposition with cited evidence; verify `cut` against final manuscript and `sourced` against provenance |
| Final package | Advertised CSV/EPUB names can be present | Independently verified content SHA-256, EPUB/PDF structural and accessibility checks, source/manifest binding |
| Rights and credit | No authorization check in inspected listing gate | Timothy confirms ownership/licence, attribution and framing A1/A3/A4/A6 |
| Storefront/payment | Draft listing gate does not create account or payment | Timothy decisions A2/A5/C1, explicit launch authorization |
| Stable identifier | Existing draft receipt has null final hashes | Timothy B6, final reproducible identifier and complete non-null release evidence |
| Dataset stage | Pinned Run 334/344/347/351 chain exists, unexecuted here | Actual source-bound HOLD receipt and altered-input rejection in isolated environment |

**Next single implementation task (GPT lane):** after source reachability returns, preregister a synthetic listing-check negative-control test using the *actual unmodified script*: (1) `cut` claim with uncut text, (2) invalid-but-present EPUB, (3) listing promising PDF without page phrase. Record whether the existing gate passes; then draft a separate HOLD-only release-evidence aggregator that fails on missing independent rights/editorial/package attestations. Do not silently expand the old marketing gate or call its success launch-ready.

**Claude lane:** independently verify rights/licence, Article 4, Gerah/rounding, claim cut/sourced editorial evidence, accessibility and storefront copy. **Timothy:** A1–A6/B6/C1 remain unapproved. Do not start a new business project. No private Testament, personal financial figures, paid inference, Cloudflare loops, outreach, accounts, spending or publication.
