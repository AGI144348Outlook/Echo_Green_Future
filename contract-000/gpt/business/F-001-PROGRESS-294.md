# F-001 TAM Protocol ebook — GPT run 294 source-pinned dataset verification (2026-10-23)

**Single continuing income project:** F-001 TAM Protocol ebook. **State: HOLD / REVIEW DRAFT ONLY.** Read existing F-001 decision sheet, §97–§100 shared plan, Claude PATCH-99, GPT run 293 test report and checkpoint. No new income pipeline, listing, publication, payments, outreach or spending. Claude owns proposed patch/build work; GPT supplies independent dataset integrity characterization. This is not a merge or deployment.

## Sources and method

- Public source repository `AGI144348Outlook/The-TAM-protocol` commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`; fetched its recursive tree via GitHub and fetched the two original datasets by pinned ref.
- Exact source Git blobs, independently checked with `git hash-object` after reconstructing the files from GitHub connector content: A `b62c970a660e0a6685b58db1ef121690daa4fce7` (610 bytes), B `12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4` (646 bytes).
- Exact `library-shared:Business/ideas/F-001-tam-build/rebuild_datasets.py` blob `fa3a62f76549ecaea6e226ba5cca41597000d790` (4,466 bytes). Executed `python3 -I -B rebuild_datasets.py <scratch-source> <scratch-output>` twice in separate clean output folders on Python 3.13.5 (Linux). Neither source repository nor shared Library was edited.
- Pre-test notice published **before testing** in Issue #13, comment `6360344954`. All output is local scratch data; no GitHub Actions, paid inference or Cloudflare calls.

## EXECUTION-VERIFIED results (real pinned source bytes, local builder)

Both runs returned **Dataset A: 6 rows, 0 rejected; Dataset B: 8 rows, 0 rejected**. Both output pairs and the report were byte-identical between the two runs:

| Artifact | SHA-256 |
|---|---|
| `dataset-a.csv` | `d3c176b9d2ff8041b093f46f28c7b56619d1e1cc3b3ea4841b12027e5ec826f2` |
| `dataset-b.csv` | `fecd151b5b7393fc69975a0b323e02c5f306eb1fd49bedc2901f849001e8afc5` |
| `dataset-check.json` | `036a85e5fe3b372c6ada0e0851f3463fd6da3e5d6ab825972cb454085f85dde4` |

Source-text SHA-256 reported by the builder: A `48437f58ee74a9a0226d901d1291b6c104764648fe7760ebbc91b74b6ba6a302`, B `bc16da657b19317e110cdcf4159a9118aa89f2cfc4f8183e7e3f1d94f2eb3b81`.

**Important new editorial discrepancy (SOURCE-OBSERVED + EXECUTION-VERIFIED):** Two of six Dataset A `stated_matches_recomputed` flags are **False**, despite 0 rejected parse rows:
- `Silver Droplet`: source states 3.42g / 0.25 Unit / `-0.03%`; builder computes expected 3.425g and `-0.146%`.
- `Small Scrap`: source states 1.71g / 0.125 Unit / `<0.01%`; builder computes expected 1.7125g and `-0.146%`.

These are **source-vs-formula inconsistencies**, not proof that the archaeological claims are true or false. Preserve original values and computed columns side by side; do not silently correct. They require Timothy/editorial disposition before publication.

## GPT read-only proposed receipt gate and characterization

Local draft `PROPOSED-f001-dataset-receipt-gate.py` (SHA-256 `070c75f7164d85847a89c9dfe9f5654f95095ae4d9d8483a5c00ebf49067c3a8`) pins both source Git blob IDs, builder Git blob ID, exact output SHA-256s, row counts, headers and zero-rejection report. It emits exit **1** for integrity failures, exit **2** for intact data needing editorial review, exit **0** only if neither remains. It is not integrated into the shared build. It records the source commit but does not independently verify Git commit ancestry, authorization, rights or claim validity.

Seven local fixture outcomes, all as expected:

| Delivered case | Exit | Observation |
|---|---:|---|
| Actual-source baseline | 2 | Integrity PASS, editorial HOLD (two False flags) |
| Truncated B CSV | 1 | Full-byte hash/row-count mismatch |
| Changed B ratio, unchanged mass | 1 | Full-byte hash mismatch |
| Changed B registry sign, unchanged mass | 1 | Full-byte hash mismatch |
| Missing B CSV | 1 | Missing artifact detected |
| Tampered dataset-check.json | 1 | Report digest/schema mismatch |
| Extra valid B row | 1 | Full-byte hash/row-count mismatch |

**Interpretation:** Claude's PATCH-99 remains useful as a quick structural/mass guard. The independent source-pinned full-byte gate adds coverage for truncated and non-mass-altered CSVs. The source's two discrepancy flags create a separate editorial release HOLD even when integrity is intact. An editable local gate and its embedded pins do not provide an independent security trust root.

**Limitations:** two dataset files only, not a complete Git clone; pinned source membership checked against GitHub tree metadata, not via local commit-object verification. Python 3.13.5 on one Linux environment, not cross-platform reproducibility. No EPUB/PDF build, Ace, EPUBCheck, listing, rights audit or production deployment; no scientific/archaeological claim validation. Source data and builder are already publicly accessible; local draft scripts and test output are in handoff package, not in shared Library.

## Deliverables and next action

- [x] One F-001 product identifier and existing shared plan/decision sheet.
- [x] Independently verify two source blobs and builder blob; clean rebuild twice; 6+8 rows, 0 rejected.
- [x] Document two unapproved numeric discrepancies as an editorial HOLD.
- [x] Test a proposed read-only source-pinned CSV integrity gate on seven actual-source-derived cases.
- [ ] Claude joint review of gate, PATCH-99 and four-artifact receipt; no overwriting Claude's work.
- [ ] Independently verify EPUB/PDF/source inclusion, accessibility, editorial claims, licence, credit, final hashes, and reproducibility across supported build environment.
- [ ] Resolve Timothy's A1–A6 and B6 release choices; B7 remains nonblocking.
- [ ] Explicit Timothy approval before any storefront, outreach, publication, spending or payment setup.

**Acceptance criteria:** all four delivered artifact hashes tied to approved source/build provenance; CSV full-byte/row/header checks pass; all editorial mismatches dispositioned; no unsupported claims; licensing/credit/terms and accessibility approved; Timothy authorizes launch. **Next action:** Claude compare the two Dataset A flags and the proposed receipt gate with §97–§100 before any integration; maintain F-001 HOLD.
