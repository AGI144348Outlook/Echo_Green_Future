# F-001 TAM Protocol ebook — GPT Run 336 continuity and release checklist

**Single continuing income project: F-001.** Read the unchanged [shared project plan](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-candidate-ebook-gumroad.md) through §140 and [decision sheet](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-decision-sheet.md) before this development. No competing pipeline selected. **HOLD / NOT LAUNCH-READY.**

**This run's bounded advancement:** Static source review of the Run 335 unique-stage coordinator identified two independently checkable gaps: a stage could trust an arbitrary child builder's reported source pins, and `Path.is_file()` also accepts symlink targets. The new [Run 336 candidate](F-001-DATASET-STAGE-GATE-336.py) **attempts** to pin the reviewed Run 334 builder by Git blob `e8af6e5f011ec3e827c94737c717937944924eb8`, independently re-check TAM source commit/blob IDs before and after child execution, and reject output symlinks. It does not replace the Run 335 draft, the shared coordinator, or the release receipt. **UNTESTED** because current Contract-000/DISC-002 could not be retrieved. [Issue #53](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53) has the original prospective P0–P8 and a prospective P9–P13 amendment, both preceding any test.

| Deliverable | Status | Acceptance and owner |
| --- | --- | --- |
| Book source, rights, credit, licence, claims | BLOCKED | Timothy A1/A3/A4/A6, source/rights/credit approval; Claude source-to-manuscript and editorial review. |
| Editorial manuscript/appendix | DRAFT, NOT APPROVED | Timothy resolves Dataset A rows 6/7, *Gerah* (and Dataset B 1/8 cross-reference), rounding note and claim classifications. |
| EPUB | REVIEW-EDITION DRAFT, NOT FINAL | Approved text, reproducible pinned build, EPUBCheck/accessibility and independent digest/receipt. |
| PDF | REVIEW-EDITION DRAFT, NOT FINAL | Approved text, reproducible build, links/fonts/accessibility and independent digest/receipt. |
| Dataset A/B CSV and JSON | Run 334 candidate: prior 13/13 reported; Run 336 stage gate UNTESTED | Pin the actual builder/source, no stale-stage promotion, exact source/rows/hashes; independent Claude challenge and preregistered GPT test before adoption. |
| Single release manifest/receipt | SPECIFIED, NOT APPROVED | Reconcile with shared `RELEASE-RECEIPT-v0-DRYRUN.json`; bind source pins, exact approved artifacts and independent verification, not just a self-issued stage marker. |
| Storefront and customer terms | BLOCKED | Timothy A2/A5/B6/C1 where applicable; explicit account, pricing, upload, payment and publication authorization. |

**Complementary division:** GPT owns the source-pinned stage-gate candidate, prospective tests and independent artifact verification; Claude independently reviews its trust assumptions, stage/exit semantics and the manuscript/editorial/rights path. Neither may overwrite the other's work. The stage-gate's marker is a candidate artifact, not a final release certificate.

**Single next action:** restore read access to current Contract-000/DISC-002; request Claude's static challenge of Run 336 changes, then execute only the prospectively published #53 controls and post a same-issue researcher-readable result. If the read blocker persists, continue safe documentation rather than silently declaring success.

**Awaiting Timothy:** A-000 identity custodian, field projection, recovery authority and DEC-0007; F-001 A1–A6/B6, exact credit/rights, Dataset A rows 6/7, *Gerah*, price/refund and final release authorization. No publication, account creation, outreach, spending, payments, paid API inference, Cloudflare loops or shared branch changes.
