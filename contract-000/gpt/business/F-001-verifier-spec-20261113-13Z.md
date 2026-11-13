# F-001 offline artifact-verification contract — GPT draft 2026-11-13 13Z

Project identifier: F-001 TAM Protocol ebook. Status: HOLD; NOT LAUNCH-READY. This is a design artifact, not executable certification or publication permission.

## Proposed independent verifier
Inputs: read-only source root, manifest, PDF, EPUB, rights receipts, editorial clearance, and explicit authorization receipt. Never infer approval from a filename, field, or self-signed manifest.

1. Resolve every path with realpath; require commonpath(source_root, candidate)==source_root. Reject symlinks escaping root and traversal.
2. SHA-256 each exact artifact byte stream and compare to the release manifest; fail if missing, mismatched, duplicate JSON keys or unknown critical schema fields.
3. PDF: parse with an independent PDF parser, validate document opening, count actual pages, verify nonempty extracted text where expected, and report parser identity/version. Do not accept regex /Type /Page counts as certification.
4. EPUB: validate ZIP central directory, required mimetype first and uncompressed, container.xml, package OPF, manifest/spine references, and internal path safety; run EPUBCheck separately for conformance and accessibility review separately. File existence is insufficient.
5. Bind rights and editorial evidence to exact source revision and exact output hashes. Keep receipts inert and private.
6. Require externally authenticated Timothy approval specifying artifacts, distribution channel, scope, and date. Absence means HOLD, never auto-publish.
7. Emit deterministic machine-readable report with check IDs, PASS/FAIL/UNKNOWN, evidence hashes, versions, and blockers. UNKNOWN is not PASS. Never modify source or artifacts.

## Acceptance checklist
- [ ] A1–A6 decisions, including A6 licensing, documented
- [ ] Rights and editorial receipts independently checked (Claude coordination)
- [ ] Manuscript source revision pinned
- [ ] Independent PDF verification
- [ ] EPUB structural/conformance and accessibility verification
- [ ] Android QA
- [ ] Artifact-hash-bound manifest
- [ ] Explicit Timothy authorization for publication

Next action: locate original builder, listing checker and current shared F-001 plan; then implement the read-only verifier on GPT branch. No repository tests until prospective issue/discussion registration. No accounts, outreach, payment, publication or spending.
