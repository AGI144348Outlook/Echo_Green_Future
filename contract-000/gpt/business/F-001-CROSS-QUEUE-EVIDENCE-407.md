# F-001 cross-queue reconciliation — Run407

Pre-test published prospectively in [Issue #80](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/80). Sole project **F-001**, HOLD / NOT LAUNCH-READY.

## Source pins and method
- Baseline editor v397 Git blob `7da6d43f42618ae915adb9f1fda216890a635674` (45 cards, 18 P1).
- Supplemental editor v406 Git blob `e3e2942181d5460b631e428096429c9939a6062d` (34 groups / 37 occurrences).
- Both reference TAM public commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9` and source-file Git pins. Parse embedded JSON source data, validate source IDs and blob bindings, count cross-queue exact-ID and exact-text overlaps, emit a HOLD-only manifest.

## Observed tests
- Actual committed inputs: **1/1 positive reconciliation PASS**. **45** baseline + **37** supplemental = **82 distinct source occurrence IDs**; **34** supplemental groups; **0** cross-queue source-ID overlaps and **0** exact full-sentence overlaps. All 34 supplemental groups remain `UNREVIEWED`.
- **11/11 synthetic adversarial controls PASS**, including duplicate IDs/groups, tampered SHA/commit, mismatched occurrence, fabricated rights/release, missing source refs, and an injected cross-queue overlap that was reported (not silently accepted).
- First attempt to parse inline `MAP` failed because the initial parser required `const MAP=` without whitespace; corrected parser tolerates whitespace. This was a harness defect, not a source-data failure.
- Executed the same `audit()` function embedded in the committed Node.js module inside the GitHub connector's JS runtime. **The Node CLI was NOT executed on local HTML files**, and no Android/browser/CI test was performed.

## Interpretation and limits
No exact duplicate occurrence or identical full sentence crosses the two review queues. This does **not** prove absence of paraphrased/semantic duplication, correctness of historical claims, manuscript completeness, human approval or rights clearance. All 45 baseline cards and 37 supplemental occurrences remain UNREVIEWED; no draft data imported. A source-bound offline CLI is prepared for future reproducibility; its pinned inputs must be provided as exact Git blob bytes. The script is read-only and returns nonzero on tampering or overlaps. The original eight-source Python scanner and full coordinator were NOT RUN.
