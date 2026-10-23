# F-001 — GPT Contract-000 Run 296 progress (2026-10-23T10Z)

**Sole legitimate income project:** F-001 TAM Protocol ebook. **State:** EDITORIAL/RELEASE HOLD, draft/preparation only. No new pipeline. **Read first:** shared decision sheet blob `2975edcc`, shared F-001 plan blob `d72d1b11a677627227db74857ff0b9c857590310` through §103, Claude's latest Issue #13 review comment `6362400994`, GPT Run 295 checkpoint, actual gate v2 and source builder. Shared, Claude-owned and main files remain untouched.

## What advanced this run

Claude independently reproduced GPT v2's 10/10 cases, then found two Dataset A cases that returned `editorial=NO_FLAGGED_ROWS` despite A being missing or having a wrong header. I accepted the finding, published the [pre-test notice](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6362437264), and prepared **GPT-owned v3** with a separate `a_evaluable` state. Dataset A's pinned source/builder, CSV digest and structural checks must succeed before the gate claims an editorial evaluation. The committed v3 is `contract-000/gpt/business/PROPOSED-f001-dataset-receipt-gate-v3.py` ([03c6a2a](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/03c6a2a540d6a2fc28281c973cf55d89517847fa)); its [14-case harness](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/ca49e29761ce44eac1871cd744cefec2b8fa6f65) remains unintegrated.

**Offline characterization, 14/14 expected outcomes:** prior 10 cases preserved (baseline integrity exit 0/PASS/HOLD; release exit 3/PASS/HOLD; seven B/report/source alterations exit 1; usage exit 64). Four new Dataset A cases (missing, wrong header, changed bytes with valid header, changed A source) each exit 1/integrity FAIL/editorial **NOT_EVALUATED**/release HOLD. [Full evidence](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/b5877073485f86e36ea93eb83aa6186a01edca5d), [post-test report](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6362500201). Local setup initially failed (SyntaxError then premature harness TypeError); corrected before final run. The local tested verifier's executable function body matches the committed v3; archived public-source-derived fixtures were not committed. These tests do not authenticate the source pin or authorize publication.

Prepared [GPT four-artifact receipt / disposition interface proposal](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/63597b91ceb862aeec680f134647116b477da1c5): EPUB, PDF, Dataset A CSV, Dataset B CSV; separate data integrity, recorded editorial disposition and independent approval. A self-reported `approved` field cannot be trusted as Timothy's permission. No fabricated EPUB/PDF hashes. Claude's review requested; not a production integration.

## Stable deliverables checklist

- [x] Preserve single F-001 identifier, source plan and existing product across runs.
- [x] Earlier independently reproducible pinned A/B datasets (6/8 rows, 0 rejected); no new rebuild claimed in Run 296.
- [x] Preserve two **previously documented** Dataset A stated-vs-computed flags for editorial disposition; do not silently change originals.
- [x] Claude's independent v2 review incorporated into v3; 14/14 local exploratory cases, pre/post Issue notice, GPT-owned code and evidence committed.
- [x] Draft four-artifact receipt schema with distinct evaluation/disposition/approval states.
- [ ] Claude independent v3 review and agreement on receipt/disposition schema; no shared production adoption yet.
- [ ] Final reproducible EPUB/PDF/CSV package with independently pinned hashes, accessibility and claims reviews, fixed B6 identifier, licensing/credit/terms decisions.
- [ ] Timothy answers A1–A6 and B6, decides the two Dataset A editorial rows, and separately authorizes any listing/publication.

**Acceptance criteria:** source/rights/credit/terms approved; full A/B bytes and row counts match trusted pins; final EPUB/PDF independently checked; claim/accessibility review complete; disposition explicitly recorded and approved; release approval by Timothy. Integrity mode exit 0 alone is never a launch signal. **Next GPT action:** incorporate Claude's v3 review, then prepare a fail-closed optional disposition parser under another pre-test notice. **Next Claude action:** inspect v3 A evaluation and the four-artifact receipt schema, without overwriting GPT files. No outreach, spending, payment, storefront creation, publication, paid inference or autonomous Cloudflare loops.
