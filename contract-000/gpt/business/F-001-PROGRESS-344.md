# F-001 TAM Protocol ebook — continuing progress, GPT Run 344 (2026-10-25 03:58 CT)

**Sole project identifier:** **F-001** (unchanged; no new business pipeline). **Status:** HOLD / NOT LAUNCH-READY. Existing [shared project plan](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-candidate-ebook-gumroad.md) blob `73d64d7`, [decision sheet](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-decision-sheet.md) `2975edc`, GPT Run 343 progress and trust-chain audit, and Claude §140 reviewed before this run. Source remains `The-TAM-protocol@d46456a`.

**Concrete advancement:** Current authoritative Contract-000 and DISC-002 recovered by reading `research-discourse-registry` as a **branch**, removing the previous governance-read blocker. GPT-only [new nested-output draft](F-001-DATASET-STAGE-GATE-344.py) blob `5d5bb8f` discards unused builder stdout/stderr instead of retaining potentially unbounded capture. [Pre-test](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6395680400) and [post-test](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6395696276) recorded in the same Issue. Synthetic subprocess checks **T1–T3 PASS**, static committed-source check **T4 PASS (6 subchecks)**; not an end-to-end TAM test. Run 342 caller still pins old gate, so the revised draft is **not integrated**.

| Deliverable | Status and acceptance criterion | Responsible next action |
| --- | --- | --- |
| Product identity, rights, exact credit and framing | **BLOCKED** by Timothy A1/A3/A4/A6; approved source branch, license and claims framing needed | Timothy chooses; Claude verifies |
| Storefront, price/refund, book identifier | **BLOCKED** by A2/A5/B6/C1; no draft default counts as approval | Timothy |
| Historical claims and arithmetic | **DRAFT/BLOCKED**: ~35 flagged claims; Dataset A rows 6/7, exact 0.85625, *Gerah* 1/8 vs 1/16 require explicit disposition | Claude editorial; Timothy adjudicates |
| Source-pinned CSV A/B + report | **DRAFT**: six A rows/eight B rows; all three outputs must match independently pinned source/hash and current invocation | GPT builds/verifies; Claude challenges |
| Stage gate / consumer / caller | **PARTIAL, NOT INTEGRATED**: revised nested DEVNULL boundary synthetic PASS; fresh-stage, failure markers, process-group cleanup, old/new gate pins require real end-to-end testing | GPT preregisters integration test; Claude reviews diagnostic tradeoff |
| EPUB/PDF review edition | **DRAFT**: actual final edition bytes, fixed ID/date, accessibility and claims consistency | Claude builds; GPT independently hashes |
| Single final receipt | **BLOCKED**: independent input/output pins, non-null PDF/EPUB/CSV/claims hashes, both reviews and explicit approval; `RELEASE-RECEIPT-v0-DRYRUN.json` is not a release | GPT + Claude; Timothy approves |
| Listing, payout, publication | **NOT AUTHORIZED**: explicit permission and completed fiscal/terms decisions required | Timothy only |

**Single next technical action:** Claude independently reviews [Run 344 gate](F-001-DATASET-STAGE-GATE-344.py) and evidence; then GPT publishes a new prospective integration test entry on Issue #53, creates a separately pinned caller revision on a GPT-only branch and tests it with a real clean pinned TAM clone. No release or shared-branch adoption until both reviews and all acceptance gates pass.

**Open Timothy decisions:** A1–A6/B6 (book shape, storefront, credit, framing, price/refunds, license/source, stable ID), Dataset A rows 6/7, *Gerah*, claims treatment, final package, publication and payment. A-000 custodian/recovery remains separate from F-001.

**Safety:** No private Testament, main/shared/Claude edits, deletion, accounts, outreach, spending, payments, publication, paid inference or Cloudflare loops.
