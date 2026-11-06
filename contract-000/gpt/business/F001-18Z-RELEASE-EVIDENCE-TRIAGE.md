# F-001 TAM Protocol ebook — same project, 2026-11-06 18Z
**Project identifier:** F-001. **Status:** HOLD; draft preparation only. Read Run603 plan, F001-EVIDENCE-WORKSHEET-591, F001-RELEASE-GATE-597.py and F001-STATIC-PACKAGING-AUDIT-595.

## Technical advancement (static review, NOT a test)
The 597 release gate checks presence/nonempty output files, basic CSV shape, JSON report keys and digest equality for EPUB, but deliberately returns HOLD regardless. The synthetic 600 fixture is explicitly fabricated and must never be counted as rights or accessibility approval. The 595 audit identifies stale output and missing PDF-generation risks in the draft builder. Therefore a release manifest must bind source and output hashes and require an empty isolated build directory; a passing synthetic fixture cannot authorize publication. Keep `pdf-report.json` evidence separate from actual PDF accessibility verification. This run did not execute a fixture or CI.

## Deliverables / acceptance
- [x] Candidate and single project F-001 retained; draft gate and synthetic fixtures exist, not validated.
- [ ] 69 rights decisions with verifiable provenance and quotation permission.
- [ ] 82 editorial decisions with Claude's independent review.
- [ ] Exact-byte preregistered tests #265/#258/#262/#256/#229 and same-thread results.
- [ ] Accessible PDF and EPUB independently checked on Android and in validators.
- [ ] Timothy A1–A6 decisions and authenticated explicit release authorization.

**Next action:** pin the exact draft builder and gate blobs, reconcile #265 fixture expectations and implement isolated-output manifest evidence; no outreach, accounts, spending or release. **Claude coordination:** editorial/rights and Unicode boundary policy; GPT technical packaging/test evidence. Await Timothy for A1–A6 and release authorization.
