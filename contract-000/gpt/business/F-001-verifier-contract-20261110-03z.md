# F-001 TAM ebook — release-manifest verifier design v0.3 (03Z; HOLD)
Single ongoing project: **F-001**. Read shared plan blob e017b38d, decision sheet 35ece85d, GPT checklist 69449fce and prior v0.2 manifest commit 854c1dc5. No new pipeline. GPT packaging/verification; Claude editorial/listing and rights evidence. No publication authorization.

## Concrete advancement: fail-closed verifier contract
Input: immutable release manifest v0.2, approved manuscript revision, editorial ledger, rights ledger, externally anchored issuer key and revocation data, built EPUB/PDF and accessibility/Android QA receipts. Output: deterministic **HOLD** with machine-readable error codes until all checks pass; a verifier cannot grant publication authority.

1. Reject absent edition/source revision or mismatched source tree hash (F001_SOURCE_UNPINNED).
2. Require 82 distinct editorial dispositions tied to source IDs and reviewer records (F001_EDITORIAL_INCOMPLETE); inherited target count must be independently confirmed before release.
3. Require 70 distinct rights decisions, each with source binding and affirmative grant (F001_RIGHTS_INCOMPLETE); never infer permission from a parsed receipt.
4. Verify canonical receipt bytes and independent issuer signature, key status and revocation at declared time (F001_ISSUER_UNTRUSTED).
5. Reject duplicate evidence IDs, replayed nonces and conflicting decisions; ledger must be durable and separately governed (F001_EVIDENCE_CONFLICT).
6. Require exact hashes of EPUB/PDF outputs and reproducible build parameters (F001_ARTIFACT_MISMATCH).
7. Require accessibility report and real Android QA tied to same edition (F001_QA_MISSING).
8. Require an independent Timothy-signed publication authorization scoped to edition, distribution channel, price and refund terms (F001_RELEASE_UNAUTHORIZED).
9. Even all-green verification produces RELEASE_ELIGIBLE_FOR_TIMOTHY_REVIEW, never autonomous storefront publication.

**Acceptance criteria:** all 9 checks reproducibly reject malformed synthetic fixtures; independent authority is never synthesized; human decision remains mandatory. **Next GPT action:** preregister a synthetic manifest linter test family, implement and execute after registration; no test executed on this design this run. **Next Claude action:** reconcile 82 editorial / 70 rights records and source revision without modifying GPT files. **Timothy blockers:** source scope A1–A5, protected issuer trust root, rights clearance and explicit publication authorization. Current status HOLD / NOT LAUNCH-READY.
