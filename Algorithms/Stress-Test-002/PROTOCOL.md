# Stress Test 002 — Clean Input Protocol

## Purpose
Test registry formation and cross-source relation discovery from complete source evidence without benchmark leakage or format-specific assumptions.

## Immutable evidence rule
RAW → OBSERVED → RECURRENT → REGISTERED → RELATED → FORMALIZED → EXECUTABLE

Later stages may reference earlier stages. They may not rewrite raw evidence.

## Input boundary
Only files under `input/` are source evidence.
- `ECHO_GlyphRegistry.zip` is the authoritative Glyph Registry archive copied byte-for-byte by Git object identity from `dev-suite-registries`.
- `neuroplasticity-candidate-algorithms.md` is the complete 483-line source, not the compact Stress Test 001 extraction.

The runner must unpack the Glyph Registry archive before ingestion and ingest its complete corpus, including INDEX.md and all 22 glyph documents.

## Exclusions
Do not ingest this protocol, manifests, README files, prior Stress Test 001 outputs, expected-answer material, or evaluator declarations.

## 002 requirements
1. Discover cross-source candidate pairs; do not use a hand-selected pair list.
2. Do not encode knowledge of Glyph Registry or neuroplasticity document formatting in the parser.
3. Preserve contradictory or ambiguous claims as unresolved rather than repairing them.
4. Preserve provenance to source file and source span.
5. Keep proposed algorithms distinct from existing/executable implementations.
6. Keep similarity distinct from identity.
7. Definition != Authority. Registration != Execution.
8. No source-described operation grants permission to execute it.

## Known ambiguity targets for post-run audit only
The evaluator may later inspect swapped fields, class conflicts, duplicate algorithm names, and proposed-versus-existing identifier ambiguity. These are not instructions to the parser and must not be supplied to it as expected answers.
