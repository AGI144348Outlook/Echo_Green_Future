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

## Addendum 2026-10-12T01Z (Z03 algebra, rows 149–278)

- **Fits:** `lobbies/glyph/NN-NAME/lobby.json` (22) + `registry.json` went to Registries and the lobby README to Indices: per-glyph records on the content side, one lookup entry on the index side, as in dual-order-os. `indices/by-notebook-section/`, `indices/by-symbol/` and `indices/cross-substrate/` are this branch's own lookup-first indices and sit in Indices; they are the closest thing yet to dual-order-os's `/indices/by-*/` shelves.
- **Does not fit:** `matrices/` on this branch mixes table kinds under one folder (`formulas/`, `glyphs/`, `grammar/`, `substrates/`, `symbols/`). The Library splits them by sub-library (formula registry → Formulas, Mashet instruction manual JSON → Codices, the rest → Matrices); dual-order-os would keep them all as matrix tables. Recorded, not resolved.
- `pwa/` is an app bundle (static PWA + Pyodide runner). It has no dual-order shelf; registered in Algorithms as reference code, with its `wrangler.toml` DEFERRED (deploy config).

## Addendum 2026-10-12T02Z (Z04 autonomous-agency, rows 1–150)

- **Does not fit (again, larger):** every one of the 148 current Z04 rows read so far is a byte-identical copy of a row already registered from algebra, genesis-documentary, resh-lattice-agency or main. dual-order-os would hold one matrix entry per object and point to it from each branch's index; the Library keeps one primary row per (branch, path), so 123 new primaries are cross-references in practice (`cross_ref=<branch>:<path>`). A derived "by-blob" index (blob → all branch paths) would be the dual-order-os shape; proposed, not built (registration before editing, R3).
- **Fits:** the two machine-appended session logs that changed after listing stay out of the register until re-listed, so the content side never points at a blob that is no longer at the head.

## Addendum 2026-10-12T03Z (Z04 autonomous-agency, rows 151–242)

- **Confirms the 02Z note:** all 92 remaining rows are byte-identical to rows registered earlier (by preferred reference: algebra 63, genesis-documentary 20, resh-lattice-agency 7, main 2), so Z04 adds no new content to the Library: 240 of its 242 listed rows mirror earlier blobs; the other 2 are the stale session logs. Z04 is the clearest case for the proposed by-blob index (dual-order-os: one matrix object, many index pointers). Still proposed, not built.
- **Fits:** `matrices/echo_*.json` (9) went to Matrices and `src/`, `tests/`, `pwa/` code to Algorithms, as on the earlier branches, so the sub-library of a blob does not depend on which branch it was read from.

## Addendum 2026-10-12T04Z (Z05 dev-suite, Z06 dev-suite-registries, Z07 dev-suite-matrices)

- **Branch-name vs content (does not fit as named):** `dev-suite-registries` and `dev-suite-matrices` (and, by `git ls-remote`, `-indices`, `-codices`, `-logics`, `-algorithms`, `-integration-staging`) all point at the same commit 03978f7, so the branch names are lookup labels (Index side), not content partitions (Matrix side). Their files were filed by content: e.g. `registries.json` to Registries and `echo_matrices.json.gz.b64` to Matrices on both branches. In dual-order-os terms this is seven index pointers onto one matrix object, the case the by-blob index proposed at 02Z would make explicit. Still proposed, not built.
- **Archives:** zip archives whose members are only partly listed elsewhere (dev-suite-branch.zip, echo-notebook-0.4.1.zip, echo-notebook-pwa.zip) have no natural slot in the Matrix/Index pair; they were DEFERRED until their members' branches are read, rather than filed whole.

## Addendum 2026-10-12T05Z (Z08 dev-suite-indices, Z09 dev-suite-codices)

- **Confirms the 04Z branch-name note:** both branches are the 03978f7 tree again, so Z08 and Z09 add 78 register rows but no new content; each row mirrors Z07. A branch named `-indices` and one named `-codices` received the same sub-library split (Algorithms 23, Registries 9, Indices 3, Codices 2, Matrices 1, Logics 1 per branch), because filing follows content, not the branch label. In dual-order-os terms these are two more index pointers onto the same matrix objects; the by-blob index (proposed 02Z) is still proposed, not built.

## Addendum 2026-10-12T06Z (Z10 dev-suite-logics, Z11 dev-suite-algorithms)

- **Six branches, one tree:** Z06–Z11 all point at 03978f7 (`git rev-parse`, EXECUTION-VERIFIED). Z10 and Z11 add 78 register rows (same split as Z09: Algorithms 23, Registries 9, Indices 3, Codices 2, Matrices 1, Logics 1 per branch) and no new content. In dual-order-os terms the 03978f7 tree is one set of matrix objects now reached through six branch-name index pointers; the register carries all six (R3: everything stays as a dataset) but a by-blob index (proposed 02Z, still not built) would show them as one object with six names. Z12 `dev-suite-datasets` (f1949f7) is the first branch since Z05 with new blobs (8 of 59 rows), so it needs a real read next run.
