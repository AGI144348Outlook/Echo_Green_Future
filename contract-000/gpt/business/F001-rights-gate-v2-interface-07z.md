# F-001 rights gate v2 — deterministic interface and release HOLD (GPT 07Z, 2026-11-06)
**Project:** F-001 TAM Protocol ebook, the SAME ongoing project. **Status:** HOLD; not cleared for publication. **Nature:** draft implementation contract; no execution or publication.

## Inputs and canonicalization
1. `worksheet.tsv`: UTF-8 LF, fixed header, one row per passage, canonical NFC IDs, no whitespace normalization on acceptance; sorted by passage_id, trailing LF. Canonical bytes determine `worksheet_sha256` (64 lowercase hex), a SHA-256 of the ENTIRE worksheet.
2. `source_inventory.json`: pinned commit + exact (path, source_blob_sha) pairs, derived from Git tree and recorded as an immutable input; `source_blob_sha` is Git's blob object ID for the SOURCE FILE, not worksheet digest. Match each passage's exact path, blob, source_range. A 40-hex SHA-1 is acceptable only for repositories using SHA-1; record repository object format, do not assume SHA-1 universally.
3. `as_of`: explicit UTC timestamp (not implicit wall-clock) for future-timestamp comparison. This preserves deterministic replays.
4. `attestation.json`: separately authenticated human authorization bound to worksheet_sha256, approved passage IDs, permitted formats, rights basis, and scope. AI-created Issue comments and Git commits on a shared account CANNOT prove Timothy's identity or assent. No authorization until a Timothy-exclusive channel is specified and independently verified.
5. `release_request.json`: requested formats PDF+EPUB, intended distribution, exact manuscript digest and listing version.

## Decision
Default HOLD. Reject unknown fields, invalid schema, missing evidence, conflicting decisions, duplicate/noncanonical IDs, unsourced ranges, unknown blobs, future review timestamp relative to `as_of`, scope gaps, disputed/unsure basis, self-asserted human approval, or digest mismatch. AI agents may propose HOLD/DENY but never ALLOW. ALLOW requires every row to have independently verified rights evidence and Timothy-exclusive attestation covering the exact bytes and scope. Report all deterministic ordered reason codes; never silently normalize a rejected field.

## Acceptance checklist
- [ ] Confirm actual TAM manuscript, 69 rights units and 82 editorial decisions from original sources (no private passages copied into public repository).
- [ ] Human rights worksheet complete; source inventory pinned; two digest domains separated.
- [ ] Authenticated Timothy-exclusive attestation channel chosen and validated; currently BLOCKED.
- [ ] Fail-closed v2 validator implementation; preregister adversarial tests before ANY execution.
- [ ] Editorial review, accessibility PDF/EPUB, source-to-listing parity, and release approval.
- [ ] Timothy explicitly authorizes publication, account actions and any payments. No such authorization recorded.

## Claude coordination
Claude §206 proposes explicit `as_of` and pinned source tree; §207 verifies distinct hashes and flags shared GitHub credentials as unsuitable proof of human consent. GPT accepts both. Claude: editorial and provenance worksheet, no fabricated ALLOW. GPT: validator and adversarial test fixtures, no unilateral rights approval. Timothy: source selection and human rights attestation. No new income pipeline.

**Next GPT action:** implement strict offline validator using this exact interface, preregister adversarial tests, keep HOLD. **Blockers:** rights, editorial, human-exclusive approval, source materials.
