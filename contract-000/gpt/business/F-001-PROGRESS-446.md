# F-001 sole-project progress — Run446 (2026-10-29 ~10 CT)

**Project identifier:** F-001 TAM Protocol speculative research-notebook ebook. **HOLD / NOT LAUNCH-READY.** Read the existing shared F-001 decision sheet and candidate §145, previous Run445 progress, 82-occurrence queue and 10-pair overlay before proceeding. No second business pipeline.

## Deliverable advanced

New standalone draft Node.js CLI: `F-001-EDITORIAL-OVERLAY-VALIDATE-446.js`. It reads the Run445 overlay, pinned 82-ID queue and Run444 reconciliation; computes Git blob SHA-1 of raw queue/reconciliation bytes, checks source commit and status pins, validates 7 baseline plus 3 supplemental exact decision pairs, disallows overlap/unknown IDs/extra decision fields, checks the separate S9/S299 annex and fails on approvals or release. **The validator is a consistency aid, not a rights, historical/geophysical fact-check, or authorization to publish.** No original source text is altered.

## Prospective test / actual outcomes

Pre-test published in [Issue #126](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/126) before diagnostic comparisons or in-memory tests. First in-memory suite: **13/14 expectations passed**; the source-queue mutation case failed because the harness altered parsed JSON without changing its synthetic pinned Git SHA. The actual CLI design hashes raw file bytes; the harness was corrected to model changed bytes with a changed SHA. Corrected suite: **14/14 expectations passed** (1 valid overlay + 13 tamper-negative cases: queue/reconciliation SHA, altered source queue, unknown/overlapping IDs, missing pair, wrong group, annex collision, premature final, release, hidden decision field, source commit, queue count). These were in-memory tests of the same `validateOverlay` function committed to the CLI; **not an executed Node CLI integration test**.

Attempted real CLI retrieval in the execution container failed: DNS could not resolve `raw.githubusercontent.com`; no Node execution on real source files succeeded. This is a recorded limitation, not a passing test. Original Python claim scanner full 8-source 42/42 independent replay also remains unperformed. Claude's earlier report of 42/42 and GPT's 8/8 source SHA corroboration remain separately attributed.

## Deliverables / acceptance checklist

- [x] Reversible 82-ID / 72-text / 10-pair editorial overlay, annex separate, no final approvals.
- [x] Draft standalone validator with 14/14 in-memory expectations (not full CLI integration).
- [ ] Run committed CLI against exact Git source bytes and independent tamper-negative file tests; independently replay original Python 42/42 scanner.
- [ ] Complete all 82 editorial dispositions plus S9/S299 annex, independently substantiate or qualify claims; Claude §145 has **26/82 provisional occurrence states**, **zero final**. Article 5's 13.7g 'flow rate' is a proposed unit correction, not approved copy.
- [ ] Timothy A1–A6 and B1/B4/B6/C1 decisions, rights/credits, source license and pricing; none presumed from draft defaults.
- [ ] Reproducible approved PDF/EPUB, independent receipt and Android check; explicit publication authorization before storefront activity.

**Single next action:** obtain the exact three JSON files in the Node execution environment and run the CLI positive/tamper-negative checks; then independently reproduce the original Python scanner full 42/42 output. Coordinate with Claude on Article 5/6 rights and evidence, without editing their files.

No accounts, outreach, publishing, spending, payments, paid inference, autonomous Cloudflare loops, main/shared/Claude/Genesis changes.