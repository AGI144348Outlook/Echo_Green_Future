# F-001 TAM Protocol ebook — T85 packaging handoff (HOLD)

**Sole project identifier: F-001.** Read shared `Business/ideas/F-001-decision-sheet.md` (Claude), and GPT-owned `business/F-001-RELEASE-EVIDENCE-DOSSIER-568.md`. This is continuation, not a new pipeline. No publication or spending authorization.

## Deliverables and acceptance checklist
- [ ] Manuscript editorial/claims worksheet with evidence links, historical qualifiers, and copyright/quotation permission — **Claude**, pending.
- [ ] Timothy A1–A6 decisions: material, storefront, exact credit, framing, price/refund, source branch/license — **Timothy**, pending; defaults are not decisions.
- [ ] Pin exact manuscript source SHA, build scripts and input checksums; preserve source provenance — **GPT**, pending.
- [ ] Execute existing pinned VER-15 verifier with prospective Issue #229 and record exact source/guard/harness, command, stdout/stderr, exit, all 15 cases — **GPT**, pending. Do not invent new verifier.
- [ ] Adversarial EPUB ZIP fixtures: traversal, duplicate/case collisions, symlinks, encrypted members, compressed/decompressed limits, mimetype, OPF — **GPT**, pending exact-source runner.
- [ ] EPUBCheck or equivalent validation and PDF inspection, accessible headings/alt text/reading order, Android phone open/read evidence — **GPT**, pending.
- [ ] Independent cross-check of final build, release manifest, hash and listing — **Claude + GPT**, pending.
- [ ] Account, upload, sale, outreach, payment — **NOT AUTHORIZED**.

## Decision precedence and technical handoff
Authority must not be inferred from a self-typed `timothy_authorized` boolean. An authenticated receipt should bind both a pinned location (`branch:path@commit`) and content digest, and be validated against an independently trusted issuer; without trust root return `BLOCKED_AUTHORITY`. Path and packaging diagnostics may still be reported, but cannot upgrade the release verdict. This is **PROPOSED**, not implemented or tested.

**Next single action:** execute the existing pinned VER-15 family from Issue #229 only after source-byte transfer and prospective protocol are verified, then same-thread observations. Maintain HOLD until all gates pass. Claude owns editorial and rights; GPT owns packaging evidence. No tests executed for F-001 in T85.
