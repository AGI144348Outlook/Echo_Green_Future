# F-001 — Run 357 source-pin and arithmetic audit (2026-10-25 ~17 CT)

**One continuing product:** F-001, TAM Protocol ebook. **HOLD / NOT LAUNCH-READY**. Prior [Run 356 progress](F-001-PROGRESS-356.md) and [14-case synthetic package-chain test](F-001-TEST-EVIDENCE-356.md) read first. [PRE-TEST Issue #53](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6403958386) was published **before** this static inspection/diagnostic. No Python builder execution, no CI, no real EPUB/PDF or publication. This is a **source identity checkpoint**, not a self-signed release proof.

## Direct GitHub observations (not assumptions)

- Source repository [The-TAM-protocol at pinned commit](https://github.com/AGI144348Outlook/The-TAM-protocol/commit/d46456a18fe412398d0ae37ec5a8c4eebb44e0c9) resolves; its Git tree SHA equals the pinned commit SHA `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9` (a valid Git coincidence when the commit's tree object is itself at that SHA? **Correction:** see the note below). Dataset A blob `b62c970a660e0a6685b58db1ef121690daa4fce7`, Dataset B blob `12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4`, README blob `213bcfaf560dcc54fbb7ae79fad932e86b660357`. Both dataset blob identities matched the returned tree entries.
- Shared `library-shared:Business/ideas/F-001-tam-build/rebuild_datasets.py` blob `fa3a62f76549ecaea6e226ba5cca41597000d790` has exact `A_FILE` and `B_FILE` strings matching the two public source paths. This establishes *path identity in the source*, not that a local clone, runtime or output CSV was independently checked.
- Dataset A source contains **six** actual data lines (plus a header and a `Source:` prose line). Dataset B contains **eight** numeric data lines. A first loose numeric-line filter also matched Dataset A's `Source:` line, giving 7 candidate lines; the builder's explicit `line.startswith("Source:")` exclusion correctly prevents counting it as a data row. **No Python builder run was performed.**
- The source has no standalone `Article 4` path in this pinned tree. Article 6 and Article 10 exist as separate blobs (`662d745f0b9b41236d1053cdbaa9351f7c020dd0`, `e82be564872f636662652d34dcb8d3437559f84f`). This is a *path observation*, not proof of whether Article 4 content appears within other documents.

## Independent arithmetic check of six source A lines

Using the builder's stated formula `expected_g = 13.7 * units` and `round((measured - expected)/expected*100, 3)` on the **read text**, without invoking the Python builder:

| Source object | Mass g | Units | Stated deviation % | Recomputed % | Within builder tolerance? |
| --- | ---: | ---: | ---: | ---: | --- |
| Ingot Slice (Heavy) | 136.98 | 10 | -0.01 | -0.015 | YES |
| Coiled Wire (Large) | 68.52 | 5 | +0.03 | +0.029 | YES |
| Hacksilber Scraps (x3) | 13.71 | 1 | +0.07 | +0.073 | YES |
| Flattened Foil | 6.86 | 0.5 | +0.14 | +0.146 | YES |
| **Silver Droplet** | **3.42** | **0.25** | **-0.03** | **-0.146** | **NO** |
| **Small Scrap** | **1.71** | **0.125** | **<0.01** | **-0.146** | **NO** |

**Observed:** exactly the two flagged rows disagree with the builder's arithmetic predicate. The data are not silently corrected. **Interpretation:** editorial disposition is necessary; source fidelity is not the same as empirical historical validation. The numerical claims and wider archaeological interpretations in the manuscript require human review; this audit verifies neither their historical truth nor source rights.

## Trust boundary, test result and limitations

The machine-readable [source inventory](F-001-SOURCE-INVENTORY-357.json) records exact Git object identifiers, public source paths and the unchanged F-001 identifier, with `release=HOLD` and `publication_authorized=false`. Git blob SHA-1 identifiers are **not interchangeable** with raw-byte SHA-256 expected in `dataset-check.json`. The inventory was assembled by GPT from connector reads, so it cannot itself serve as an independently trusted publication pin or prove that a local clone matches. No Git tree commit signature, external timestamp witness, third-party archival copy, or independently reviewed release package was obtained.

**Correction of terminology:** the Git tree endpoint accepted a commit-ish `d46456a...` and returned a top-level `sha` of that same value; treat it as the *requested resolved ref*, not independent proof of the underlying tree object's SHA. The two **blob entries** and fetched blob contents were independently compared for identity. Do not cite the endpoint's `sha` as a verified tree object identifier without reading the commit's `tree.sha` separately.

**Prospective expected:** both input blob identities and builder path strings match. **Observed:** matched. **Challenge observed:** two source-stated Dataset A percentages fail the builder's tolerance; an external pin and editorial rulings remain missing. **Not run:** actual Python parser/rebuilder, independent TAM clone/CSV SHA-256 rebuild, three-script stage coordinator, EPUBCheck/Ace/PDF, hostile-writer concurrency, manuscript claims/rights or storefront gates. No paid inference, Cloudflare loops, outreach, account creation, spending or publication.

**Next single GPT action:** independently verify the exact source commit/tree and bytes through an authorized read-only clone, preregister and run the real dataset rebuild and F-001 HOLD bundle checks, then cross-check the two discrepancy dispositions. **Claude complementary action:** continue claims/rights/listing review and independently challenge whether the two numeric mismatches should remain flagged in the review edition. **Timothy blockers:** F-001 A1–A6, B6/C1, two Dataset A discrepancies, Gerah 1/8 vs 1/16, claim/credit/licence/book-ID decisions and explicit publication authority.
