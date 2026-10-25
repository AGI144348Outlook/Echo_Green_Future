# F-001 — TAM Protocol ebook, single continuing project, Run 340 (2026-10-25 00:05 CT)

**Project identifier:** F-001 (unchanged). **Disposition: HOLD / NOT LAUNCH-READY.** This run did not open another income pipeline. Read shared `Business/ideas/F-001-candidate-ebook-gumroad.md` (blob `73d64d74`) and `F-001-decision-sheet.md` (blob `2975edcc`), previous [Run 339 progress](F-001-PROGRESS-339.md), and actual GPT v339 staging-gate source (blob `25f0130`), as well as Claude's shared coordinator/verified-copy probes. Current protected Contract/DISC unavailable; no tests.

**This run's product advancement:** drafted [F-001-STAGE-CONSUMER-340.py](F-001-STAGE-CONSUMER-340.py), a separate, **UNTESTED**, read-only stage-consumer consistency check. Unlike the builder, it consumes the coordinator's captured stdout and actual OS exit code for one gate invocation, checks exactly one stage under an operator-specified root, and compares stage marker, pinned source reports, CSV hashes and sizes. It returns `release: HOLD` even when consistent. [Issue #53 P25–P31 prospective test registration](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6393750151) preceded any possible future testing; **none executed**.

**Important limitation:** A replayed old *successful* stdout plus an incorrectly supplied zero exit code can still pass. This tool does not authenticate freshness or publication rights. The calling coordinator must bind captured stdout/exit to a freshly spawned process (future possible nonce handshake), must not select previous stages by directory scan, and must separately verify editorial approval, receipts and package files. No production integration or final package occurred.

| Deliverable / checklist | State | Acceptance criterion and complementary responsibility |
| --- | --- | --- |
| Rights, book source, exact credit, licence, claim boundaries | BLOCKED | Timothy resolves A1/A3/A4/A6; Claude verifies source and editorial claims; no sale without rights. |
| Manuscript and numeric supplement | DRAFT | Review ~35 claim markers, Dataset A rows 6/7, unresolved *Gerah* A/B discrepancy; Claude editorial disposition. |
| EPUB and PDF | REVIEW DRAFT | Approved text, stable book ID/date, independently checked accessibility, content, TOC and hashes; GPT package check, Claude editorial cross-check. |
| Dataset A/B CSV and source report | GPT DRAFT | Real pinned inputs, exact reference hashes and independent source checks; previous #50–#52 tests are historical, not current test evidence. |
| Stage-gate and consumer handoff | GPT v339 + v340 UNTESTED | Preregistered #53 P0–P31, independent Claude challenge, successful real-source and synthetic negative tests, fresh-process correlation; **no false release signal**. |
| One final receipt/manifest | DRAFT | Bind *approved* EPUB/PDF/CSV and editorial decisions to immutable pins, independent verifier, clear provenance; never substitute stage marker. |
| Storefront, pricing, refunds, payouts, tax handling | BLOCKED | Timothy resolves A2/A5/B6/C1 and expressly authorizes publication/account actions; no placeholders as decisions. |

**Next action:** restore read access to current Contract-000 and protected DISC-002; ask Claude to review the consumer's replay limitation and whether the coordinator can bind current process stdout and exit. After authorized prospective test execution, post actual results to Issue #53. Only then decide whether to adopt a gate or improve it.

**Awaiting Timothy:** A-000 identity custodian/recovery and DEC-0007 boundaries; F-001 A1–A6/B6, Dataset A flagged rows, *Gerah*, rights/credit/claims, pricing/refund/identifier, and final release authority. No accounts, outreach, publication, spending, payment, paid API inference, or autonomous Cloudflare loops.
