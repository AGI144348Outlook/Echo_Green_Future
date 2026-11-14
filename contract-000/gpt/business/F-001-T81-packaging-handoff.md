# F-001 TAM Protocol ebook — T81 packaging handoff (GPT-owned)

**Project ID:** F-001 (unchanged). **Status:** HOLD / NOT LAUNCH-READY. No publication, account, payment, outreach or spending authorized.

## Source review
Read Claude's existing F-001 decision sheet blob `35ece85d203b8f1a5bac5a2bf3b5d6b8780ac2eb`, GPT T80 checkpoint `beb0704a`, and prior packaging protocol Issue #466. Claude's sheet contains blocking A1–A6 (including source-text license), not just A1–A5; these are NOT settled by draft defaults. Claude retains manuscript, editorial, rights and listing. GPT owns independent packaging validation. Never overwrite Claude's work.

## Deliverables checklist
- [x] Source/role separation and decision-gate inventory
- [x] Draft EPUB ZIP preflight and corrected single-backslash candidate (not certified)
- [ ] Verify exact Git blob bytes of corrected preflight source and its hash in isolated execution environment
- [ ] Execute preregistered Issue #466 synthetic positive/negative ZIP fixtures; post actual results there
- [ ] Integrate ZIP preflight with container.xml/OPF/spine checks; validate malformed and parent-relative paths
- [ ] Independently inspect PDF structure, accessibility, font embedding and source reproducibility
- [ ] Android reader QA, accessible EPUB navigation, package manifest and SHA-256 checksums
- [ ] Claude editorial/rights verification and A1–A6 resolved by Timothy
- [ ] Cross-review and explicit Timothy release authorization

## Next exact action and acceptance criteria
Acquire a byte-identical checked-out validator source with Git SHA verification. Then **before tests** amend existing Issue #466 if fixture semantics change; run bounded offline cases; post observed vs expected, environment, output hashes and failures in #466. Acceptance: no false accept on unsafe paths, encrypted ZIP entries, oversized decompression, duplicate normalized members or invalid EPUB mimetype; valid compliant archives are not rejected without documented rationale. A successful synthetic fixture suite is not certification of the book or security.

## Blockers
No byte-certified test runtime path in this pass; A1–A6, EPUB/PDF accessibility and manuscript rights outstanding. Avoid inferred Gumroad fees or tax advice. Preserve F-001 as sole income project.
