# F-001 TAM Protocol — 37-candidate source-bound triage packet (Run401)

**Project:** F-001 only. **Release state:** HOLD / NOT LAUNCH-READY. **Prospective test registration:** [Issue #74](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/74), posted before execution. No paid inference, CI, accounts, outreach, publication or spending.

## Source and method

Read the previous F-001 plan/progress and `library-shared:Business/ideas/F-001-decision-sheet.md` (blob `2975edcc4cae8a17499e873b68ba75f5c39ea527`); no A1–A6 authorization was inferred from draft defaults. Read Run400 [source coverage receipt](F-001-SOURCE-COVERAGE-400.json) blob `50fe65a1c17fcc3f7270e4128881634b72eacf39` and Run388 [45-card existing queue](F-001-FULL-SENTENCE-QUEUE-388.json) blob `06530d6729c3af39feebce9a6999650270008bf5`. Fetched all eight public `AGI144348Outlook/The-TAM-protocol` files at commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`, checked every Git blob SHA against Run400 pins. Reproduced Run400's exact sentence segmentation (`/(?<=[.!?])\\s+|\\n{2,}/`) to expand 37 truncated 220-character candidate excerpts into **complete source passages**, with previous and next source segments, file, occurrence number and source blob. All records retain `UNREVIEWED` and blank editorial, evidence, rights and reviewer fields. The [reusable generator](f001_coverage_triage_packet_401.js) is Node stdlib, local-only, fail-closed on mismatched source Git blob pins.

## Observations — separate from interpretation

- **14/14 V8 controls passed**: seven positive schema/source-bound assertions and seven synthetic negatives (wrong source SHA, missing source, duplicated candidate, existing queue collision, changed excerpt, changed source commit, missing candidate).
- Independently retrieved committed packet blob `dfa28a6a750967a2bb600e56a6e962117890478b` and generator blob `359fc2cec2921cfcc596f234ddd24a17f28dda32`; re-fetched eight pinned public source blobs. **37/37 full passages and previews match their source occurrence exactly**; zero source pin failures or existing queue-ID collisions.
- **37 occurrences across seven files**: README 3, Article 1 2, Article 2 4, Color/Dental 2, Article 5 3, Article 6 3, Collective 20; Article 10 0.
- **Three exact-text duplicate pairs** inside the 37 (six occurrences): `Article 6#S1` ↔ `Collective information#S150`, `Article 6#S12` ↔ `Collective information#S161`, `Article 6#S19` ↔ `Collective information#S168`. Thus 34 unique normalized passages; no exact-text overlap with existing 45-card queue.
- Several records combine headings and prose because the original segmentation groups adjacent lines. That is a *candidate-classification limitation*, not evidence that every record is an independent claim.

## Interpretation, limitations and next action

The packet makes Claude's **human editorial triage** materially easier without claiming that all 37 are real omissions. The source includes quantitative/historical claims and metaphorical or conditional language that require independent evidence and careful framing. A reviewer must classify each as `ADD_TO_QUEUE`, `ALREADY_COVERED`, `NOT_AN_EDITORIAL_CLAIM`, or `DEFER_MORE_EVIDENCE`, with reasoning, primary references and rights. Duplicate occurrences must be handled individually before any manuscript correction. **No automated admission to the 45-card queue and no approved changes.**

Original Python `claim_scan.py` on the actual eight files remains **NOT RUN**; this was JS V8 packet generation and source-binding verification, not a Node CLI execution, Android browser test, full dataset-staging coordinator, editorial truth test or final EPUB/PDF validation. Source pins authenticate retrieved Git content against a chosen commit, not the historical truth of its claims or the authority of the pin issuer.

**Claude coordination:** independently review the 37 entries, beginning with the three duplicate pairs and empirical quantitative assertions, returning source-backed provisional decisions in Claude-owned records/Issue #13. **GPT next:** obtain a supported local materialization of all eight source files for exact original Python scanner replay, then the smallest HOLD-only Run334→344→347→351 coordinator integration. **Timothy:** A1–A6/B1/B4/B6/C1, independent editorial and rights approval, explicit publication authorization. F-001 remains HOLD.
