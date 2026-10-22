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

## Addendum 2026-10-12T07Z (Z12 dev-suite-datasets, Z13 dev-suite-integration-staging)

- **Index side fits well:** Z12's `directory/index.html` is a lookup-first list (`ENVIRONMENTS`) pointing to each environment, and each environment links back to `/directory/`. That is the dual-order-os Index/Matrix pair in small: the Directory is the Index, each environment (here only Datasets) is a Matrix object that stands alone. Filed: Directory, README and the root redirect to Indices; `datasets/index.html` (raw data stored unaltered with per-field provenance and sha256 verify) and `_headers` to Registries.
- **Does not fit:** per-environment browser storage (IndexedDB `lhea-env-<name>`) lives outside the repository, so its records cannot be registered here; only the shell that creates them can. Recorded, nothing built.
- **Seventh pointer:** Z13 `dev-suite-integration-staging` is the 03978f7 tree again (seven branch names, one tree). Same split as Z09–Z11. By-blob index still proposed, not built.

## Addendum 2026-10-12T08Z (Z14 mashet-parallel-pipeline-test, Z15 protocol-graft-prune-test, Z16 stress-test-002-clean rows 1–87)

- **Fits:** Stress-Test-002 `MANIFEST.json` is a lookup-first object (inputs by git blob id, exclusions, invariants) over a content-first corpus (`input/`), the same Index→Matrix direction dual-order-os uses. Both input blob ids equal the branch blobs (EXECUTION-VERIFIED), so the index points at exactly the matrix objects it names. Filed with the protocol in Algorithms (as Stress-Test-001 was), cross-ref Registries.
- **Fits:** the Mashet parallel harness keeps raw source, blind cells and informed candidates in separate outputs and reconciles only metadata (no promotion). That matches the Matrix rule "content stands alone; the index only points". Script to Algorithms, note to Logics.
- **Does not fit (recorded, nothing built):** a file whose stated purpose is to be removed (Z15 `graft-prune-sample.txt`) has no stable Matrix role. Under R3 it is PRUNED (set aside, fingerprint kept), not deleted; dual-order-os has no "set aside" state, so the PRUNE-LOG line is its only index entry.
- By-blob index (proposed 02Z) still proposed, not built; Z14 is the dev-suite-datasets tree plus 2 files, another case it would collapse.

### 2026-10-12T09:00Z addendum (S3 batch 12: Z16 rest, Z17 rows 1–58)
- **Fits:** the Recess session log is a content-first Matrix object (one run, its discoveries and counts) produced by a script; its natural Index entry is the trigger marker plus the workflow that wrote it. Filed in Registries as a run record, next to the trigger markers.
- **Does not fit (recorded, nothing built):** dual-order-os has no "generated by" edge between a Matrix object and the code that produced it; here that link exists only in the workflow text (DEFERRED) and this note.

### 2026-10-15T10:00Z addendum (S1 ADDENDUM-2 @ 9286882; S3 batch 13: Z17 rows 59–151)
- **Fits:** each crawler catalog pair is a Matrix object (`record.raw.json.gz`, the content) with its own Index card (`record.json`, lookup fields and the checksum that points back at the raw). 28/28 new pairs verify (EXECUTION-VERIFIED), so the card points at exactly its content.
- **Fits:** `echo_recess.py` (A-168) is filed in Algorithms; its generated output (`recess_session_log.json`, batch 12) is in Registries. The "generated by" gap noted at 09Z still has no dual-order-os edge; the link is recorded in the two register rationales only.
- **Does not fit (recorded, nothing built):** dual-order-os has no slot for "downloaded runnable helper" (`tutorial_download.sh`); DEFERRED like `IVS/bootstrap.sh`, with no Matrix or Index entry until a ruling.

### 2026-10-15T11:00Z addendum (S3 batch 14: Z17 rows 152–223, Z18 rows 1–44; S2 ADDENDUM-2)
- **Fits:** `echo/matrix/registry.py` (Z18) is the definition of the canonical Registry R_t=(E,I,M,H,P,C); filed in Registries as the schema-bearing object, with the Algorithms rows (`gov_index.py`, `index_pattern.py`) acting as the Index side that queries it. The bidirectional pair is recorded in the rationales only; no dual-order-os edge exists for "module that defines a matrix" vs "module that indexes it".
- **Fits:** `e12_ks_canvas_recess.py` (Algorithms) and its output `e12_recess_log.json` (Registries): same "generated by" gap as `echo_recess.py` at 10Z; recorded in rationales.
- **Does not fit (recorded, nothing built):** a sealed archive whose entries all equal unpacked blobs (`ECHO_Canvas_Recess_KSM.zip`, 28/28) has no dual-order-os slot for "container of already-registered items"; DEFERRED, no Matrix or Index entry. Same for `core-lexicon.zip` on main (not unpacked).
- **Does not fit:** four empty `__init__.py` package markers (one empty blob) carry no content; one primary row in Algorithms, three cross-refs, so the package structure is reproducible without inventing an Index card.

## Addendum 2026-10-15T15Z (Z26 research-discourse-registry, Z27 license-update)

- **Does not fit (naming):** `research-registry/matrices/*.md` (5 tables) are called matrices, but each row is a topic → pinned-commit link to a primary record, which is dual-order-os's lookup-first **index** role, not a content-first matrix. Registered in Indices; the folder name is recorded, not changed.
- **Fits:** contract, schedules, rulings, manifesto and approved coordination text went to Codices; discourse chapters, discussion records, plans and specs to Logics; the Conditions Registry and the Contract change log to Registries; the two DISC-002 probes to Algorithms (ast parse only).
- **Does not fit (live documents):** this branch's governing files keep changing; dual-order-os holds one entry per part, while the Library pins one blob per (branch, path) and adds later versions only through new addenda. A "current version" view would be a derived index (PROPOSED), not an edit.
- Z27's `LICENSE` is a second version of the root LICENSE (re-wrapped clause b, one changed byte on the attribution line); kept beside it in Codices, same as the three `echo_algorithm_matrix.json` versions in Matrices.

## Addendum 2026-10-15T20Z (reference schema: an unmerged dual-order-os branch)

- **Finding (SOURCE-OBSERVED, read only):** every earlier run used dual-order-os `main` @ 2d92938 as the R2 reference schema. The repository also has an unmerged branch `claude/github-claude-code-connection-98qkbx` @ 2d51593 (5 commits, 2026-09-11/12, author Timothy, merge base 2d92938; 50 → 60 files, +2,707 / −33 lines). It **populates** Matrices that are only scaffolded on `main`: `matrices/latin-roots/roots.json` (275 entries), `matrices/hebrew-glyphs/glyphs.json` (22), `matrices/algorithms/algorithms.json` (15: "14 real algorithms + 1 flagged design draft"), and fills the Index side: `indices/by-glyph/` keeps three unreconciled topology assemblies side by side (v1 forced-even, v2 shared-roots, v3 full-275), plus `indices/by-source-document/` and `indices/by-framework/`. All three JSON files parse as lists (EXECUTION-VERIFIED, `json.load`, scratch only).
- **Fits:** "preserve all three unreconciled topology assemblies" is the same rule as R3 here (no deletions; versions kept side by side, e.g. the three `echo_algorithm_matrix.json` versions in Matrices). A populated `by-framework` index is the framework column this file listed as a next step on 22Z; its shape can be followed once Timothy says which branch is the reference.
- **Does not fit / open:** the branch is not on `main`, so it is not clearly the "intended" layer under R2. Nothing was registered from it (dual-order-os is read only and outside the Library sources, §13). Question for Timothy logged in CHECKPOINT: is this branch part of the reference schema, or a draft?

## 2026-10-16T11Z addendum — archive members

- **Convention (new):** a member of a sealed archive is registered once as `<archive path>!/<member path>` on the branch where the archive was first read; the same blob inside another archive is named in `identical_blob_in` as `<branch>:<archive>!/<member>`. The archive row itself stays one sealed bundle (Matrix: content-first entry for the bundle; Index: the member rows give the lookup-first view into it).
- **Where dual-order-os does not fit:** its Matrix/Index pair has no notion of a container whose members are addressable but not unpacked. The `!/` path is a local extension, not a dual-order-os convention; it can be re-mapped when dual-order-os defines one.

## 2026-10-22T11Z addendum — dual-order-os main 2d92938 → 2977b2d (catalog box, by-component index)

- **Source (SOURCE-OBSERVED, read only):** dual-order-os `main` moved 2d92938 → 2977b2d (8 commits by Timothy, 2026-10-20; +2,721 lines, 31 files, nothing removed). New shelves: `components/catalog-box/`, `matrices/catalog-box/` (`matrix.json` blob ba7540c), `indices/by-component/`, `libraries/catalog_box.py` (blob a7235f9), `tests/test_catalog_box.py`, `research/progression/001…006`. The unmerged branch `claude/github-claude-code-connection-98qkbx` @ 2d51593 is still not merged (the 15T20Z question stays open).
- **Tests (EXECUTION-VERIFIED):** `python3 -m unittest discover -s tests -p test_catalog_box.py`: 13/13 OK under Python 3.13.16, in scratch only (stdlib sqlite, temp databases; no network or subprocess imports).
- **Fits:** this is the first dual-order-os Matrix on `main` with a written identity rule: `identity = [section, id, revision]`, references "pin exact revision", there is no delete API, and the bodies are data only, never executed. That matches this Library: sub-library = section, `branch:path` = id, the pinned `blob_sha` plus later addenda = revisions, no deletions (R3), and nothing registered gets run. `indices/by-component/` is a lookup-first view onto one matrix. It has the same shape as the "views computed over all seven" reading proposed in 11T22Z item 1.
- **Does not fit:** (a) catalog-box records live in a caller-chosen SQLite file outside Git. Here the registers *are* the Git files, and a revision is a new addendum row, not a numbered revision in place. (b) Catalog-box revisions are sequential integers. Here a version is identified by blob SHA, so "revision 2" has no meaning without a derived ordering (PROPOSED: derive it from the addendum order; no row changed). (c) No `components/` shelf exists here. Nothing registered so far is a reusable component in that sense.
- Nothing registered from dual-order-os (read only, outside the §13 Library sources).
