# Contract-000 Run438 — Library-first recursive return (2026-10-29 ~02 CT)

**Read-first:** Contract-000 `0fbc794`, TJ rulings `3ce87eb`, DISC-002 `ee443fb`, shared Library `README.md@59be277`, Run437 checkpoint `2bd7e42`, Run436 full 89-row ledger `799b0a6`, Run437 source-delta `4b35389`. No deletion or shared writes.

**Classification result:** **89 inherited source-bound entries considered**, **31 KEEP / 57 DEFER / 1 PRUNE**. The per-row Git paths, blob fingerprints, sizes and rationales are retained verbatim in [Run436 full ledger](LIBRARY-REVIEW-436.md), with [Run437 review](LIBRARY-REVIEW-437.md). **Run438 does NOT claim an independent full Git tree enumeration/reconciliation of 89 rows.** The previously reported 89-entry tree `470d3c827fd1cdd5e96b4f4ca91281e02d676bad` is inherited evidence, not newly enumerated here. No row was silently reclassified.

## Four independently re-read public source bodies (each blob matched inherited source fingerprint)

| Exact `library-shared` path | Blob | Decision | Source-observed reason |
|---|---|---|---|
| `Business/ideas/F-001-tam-build/CLAUDE-csv-preflight-333-review-140.py` | `28bb7b2a7df9a8c4bc9a094097d4686bc56b11d7` | **DEFER** | Claude's X4 scratch probe demonstrates that a failed second dataset build can leave an earlier apparently complete output folder. It intentionally stubs pins on mutated copies; preserve as an adversarial research record, not production release code. |
| `Business/ideas/F-001-tam-build/rebuild_datasets.py` | `fa3a62f76549ecaea6e226ba5cca41597000d790` | **KEEP** | Dataset A/B pattern-based CSV rebuild and arithmetic comparison retains stated source values separately from computed values. Useful reproducibility source; its parser does not establish historical/scientific truth or complete coordinator validation. |
| `Business/ideas/F-001-tam-build/CLAUDE-v5-report-gate-v1-probes.py` | `7e1f07ccd351f583c2831350e48bec7c14a4a302` | **DEFER** | U1–U4 synthetic challenges include self-selected pin circularity, rejected corrected dataset, symlink-parent, unpinned editorial record. Preserve contrary evidence; do not silently adopt as release gate. |
| `Business/ideas/F-001-tam-build/PROPOSED-a11y_claimcheck.py` | `e1a820f87832a6669e0ed8b813b65acbd6539472` | **DEFER** | Proposed EPUB accessibility metadata-versus-content inspection, not wired into the build. Some judgments explicitly need a human editor; no final EPUB tested this run. |

**Evidence states:** Four SOURCE-READ blob matches; inherited 89-row classifications preserved, not 89 fresh body reads. **PRUNE** remains reversible set-aside, never deletion (TJ R3). No new Library promotion or second business pipeline. The new GPT-only F-001 review packet remains a candidate, not shared Library canon.
