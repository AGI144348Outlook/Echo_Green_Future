# F-001 TAM Protocol ebook — GPT T80 packaging handoff (draft)

Project identity **F-001** remains unchanged; see shared `Business/ideas/F-001-decision-sheet.md` (blob `35ece85d203b8f1a5bac5a2bf3b5d6b8780ac2eb`) and `F-001-gpt-checklist.md` (blob `69449fceac9d4b7b5ac516318c685ec610fdd6df`). This is an inert GPT-only draft, NOT a modification of Claude's shared files.

## Deliverables and acceptance gates
- [ ] A1 material choice and rights verified by Timothy/Claude; manuscript source provenance
- [ ] A2 storefront, A3 exact credit line, A4 speculative framing, A5 price/refund choice explicitly approved (defaults are NOT decisions)
- [ ] Exact-byte checkout of GPT EPUB ZIP preflight v2, with preregistered positive/negative fixtures and logged Python/runtime/hash; Issue #466 currently 0/10
- [ ] EPUB container.xml, OPF manifest/spine and path-safety validation, including single backslash, traversal, duplicate names, decompression budgets and unsupported encryption
- [ ] Independent PDF parsing, embedded fonts, metadata, navigation and rendering checks
- [ ] Accessibility and Android reader QA, stable book identifier and checksum/receipt
- [ ] Claude editorial/rights clearance, final manuscript approval, and Timothy explicit publication authorization

**Acceptance:** all checks have artifact-specific source fingerprints, reproducible reports, no unresolved material rights/credit/framing questions, and Timothy authorizes publication. **Status HOLD / NOT LAUNCH-READY.**

**This run's advance:** reconciled the shared decision sheet's five blocking A-questions with GPT packaging gates; assigned GPT next action to obtain byte-certified ZIP-preflight source and execute Issue #466 fixtures, without modifying Claude's editorial/rights material. No tests or releases for F-001 in T80.
