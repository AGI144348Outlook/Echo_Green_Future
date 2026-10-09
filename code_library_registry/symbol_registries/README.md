# Symbol Registries — plan of record (2026-10-08)

**Status:** planning record. Nothing here is a validated registry yet.
**Compiled from:** Timothy's discussion with Claude on 2026-10-08.
**Labels:** **Declared** = Timothy stated it. **Reading** = Claude's interpretation, not yet confirmed. **Proposed** = a design suggestion awaiting Timothy.

The authoritative, up-to-date copy of every rule lives in Cloudflare D1 (`echo_knowledge`, tables `rules` and `rule_events`). `rules-snapshot-2026-10-08.json` in this folder is a frozen copy of those 51 rules as first stored. If the two disagree, D1 wins.

## 1. Purpose: one parsing framework for the whole spectrum

**Declared (R-SPEC-1):** the parsing framework must cover everything from data in a language whose semantic mechanics are already understood, to an undeciphered language like the Indus Valley Script, or one met on another planet.

**Proposed (R-SPEC-2, R-SPEC-3):** the pipeline stays the same along the spectrum; only the declarations change. At the undeciphered end, segmentation and reading direction are hypotheses, never inputs.

| Case | Declared before parsing | Parser must discover |
|---|---|---|
| Known language (English) | segmentation, direction, meanings | nothing; it checks the parser |
| Hebrew under Timothy's operators | letters, direction, operator meanings | how operators combine |
| Indus Valley Script | sign list, reading direction | structure, perhaps meaning |
| Unknown script | nothing | what a symbol is, direction, whether it is language |

## 2. The symbol systems and their roles

**Declared (R-ROLE-1 to R-ROLE-15).** Notation is stored exactly as Timothy typed it.

| # | System | Role | Notation |
|---|---|---|---|
| – | Indus Valley icons | Nouns: people, places, things | `IVS ≈ [Nouns]:{people,places,things}` |
| – | Hebrew glyphs | Verbs | `Hebrew ≈(verbs` |
| – | Latin | Logic profiles | `({•})=(•)←{•,•,•}→[•]=[{•}]` |
| – | Chinese / Cuneiform | Words as units (one role or two: open) | `\|__[(ש)←{Words}→(ש)]__(=)__{•}__\|` |
| – | English | Bridge between sets | `English/{•}←[\|]→{•}\Cuniform` |
| – | English dictionary | Hypernyming laterally and vertically | `§•~§•~§•~§•~§•` |
| 1 | I-Ching | Ordering `{∆}` and syntaxing `{¥}` | |
| 2 | Brackets | Structuring | `\|[{(\|)}]\|` |
| 3 | Combined | Structure + mapping + syntax/ordering | `__\|[{(\|)}]\|_/_{•}←[\|]→{•}_/_[{¥}+{∆}` |
| 4 | Punctuation | Compiling; hypernyming | `(•)ⁿ→{•:•::•:•}←[•]ⁿ` ; `§•~§•~§•;` |
| 5 | Numerators | Math / science | |
| 6 | Continuum | Algorithms | `(ש\|ש) = \|ש\| = \|\|` |
| 7 | The 96 | Neurons and their neuroplasticity | finite set, exponential arrangements |
| 8 | Developing notation | Generalization | stages t⁰–t⁶ (R-ROLE-14) |
| 9 | Open | Where an undeciphered script lands | |

**Proposed (R-ROLE-16, R-ROLE-17):** a role is a removable declaration; role-like behaviour is still measured beneath it. An unknown script gets no roles until it earns them.

**Proposed (R-DET-1 to R-DET-5):** I-Ching trigrams (8) or hexagrams (64) as **determinatives**: silent category marks, combinable line by line, with ∆ meaning one line flipped. Open: 8 or 64, and whether traditional associations are kept or start empty.

## 3. The registries to build

One registry per symbol system, each with immutable IDs (R-REG-1), add-only history (R-REG-2), and provenance on every entry.

| Registry | Source material | Notes |
|---|---|---|
| Indus Valley signs | `mayig/indus-valley-script-corpus` (IVS branch tests 001–002); `field-cady` (5,000+ inscriptions) | Listed left-to-right, read right-to-left (R-IVS-1); damage/uncertainty flags (R-IVS-2) |
| Hebrew glyphs | 22 letters + 5 final forms + vowel marks | See `hebrew-index.md` (Sefer Yetzirah grouping, LHEA Latin profiles, modules) |
| The 96 | Mashet Symbology legend MS-001–MS-096 | Four competing 96-legends exist in the control-surface source; canonical one still to be declared |
| Notation | Timothy's brackets, strokes, `_`, `\|`, `::` | Seed, condensation and Governor rules below |
| Punctuation | Unicode punctuation | Compiling role |
| Latin | Latin roots, prefixes, suffixes | Existing D1 tables `latin_roots`, `latin_prefixes` in `mashet-stamp-registry` |
| I-Ching | ☰–☷ (U+2630–2637), ䷀–䷿ (U+4DC0–4DFF) | All direction-neutral in Unicode bidi; pulled into Hebrew runs |
| Chinese / Cuneiform | to source | Determinatives in cuneiform are a precedent for category signs |
| Numerators | digits, super/subscripts, math operators | |

**Registries vs matrices (Proposed, R-MAT-1 to R-MAT-3):** a registry is one row per thing; a matrix holds relations between registered things (adjacency, position, co-occurrence). Matrix axes may only use registry IDs; matrices are derived and can be rebuilt by rescanning.

## 4. Notation rules

**Declared:**

- **Seed (R-SEED-1):** `||::||` is the Formula's seed.
- **Seed expansion (R-SEED-2):** `|י|::|י|__(=)__\` then `__\→|__י__|::|__י__|←`.
- **Letters dropped (R-SEED-3):** `||_|...|←|_|::|→|[|]::[|]::[|]::++++→|_||` — the `[|]` frames repeat (`++++`).
- **Condensation (R-CON-1):** `[|]` is the most generalized way to condense something to its most absolute Condensity; expanding out is `[||]`.
- **Condensation cycle (R-CON-2):** `__\¹_ש←[|]→ש_\²_[|ש|]_\³_[|_|]__\=\¹←\³=` ; `/³={_(|ש←||):(|=||)_}=\⁴{|ש=←||}` ; `|:Continuum:: Algorithm:/⁴{|ש|}`
- **Interchangeability (R-GEN-1):** `#`, `|#|` and `x` are interchangeable; the meta-specification counters biasing impositions by enabling interchangeability, the difference between Specifications and Generalizations.
- **Strata (R-STRATA-1):** the Suprastrate and Substrate connect at the IETF (0,0,0) and the Relational Formula's `|x|`, an agentically employable harness wrapped around the Datastrate.
- **Continuation (R-CONT-1):** `)))` means "continues until the end", like `…`.

## 5. Governor / Auditor formula (revision in progress)

**Declared (R-GOV-1, R-GOV-2):**

```
[_{(?):(?)}::{(?):(?)}_]א_|ת→א|י|::|י|א←ת|_א[_{(?):(?)}::{(?):(?)}_]
```

- Kernel `]א_|ת→א|י|::|י|א←ת|_א[` is the Formula's (0,0,0) in practicality.
- `[_{(?):(?)}::{(?):(?)}_]__(=)__[|]`
- `|'||::||'|←__(=)__|[א]::[|]::[|]::[|]::←[ת]|ת||`
- Bounded at the ends with `||ת|→`
- `(?)` can = `(?±?)` where `[±] = {<,>,=,}`

**Readings (Proposed):** the kernel mirrors around `::` (R-GOV-4); stripping its letters leaves the seed (R-GOV-5); the empty fourth relation means "not compared / open" (R-GOV-6, unanswered).

**Retired:** R-GOV-3 (Claude's reading that each `[|]` is one full frame), corrected by R-CON-1.

## 6. The 96 as neurons

**Declared (R-ROLE-13):** the 96 are like neurons with neuroplasticity: the hard constraint of the skull still allows an exponential set of arrangements within a finite limit.

| Arrangement of the 96 | Count |
|---|---|
| Directed pairs (A→B, A≠B) | 9,120 |
| Subsets active together | 2⁹⁶ ≈ 7.9 × 10²⁸ |
| Orderings of all 96 | 96! ≈ 9.9 × 10¹⁴⁹ |
| One relation from `{<,>,=,␣}` per directed pair | 4⁹¹²⁰ ≈ 10⁵⁴⁹¹ |

**Proposed (R-NEU-1, R-NEU-2):** the 96 are fixed and their relations are plastic; an IETF node holds one arrangement of the 96. The mechanisms for that plasticity are in `../design_notes/neuroplasticity-candidate-algorithms.md`.

## 7. Open questions

1. Which 96-symbol legend is canonical?
2. Chinese and cuneiform: one role, or split into whole-word signs and component signs?
3. Determinatives: 8 trigrams or 64 hexagrams; traditional associations or empty categories?
4. Is the empty fourth relation in `{<,>,=,}` the "open / not compared" relation?
5. Sefer Yetzirah: which translation to archive (see `hebrew-index.md`).

## Files

| File | What it is |
|---|---|
| `README.md` | This plan |
| `hebrew-index.md` | Hebrew registry index: letter groups, Sefer Yetzirah, LHEA profiles, modular components |
| `rules-snapshot-2026-10-08.json` | Frozen copy of the 51 rules first stored in D1 |
| `../design_notes/neuroplasticity-candidate-algorithms.md` | Neuroplasticity → systems candidate algorithms (2026-10-06) |
