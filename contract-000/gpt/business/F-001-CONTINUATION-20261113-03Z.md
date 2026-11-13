# F-001 — single income project continuation, 2026-11-13 03Z

**Project ID:** F-001 / TAM Protocol ebook. **Status:** HOLD / NOT LAUNCH-READY. Same project, no new pipeline. This is a specification, not a release or executed validation.

## Evidence read first
- Contract-000 and shared Business/ideas/F-001-decision-sheet.md (blob 35ece85d203b8f1a5bac5a2bf3b5d6b8780ac2eb).
- Previous GPT checkpoint 2026-11-13 02Z and F-001.md.
- Decision rows A1-A5 and **A6**, B1-B6; A6 is an open license/source question, not an MIT grant. Claude owns editorial/rights evidence; GPT owns packaging and independent admission checks.

## Concrete next deliverable: fail-closed decision-sheet adapter (draft specification)
1. Parse only a pinned exact source blob, preserving row identifiers and text; required blocking IDs A1-A6, nonblocking B1-B6.
2. Reject duplicate IDs, absent IDs, unrecognized extra blocking IDs, conflicting values, placeholder strings and defaults masquerading as approval.
3. Keep **document row existence**, **Timothy decision**, **issuer verification** and **artifact binding** separate. A6 exists but is unanswered. A plain `approved: true` field cannot grant release.
4. Require release receipt tied to the exact PDF/EPUB SHA-256 and approved source/license revision; authenticated issuer, scope, expiry, nonce/replay and revocation checks are external to this parser.
5. Check structural PDF page count with a PDF parser rather than raw byte regex, EPUB integrity, accessible contents, dataset/listing/sample parity, and reproducible output hashes.
6. Do not accept launch unless all blocking rights/editorial/authorization gates have independent evidence.

## Prospective negative vectors for a later preregistered test
Missing A6; duplicate A6; placeholder A6; MIT license on an unmerged branch asserted as release license; spoofed issuer; mismatched artifact hash; revoked receipt; unverified PDF page count; contradictory listing price; stale editorial rights ledger. **These vectors were not executed this run.**

## Deliverables checklist
- [x] Existing project identified and source decision sheet read.
- [x] Release-admission adapter and negative vectors specified.
- [ ] Rights dispositions and editorial dispositions authenticated (historical counts 70/82 need recheck).
- [ ] A1-A6 and relevant B decisions confirmed by Timothy; exact licensing/source revision fixed.
- [ ] Accessible PDF+EPUB, artifact hashes, listing/sample parity and Android QA independently verified.
- [ ] Timothy explicitly authorizes publication of the exact artifact.

**Acceptance:** All required evidence gates pass against immutable artifacts, and Timothy explicitly approves release. **Next GPT action:** implement adapter on GPT-owned branch, preregister its synthetic tests, and run them without altering shared files. **Next Claude action:** continue rights/editorial receipt work and confirm authoritative row schema. No accounts, outreach, publication, spending, or payment.
