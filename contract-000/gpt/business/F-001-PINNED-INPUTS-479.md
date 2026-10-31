# F-001 — exact pinned v472 generator inputs located (Run479)

**Discovery:** The three exact Git blob SHAs embedded in `contract-000/gpt/business/f001_review_companion_472.js` are already in the GPT development branch's own history, rather than in shared Library. This resolves the *location* blocker without changing the F-001 project identifier.

| Generator argument | Exact source path on GPT branch | Git blob SHA |
| --- | --- | --- |
| register.tsv | `contract-000/gpt/business/F-001-EDITORIAL-DECISIONS-458.tsv` | `300dfcf0ba9e9d236326d09b2a4b6c5467d3874c` |
| locations.tsv | `contract-000/gpt/business/F-001-SOURCE-LOCATION-RESULTS-462.tsv` | `7fb5cd952127de7a0469cfb3d0139d7bdfb60b86` |
| intake.tsv | `contract-000/gpt/business/F-001-DECISION-INTAKE-PENDING-463.tsv` | `4cc1617d1f1bbea1661f74ba931f86660c087939` |

All three SHA matches were observed in the Run478 Git tree. **Not yet generated or executed:** copy exact bytes to local temporary TSV files and run `node f001_review_companion_472.js register.tsv locations.tsv intake.tsv output.html`; compute output Git blob hash and commit generated HTML to GPT-only branch. Before running the executable regression suite, use the existing prospective Issue #154 and post actual positive/tamper-negative results there. Issue #157 contains this run's discovery PRE/POST. Do not use unpinned TSV substitutions.

Project **F-001 TAM Protocol ebook** remains **HOLD / NOT LAUNCH-READY**. 82 editorial decisions pending authenticated review; 69 rights decision units cover 77 quoted spans, all UNREVIEWED. Claude's `intake_check.py` is a complementary provenance worksheet guard, not legal clearance. Outstanding: exact HTML generation, #154 test POST, quotation provenance and rights, historical claims, EPUB/PDF QA, Android/screen-reader QA and Timothy's publication authorization. No publication, outreach, accounts, spending, payment or paid inference.
