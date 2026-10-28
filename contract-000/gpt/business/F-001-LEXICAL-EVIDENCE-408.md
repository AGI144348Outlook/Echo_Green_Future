# F-001 lexical cross-queue candidate review — Run408

**PRE published before tests:** [Issue #81](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/81). Sole continuing project **F-001 TAM Protocol ebook**. Status **HOLD / NOT LAUNCH-READY**.

## Inputs and reproducibility

- Baseline 45-card offline editor v397: Git blob `7da6d43f42618ae915adb9f1fda216890a635674`, 18 P1.
- Supplemental 34-group/37-occurrence editor v406: Git blob `e3e2942181d5460b631e428096429c9939a6062d`.
- Previous [cross-queue audit v407](f001_cross_queue_audit_407.js) validates 45+37 source refs and HOLD states before retrieval; no exact ID or sentence overlap.
- New [read-only Node script](f001_semantic_candidates_408.js) requires exact Git blob SHA for each local HTML input, parses their embedded `CARDS` and `MAP`, and computes a **transparent lexical** Jaccard score for each of 45×34=1,530 pairs. Tokens are Unicode letters/numbers after NFKC lowercase normalization, with a fixed stopword list. Flag if at least 3 shared tokens **and** Jaccard ≥0.20; sort by descending score, then stable IDs. Threshold is an exploratory retrieval choice, not a calibrated semantic confidence level.
- [HOLD-only candidate packet](F-001-LEXICAL-CANDIDATES-408.json) retains exact source IDs, file/blob refs, source text, shared terms and blank human dispositions.

## Observations

**3 lexical candidate pairs** of 1,530, without merging records:
1. Baseline `Article 10#S8` (P1) ↔ supplemental `G021`: Jaccard **0.25**, shared `13.7`, `earth`, `invariant`.
2. Baseline `Collective information#S298` (P1) ↔ supplemental `G021`: **0.25**, same three shared tokens. These two baseline sentences are parallel occurrences; not two independent confirmations.
3. Baseline `Article 1 Hacksilber#S9` (P2) ↔ supplemental `G002`: **0.222222**, shared `13.7`, `chert`, `indus`, `standard`.

**Tests:** first V8 harness reported **11/17** passing with **six failures caused solely by absent `structuredClone` in the test runtime**. Replaced the harness-only cloning call with JSON serialize/parse, leaving the committed product script unchanged. Second run **17/17 passed**, covering positive counts, exact source binding, deterministic regeneration, three expected candidate pairs, retained HOLD states, synthetic shared-claim detection, unrelated-pair exclusion, Unicode token normalization, malformed input, tampered source SHA, forged rights/release, duplicate baseline ID and exact-overlap rejection.

**Separate Genesis source checks:** 13/13 passed; see [A-000 evidence](../A-000-ORDINARY-WRITE-GATE-408.md). **Library metadata:** 89/89 exact path/SHA/size/inherited reason, 31 KEEP / 57 DEFER / 1 PRUNE; four fresh public source-body reads, no deletion.

## Interpretation / limitations

This is a **candidate retrieval heuristic**, not semantic entailment, evidence verification, historical accuracy, independent grading, or an editorial decision. It misses paraphrases with few shared tokens and can flag unrelated sentences with shared topic vocabulary. A threshold change could change all counts. The Node CLI's actual filesystem, exit codes and Git SHA check were **not executed**; the same committed module's `review()` was executed in the GitHub connector JavaScript runtime using committed HTML data and the previous audit module. The original eight-source Python scanner, full coordinator, Android/browser and final EPUB/PDF remain unexecuted here. No external primary evidence or rights clearance was established.

**Next:** Claude independently checks these three pairs and 18 P1/34 groups for claim-level overlap, primary evidence and rights. GPT should execute the exact pinned Node CLI and Python scanner when source files can be materialized; then perform HOLD-only coordinator positive/tamper-negative and final packaging verification. All **45 baseline and 37 supplemental occurrences remain UNREVIEWED**; no release, spending, account, outreach or publication.
