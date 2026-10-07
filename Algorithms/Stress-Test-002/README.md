# Stress Test 002 — Unstructured Symbolic Intake

## Purpose
Test whether Echo can ingest unstructured symbolic material without prematurely converting observed form into asserted meaning.

## Core invariant
LOSSLESS PRESERVATION PRECEDES INTERPRETATION.

The raw source must remain byte-for-byte recoverable (UTF-8 text) from the intake record. Parsing, geometric classification, motif detection, syntax hypotheses, semantic annotations, and executable interpretations are separate derived layers.

## Required provenance states
Every derived claim must carry exactly one provenance state:
- OBSERVED — directly present in source form.
- DECLARED — semantics explicitly supplied by the human/source.
- INFERRED — interpretation proposed by the system.
- VALIDATED — interpretation supported by an explicit validation procedure.

INFERRED must never be silently promoted to DECLARED or VALIDATED.

## Intake layers
D0 RAW: preserve original text, Unicode, whitespace, line order, punctuation, repetitions, and malformed/unfinished forms.
D1 PRIMITIVES: identify atomic visual/symbolic units without assigning semantic meaning.
D2 GEOMETRY: classify primitive shapes into straight, curved, or combination where applicable.
D3 MOTIFS: detect recurrence, boundaries, nesting, adjacency, symmetry, alternation, and repeated constructions.
D4 CANDIDATE SYNTAX: propose structural roles only as hypotheses.
D5 SEMANTICS: attach human-declared or system-inferred meanings with provenance.
D6 FORMALIZATION: only validated structures may become Codex rules or executable Algorithms.

## Recursive requirement
A slot such as (?) may contain a word, relation, Boolean expression, symbolic expression, or another complete nested structure. The parser must therefore preserve recursive containment and must not flatten nested expressions.

|x| is a candidate recursively nestable structural container. Its meaning is not assumed by the parser.

## Environment declarations in supplied corpus
The source contains human-declared candidate forms for:
- Dataset: מ
- Registry: ם
- Codex: ת
- Algorithm: ר

These are DECLARED annotations for this corpus, not universal parser rules.

The source also temporarily declares:
- ו = noun
- ש = verb
- ט = adverb
- כ = adjective

These remain temporary DECLARED semantics and must not be generalized beyond the supplied context without validation.

## Pass conditions
1. Raw source can be reproduced exactly.
2. Unknown or malformed structures are retained, not discarded.
3. Unicode glyphs are not normalized into replacements that lose identity.
4. Primitive/geometric classification does not assign semantics.
5. Recurring motifs are reported separately from their proposed meanings.
6. Nesting is represented recursively.
7. Human-declared semantics are distinguishable from system inference.
8. The system can say UNKNOWN/UNRESOLVED instead of filling semantic gaps.
9. No candidate syntax becomes executable merely because it parses.
10. Output records enough provenance to audit every semantic claim back to source or validation.
11. The irregular final block is processed rather than rejected solely for failing the cleaner candidate grammar.
12. The test report explicitly lists information loss, unsupported assumptions, and unresolved structures.

## Expected developmental flow
Raw → Observed → Recurrent → Registered → Related → Formalized → Executable

This flow is directional for the test: later layers may reference earlier layers; they may not rewrite the raw layer.
