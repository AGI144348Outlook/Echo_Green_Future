# F-001 — TAM Protocol ebook continuing checklist (GPT Run 343, 2026-10-25 02:55 CT)

**Project ID F-001 unchanged. Status HOLD / NOT LAUNCH-READY.** Same income project as Runs 332–342; no new pipeline. Existing plan `Business/ideas/F-001-candidate-ebook-gumroad.md` `73d64d7`, decision sheet `2975edc`, and previous [Run 342 checklist](F-001-PROGRESS-342.md) read before development. Shared source `library-shared@470d3c8` not edited.

**Actual advancement:** [Run 343 source-level trust-chain audit](F-001-TRUST-CHAIN-AUDIT-343.md) found that the Run 342 outer spool/size limit does not bound the Run 339 gate's nested `subprocess.run(capture_output=True)` memory use. Proposed one bounded diagnostic-capture correction and a targeted prospective test amendment; **no implementation or test** was claimed. The previous one-receipt handoff remains valid. Six shared Library sources freshly reviewed for release-provenance limitations.

| Deliverable | Status / acceptance criterion | Owner and next action |
| --- | --- | --- |
| Source selection, rights, exact credit and framing | **BLOCKED** A1/A3/A4/A6; source and licensing actually approved, not assumed | Timothy decision; Claude checks |
| Storefront, price/refund, book identifier | **BLOCKED** A2/A5/B6/C1; stable identifier and approved terms | Timothy only |
| Historical claims worksheet | **DRAFT/BLOCKED**; every flagged claim adjudicated or qualified; A rows 6/7 and *Gerah* resolved/marked | Claude editorial; Timothy |
| Source-pinned dataset A/B CSV + JSON | **DRAFT**; 6/8 rows, independent byte hashes and exact source pins; verified current stage with no stale outputs | GPT test; Claude challenge |
| Nested gate / consumer / session | **UNTESTED**; bounded nested stdout/stderr, child timeout cleanup, fresh-stage binding, independent pin and failure-marker checks, Issue #53 post-test narrative | GPT proposal; Claude review |
| EPUB/PDF final review bytes | **DRAFT**; fixed ID/date, accessibility, verified checksums, source/claims reconciliation | Claude build, GPT check |
| One final signed review receipt | **BLOCKED**; nonnull claims/PDF/EPUB/CSV SHA, script/source pins, independent verifier versions and external editorial approvals; release remains HOLD until explicit authorization | Both review; Timothy |
| Listing, payout, publication | **NOT AUTHORIZED**; no external action without explicit Timothy approval | Timothy |

**Single next technical action:** Claude independently reviews Run 343's nested capture finding. When authoritative Contract-000 and protected DISC-002 become accessible, GPT registers a focused prospective amendment to Issue #53, then makes and tests a bounded Run 339 gate replacement in a GPT-only branch. Do not modify shared or Claude files. A failed test is reported in the same Issue with observed evidence; a plan is not a result.

**Evidence:** SOURCE-OBSERVED = actual Run 339/340/342 Python and shared plan/receipt; INFERRED = unbounded nested capture risk; PROPOSED = bounded capture/test; EXECUTED THIS RUN = zero tests or CI. No private Testament, spending, accounts, outreach, publication, payments, paid inference or Cloudflare loops.
