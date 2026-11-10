# F-001 TAM Protocol ebook — GPT packaging release-manifest v0.2 (draft; HOLD)
**Single project ID:** F-001. Source: library-shared Business/ideas/F-001-candidate-ebook-gumroad.md blob e017b38d; decision sheet 35ece85d; GPT checklist 69449fce; Timothy R1 in TJ-RULINGS blob 3ce87eb6. Claude retains editorial/listing work; GPT owns packaging and reproducible file verification. No new business pipeline.

## Deliverables and acceptance checklist
- [ ] A1: Timothy chooses exact TAM manuscript scope and approved source revision; working source is AGI144348Outlook/The-TAM-protocol per R1. A2–A5 are choices, not accepted defaults; A6/rights and external issuer authority require evidence.
- [ ] 82 editorial dispositions and 70 rights decisions linked to content hashes and reviewer identity; no missing or ambiguous item treated as approved.
- [ ] Independently authenticated rights receipts: canonical bytes, protected issuer key, signature, revocation status, evidence binding and replay resistance; parser alone cannot establish rights.
- [ ] One approved source tree -> both EPUB and PDF; stable edition ID, deterministic build environment, output SHA-256, accessible heading/navigation/alt-text checks and Android reading QA.
- [ ] Cross-review by Claude and GPT; Timothy explicitly approves listing, publication, price/refund, and storefront; only then can release status change from HOLD.

## Proposed machine-readable manifest schema (no production implementation)
```json
{
  "schema":"F-001-release-manifest/v0.2",
  "project_id":"F-001",
  "status":"HOLD",
  "edition_id":null,
  "approved_source":{"repository":"AGI144348Outlook/The-TAM-protocol","commit":null,"tree_sha256":null},
  "editorial":{"expected":82,"approved":0,"ledger_sha256":null},
  "rights":{"expected":70,"cleared":0,"ledger_sha256":null,"issuer_trust_root":null},
  "artifacts":{"epub_sha256":null,"pdf_sha256":null,"accessibility_report_sha256":null,"android_qa_sha256":null},
  "authorization":{"timothy_release_receipt":null,"claude_review":null,"gpt_review":null}
}
```
Null means UNVERIFIED, not false assurance of completeness. Counts are inherited blockers, not independently recounted this run. A release verifier must reject null required fields, mismatched edition/source, missing rights/editorial rows, invalid signature or stale revocation, missing accessibility/Android evidence, and any missing Timothy authorization. It must never infer release permission from an assistant-authored file or SHA-256 alone.

**Concrete advance:** versioned field-level release manifest and fail-closed acceptance map for the SAME F-001 product. **Next GPT action:** implement offline manifest linter against synthetic fixtures, preregister in an Issue before any tests, then validate actual EPUB/PDF only after source and approval are pinned. **Next Claude action:** reconcile editorial/rights evidence and source revision, not GPT files. **Timothy blockers:** A1–A5, source/rights approval, independent trust root and explicit publication authorization. **Status HOLD / NOT LAUNCH-READY.** No outreach, accounts, spending, publishing or payment.
