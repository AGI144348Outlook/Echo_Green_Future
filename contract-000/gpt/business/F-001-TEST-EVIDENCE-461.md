# F-001 — Run461 independent real-register evidence (2026-10-30 ~01 CT)

**PRE:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/142, published before Run461 tests. **POST:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/142#issuecomment-6516139483. Tests are **not** a frozen race.

**Input:** GitHub `fetch_file` on GPT Run460 for `F-001-EDITORIAL-DECISIONS-458.tsv`; connector returned Git blob `300dfcf0ba9e9d236326d09b2a4b6c5467d3874c`. Independent V8 JavaScript UTF-8 encoding, from-scratch SHA-256, TSV parsing and structural comparisons (not the Python CLI). Known SHA-256 vectors empty string and `abc` both passed.

**Observed real-source:** 38,025 UTF-8 bytes; independent SHA-256 `cb0bdae1bf8d7a2809619ee91d2aa8157cd1fce3834a9c68b1ea34537d59a0fd`, matching the previously recorded receipt. All **15/15** checks true: GitHub blob metadata, SHA-256, canonical LF, exact header, 82 rows, 10 columns, unique IDs, project F-001, all proposed/unapproved, all HOLD, exact source pin, exact manuscript pin, ten exact copy links, nonblank evidence, and existing copy targets. The 82 proposals and ten copy references are real source data, not synthetic fixture counts.

**Negative control:** Changed the first `PROPOSED_NOT_APPROVED` label to `APPROVED_BY_TIMOTHY` in memory without re-pinning. New SHA-256 `c268abe650fb2b3fc2241315fa022eab35799ce2c22f54127e41fcc41d461a2f` mismatched the pinned digest; approval-state predicate also failed. This is a **predicate-level V8 check**, not proof that the unchanged Python CLI refused it.

**Deviations/failures:** Local `curl` failed DNS (`Could not resolve host: raw.githubusercontent.com`); actual Python `-I` production CLI was **NOT RUN**, so no Python exit-code or stdout claim. Git blob SHA came from connector metadata rather than local Git SHA-1 rehash. Source historical truth, 82 editorial judgments, copyright/licensing, EPUBCheck/Android, PDF and release authorization remain unverified. No paid inference, CI, Cloudflare loop, account, publication, outreach or spending.

**Interpretation:** Real register's returned text matches the pinned SHA-256 and all 15 tested schema predicates. The new human review packet is presentation only, with **0 final approvals**. Next: independent local Python production replay when bytes are available, or complementary Claude replay; Timothy's explicit decisions before approved-text overlay.
