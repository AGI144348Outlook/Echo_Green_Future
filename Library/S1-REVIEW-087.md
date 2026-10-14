# Contract-000 GPT Library recursive review — run 087 (2026-10-14 CT)

Source: `Echo_Green_Future:library-shared`; each row read through GitHub `fetch_file` and fingerprinted by its returned Git blob SHA. Evidence state: SOURCE-OBSERVED for code/docs; risk decisions are GPT judgments, not promotion approvals. R3: KEEP/PRUNE/DEFER is an active-use decision, **never deletion**. Shared branch untouched.

| Source path | Blob SHA-1 | Decision | Evidence and reason |
|---|---|---|---|
| `Business/ideas/F-001-tam-build/build.py` | `96e4ef3b47f0f4be692337650e61c4596f58ce09` | **KEEP** | Offline draft builder with optional deterministic EPUB metadata; still needs complete pinned source and Pandoc. |
| `Business/ideas/F-001-tam-build/build_pdf.py` | `c029cd67c81c375a34d74ac77baaaf9fdd762524` | **KEEP** | Review PDF step and page-count report; conversion engines external, not release evidence alone. |
| `Business/ideas/F-001-tam-build/claim_scan.py` | `31f3dcff486c4c8cc96d514eb425da86834d00c3` | **DEFER** | Skips absent article inputs without failing; claim worksheet is not a complete-source or truth gate. |
| `Business/ideas/F-001-tam-build/epub_check.py` | `176d42ee19f82580702a0bfc1941b0d28932ec31` | **KEEP** | Useful preliminary EPUB structure checks; not EPUBCheck or accessibility conformance. |
| `Business/ideas/F-001-tam-build/ledger_map.py` | `8dd95e339b98acbce6816b9e0515d29ccdc8acc9` | **DEFER** | Real sales-export column mapping and refund fee treatment unverified; must keep actual figures private. |
| `Business/ideas/F-001-tam-build/listing_check.py` | `e329b64d2768deb8fe896a0ed383160c29d7481b` | **DEFER** | Permissive checks can pass without actual sale files and can miss page-count claims; companion release gate required. |
| `Business/ideas/F-001-tam-build/rebuild_datasets.py` | `fa3a62f76549ecaea6e226ba5cca41597000d790` | **KEEP** | Strict-pattern numerical reconstruction flags differences while preserving originals; no historical validation. |
| `Business/ideas/F-001-gpt-checklist.md` | `69449fceac9d4b7b5ac516318c685ec610fdd6df` | **KEEP** | Defines GPT packaging versus Claude editorial division; still draft. |
| `Business/ideas/F-001-candidate-ebook-gumroad.md` | `7caeec553380e48058528a0a09fd256c6983677b` | **KEEP** | Continuing F-001 project plan and Claude's dated refinements; not an approved Fiscal Contract. |
| `Workshop/pipelines/P-001-budgeted-inference/README.md` | `cae451754258a855ea914be8e0cbcec316bb246d` | **KEEP** | Reference budgeted inference design; no invocation, paid inference, or autonomous loop authorized. |
| `Business/ledger/SCHEMA.md` | `1a330a172d62775fc5a708502d7bdf4ada05e310` | **KEEP** | Public schema only; actual transaction and customer data stay private. |
| `Business/records/RETENTION.md` | `a303c78e739c2592f90dffdeb6991f1aacbe8e51` | **KEEP** | Draft private record retention convention; jurisdiction-specific duration still unverified. |

**Totals:** 12 assessed; 9 KEEP, 0 PRUNE, 3 DEFER. All original source blobs remain untouched. This is a recursive return review of the Business/Workshop working set, not a claim of 150 fresh rows or a completed global inventory.

**Promotion blockers:** The 3 DEFER rows require source completeness, release-file verification, and real private export evidence respectively. F-001 remains the **only** income project. No commercial publication or API inference.
