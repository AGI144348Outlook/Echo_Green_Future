# GPT Contract-000 — Library-first review 022 (2026-10-12)

**Owner:** ChatGPT; **branch:** `mirror-chatgpt-root`; **source:** `code-library-registry@e104608aa6eda5dfb5b308fabefbb85b6a69b61f`; **shared Library consulted:** `library-shared@7c16c416c4e3e3efd7fea48bbfb3b2f7aec87b6c`. Retrieval: 2026-10-12. No source content was edited or deleted.

These are **source-specific** KEEP/DEFER/PRUNE decisions, not permission to execute or republish. Every entry remains recoverable by source branch/path/blob.

| Source path (relative to `code-library-registry/`) | Git blob SHA | Decision | Evidence and reason |
|---|---|---|---|
| `code_library_registry/modules/MOD-0008/ASSESSMENT.md` | `c6bb04985475e282af895167b0421af2fe6f6a18` | KEEP | Historical assessment explicitly distinguishes observed crawler execution from correctness and acknowledges unresolved licensing. |
| `code_library_registry/modules/MOD-0008/ABSTRACTION_LOCK.md` | `11bf3f9e1145cd7b29d0da2c4a85d81dca975a96` | DEFER | Records four SHA-256 declarations; file contents' digest parity and historical pre-search order were not independently verified this run. |
| `code_library_registry/modules/MOD-0008/provenance.json` | `54b8ef7ddd7b2c683e1661a2fbe065e20f3ab0f6` | KEEP | Names source commit `75c3056`, blob `baf1d65`, original crawler path and unresolved license. Lineage assertion retained; original blob not independently re-fetched. |
| `code_library_registry/modules/MOD-0008/original/NOTICE.md` | `83953049ba7b7ba6f3ac64b9f08f39ed3c7cf993` | KEEP | Explicitly disclaims any license grant for preserved excerpt. Retain notice with the source. |
| `code_library_registry/modules/MOD-0008/original/schedule_excerpt.py` | `70a539474b051ea13741910ad7161eaaaf051bf3` | KEEP | Preserved source behavior (schedule grammar and `is_due`), including permissive duplicate timezone declarations. Historical comparison only, not production adoption. |
| `code_library_registry/modules/MOD-0008/generalized/CONTRACT.md` | `901f142fba64025817497bee6eb4754b6c12f27f` | KEEP | States pure deterministic decision contract and explicitly excludes durable state, locks, retries and clock quality. |
| `code_library_registry/modules/MOD-0008/generalized/schedule_gate.py` | `26cfdf845eaf9d13a5e3e41855e43d0b1d9a6775` | DEFER | SOURCE-OBSERVED: daily/weekly slot uses `local_now.replace(hour=...)`. Executed independent exact-expression reproduction: on 2026-11-01 07:30 UTC, America/Chicago daily 01:00 selects **second** 01:00 (07:00 UTC) although first slot (06:00 UTC) had been consumed at 06:05 UTC. Duplicate civil-date run possible. DST fold policy is unspecified; needs explicit specification and regression test before executable promotion. |
| `code_library_registry/modules/MOD-0008/generalized/test_schedule_gate.py` | `c876680fc2226e76dae5bf7bb0a41df2e5d3ea48` | DEFER | Nine tests documented, but fall-back test only uses 08:00 (nonambiguous); no repeated 01:00 fold or nonexistent 02:00 spring-gap policy test. |
| `code_library_registry/modules/MOD-0008/validation/VALIDATION.md` | `e5fc1343d96390cfa72a50e4ac4bffdb8a3a264d` | DEFER | Reports 3 source assertions and 9 generalized tests; no independent execution of exact module files in this run. |
| `code_library_registry/modules/MOD-0008/validation/test_original_characterization.py` | `ed63e68b174f1c07546cd7c0bbae7f969e8361a3` | DEFER | Three source-characterization tests do not cover DST folds, missing source schedule, or naive timestamps. |
| `code_library_registry/reviews/MOD-0008_DISCOVERY_BATCH_2026-10-08.md` | `cc5956e5a6c7a69a404fbdd49a36a73388b0a14e` | DEFER | External issues/license/current-activity claims are historical leads, not freshly verified; do not contact or submit patches on their basis. |
| `code_library_registry/core_formula_algebra/README.md` | `10306d51a47c0cea9d3d83e8c57c2e9936a5b491` | KEEP | Separates algebraic equivalence, defined specialization, and implementation heuristic; avoids false equivalence of historical formula families. |
| `code_library_registry/symbol_registries/README.md` | `e463153f3b55b595b4503dde7cc4883cc763e8a9` | KEEP | Planning record labels Timothy declarations versus Claude interpretations/proposals; explicitly says not validated. D1 freshness not verified. |

**Batch: 13 examined = 7 KEEP / 6 DEFER / 0 PRUNE.** No deletions. Reassessment of deferred entries requires original blob, license review, policy for DST gaps/folds, and exact-module regression execution. These results supplement, not replace, prior S1 reviews.

**New falsifiable defect candidate (MOD-0008):** A daily 01:00 schedule in `America/Chicago` on 2026-11-01 can be marked due twice for the same local date. The local reproduction executed Python's `zoneinfo` and the exact `replace(...).astimezone(UTC)` expression seen in the source; the original module itself was not executed. Proposed policy: once per civil date unless user explicitly requests both folds. Do not silently change scheduling semantics before policy approval.
