# F-001 TAM Protocol ebook — GPT 16Z technical custody advancement

**Single project:** F-001 only; previous progress `contract-000/gpt/business/F-001-PROGRESS-1500.md` blob `d442640874bf45bdb72f1dba4b7214cd91c9859b`. Shared Claude decision sheet `Business/ideas/F-001-decision-sheet.md` blob `2975edcc4cae8a17499e873b68ba75f5c39ea527`; original plan `Business/ideas/F-001-candidate-ebook-gumroad.md` blob `8469584d9bc3607b35de9799f3ccfcfcad6c77ef`. GPT owns packaging/custody, Claude owns editorial, rights and listing. No change of income pipeline.

## New work: source-specific static threat review (NO TEST EXECUTED)
Read `contract-000/gpt/business/f001_h3c_custody_draft_1500.py`, blob `db8131dffa4cbc040bc9f23a5755fb2b31c3325f`. It uses directory-relative no-follow opens for every component, fstat before/after, SHA-256 and byte count, rejects malformed paths and duplicates, and always returns HOLD even with approval booleans true. This is a meaningful improvement over a path-based parent lstat/open race, but **the following gaps remain**:

1. **Unbounded read:** `while True: os.read(fd,65536)` has no maximum total size. A malicious regular file can exhaust time and storage budget. Proposal: hard limit (e.g. 16 MiB per source, adjustable only with explicit pinned policy) checked from fstat *and* cumulative bytes.
2. **Root provenance:** caller-supplied `root` and `source_commit` are not independently authenticated. A self-consistent manifest and modified source can pass internal digest checks. Proposal: independent trusted source pin and out-of-band custody witness; never treat a JSON `source_commit` string as evidence by itself.
3. **Approval booleans:** three literal true fields are self-asserted, not signed editorial, rights, or owner approval. Keep HOLD, require separate provenance-bound receipts, and never infer publication authorization from fixture data.
4. **Close/exception behavior:** `os.close(fd)` in finally may raise after a successful read, resulting in a caught OSError/HOLD; good fail-closed behavior, but it can obscure the primary cause. Record close errors separately without promoting status.
5. **Race/custody limits:** before/after fstat does not prove no byte mutation with restored metadata or establish a trusted root. Directory fd traversal reduces path replacement risk but does not protect a mutable file inode from concurrent writes. Need immutable snapshot or authenticated source pin.
6. **Source size / duplicate semantics:** no maximum count of manifest entries; duplicate paths are rejected but many distinct entries can cause resource exhaustion. Proposed bounded manifest count and total bytes, with fail-closed policy.
7. **Cross-platform:** `O_DIRECTORY`, `O_NOFOLLOW`, `dir_fd` may be unavailable on some hosts. Platform failure must HOLD; do not advertise portability without tests.

## Deliverables / acceptance
- [x] Source-pin static review and threat ledger (this artifact; source observed, not execution).
- [x] Inert fail-closed H3c verifier draft from 15Z (untested).
- [ ] Preregister separate adversarial test family BEFORE executing source, with changed bytes, symlink, traversal, oversized source, many entries, concurrent mutation, close error, approval spoof, stale pin, and independently signed receipt.
- [ ] Execute exact-source tests, report actual outputs to same issue, fix observed defects and version code.
- [ ] Reproducible PDF/EPUB source-pinned build and byte integrity.
- [ ] Independent accessibility/Android review and cross-check.
- [ ] Claude editorial/quotation rights dispositions; Timothy A1–A6 and explicit release approval.

**Acceptance:** all mandatory technical gates have evidence; independent rights and editorial approvals exist; Timothy authorizes publication; no synthetic self-asserted approval substitutes for that. Until then **F-001 HOLD / NOT LAUNCH-READY**.

**Next GPT action:** publish F-001-specific prospective test plan, execute exact pinned verifier bytes in suitable offline Python environment and report failures. **Next Claude action (requested):** continue editorial/rights decisions against the same F-001 manuscript and flag conflicts in the release manifest. No accounts, outreach, publication, payment or spending.
