# Code Library Assessment — CLR-0043

## Artifact identity

- **Registry ID:** CLR-0043
- **Artifact name:** Lexicon Registry
- **Submitted filename(s):** `artifacts/CLR-0043/lexicon_registry.template.html`, `grammar.js`, `starter.json`, `build/*.py`
- **Approximate creation date:** 2026-10-09
- **Original author/context:** Claude, at Timothy's direction; notation and grammar profile authored by Timothy (index cards, Legend v0.1)
- **Language / format:** HTML + JavaScript single page; Python build scripts; Pyodide in-page
- **Execution status:** Runs (headless Chromium check 2026-10-09: tagger, structure scan of 395 starter sentences → 82 patterns, Pyodide `tag()` call). Published as a claude.ai artifact with db, user and sample capabilities.

## Executive description

Uses a dictionary as the practice Dataset for the Registry pipeline. Words are ordered most general first (WordNet depth and hyponym span for nouns and verbs, corpus frequency for adjectives and adverbs). Index cards hold query lines whose output is a matrix; matrices can be admitted to the Registry or saved as widgets. The Registry is read two ways: Matrix (by word) and Index (by facet). A rule-based grammar layer tags sentences in Timothy's bracket notation and recursively parses embedded clauses into structure patterns beyond SVO.

## Structural inventory

- Query language: `w def pos hyper depth rank span len letter via ex top sort cols src tag py ask`, clauses joined by `&`.
- Registry storage: artifact db, bucketed `registry/<2 letters>-<hash%8>` documents holding entry maps; `cards/`, `widgets/`, `structures/`, `glyphs/` collections.
- Grammar (`grammar.js`): closed-class lexicon, suffix lemmatizer with irregular map, context disambiguation, chunker (NP/VG/PREP/embedded), clause labeler, notation renderer, recursion with depth limit.
- Python (Pyodide 0.26.4, served from artifact files): globals `dataset`, `registry`, `q()`, `admit()`, `widget()`, `tag()`.
- Claude console (sample capability) with page tools: query, run_python, admit, make_widget.

## Behavioral assessment

- Deterministic tagger and parser; no LLM in the grammar layer.
- On all 41,948 WordNet example sentences: ≈36% fragments with no operation (`∅NP`), which reflects WordNet's example style; top full patterns SVA, SVO, SVOA, SV, SVC.
- Embedded clauses end at the next comma or, for relatives after a noun phrase, at the second verb group.

## Limitations and defects

- Rule tagger errors on ambiguous words (e.g. "ran home" tags *home* as a property; some subjectless sentence-initial verbs read as nouns).
- No word-sense disambiguation; the ⁿ sense slot is in the legend but not filled automatically.
- Glyph catches below the exact word follow WordNet ancestor paths only for words in the loaded dataset.
- Registry bucket documents are rewritten whole on change (last-writer-wins).

## Echo relevance

Registries; Indices/Matrices (bidirectional reading); Glyphic systems (Hebrew glyph profile cards); Semantic/hypernym structures; Generalization (general-first ordering, Generalization → Specification); Notebook/UI/PWA; Tooling/testing.

## Status

Assessed; Candidate.
