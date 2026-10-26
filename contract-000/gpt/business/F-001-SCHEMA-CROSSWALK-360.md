# F-001 — real Run 358 CSV to pinned Run 334 stage: structural incompatibility (Run 360)

**Project F-001 TAM Protocol ebook; status HOLD / NOT LAUNCH-READY.** Continue existing F-001 only; no new income pipeline. [Prospective test plan](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6405917004) was published **before** the diagnostic. [Actual results and narrative](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6405947402) were posted afterward in the same Issue.

## Source pins and method

Authenticated GitHub reads of exact Run 358 committed files: `dataset-a.csv` Git blob `8ef7fa41ef0229ce9a2754737f0aa0e774fd3b7b`, `dataset-b.csv` `0df0e4153cf2ae9c292dd05588485e13bfd999f3`, `dataset-check.json` `0f333dd8d9a86dff947883bd41d46a585dc83c59`. Read pinned Run 334 builder `F-001-REBUILD-DATASETS-334.py` blob `e8af6e5f011ec3e827c94737c717937944924eb8`; gate 344 `5d5bb8f85db7f21c50ca71625e82c51102fed088`; consumer 347 `b2a97390ba39959cd2f86a5e51ea186348f31fb2`; coordinator 351 `68eea27de6e9a961f31122a08585ee6e24fed2df`. The separate shared `rebuild_datasets.py` is Git blob `fa3a62f76549ecaea6e226ba5cca41597000d790`, **not** the pinned Run 334 builder. Read these sources before running a pure-JavaScript V8 structural crosswalk; no Python source was executed.

## Actual observations

- Actual Run 358 Dataset A has **9 columns**; pinned Run 334 builder requires **11** (adds `within_0_01_pct_points_of_recomputed`, `calculation_method_from_source`, `terminology_conflict` while replacing `stated_matches_recomputed`).
- Actual Run 358 Dataset B has **8 columns**; Run 334 requires **9** (adds `terminology_conflict`).
- Actual Run 358 `dataset-check.json` contains `base_g_per_unit` and `files`, but lacks `source_commit` and both A/B `git_blob` attestations required by gate/consumer.
- Gate/consumer/coordinator reference the same pinned Run 334 builder, but the Run 358 outputs came from the shared builder. The mismatch is an **expected version distinction**, not evidence that the Run 334 builder fails.
- The real Run 358 fixture was rejected for **five reasons**: `A_HEADER_NOT_334`, `B_HEADER_NOT_334`, `SOURCE_COMMIT_NOT_ATTESTED`, `A_SOURCE_BLOB_NOT_ATTESTED`, `B_SOURCE_BLOB_NOT_ATTESTED`.
- **9/9 V8 structural assertions passed:** one real-fixture negative, one synthetic structural-positive, and seven deliberate header/source/count/rejection negatives. [Machine-readable results](F-001-SCHEMA-CROSSWALK-RESULTS-360.json); [reproducible Node structural preflight](F-001-SCHEMA-CROSSWALK-360.js). Synthetic structural success is not digest or stage success.

## Interpretation, limits and next action

**The Run 358 real CSVs are review data, not byte-compatible inputs for the pinned Run 334 staging chain.** Never fabricate missing attestations or self-repin changed output to force a pass. To complete the product, obtain a clean pinned public TAM checkout at `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`; run the exact independently pinned **Run 334** builder through the bounded coordinator on an isolated preexisting stage root; verify SHA-256 output pins, a fresh `STAGED_ONLY` gate notice, consumer HOLD receipt and altered-input rejection, under a **new prospective Issue pre-test**. The Python stage coordinator and real TAM rebuild were **NOT RUN** this run; no raw SHA-256 was recomputed, and no real EPUB/PDF, accessibility, manuscript claims, rights, CI or release verification occurred. The attempt to fetch public GitHub raw files into the local Python container failed due to unavailable DNS, so no local source checkout was assembled. GitHub connector source reads succeeded. No new account, outreach, spending, payment, publication, paid inference, Cloudflare loop, shared Library change or private Testament access.

**Claude complementary review:** independently check the versioned builder headers and receipt requirements, then handle Gerah, ratio-1 rounding convention, editorial claims and rights. **Timothy blockers:** A1–A6, B6/C1, credit, licence, source branch, identifier, final signoff. **F-001 remains HOLD.**
