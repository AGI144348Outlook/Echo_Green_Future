# F-001 TAM Protocol ebook — authenticated-source editorial assembly map, Run 326

**Status: DRAFT / HOLD / BLOCKED / NOT LAUNCH-READY.** This is a preparatory source map for the **same** F-001 ebook, not a new business project, historical verification, published ebook, rights certification or release approval. Read current shared F-001 plan §133 (blob `89fd5f35a4162f32aa5c50a877de9289ae14edba`), F-001 decision sheet (blob `2975edcc4cae8a17499e873b68ba75f5c39ea527`), Timothy's R1 ruling and previous GPT progress. Claude continues manuscript/editorial/rights/listing; ChatGPT handles independent source/packaging evidence on its own mirror.

## 1. Pinned public source baseline

- Repository: `AGI144348Outlook/The-TAM-protocol`; ref `main`; **commit/tree `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`**; complete Git tree, 11 blobs, `truncated=false`. Git blob fingerprints below are Git content IDs, **not** independently checked SHA-256 receipts or attestations of authorship/accuracy. Any later source change requires a new reviewed baseline, not silent replacement.
- Read-only source audit pre-registered at [Issue #45](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/45) before T1–T5. All 5 source observations matched the predeclared expectations; T6 is checked only after this packet exists. No external URLs followed or rights presumed for infographics.

| Source file (literal repository path) | Git blob SHA-1 | Bytes | Candidate editorial role | Decision / limitation |
|---|---|---:|---|---|
| `README.md` | `213bcfaf560dcc54fbb7ae79fad932e86b660357` | 2561 | Context and claim register | KEEP as source; do not reprint unverified conclusions as established history. |
| `Article 1 Hacksilber` | `237bd3335abdcc0f0465817dffe01ad6eaa86055` | 2345 | Chapter candidate 1 | KEEP; title/claim review required. |
| `Article 2 Water Weight Computes` | `ec657c3fa0f70da9686fb1ae52983d28f77c6c4c` | 2535 | Chapter candidate 2 | KEEP; physical/calibration claims need sourcing. |
| `The Color Dyed and Dental Records` | `b525ad60ab37cb2d72ea43c40ba687b0fe2a348d` | 2974 | Contains text labeled **Article #3** | KEEP; no separately named Article 3 file. Split only as editorial proposal. |
| `Article 5` | `c8c1bf617c0d81389f6c2408ed975131695857ff` | 3969 | Chapter candidate 5 | KEEP; source does not establish a separate Article 4. |
| `Article 6` | `662d745f0b9b41236d1053cdbaa9351f7c020dd0` | 3210 | Chapter candidate 6 | KEEP; overlapping text also appears in Collective information. |
| `Article 10` | `e82be564872f636662652d34dcb8d3437559f84f` | 812 | Chapter candidate 10 | KEEP; numerical predictive claim flagged for review. |
| `Collective information` | `710ad3cd4feeae7bafa329d7437a78df4c40cfa8` | 33708 | Includes text labeled Articles #6, #7, #8, #9, #10 | KEEP; **do not duplicate** 6 or 10 automatically; B2 editorial decision pending. |
| `Dataset A: The Eshtemoa Inventory (Forensic Weight Distribution)` | `b62c970a660e0a6685b58db1ef121690daa4fce7` | 610 | Dataset A CSV source | KEEP as source; CSV extraction/row 6–7 disposition pending. |
| `Dataset_B_Binary_Matrix.md` | `12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4` | 646 | Dataset B CSV source | KEEP as source; denominators and naming conflict pending. |
| `URLs to storedNotebookLM Diagramed Infographics` | `127cca3d0eb99054b6088ac31f0f8d4bcbe2179a` | 286 | Optional external illustration references | DEFER; link targets, license, provenance and image bytes **not inspected**. |

**Source limitations:** Only these 11 Git blobs exist on the pinned `main` tree; no `.epub`, `.pdf` or `.csv` output exists there. No separately named `Article 4` path exists. This does **not** prove an Article 4 was never written elsewhere or that a complete source manuscript has been authenticated. The named files do not certify scholarly claims.

## 2. Editorial truth/claims register — do not silently resolve

| Flag | SOURCE-OBSERVED wording/relationship | Status and required action |
|---|---|---|
| C-326-01 | Dataset A's `Small Scrap` says **0.125 Unit (1/8)** and names **Gerah**. | **CONFLICT OPEN:** Dataset B calls `0.85g (Stroke) 1/16 Unit` **Trace/Gerah Base**. Do not choose one definition, merge the terms or market it as a proven historical unit. Seek Timothy's editorial ruling B4 and sources. |
| C-326-02 | Dataset A reports `1.71g` for the small scrap; Dataset B maps `1.71g` to `1/8 Unit`. | Numeric alignment in the source is not independent confirmation of a historical relationship. Verify provenance, rounding, and Dataset A disputed rows 6/7 before CSV release. |
| C-326-03 | `Article 10` claims predicting lost nodes with **99.9% accuracy**. | **UNVERIFIED**, not an observed test metric. Do not use as marketing copy; require data, held-out evaluation, error bars and independent replication, or label as author hypothesis/remove. |
| C-326-04 | `README.md` predicts **>95% correlation** and treats it as proof of a locked registry. | **UNVERIFIED predictive assertion**; no model, sample size, sampling method or reproducible result established by this source inspection. Do not present as measured. |
| C-326-05 | `Collective information` repeats numbered Article #6 and #10 material; Article #7–9 sections appear there. | **EDITORIAL B2 OPEN:** split, deduplicate and map provenance before a final table of contents. Never count repeated chapters as new authored material without a record. |
| C-326-06 | `The Color Dyed and Dental Records` contains a heading `Article #3`; no `Article 4` path. | **EDITORIAL B1 OPEN:** no invented Article 4 or invented 10-article count. Mark any gap plainly until author resolves. |
| C-326-07 | README makes claims about archaeological provenance, isotope/dental data and trade connections. | **UNVERIFIED** by this source audit. Require primary citations or clearly label reconstruction/speculation; source statements are not independently established facts. |

## 3. Genuine four-artifact acceptance and packaging contract

| Deliverable | Actual state at this checkpoint | Acceptance condition |
|---|---|---|
| Book manuscript | Source blobs inventoried; source-selection A1, editorial B1/B2 and claim decisions unresolved | Exact chosen source commit and chapter boundaries, unique provenance per section, claims annotated as verified/inferred/speculative, approved rights and credit. |
| EPUB | **Not generated or authenticated in this run** | Reproducible build from approved manuscript; full EPUBCheck, rendering/a11y review, independent digest and editorial signoff. ZIP32 v5 synthetic tests alone do not satisfy this. |
| PDF | **Not generated or authenticated in this run** | Reproducible rendering, pagination, metadata, link and accessibility checks, independent digest and signoff. Synthetic PDF heuristics are insufficient. |
| Dataset A CSV | Source pinned, editorial conflict and rows 6/7 unresolved | Reviewed conversion preserving every source value, provenance, disputed-row dispositions, schema checks and independent digest. |
| Dataset B CSV | Source pinned, conflicting *Gerah* wording unresolved | Reviewed conversion, schema checks, cross-dataset vocabulary reconciliation and independent digest. |

**Publication gate:** ALWAYS `HOLD / BLOCKED / publication_authorization=ABSENT` until Timothy explicitly approves source selection A1, storefront A2, exact credit A3, framing A4, price/refund A5, license/source branch A6, identifier B6, Dataset A disputed rows, editorial claims and release. These defaults are not approvals. No outreach, account creation, spending, payment, publication or Cloudflare loop.

**Next complementary action:** Claude: independent editorial reconciliation of source mapping and claims, manuscript/rights/EPUBCheck/a11y/listing; ChatGPT: prepare a reproducible *non-publishing* source-to-artifact receipt only after editorial choices, then independently validate real four-artifact bytes. Do not create more ZIP-checker variants without a newly evidenced defect.
