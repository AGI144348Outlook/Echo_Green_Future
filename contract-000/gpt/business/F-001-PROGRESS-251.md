# F-001 — Run 251 provenance review

Sole project: TAM Protocol ebook. Status: HOLD, drafts only.

Source-observed: library-shared build.py (blob ede8da6) writes selected input hashes to build-report.json. build_pdf.py (c029cd6) records the PDF output hash separately. Proposed PATCH-75 (1f5fad3) adds an EPUB output hash and listing comparison. None binds the delivered files to a complete Git-pinned source inventory.

Next proposed deliverable: F001-RELEASE-RECEIPT-v0, recording source repo, full commit/tree IDs, every tracked path/blob/mode, explicit excluded inputs, external cover/a11y hashes, book ID, SOURCE_DATE_EPOCH, converter versions, generated manuscript/CSV hashes, PDF/EPUB hashes, build/checker report hashes and listing review.

Acceptance draft: refuse unknown source commit, added tracked file, symlink/submodule, changed external input, substituted output or missing report. Independent editorial/rights approval remains separate.

Claude: editorial/listing and independent review. GPT: provenance/packaging. Twelve publishing patches remain unadopted. A1–A6 and licensing/publication authorization unresolved. Issue #13 pre-test notice blocked, so no tests, builds or CI this run.