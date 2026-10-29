# F-001 Run438 — eight-source connector-side candidate replay (actual prospective-test results)

**Pre-test:** [Issue #118](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/118) published BEFORE this diagnostic. **Project:** F-001 TAM Protocol research-notebook ebook only, **HOLD / NOT LAUNCH-READY**.

## Method and provenance

Read unmodified original Python `library-shared:Business/ideas/F-001-tam-build/claim_scan.py@31f3dcff486c4c8cc96d514eb425da86834d00c3`, and earlier GPT 42-row manifest `contract-000/gpt/business/F-001-CONNECTOR-CLAIM-CANDIDATES-436.json@6a34737cf9c0da3fabbc5ad3efbec4c984b7a41d`. Fetched **all eight public** TAM source texts through the connected GitHub read tool at exact commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`. Compared each returned Git blob SHA to the manifest. Reimplemented Python's `sentences()` split and four `TRIGGERS` regexes in bounded JavaScript, comparing source file, 1-based sentence number, trigger names and 170-character excerpt to each old row.

| TAM source | Verified Git blob SHA | Replayed candidates |
|---|---|---:|
| `README.md` | `213bcfaf560dcc54fbb7ae79fad932e86b660357` | 1 |
| `Article 1 Hacksilber` | `237bd3335abdcc0f0465817dffe01ad6eaa86055` | 2 |
| `Article 2 Water Weight Computes` | `ec657c3fa0f70da9686fb1ae52983d28f77c6c4c` | 3 |
| `The Color Dyed and Dental Records` | `b525ad60ab37cb2d72ea43c40ba687b0fe2a348d` | 3 |
| `Article 5` | `c8c1bf617c0d81389f6c2408ed975131695857ff` | 3 |
| `Article 6` | `662d745f0b9b41236d1053cdbaa9351f7c020dd0` | 3 |
| `Article 10` | `e82be564872f636662652d34dcb8d3437559f84f` | 4 |
| `Collective information` | `710ad3cd4feeae7bafa329d7437a78df4c40cfa8` | 23 |
| **Total** | **8/8 source pins matched** | **42** |

**Observed:** 42 current candidates; **0 missing coordinates, 0 extra coordinates, 0 trigger differences, 0 excerpt differences** against the Run436 manifest once its existing **170 UTF-16 code-unit** excerpt convention was applied. No source fetch failed. This is an independently repeated connector-side extraction at the same immutable commit, not an independent programming-language parity test.

**Deviation disclosed:** first diagnostic used a **160-character** excerpt assumption, producing 19 excerpt-only differences (coordinates and triggers all matched). Inspection of the prior manifest revealed 170-character truncation; the prospective comparison was rerun with 170 and produced 42/42 exact matches. This correction was a comparison-format fix, **not a change to the source or trigger rules**.

**Limitations:** Original Python scanner on an actual eight-file local TAM snapshot **NOT RUN**; no independent raw-byte SHA256, no JS/Python Unicode regex equivalence proof, no full coordinator, no final EPUB/PDF or Android checks. Git blob SHA comparison is connector-returned metadata, not independent local hashing. A repeated JS scan does not prove archaeological, scientific, statistical or copyright claims. The 42 regex candidates are separate from **82 human editorial occurrences**, all still UNREVIEWED. No release authorization.

**Next:** acquire exact eight raw source files through an authorized container path, run original `claim_scan.py` behind the existing fail-closed source and output gates, and reconcile outputs; Claude independently reviews source evidence/rights, Timothy adjudicates release decisions. No second project or consequential action.
