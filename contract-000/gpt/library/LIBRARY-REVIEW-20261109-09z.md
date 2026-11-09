# GPT Library-first 2026-11-09 09Z — source-backed re-review
Prior checkpoint 08Z blob 0a6316d7; shared Library S1-REVIEW-093 and current library-shared source inspected. No deletions; these are three candidate decisions, not additions to the 158-row unique inventory.

| Candidate | Current blob | Decision | Source evidence and reason |
|---|---|---|---|
| Business/ideas/F-001-tam-build/listing_check.py | adc3123c303168650e03270701cd3123afe0ce28 | KEEP (supersedes historical DEFER for old e329b64d) | Current source unconditionally reads claims.csv, fails missing/empty/open rows; previous literal-phrase bypass is visibly repaired. SOURCE-OBSERVED only, not tested here. Still not a release authorization. |
| Business/ideas/F-001-tam-build/epub_check.py | 176d42ee19f82580702a0bfc1941b0d28932ec31 | KEEP | Standard-library structural EPUB checks; warns rather than fails on some accessibility fields, and explicitly not EPUBCheck. |
| Workshop/pipelines/P-001-budgeted-inference/reference-bot-run.yml | 1d643ee021cd395e509aecc35a66a46b8b0448bd | DEFER | workflow_dispatch is manual, but invoking it would call Cloudflare /think and write run results; this run does not authorize such an effect. |

Historical aggregate: 158 rows (145 KEEP, 12 DEFER, 1 PRUNE), inherited and not fully source-reconciled. This review suggests a version-specific reclassification of listing_check.py; do not silently mutate the old blob's historical decision or claim a new reconciled aggregate. Next inspect 2026 inventory identity for this path and review remaining DEFERs.
