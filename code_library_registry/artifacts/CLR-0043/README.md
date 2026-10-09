# CLR-0043 — Lexicon Registry

Published artifact (private to Timothy until shared): https://claude.ai/artifact/8Ks7i42udDoFq2hxJiNkAp

A dictionary-to-Registry workbench built 2026-10-09 by Claude with Timothy. A general-first WordNet dataset is filtered into a saved Registry through index-card query lines (`type/:value`), and example sentences are tagged in Timothy's bracket notation (Legend v0.1) with a recursive structure scan. Glyph profile cards for the 22 Hebrew letters catch words per grammar component.

## Files

- `lexicon_registry.template.html` — page source with `/*STARTER*/` and `/*GRAMMAR*/` placeholders
- `grammar.js` — rule-based tagger, chunker and recursive clause parser (no LLM); exports `parse`, `tag`, `LEGEND`, `PATTERNS`
- `starter.json` — 1,031 most general WordNet words with examples, POS sets and ancestor paths
- `build/` — generators for the starter set, the full 147,306-word dataset, enrichment, and page assembly

Large derived data (≈11 MB) and Pyodide are not committed here; `build/` regenerates them.

## Legend v0.1 (innermost evaluated first)

| Slot | Role |
|---|---|
| `[•]` | Noun: a state (operator or operand) |
| `{•}` | Adjective: property of a state |
| `\|•\|` | Anchor: this/that, here/there, now; articles, possessives |
| `(•)` | Verb: an operation |
| `<•>` | Adverb: magnitude or effect of an operation |
| `<•)` | Fused: magnitude opening into an operation (left mark modifies, right mark is head) |
| `/•/` `\•\` | Preposition forward D.O→I.O / backward I.O←D.O |
| `>•<` | Interrogative, the empty slot (?); also opens a nested clause |
| `/•\` `\•/` | Pair: join (and) / split (or) |
| `}•{` | Relation: same, different, like, as, than |
| `]•[` | Absence: no, not, none, never |
| `)•(` | Turned operation: passive or reflexive |
| `⟨…⟩` | Nested clause, parsed one level deeper |
| `^x` | Glyph catch (superscript) |

Pattern letters: S subject, V operation, Vᵖ passive, O object, C complement, A adverbial, ∃ existential, Q question, ! imperative, ∅ fragment, ⟨⟩ nested clause patterns.

Overarching principle (Timothy): Generalization → Specification.
