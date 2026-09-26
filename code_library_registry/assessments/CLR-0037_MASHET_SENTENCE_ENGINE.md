# CLR-0037 — Mashet Sentence Engine

## Classification
Recovered compositional language-workbench prototype / Notebook language-tool ancestor / Assessed.

## Architecture
Interactive browser engine for:
- building words from glyph rows,
- assembling words into sentences,
- word-level selection and deletion,
- null-cell operator selection,
- inversion and superposition word states,
- sentence termination,
- per-word resonance/definition displays,
- Hebrew/romanized/IPA presentation,
- sentence-level definition and resonance panels.

## Strong contribution
This is a concrete ancestor of a Notebook compositional editor. It moves from “generate one Mashet word” toward user-controlled hierarchical composition:

Glyph -> Word -> Sentence -> Sentence Analysis.

The null-cell operator map is especially relevant to typed composition because it makes transformations between words explicit rather than silently changing semantic metadata.

## Audit notes
Constructed glyph sequences must remain labeled Mashet constructions unless independently validated as Hebrew words. Romanization/IPA/approximate meanings need a clear provenance layer.

Inversion and superposition should be typed operators with explicit algebraic semantics rather than visual states alone.

Recommended structure:
GlyphExpression -> WordExpression -> SentenceAST -> OperatorTrace -> Analysis/Evidence -> Rendering.

## Status
Assessed / Genuinely new recovered code family / Very high Notebook relevance.
