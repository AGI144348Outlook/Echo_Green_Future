# F-001 TAM Protocol ebook — single-project progress and acceptance, Run 338 (2026-10-24 CT)

**Project ID: F-001, unchanged.** The sole active income-product draft is the TAM Protocol ebook/research notebook, not historical dataset-digest or provenance-kit candidates. **HOLD / NOT LAUNCH-READY.** No account, publication, outreach, spending, payments, paid inference or autonomous Cloudflare work.

**Read-first evidence:** current shared `library-shared@470d3c8` [F-001 plan through §140](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-candidate-ebook-gumroad.md), [decision sheet](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-decision-sheet.md), [Run 337 project checklist](F-001-PROGRESS-337.md), and [Run 337 stage gate](F-001-DATASET-STAGE-GATE-337.py). Claude's independent §139–140 reviews and Issue #13 handoffs remain separately attributed. Current Contract/DISC authority remains unavailable.

**This run's bounded deliverable:** [GPT-only, UNTESTED stage gate v338](F-001-DATASET-STAGE-GATE-338.py). Static source review found that valid JSON with the wrong top-level/nested type could throw uncaught `AttributeError` before a failure marker, and that the builder's initial SHA-256 was read outside the exception boundary after stage creation. The draft checks JSON object shapes before member access, hashes the builder inside the failure-recording `try`, and catches Unicode decoding errors. Source pins, expected CSV digests, staging-only semantics and no-clobber design remain unchanged. Prospective P18–P21 were posted **before any future test** in [Issue #53](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6392733759). **ZERO tests executed in this run**; this is not evidence that the patch works.

| Deliverable | Status | Acceptance criterion and complementary owner |
| --- | --- | --- |
| Source rights, exact credit, license and claims | BLOCKED | Timothy answers A1/A3/A4/A6; Claude independently checks manuscript and attribution. |
| Manuscript and precision appendix | DRAFT | Resolve ~35 claim markers, Dataset A rows 6/7, *Gerah* conflict and placement/wording; Claude editorial review. |
| EPUB and PDF | REVIEW DRAFT | Timothy-approved text, fixed ID/date, reproducible build, accessibility checks, independent hashes and receipt. |
| Dataset A/B CSV + JSON | GPT UNTESTED stage-gate v338 | Prospectively run #53 P0–P21 with real pinned source and controlled malformed inputs; verify digest, stage isolation, failure records and no stale-package acceptance; independent Claude review. |
| One release manifest/receipt | DRAFT | Bind approved EPUB/PDF/CSV/JSON and immutable pins; independent verifier, no self-issued stage marker as final authority. |
| Storefront/customer terms | BLOCKED | Timothy A2/A5/B6 and payout C1 as applicable, explicit approval for account/upload/publication. |

**Division:** GPT owns isolated stage-gate draft and later independent artifact/hash checks; Claude reviews failure/receipt trust boundary and continues editorial/rights/build preparation without overwriting GPT's branch. **Next action:** restore authoritative Contract/DISC read access, get Claude's static review of v338, then run prospectively registered tests and report actual outcomes in the **same Issue #53**. No other business pipeline.

**Timothy decisions outstanding:** A-000 identity/recovery/DEC-0007; F-001 A1–A6/B6, Dataset A rows 6/7, *Gerah*, rights/credit/claims, final artifacts and explicit release authorization.
