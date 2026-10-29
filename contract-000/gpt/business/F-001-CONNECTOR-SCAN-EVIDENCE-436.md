# F-001 Run436 — eight-source connector claim scan (HOLD-only)

**Sole project:** F-001 TAM Protocol speculative research-notebook ebook. **HOLD / NOT LAUNCH-READY.** PRE-TEST Issue #116 was published before new diagnostics. No original source or shared scanner was edited; no publication, account, outreach or payment.

## Observations and method

1. Read exact public TAM commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9` using GitHub connector `fetch_file` for the eight source paths from `F-001-TAM-PINS-435.json`. All eight returned Git blob SHA values match the pinned manifest. This is **connector metadata**, not independent raw-byte hashing.
2. Independently transcribed the four trigger regexes and Python sentence split from original `library-shared:Business/ideas/F-001-tam-build/claim_scan.py` blob `31f3dcff486c4c8cc96d514eb425da86834d00c3` into JavaScript, and applied them to connector-returned source text in memory. **42 candidate sentences**: README 1; Article 1 2; Article 2 3; Color Dyed 3; Article 5 3; Article 6 3; Article 10 4; Collective 23. Trigger incidences: accuracy 13, certainty 12, superlative 20, percent 2 (a sentence may have multiple triggers).
3. Committed `F-001-CONNECTOR-CLAIM-CANDIDATES-436.json` with all 42 source path/blob/sentence-position/trigger/excerpt records, all `CANDIDATE_UNREVIEWED`. Follow-up connector-side checks: 8/8 source pins match, 42/42 statuses remain unreviewed, zero duplicate source+sentence positions.
4. Attempted to obtain raw public source bytes in the local Python environment. Python HTTPS request to raw.githubusercontent.com failed with DNS/connection error. Container downloader rejected the URL because its web-access precondition was unmet; web open returned cache miss. **No local exact-byte snapshot, no original eight-file Python `claim_scan.py` execution, and no independent SHA-1 or SHA-256 byte validation occurred.** This is a deviation from the pre-test plan, disclosed rather than reclassified as a success.

## Interpretation / limitations

- The 42 count agrees with prior connector-side JS transcription reports, **but is not independent original-Python parity**. Python Unicode `\\b` and JavaScript `\\b` differ on some non-ASCII boundaries; sentence handling can also differ on edge cases. The 42 rows are *candidate discovery*, not truth, validity, scientific evidence, rights clearance, or an accepted publication checklist.
- The existing **45 baseline + 37 supplemental = 82 editorial occurrences** are a separate review queue, all **UNREVIEWED**. The 42 regex matches must not silently replace or subtract from those 82 items. There is no new editorial disposition.
- The full Run334→344→347→351 coordinator remains unverified; original Run358 CSVs unchanged. No EPUB/PDF/Android QA or final listing review was performed. Source text contains scientific and historical assertions requiring independent object-level review.

## Next exact action / acceptance

When raw bytes become available via an authorized path: materialize all eight at pinned commit; independently hash Git blobs; run Run434 presence gate and Run435 external pin gate, then execute the **unmodified original Python scanner** in a separate output directory. Compare its CSV/report with the 42 connector candidates and reconcile with the distinct 82 editorial occurrence records. Negative controls must reject missing, modified, symlinked and malformed sources; do not infer complete coordinator success from this partial check. Claude independently handles historical metrology, rights and editorial assessment; Timothy must answer A1–A6/B1/B4/B6/C1 and authorize any release. **HOLD remains binding.**
