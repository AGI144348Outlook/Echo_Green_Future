# F-001 TAM Protocol ebook — ChatGPT Run 221

**One project only: F-001. RELEASE HOLD.** Working source is The-TAM-protocol (TJ R1). Claude owns editorial/cover/listing; ChatGPT independently verifies packaging and integrity. This run did not edit shared build scripts or source manuscripts.

## New deliverable: section-local publication parity gate

The Run-220 global parity checker accepted a deliberately mutated EPUB in which a complete paragraph was moved from Article 1 into Article 2; global text remained present, so 6-gram coverage alone passed. The Run-221 gate rejects this by checking source paragraphs against their corresponding EPUB chapter and PDF body section, not the whole document. It also validates EPUB navigation link targets (not only heading words), ordered headings in EPUB/PDF, and internal-review hold text inside both delivered artifacts.

On the unchanged five-article/two-dataset review preview: 9 sections, 59 EPUB and 59 PDF paragraph checks, no errors. **48/48 offline tests passed (19 new, 29 inherited).** Deliberately moved paragraphs, tampered TOC targets, swapped sections and removed release-hold markers were rejected. This is a technical content-integrity check, not factual/rights/accessibility certification. Local executable gate, tests and SHA256 manifest are packaged in the Run-221 handoff.

## Checklist and acceptance

| Deliverable | State | Acceptance criterion |
|---|---|---|
| Manuscript editorial claims | HOLD: 13 OPEN | Claude and Timothy disposition with evidence |
| Source selection, credit, license, terms | HOLD: A1–A6 | Timothy explicit decisions |
| Source/dataset provenance | PARTIAL | All final chapter/CSV sources pinned and independently checked |
| Full patched production builder | PROPOSED: 12 patches | Execute in disposable checkout; no unreviewed shared writes |
| PDF + EPUB + datasets | PARTIAL: internal five-article preview | Full approved edition, consistent source/TOC/data and accessibility checks |
| Cross-format paragraph parity | PASS for internal preview | Repeat on production build with source fingerprints |
| Illustration rights / accessibility | OPEN | Rights record, EPUBCheck/Ace and independent review |
| Storefront, payments, publication | NOT AUTHORIZED | Explicit Timothy approval; no account/spend/outreach |

**Next:** Claude reviews the 13 claims and revised articles; ChatGPT integrates the new gate into the disposable production staging and checks PDF/EPUB/datasets with exact source pins. No new income pipeline. No publication or spending.
