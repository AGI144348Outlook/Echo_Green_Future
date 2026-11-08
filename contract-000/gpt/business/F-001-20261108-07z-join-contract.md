# F-001 TAM Protocol ebook — 07Z continuity, GPT-owned
**Sole project ID:** F-001; no alternative pipeline initiated. Sources: library-shared F-001 decision sheet (A1–A6 pending), v3 custody schema blob 566b9506, GPT 06Z v3.1 draft, Claude 07Z reply Issue #13 comment 6718506842 and shared section 253 (Claude adopts per-reference join table). **Status: HOLD / NOT LAUNCH-READY.**

## Concrete design advance: v3.1 join-row contract, for future independent testing
Keep v3's 17 unit fields and five package fields unchanged; retain scalar `editorial_evidence_ref`. Auxiliary rows keyed by (`unit_id`, `editorial_occurrence_id`, `editorial_evidence_ref`) with `evidence_source_blob_sha`, `byte_start_inclusive`, `byte_end_exclusive`, `slice_sha256`, `grapheme_boundary_status`, `reviewer`, `editorial_decision`, `decision_evidence_ref`, `review_timestamp`. Exact byte intervals are half-open raw UTF-8 offsets into immutable source bytes. Reject out-of-range/empty/UTF-8-split intervals, duplicate keys, digest mismatch, missing provenance or conflicting decisions. Grapheme boundary needs independent verification; UTF-8 validity alone is not sufficient. Every row defaults HOLD; source-span overlap never implies acceptance. Preserve original scalar verbatim even if multiple join rows; rollback reconstructs original v3 record byte-for-byte after canonical JSON normalization, or explicitly reports incompatible fields. No rights decision is inferred from editorial decisions.

## Deliverables and acceptance
- [ ] Source blob and quotation hashes U01–U03 independently verified.
- [ ] U70 rights evidence/clearance and remaining rights holds adjudicated.
- [ ] v3.1 synthetic migration fixture + rollback test preregistered in a separate Issue before execution.
- [ ] All 82 editorial occurrences individually adjudicated; U03 multi-occurrence references preserved.
- [ ] Accessible EPUB and PDF, reproducible package hashes, Android QA.
- [ ] Timothy explicitly authorizes final source, credit, rights, price, distribution and package hashes (A1–A6).
**Next GPT action:** commit a minimal offline synthetic migration validator and preregister test before running; Claude complementary work: U03 editorial occurrence mapping, U70 rights source evidence, schema review. No account creation, outreach, spending, publication or payments.