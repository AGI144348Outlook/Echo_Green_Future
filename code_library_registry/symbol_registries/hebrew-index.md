# Hebrew Index (2026-10-09)

**Status:** index for the Hebrew registry that is still to be built. This file gathers what already exists in one place. Nothing here is a validated registry entry.
**Role (Declared, R-ROLE-2):** `Hebrew ≈(verbs`
**Labels:** **Declared** = Timothy stated it. **Source** = taken from a named document. **Open** = waiting on Timothy or on a source.

Letters are stored exactly as typed, in logical (typed) order (R-BD-1).

## 1. The 22 letters

Columns:
- **SY group**: the Sefer Yetzirah division into Mothers, Doubles and Simples. Its source is not yet archived; see §3.
- **Latin root**, **J** and **T / C**: from LHEA. The source is the project doc `Latin Root Hebrew logic .pdf`, section 3.3. T is topology and C is closure.
- **Gem.**: standard gematria. The same table is used in `echo_governor_skeleton.py`.

| # | Letter | Name | SY group | Gem. | Latin root (operator / operand) | J | T / C |
|---|---|---|---|---|---|---|---|
| 1 | א | Aleph | Mother | 1 | ORIRI (Origo / Ortus) | J16 | Composite / Open |
| 2 | ב | Bet | Double | 2 | CLAUSTRUM (Clausura / Clausum) | J19 | Enclosure / Partial |
| 3 | ג | Gimel | Double | 3 | FERRE (Latio / Latum) | J3 | Transitive / Open |
| 4 | ד | Dalet | Double | 4 | LIMEN (Liminatio / Limen) | J21 | Threshold / Partial |
| 5 | ה | He | Simple | 5 | MITTERE (Missio / Missum) | J8 | Projective / Open |
| 6 | ו | Vav | Simple | 6 | JUNGERE (Junctio / Junctura) | J11 | Linear / Closed |
| 7 | ז | Zayin | Simple | 7 | SCINDERE (Scissio / Scissum) | J13 | Aperture / Broken |
| 8 | ח | Chet | Simple | 8 | FINIS (Finitio / Finem) | J20 | Enclosure / Closed |
| 9 | ט | Tet | Simple | 9 | VERTERE (Versio / Vertex) | J9 | Contained / Closed |
| 10 | י | Yod | Simple | 10 | RADIX (Radicatio / Radicem) | J18 | Point / Closed |
| 11 | כ | Kaf | Double | 20 | FUNDUS (Fundatio / Fundamentum) | J17 | Vessel / Partial |
| 12 | ל | Lamed | Simple | 30 | DUCERE (Ductio / Ductus) | J4 | Ascending / Open |
| 13 | מ | Mem | Mother | 40 | FLUERE (Fluxus / Flumen) | J1 | Enclosure / Open |
| 14 | נ | Nun | Simple | 50 | CADERE (Casus / Casum) | J5 | Descending / Open |
| 15 | ס | Samech | Simple | 60 | STARE (Status / Statio) | J2 | Circular / Closed |
| 16 | ע | Ayin | Simple | 70 | VACUUS (Vacuatio / Vacuum) | J24 | Forked / Open |
| 17 | פ | Pe | Double | 80 | MITTERE (Missio / Missum) | J8 | Enclosure / Partial |
| 18 | צ | Tsadi | Simple | 90 | TENDERE (Tensio / Tentum) | J7 | Hooked / Partial |
| 19 | ק | Qof | Simple | 100 | MUTARE (Mutatio / Mutatum) | J22 | Descending / Partial |
| 20 | ר | Resh | Double | 200 | SURGERE (Surrectio / Surrectum) | J6 | Curved / Open |
| 21 | ש | Shin | Mother | 300 | MUTARE (Mutatio / Mutatum) | J22 | Branched / Open |
| 22 | ת | Tav | Double | 400 | FINIS (Finitio / Finem) | J20 | Crossed / Partial |

LHEA facts worth carrying into the registry:

- **Shared roots, different manner.** Three roots are shared by two letters each, told apart by topology:
  - He and Pe (MITTERE);
  - Qof and Shin (MUTARE);
  - Chet and Tav (FINIS).
- **Root and manner.** The Latin root gives the *type* of operation; topology gives the *manner*.
- **Operator and operand.** A letter in operator position uses the root's action noun; in operand position, its result noun.
- **The 22×22 matrix.** Cell (i, j) = row letter acting on column letter. That gives 484 ordered cells.
- **Self-reference.** ר acting on ר is the only self-referential cell.
- **Jurisdictions with no letter.** Seven of the 26 Latin jurisdictions are no letter's primary root: J10 FRANGERE, J12 SOLVERE, J14 CRESCERE, J15 PONERE, J23 TENSIO, J25 NEXUS, J26 PATI. Two of them, J23 and J26, are among the jurisdictions LHEA says a correct parse of the consent paradox needs.
  - **Open:** are these gaps, or are they reached only through combinations?

## 2. Final forms and marks

| Base | Final | Gem. (extended) |
|---|---|---|
| כ | ך | 500 |
| מ | ם | 600 |
| נ | ן | 700 |
| פ | ף | 800 |
| צ | ץ | 900 |

**Open (LHEA Q4):** do final forms traverse separately or share their base letter's profile? LHEA proposes that final forms traverse only entries in terminal position.

Vowel and cantillation marks (U+0591–U+05C7) are combining characters with no letter profile yet. The Pad's KB3 Hebrew set already carries the vowel marks. Whether marks are registry entries of their own, or modifiers recorded on a letter entry, is **Open**.

## 3. Sefer Yetzirah material

**Status:** discussed, not yet archived. No repo or project doc holds the text. The only existing mention is a passing one in "Diagram Assessment – Mashet–Indus–Hebrew.txt".

The grouping in §1 is the book's standard structural division, which every edition shares:
- **3 Mothers:** א מ ש
- **7 Doubles:** ב ג ד כ פ ר ת
- **12 Simples:** ה ו ז ח ט י ל נ ס ע צ ק

The book's further correspondences differ between versions, so they are left empty until a text is archived:
- elements for the Mothers;
- planets, days and paired opposites for the Doubles;
- signs, months and senses or faculties for the Simples;
- the 231 Gates, which is C(22,2) unordered pairs.

**Next step:** archive one public-domain translation with its provenance. Candidates:
- Isidor Kalisch, *A Sketch of the Talmud… Sepher Yezirah* (1877);
- W. Wynn Westcott, *Sepher Yetzirah* (1887).

The versions are also disputed (Short, Long, Saadia, Gra), so the registry records which version every correspondence comes from.

**Link to LHEA:** the 231 Gates are unordered pairs. The LHEA operator matrix is 484 ordered cells: 22×22, including the diagonal. LHEA states the difference itself (484 rather than 231) and explains it by operator and operand.

## 4. Modular algorithm components

**Reading, waiting on Timothy:** "the modular algorithm components, which is in the Library already" is taken to mean the modules below and the CLR-0017 assessment. The Hebrew column is intentionally empty: no letter assignment has been declared, and Claude does not assign one.

| Module | Mechanism (from its README) | Hebrew letter(s) |
|---|---|---|
| [MOD-0001](../modules/MOD-0001-verified-resource-gate/) | Verified resource gate: authorize → create → verify layout → expose storage | unassigned |
| [MOD-0002](../modules/MOD-0002-bounded-composition-search/) | Bounded breadth-first primitive composition | unassigned |
| [MOD-0003](../modules/MOD-0003-structured-workspace-registry/) | Structured workspace registry: collections, items, relations | unassigned |
| [MOD-0004](../modules/MOD-0004-safe-relative-entry-writer/) | Safe relative entry writer | unassigned |
| [MOD-0005](../modules/MOD-0005-bounded-affinity-admission/) | Bounded affinity admission: similarity window, weighted ties | unassigned |
| [MOD-0006](../modules/MOD-0006-static-python-flow-outline/) | Static Python flow outline (AST) | unassigned |
| [MOD-0007](../modules/MOD-0007-actor-scoped-command-admission/) | Actor-scoped command admission | unassigned |
| [MOD-0008](../modules/MOD-0008/) | Timezone schedule decision: parse schedule, evaluate due | unassigned |

**[CLR-0017](../assessments/CLR-0017_EXECUTABLE_OPERATOR_HEBREW_BASIS.md)** is the existing *method* for indexing an operator to the Hebrew letters. It works like this:
- it fixes 22 d×d matrices as a basis;
- it decomposes any operator by least squares: W ≈ Σ c_j ℓ_j;
- its words are ordered products of operators.

**Proposed:** an operator indexed to Hebrew is described by its coefficient vector c, with one weight per letter, rather than by a single letter. Two things would then make CLR-0017's basis line up with the table in §1:
- a module's mechanism, read as Latin jurisdictions (the J column), would give the candidate letters;
- the 22 basis matrices would need to follow the LHEA order, א through ת.

## 5. Related files

| File | What it holds |
|---|---|
| `README.md` (this folder) | Plan of record for all symbol registries |
| `rules-snapshot-2026-10-08.json` | Frozen copy of the rules in D1 (R-ROLE-2 etc.) |
| `../design_notes/neuroplasticity-candidate-algorithms.md` | Neuroplasticity candidate algorithms, the mechanisms behind R-ROLE-13 / R-NEU-1 |
| `../../Algorithms/Stress-Test-001/input/glyph-registry-INDEX.md` | Existing glyph registry index (stress test input) |
| Project docs: `Latin Root Hebrew logic .pdf`, `Latin-Hebrew Execution Architecture (LHEA).pdf` | LHEA source for §1 (not in this repo) |
| Cloudflare D1 `mashet-stamp-registry`: `latin_roots`, `latin_prefixes` | Latin side of the profiles |

## 6. Open questions for Timothy

1. Are MOD-0001 to MOD-0008 and CLR-0017 the modular components you meant, or is it a different folder?
2. Which Sefer Yetzirah translation and version should be archived?
3. How should modules be indexed to Hebrew: one letter per module, or a coefficient profile across all 22 (CLR-0017 style)?
4. Final forms: separate profiles or shared?
5. The seven jurisdictions with no letter (J10, J12, J14, J15, J23, J25, J26): gaps, or combinations?
