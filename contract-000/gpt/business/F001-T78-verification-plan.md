# F-001 — TAM Protocol ebook, T78 packaging continuation

Project identifier **F-001** remains the sole Contract-000 income project. **HOLD / NOT LAUNCH-READY.** GPT owns packaging verification; Claude owns manuscript, editorial and rights clearance. This is a planning artifact, not an executed test or permission to publish.

## Source review
- GPT T77 candidate `contract-000/gpt/business/f001_epub_zip_preflight_t77_candidate.py`, blob `6cc986cedb090c0b0146fb15d7af0e8ca3ad91ae`.
- Corrected single-backslash refusal is present in source; no exact-source execution yet.
- Metadata budgets are based on ZIP declared sizes, so they cannot establish full decompression safety; parser integration and resource limits remain separate.
- ZIP preflight does not itself validate EPUB container.xml, OPF, spine, content links, PDF, accessibility or licensing.

## Next bounded verification, already prospectively described in Issue #465
1. Byte-identical GitHub source retrieval and SHA-256 record.
2. Run synthetic valid EPUB mimetype-first/stored baseline and negative fixtures for wrong/nonfirst/compressed mimetype, duplicate names, traversal, single backslash, size and ratio budgets, directory and malformed ZIP.
3. Publish observed vs expected outcomes and deviations in Issue #465 *after* execution.
4. Integrate independent EPUB structure parser, then PDF and accessibility review, with fresh preregistration for any material test changes.

## Deliverables and acceptance
- [ ] Manuscript, copyright permissions and attribution confirmed by Claude and Timothy.
- [ ] EPUB ZIP + container + OPF + spine independent parser pass with reproducible evidence.
- [ ] PDF layout and metadata validation.
- [ ] Accessibility and Android reader QA.
- [ ] Final rights, provenance and release receipt.
- [ ] Explicit Timothy approval for publication, accounts, outreach, payment or spending.

Acceptance requires all gates and no unresolved rights issues; no sales or launch claims. Do not overwrite Claude's work or shared Library.
