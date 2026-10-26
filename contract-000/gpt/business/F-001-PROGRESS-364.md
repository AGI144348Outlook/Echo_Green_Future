# F-001 — continuing TAM Protocol ebook checkpoint (GPT Run 364)

**Project ID:** F-001 (unchanged). **State:** HOLD / NOT LAUNCH-READY. **Scope:** draft/research only. Read shared decision sheet, Workshop P-001 README, Run 363 progress, and exact pinned stage source before development. No new income project.

## Actual increment

- **Source/CLI audit:** [Issue #56 PRE](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6408620573) and [POST](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6408648957). Exact Run 334 builder, 344 gate, 347 consumer and 351 coordinator read by GitHub connector. [17/17 static assertions matched](F-001-CLI-PIN-AUDIT-364.json); these are **not runtime stage tests**. New operational defect: coordinator docstring says builder `332.py` although its actual pin requires `334.py`.
- **Deliverable:** [corrected exact-pin HOLD-only handoff](F-001-REAL-STAGE-HANDOFF-364.md) with public source commit, all four script Git blobs, CLI flags, safe stage-root requirements, expected hashes, failure/negative controls, and the requirement to preregister the next real execution.
- **Observed blocker:** `git ls-remote` against public TAM repository failed with `Could not resolve host: github.com` (exit 128). **Not run:** pinned TAM checkout, Run 334→344→347→351 Python staging, real HOLD receipt, altered-input rejection, actual EPUB/PDF, accessibility verification or CI. Handoff shell recipe is unexecuted.
- **Coordination:** GPT owns pin/packaging diagnostics; Claude owns independent rights, editorial, claims, accessibility and listing review. Current protected Contract/DISC returned 404; no claim to newer Claude protected text.

## Same-product checklist and acceptance criteria

| Deliverable | Status and evidence | Next action / owner |
| --- | --- | --- |
| Project continuity | F-001 TAM ebook **KEEP** | Do not open a second pipeline |
| Source selection, rights, licence, exact credit and framing | A1/A3/A4/A6 OPEN; pinned public TAM source d46456a | Timothy decisions; Claude rights/claim audit |
| Storefront, price/refund and payout | A2/A5/C1 OPEN; no account/payment | Timothy decisions; Claude draft listing |
| Editorial article/term/numerical claims | Article 4 gap; Gerah and rounding unresolved | Claude review; Timothy disposition |
| Stable EPUB identifier | B6 OPEN | Timothy choose before final build |
| Dataset source identity | A/B Git blobs pinned, Run 358 shared-builder CSVs incompatible with Run 334 stage | Use exact 334 builder and public TAM pinned checkout |
| Correct stage CLI / pin references | **NEW: Run 351 usage typo identified; 17/17 source assertions matched** | Review Run 364 handoff, use builder 334 |
| Fresh bounded HOLD stage, receipt and tamper rejection | NOT RUN, local DNS failure | New prospective Issue, execute pinned chain, record receipt/negative control |
| Supplementary strict report parser | Run 363 synthetic 7/7 Python methods; no actual report input | Integrate only after independent real-stage review |
| EPUB/PDF, accessibility, source-claims and package hashes | Historical draft checks, no final independent real artifacts | Claude editorial/accessibility; GPT final package verification |
| Cross-review and publication | HOLD / NOT LAUNCH-READY | Claude+GPT review; Timothy explicit authorization |

**Acceptance criteria:** clean exact public source checkout with independently verified file bytes; Run 334 CSVs and real Run 344→347→351 staging and tamper negatives; editorial/rights/credit/identifier decisions; reproducible EPUB/PDF and accessibility checks; consistent listing and financial terms; independent Claude/GPT signoff; Timothy's explicit permission to publish. A static or synthetic PASS is not launch approval.

**Immediate next action:** when GitHub DNS works in the execution environment, publish a fresh prospective test record and execute the corrected [HOLD-only recipe](F-001-REAL-STAGE-HANDOFF-364.md). If still blocked, do not multiply checker scripts; ask Claude to complete editorial dispositions and preserve the staging blocker. No accounts, outreach, spending, payments, paid inference, autonomous Cloudflare loops or publication.
