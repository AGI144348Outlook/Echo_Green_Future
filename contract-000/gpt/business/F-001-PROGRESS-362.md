# F-001 — TAM Protocol ebook: continuing product checkpoint (GPT Run 362)

**Single income project identifier: F-001. Status: HOLD / NOT LAUNCH-READY.** No new income pipeline. Shared [decision sheet](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-decision-sheet.md), [Workshop README](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Workshop/README.md), prior [Run 361 progress](F-001-PROGRESS-361.md), and pinned Run 334/344/347/351 code were read before this increment. GPT maintains independent technical validation/packaging; Claude retains independent editorial/claims/listing/rights review. Protected Contract/DISC remains 404; this is not authority to bypass it.

## New increment, observations and evidence

- [PRE-TEST](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6407217718) before source-level diagnostics; [POST-TEST](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6407235051) afterward, same issue.
- Read exact pinned builder `e8af6e5`, gate `5d5bb8f`, consumer `b2a9739`, coordinator `68eea27`. **Source observation:** builder emits source SHA-256 fields in `dataset-check.json`; gate/consumer validate Git blob identity, row counts, rejected rows, source commit and pinned CSV output digests, but do not cross-check the report's source SHA-256 fields. This is an **evidence-consistency gap, not an established stage-security bypass** because actual Git blob pins are checked separately.
- Developed [F-001-REPORT-PIN-362.js](F-001-REPORT-PIN-362.js), a *supplementary HOLD-only* check of report fields against the exact pinned source commit, source A/B Git blobs and SHA-256 values recorded by the Run 358 actual-source read, base 13.7, rows 6/8 and no rejected lines. It never returns RELEASE or APPROVED.
- Executed its same validator function in V8 with one synthetically complete pinned report and eleven negative fixtures: **12/12 expected outcomes**. [Machine-readable results](F-001-REPORT-PIN-RESULTS-362.json). **Node CLI not executed.** The older Run 358 report intentionally fails this stricter shape because it was produced by a different builder and lacks the required source-commit and Git-blob fields.
- Attempted `git ls-remote https://github.com/AGI144348Outlook/The-TAM-protocol.git HEAD` in the local execution container after pre-registration: **FAILED, DNS `Could not resolve host: github.com`**. This is not a source integrity failure. No clean runnable TAM checkout; **Run 334→344→347→351 Python stage chain NOT RUN**, no real HOLD receipt. The source SHA-256 reference values are not an external signature; the JS CLI's JSON parser does not reject duplicate keys. Treat this as an independent *review aid*, not an adopted release gate.

## Same-product deliverables and acceptance criteria

| Deliverable / acceptance criterion | Current evidence | Next action / owner |
| --- | --- | --- |
| F-001 identity, one product | **KEEP** TAM Protocol ebook only | Continue F-001 until launch-ready; no alternate project |
| Rights/source/licence/credit/framing (A1/A3/A4/A6) | **OPEN**; no final source or rights grant | Claude: prepare evidence/options; Timothy: explicit decisions |
| Storefront, price, refund, payout (A2/A5/C1) | **OPEN / NOT AUTHORIZED** | Draft only; Timothy authorizes |
| Article/terminology/rounding editorial (B1–B5) | Public TAM arithmetic and Gerah ambiguity documented; claims worksheet not fully adjudicated | Claude editorial evidence-state pass; Timothy decisions |
| Stable book identifier (B6) | **OPEN**; reproducible public draft requires pinned identifier | Timothy decision before final release build |
| Source identity | TAM commit `d46456a`, A/B Git blobs pinned; Run 358 source read | Obtain clean local pinned checkout; independently verify bytes and hashes |
| Run 334 builder output | Expected 11/9-column CSVs and source report; real stage output **NOT RUN** | Execute exact builder on clean checkout, no clobber |
| Run 344/347/351 HOLD staging | Static pin coherence Run 361; new report field cross-check Run 362 **12/12 synthetic** | Execute real chain, verify receipt and adversarial tamper cases |
| Source-report coherence | New HOLD-only report-field validator; **synthetic only** | Run Node CLI and compare source SHA to independently read raw source bytes |
| EPUB/PDF and accessibility | Shared Claude reports historical offline checks; **not re-run by GPT this run** | Independent final artifact inspection after editorial freeze |
| Rights/credit/listing and package signoff | **NOT COMPLETE** | Two-party cross-review; Timothy alone authorizes publication |
| Launch | **HOLD** | Never publish, contact, spend or collect payments without Timothy's explicit authorization |

**Acceptance:** a clean, pinned TAM source; approved source rights/credit/framing and claims; reproducible complete EPUB/PDF with accessible packaging; independently verified hashes and receipts; internally consistent listing, pricing/refunds and identifier; two-party review; explicit Timothy authorization. A synthetic passing check is not acceptance.

**Immediate next action:** acquire a clean read-only pinned TAM checkout in an authorized execution environment, run the exact Run 334 builder and Run 344→347→351 HOLD staging under prospective Issue #56 registration, and verify raw-source SHA-256 independently; meanwhile Claude should independently resolve editorial/rights evidence. **Blockers awaiting Timothy:** A1–A6, B6, C1, identity issuer/witness/recovery. No paid inference, autonomous Cloudflare loops, account creation, outreach, publication or payments.
