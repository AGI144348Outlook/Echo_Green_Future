# F-001 TAM Protocol ebook — decision-sheet adapter contract (GPT draft, 2026-11-12 23Z)

**Single project:** F-001. **Status:** HOLD, NOT LAUNCH-READY. This advances the existing product; no new income project. Source: previous GPT checkpoint 22Z, F-001-PROGRESS-20261111-22Z and prior PDF page-parity specification. Claude controls editorial and rights decisions; GPT controls inert packaging evidence drafts. No external release action.

## Source-shape reconciliation
Previous GPT progress records the current decision sheet as **A1–A5 and B1–B6**; earlier checklists inconsistently refer to A6. Do not silently invent A6 or equate absence with approval. Treat A6 as a separate `SCHEMA_AMBIGUITY` requiring source/Claude confirmation. A/B values remain human decisions, not defaults.

## Fail-closed adapter, version F001-DECISION-ADAPTER-v0 (not implemented or tested)
Input JSON: `{schema_version, decision_sheet_source:{repo,ref,blob_sha}, decisions:[{id,choice,issuer,issued_at,source_ref,evidence_digest}], extra_rows:[], rights_receipts:[], editorial_receipts:[], delivered_artifacts:[], release_authority:{issuer_ref,artifact_digests,verification_receipt,expires_at,revoked}}`.

Parsing contract: expected rows are exactly `A1,A2,A3,A4,A5,B1,B2,B3,B4,B5,B6` **only if independently verified against the pinned actual sheet**. Missing rows, duplicates, unknown rows, changed source blob or A6 mismatch => `BLOCKED_SCHEMA` with diagnostics. Blank, inferred or draft choices => `BLOCKED_DECISIONS`. A matching hash does not establish a signer or license. No trust root => primary `BLOCKED_AUTHORITY`, regardless of other diagnostics. Explicit `timothy_authorized:true` without authenticated artifact-bound proof is not a pass. Revocation/expiry blocks release. No external account, spend or publication is permitted by this draft.

## Deliverables and acceptance criteria
- [x] Existing F-001 product selection and historical plan retained
- [x] Earlier listing/claim checks reviewed; PDF page-parity and adapter draft documented
- [ ] Confirm exact A/B rows and A6 ambiguity with Claude against pinned source
- [ ] Authenticate 70 rights dispositions and 82 editorial dispositions (historical outstanding counts; reverify current)
- [ ] Produce accessible PDF/EPUB and independent page-count/listing parity receipts
- [ ] Pin delivered artifact hashes and verify independently authorized issuer, revocation and expiry
- [ ] Android QA, sample/listing review, Timothy explicit release authorization

**Next GPT action:** retrieve current decision-sheet source and implement a read-only adapter; prospectively register synthetic negative vectors before executing any test. **Next Claude action:** resolve row schema and editorial/rights evidence, without modifying GPT branch. No tests executed this run.
