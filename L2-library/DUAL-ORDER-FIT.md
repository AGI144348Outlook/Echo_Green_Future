# Dual-Order fit of the Library sub-libraries (R2)

Timothy's ruling R2 (2026-10-11): `AGI144348Outlook/dual-order-os` is the intended consolidation layer for all his repositories, and its Matrix/Index bidirectional structure is the reference schema for these sub-libraries. Read at dual-order-os 2d92938 (2026-08-10; README: "empty, marked shelves"). This note records where Claude's Library follows that structure and where it does not yet. Nothing here is canon (§13); first written 2026-10-11T22Z.

## Where it fits

| dual-order-os | Claude's Library | Fit |
|---|---|---|
| `/matrices/<table>/` — content-first: one kind of elemental part per table, index into its rows | `Matrices/REGISTER.tsv` | Fits. Z01 batch registered the genesis-documentary `matrices/*.json` tables here (algorithm, formula, number, equilibria, LHEA chains, lobby agents, Mashet corpus, VGM, WordNet chains). |
| `/indices/by-source-document/` — given a part, which document it came from | every `REGISTER.tsv` row (`branch, path, blob_sha, bytes, source_commit, retrieval_time`) | Fits in substance: each row is a by-source-document entry with a fingerprint (§15.1). It is stored per sub-library, not as one index folder. |
| `/indices/by-framework/` — given a framework, which parts belong to it | `Indices/REGISTER.tsv` + `cross_ref` column | Partial. `cross_ref` links an entry to other sub-libraries, not to frameworks (Mashet, LHEA, NVE-D, ECHO Governor). |
| `/libraries/` — importable code built from matrices/indices | `Algorithms/REGISTER.tsv` | Partial: Algorithms registers source code as references; nothing is built or imported from it yet. |

## Where it does not fit (yet)

1. **Seven sub-libraries vs two orders.** Contract 000 §3 fixes seven sub-libraries (Registry / Matrix / Index / Codex / Logic / Algorithm / Formula); dual-order-os has two navigation orders plus code. Registries, Codices, Logics and Formulas have no dual-order shelf. Proposed reading (PROPOSED): all seven are "matrices" in the dual-order sense (content-first tables of one kind of part), and the dual-order "indices" are views computed over all seven.
2. **No lookup-first indices yet.** `by-glyph`, `by-jurisdiction` and `by-framework` do not exist in this Library. They can be generated from the registers once a `framework` column is added (PROPOSED; additive, no row changed).
3. **Rows point to files, not elemental parts.** dual-order matrices hold parts (a root, a glyph, a constant); these registers hold whole files. Going down to part level is editing, which R3 places after registry formation.

## Next (PROPOSED)
- Add a `framework` column in a new append-only register version, then generate `Indices/by-framework.tsv` and `Indices/by-source-document.tsv` as derived views.

## Addendum 2026-10-11T23Z (Z02 resh-lattice-agency)

- **Fits:** the A-144/A-145/A-165..A-167 spec docs went to Logics, their code to Algorithms, the two sandbox run records to Registries, consistent with Z01.
- **Does not fit:** `matrices/echo_algorithm_matrix.json` exists in two different versions (genesis-documentary and resh-lattice-agency, different blobs). dual-order-os keeps one table per kind of part; the Library keeps one row per (branch, path) version, so Matrices now holds two versions of one table. Reconciling them into one table is editing and comes after registration (R3); both carry an A-000 "Governor" slot (DISC-002 / R5).


## Addendum 2026-10-12T00Z (Z03 algebra, rows 1–148)

- **Fits:** glyph cards (22 per copy) went to Codices with the glyph INDEX.md in Indices, matching dual-order-os's split of content-first entries (Matrix side) from lookup-first entries (Index side); `glyph_algorithm_index.json` and `tsadi_interrogative_index.json` went to Indices for the same reason.
- **Does not fit:** the same 23 glyph files sit at two paths on one branch (`ECHO_AutonomousAgency/docs/glyphs/` and `ECHO_GlyphRegistry/`, identical blobs, plus a zip of the second set). dual-order-os would hold one entry and point to it from the index; the Library keeps one primary row per (branch, path), so the card text is registered twice with `identical_blob_in=algebra` linking them. Collapsing them is editing and comes after registration (R3).
- A third version of `echo_algorithm_matrix.json` (`ECHO_AutonomousAgency/matrices/`, 13,024 bytes, also with an `A-000` key) is now in Matrices beside the genesis-documentary and resh-lattice-agency versions; relevant to RC-R5 (R5).
