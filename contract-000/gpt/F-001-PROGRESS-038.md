# F-001 TAM Protocol ebook — GPT Progress 038 (2026-10-12)

**One continuing project identifier: F-001.** TAM Protocol research ebook (PDF + EPUB + datasets A/B). Claude owns editorial/cover/listing preparation; GPT owns independent packaging/integrity preflight. No new pipeline or product. Existing project plan: `library-shared:Business/ideas/F-001-candidate-ebook-gumroad.md` §§24–26; shared builder `Business/ideas/F-001-tam-build/`. Source revision `AGI144348Outlook/The-TAM-protocol@d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`. Timothy owns the material, but third-party materials still need commercial-rights review. No publication authorization.

## Development this run

Integrated two **existing GPT gates**, not a new income pipeline: (1) 037 PDF/EPUB/build-report freshness gate; (2) a new check in 038 unified preflight comparing the built `dataset-a.csv`, `dataset-b.csv` and `dataset-check.json` byte-for-byte (SHA-256) with independent pinned-source regeneration. The previous 036 preflight validated *newly generated temporary datasets* but did not compare those to the actual release candidate's CSVs. An altered built CSV with the same row count could therefore escape that independent parity check. The 038 integrated tool closes this gap.

**EXECUTION-VERIFIED:** 9 new tests pass against real pinned TAM dataset source files, exact shared generator Git blob `fa3a62f76549ecaea6e226ba5cca41597000d790`, and independent parity auditor SHA-256 `5d0781d12a04bd71fd53b4010f35d1850651398b9f11f15bd9605e736537595f`. A=6 rows, B=8 rows; source regeneration passes. Tampered CSV with unchanged row count, altered dataset report, and missing CSV all fail. On unchanged data, `dataset_build_parity=PASS`; the deliberately incomplete build still has `technical_pass=false`, `release_ready=false`. Regression: 12 prior unified preflight + 12 artifact freshness tests passed. The integration remains a GPT-owned local candidate until fully packaged into the shared build and cross-reviewed by Claude.

## Deliverables checklist and acceptance criteria

| Deliverable | State | Acceptance |
|---|---|---|
| Source inventory and reproducible build | DRAFT | Pinned source and complete input list |
| Datasets A/B | 6+8 rows verified for parsing | No rejected rows; built CSV equals source regeneration; two numerical discrepancies editorially resolved |
| Complete PDF and EPUB | PARTIAL | Final intended chapters, page count, TOC, consistent metadata and reproducible outputs |
| EPUB nav/accessibility | PARTIAL | Structural check, independent EPUBCheck, truthful metadata and accessibility review |
| Artifact/report parity | 038 integration locally tested | PDF, EPUB, dataset hashes and reports all agree for the same final build |
| Claims, Article 4, Gerah glossary, edition scope | OPEN | Timothy disposition, historical evidence and factual qualifiers |
| Cover and third-party rights | OPEN | Commercial permissions and approved cover |
| Listing and Fiscal Contract | NOT AUTHORIZED | Independent listing-vs-artifact cross-check, Timothy approval |
| Publication | NOT AUTHORIZED | Explicit Timothy authorization, private ledger/storefront ready |

**Next action:** Claude completes and editorially flags the *same* TAM manuscript and build with opt-in book identifier, cover and accessibility metadata. GPT applies 038 unified preflight to that exact full build, provides a single signed-off technical report and flags blockers. No account creation, outreach, spending, publication, paid inference or autonomous Cloudflare loops. Technical PASS alone is never release approval.
