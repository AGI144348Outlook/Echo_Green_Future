# F-001 — TAM Protocol ebook, continuing single business project (GPT Run 342, 2026-10-25 02:03 CT)

**Project identifier: F-001, unchanged. Status: HOLD / NOT LAUNCH-READY.** This is the same project as Runs 332–341, not a new income pipeline. Read current shared plan `Business/ideas/F-001-candidate-ebook-gumroad.md` blob `73d64d7` (through Claude §140), decision sheet `2975edc`, shared dry-run release receipt `11ea9b3`, GPT Run 341 checklist/session, Claude's latest accessible 23Z Issue #13 contribution, and current Library ledger.

**Concrete development this run:** [Run 342 draft session](F-001-STAGE-SESSION-342.py) refines the untested Run 341 caller by creating isolated POSIX child sessions, terminating process groups on timeout or after direct-child exit, and spooling output to temp files before enforcing a 16,384-byte acceptance limit. This addresses a **source-identified descendant-survival risk**; it is **NOT TESTED**, does not cap temporary-file disk growth and cannot stop a child that detaches its own session. It neither edits nor replaces Claude's coordinator or shared build. [Prospective P40–P47](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6394715119) was posted **before any possible future test**; no execution followed.

**Second deliverable:** [single-receipt integration map](F-001-RELEASE-HANDOFF-342.md) crosswalks the *actual* shared dry-run receipt's null claim/PDF/EPUB/CSV hashes and missing verifier version to separate editorial and independently checked packaging evidence. It prevents treating a GPT dataset-stage `STAGED_ONLY` marker as a final book-release receipt. This is a proposal for Claude's review, not a completed receipt or approval.

| Deliverable | Status / acceptance criteria | Complementary owner |
| --- | --- | --- |
| Source selection, rights, licence, exact credit, framing | **BLOCKED**: Timothy A1/A3/A4/A6; no assumption that the source can be sold | Timothy decision; Claude review |
| Storefront, price/refund, stable book identifier | **BLOCKED**: Timothy A2/A5/B6; no account, payout, listing or publication | Timothy |
| Claims worksheet and historical framing | **DRAFT / BLOCKED**: ~35 claims adjudicated; A rows 6/7 and *Gerah* 1/8 vs 1/16 resolved or explicitly qualified | Claude editorial; Timothy approval |
| Source-pinned A/B CSV and dataset-check report | **GPT DRAFT**: 6/8 rows, 0 rejected, exact values, independent real-source hash parity; prior #50–#52 tests do not validate Run 342 | GPT verification; Claude cross-check |
| Fresh-stage gate + session + consumer | **UNTESTED**: P0–P47 on isolated authorized fixtures, no stale stdout, late grandchild or false `release`; same-Issue actual results required | GPT draft; Claude independent process/TOCTOU review |
| Final EPUB/PDF and accessibility | **REVIEW DRAFT**: fixed book ID/date, TOC and content review, actual file hashes, independent EPUB/PDF checks | Claude build/editorial; GPT independent verification |
| One final release receipt/manifest | **BLOCKED**: null fields and missing verifier versions resolved, one consistent receipt, approved source/claims/bytes | Both independent checks; Timothy release decision |
| Storefront/payout/records | **BLOCKED**: A2/A5/C1 and explicit separate action authorization | Timothy only |

**Next action:** regain current Contract-000 and protected DISC-002 access, get Claude's independent review of the Run 342 process-group boundary and one-receipt map, then run prospectively registered isolated tests and post observed results to Issue #53. In parallel, the shortest editorial path remains Timothy's existing A1–A6/B6 decision card; this run adds no new questions. The product must not be called launch-ready while rights, editorial claims, actual final bytes, and publication authority are unresolved.

**Evidence boundary:** SOURCE-OBSERVED = current shared plan/decision/receipt and Python source; INFERRED = risk of surviving descendants and aliasing; PROPOSED = new draft and receipt map. **No tests, diagnostics, CI, Python execution/import, paid inference, spending, outreach, accounts, publication or Cloudflare loops in Run 342.** Current authoritative Contract/DISC inaccessible through linked GitHub.
