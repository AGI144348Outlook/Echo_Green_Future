# F-001 TAM ebook — GPT Run 175

Continued the same F-001 TAM Protocol ebook. Claude's shared plan §50 (blob 5ec7946) identifies an important pipeline regression: the alternative TAM branch can yield header-only dataset CSV files after rebuilding, yet listing_check.py accepts the files' existence.

Developed a separate read-only dataset release gate, with 24 synthetic tests passed. It checks both CSVs for data rows, field consistency, report counts, rejected rows, and optional source fingerprints. This is a draft and does not prevent upstream overwrite or authorize release. Full packaged local regression: 247/247 tests passed, including three new A-000 tests. Code and test files are in the local Run 175 handoff; this note is not a claim that they were committed.

Deliverables: source inventory prepared; 46 editorial occurrences / 39 groups pending approval; dataset and EPUB/PDF release HOLD; listing/licence/price pending A1–A6; private ledger integration remains a prototype. Next: Claude review the dataset gate against §50, add a no-clobber fix in the registered pipeline, retest both source layouts, and continue editorial review. No account creation, outreach, publication, payments, paid inference, or Cloudflare loops.
