# F-001 TAM Protocol ebook — GPT Run 335 continuity and package readiness

**Single project identifier: F-001 (unchanged).** [Shared F-001 plan](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-candidate-ebook-gumroad.md) §§138–140 and [Timothy decision sheet](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-decision-sheet.md) read first. B/C income candidates remain DEFER. **HOLD / NOT LAUNCH-READY.** No second pipeline.

**New draft deliverable:** [F-001-DATASET-STAGE-GATE-335.py](F-001-DATASET-STAGE-GATE-335.py), an **UNTESTED GPT-only** unique-stage coordinator candidate. It calls the Run 334 builder in a newly created directory, requires child exit zero, exact three files, pinned commit/blob IDs and A/B row counts, hashes outputs, and writes `VERIFIED-STAGE.json` only after these checks. Failures attempt to write `FAILED-STAGE.json` instead. It never selects a prior directory as the new run and never promotes a stage to release. This is an implementation draft, **not an executed safeguard or production gate**. [Prospective Issue #53](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53) exists before any testing; no tests or CI triggered because current Contract/DISC repository is inaccessible to this connector. Future evaluation must challenge filesystem races, marker write failures and hostile inputs; this code makes no adversarial-sandbox or atomic-publication claim.

| F-001 deliverable | Current evidence/status | Acceptance criteria and owner |
|---|---|---|
| Rights, scope, credit, licence, claims | **BLOCKED** | Timothy resolves A1, A3, A4, A6, Article 4 and exact rights/credit; Claude verifies manuscript-source correspondence. |
| Editorial manuscript and appendix | **DRAFT / BLOCKED** | Timothy disposition of Dataset A rows 6/7, *Gerah* (including B 1/8 cross-reference), rounding method and unsupported claims; Claude editorial review. |
| EPUB | **DRAFT / NOT FINAL VERIFIED** | Approved bytes; pinned build, EPUBCheck, accessibility and independent digest/receipt. |
| PDF | **DRAFT / NOT FINAL VERIFIED** | Approved bytes; reproducible build, fonts/links, accessibility, independent digest/receipt. |
| Dataset A/B CSV and JSON | **GPT Run 334 candidate tested 13/13; new stage gate UNTESTED** | Source-pin verification, exact A/B rows, output hashes, no reuse of stale stages; independent Claude review; final approved source. |
| One manifest/receipt | **SPECIFIED / NOT RELEASED** | Bind actual four deliverable hashes, source pins, independent verification, explicit approvals; reconcile with shared `RELEASE-RECEIPT-v0-DRYRUN.json`; no self-attested release. |
| Storefront, price, refunds, payouts/tax | **BLOCKED** | Timothy A2, A5, B6/C1 as applicable, and explicit publication/account/payment authorization. |

**Complementary tasks:** GPT owns the draft stage-gate and future independent pin/digest checks; Claude owns independent coordinator/exit-code review and editorial-source checks. Neither modifies the other's code. Ask Claude to review whether a failed child or partial directory can ever be mistaken for an approved stage; ask for a separate, read-only challenge to the code before promoting it.

**Single next action:** restore access to current Contract-000/DISC-002 and reconcile latest Claude contribution, then review the draft and execute **only** the preregistered #53 cases on an authorized GPT-only branch, with a same-issue post-test narrative. Do not integrate into shared F-001 build or publish without review/authorization.

**Awaiting Timothy:** A-000 custodian/recovery/field set/DEC-0007; F-001 A1–A6, B6, Dataset A rows 6/7, *Gerah*, credit/rights, price/refund and release permission. No spending, outreach, accounts, publication, paid inference or Cloudflare loop.
