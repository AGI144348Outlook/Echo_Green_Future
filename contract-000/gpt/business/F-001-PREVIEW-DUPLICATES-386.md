# F-001 TAM Protocol ebook — source-preview integrity and duplicate editorial workload (Run386)

**Sole project:** F-001. **State:** HOLD / NOT LAUNCH-READY. **PRE-TEST and addenda:** [Issue #59](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/59) (published before diagnostics). **Inputs read:** [F-001 decision sheet](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-decision-sheet.md) blob `2975edcc`, Run385 progress, Run383 45-card editorial queue blob `3346ad7583225d82ddf435f8daf691c78aca7330`, original Python scanner blob `31f3dcff486c4c8cc96d514eb425da86834d00c3`. Public TAM source commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`. No private material or live customer data.

## Observations — actual pinned public source text, GitHub connector + isolated JS diagnostic

All **8/8 source files** returned expected Git blob SHAs; all **45/45** editorial previews matched the **prefix** of their numbered source sentence. **Only 25/45** were complete sentence-equal. The other **20/45 previews were truncated at exactly 155 characters** (their full sentences are longer). This clarifies previous reports of 45/45 "source bindings": prefix binding is true; complete-sentence equality is not. The first targeted 14-card check initially yielded **10/14 full-equality**, which led to the separately preregistered full inventory diagnostic. No incorrect prefix or source-blob mismatch was observed.

The 45 occurrence IDs represent **38 distinct normalized sentence texts**: **7 exact duplicate groups** (14 occurrences, 7 additional copies). The duplicate pairs are:

| Original article | Duplicate in Collective information | Priority |
| --- | --- | --- |
| Article 6#S4 | Collective information#S153 | P2 |
| Article 6#S23 | Collective information#S172 | P1 |
| Article 6#S29 | Collective information#S178 | P2 |
| Article 10#S3 | Collective information#S293 | P1 |
| Article 10#S4 | Collective information#S294 | P2 |
| Article 10#S5 | Collective information#S295 | P1 |
| Article 10#S8 | Collective information#S298 | P1 |

Thus the existing **18 P1 + 27 P2 occurrence cards** include four duplicate P1 pairs and three duplicate P2 pairs; **14 distinct P1 / 24 distinct P2 sentence texts** under the exact normalized-text criterion. Do **not** delete, merge, auto-approve, or alter any occurrence card: each retains its own source position and review status. A reviewer may reuse one evidence analysis across matching text, but should still check context and disposition separately.

**Limit:** the connector-side sentence check used a JavaScript translation of the Python splitter; the original Python scanner was **NOT executed against the eight actual files**. The original Python claim scanner's 42 baseline candidate result and three supplemental candidates are inherited from earlier source-bound investigations, not newly reproduced by Python here. Container GitHub DNS failed with `Temporary failure in name resolution`; this blocked safely materializing all eight source files in Python. No Run358 CSVs or source files were changed.

## New executable development

[Read-only offline audit](f001_editorial_source_audit_386.py) accepts the existing queue JSON and a local directory of eight pinned TAM sources. It verifies each card's Git blob SHA, sentence number, preview prefix, UNREVIEWED status, unique occurrence ID, source-path safety, and HOLD flag; it reports full-sentence hashes, explicit `excerpt_is_truncated` flags and duplicate full-sentence groups. It does not rewrite source, queue or manuscript. [Tests](test_f001_editorial_source_audit_386.py) were executed locally: **10/10 synthetic Python unittest cases passed**, including positive, missing file, changed blob, wrong excerpt, symlink, duplicate ID, invalid sentence index, traversal, release flag and unauthorized status. Committed code Git blob `69b8605835be21f16fd91b6ee4b37ccb636082ea`; test blob `8ad257badff9e7059df7c02c7f04a3e1e5382fa8` both matched locally tested bytes.

**Important distinction:** synthetic tests demonstrate expected gate behavior, not that the Python audit was executed against all eight actual TAM files. The 45-card source-prefix and duplicate checks were connector-side JavaScript diagnostics. The gate always reports HOLD and does not grant release authority.

## Coordination, acceptance and next action

**Claude:** use the seven duplicate pairs to avoid duplicating *evidence gathering* while preserving independent source-context review; prioritize the four P1 groups, the 20 truncated previews, Article 4, Gerah and rights. Please independently review the offline audit before adoption. **GPT next:** replay original pinned Python scanner and this audit on all eight actual source bytes when safely materialized; then independently trace 334→344→347→351 staging without changing Run358 CSVs. **Timothy:** A1–A6/B1/B4/B6/C1 and explicit release authority remain open. All **45 cards remain UNREVIEWED**; editorial claims are neither fact-checked nor cleared. No new income project, account, payment, outreach, publication, CI, paid inference or Cloudflare loop.
