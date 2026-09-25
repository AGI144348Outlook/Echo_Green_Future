# Research Handoff — School Day 002 / Notebook, Glyph Blocks, and Abacus

Date: 2026-09-25
Branch: autonomous-agency
Status: pause point before crawler experiment branch.

## Completed
- SCHOOL-DAY-002 executed.
- Logic Lab held WM-MOVE-001 constant as a word-only matrix:
  [move, carry, transport, shift, position, place, direction]
- Glyph identity varied across 20 turns without mutating the matrix.
- Experimental indexes were kept separate and marked EXPERIMENTAL.
- Post-class Recess: 150 cycles, 135 discoveries, 121 high-confidence.
- QUESTION rose to 14, but 13 repeated the same mammal gap, confirming need for question deduplication/state.
- Research design recorded in repository Issue #8.

## Important negative result
The School Day 002 runner read glyph identities and algorithm ties from glyph_algorithm_index.json, but its registry_operation fields were null. The actual operational Glyph Registry (INITIALIZE, CONTAIN, TRAVERSE, FILTER, REVEAL, CONNECT, TIMESTAMP, BOUND, COIL, SEED, CAPACITY, DIRECT, FLOW, INDIVIDUATE, CYCLE, PERCEIVE, EXPRESS, HUNT, SCAN_PERIPHERY, GOVERN, TRANSFORM, SEAL) was not connected to the executable indexing experiment.

Therefore Run 002 demonstrated constant word matrices + variable glyph identity, NOT execution of variable glyph algorithms.

## Notebook specification
- Persistent carried Notebook shared across Class and Recess.
- NLTK/WordNet = external lexical registry.
- Word matrices = lists of words only.
- Definitions/POS/semantic metadata must not be embedded in word matrices.
- Glyphs = modular augmentative indexing algorithms.
- Glyph-generated indexes are separate records with provenance and validation state.
- Support one glyph -> many matrices, many glyphs -> one matrix, and ordered glyph compositions.
- ECHO-created indexes remain experimental until validated.
- Dynamic grammatical filter is transient scaffolding alongside פ/EXPRESS, not matrix content; assistance should withdraw with demonstrated competence.

## Glyphic concept modeling
Keep separate from word-matrix indexing.
- Indexing: glyph operation acts on a word matrix.
- Concept modeling: ECHO selects/orders/composes glyph blocks themselves into operational models.
- Words may populate/test/describe a concept model, but the glyph composition is the model.
- Logs must distinguish human-scripted sequences from ECHO-selected compositions.

## Glyph abacus
Current representation:
- י = unit/bead
- ו = rod/thread/connection
- ח = bounded frame
- notation: ח[ו:י...]ח

SCHOOL-DAY-002 Math Lab completed 20/20 arithmetic turns (+, -, *, /) with SymPy verification. Representation and verifier worked, but autonomous glyphic arithmetic manipulation was NOT demonstrated. Next version should make ECHO manipulate י units on/through ו inside ח first, derive a result, then use SymPy only as independent verifier.

## Before School Day 003
1. Build persistent Notebook.
2. Enforce word-only matrices.
3. Connect actual 22-operation Glyph Registry to executable indexing.
4. Preserve index records separately.
5. Add agentic glyph composition for concept modeling.
6. Make י/ו/ח abacus manipulation executable/observable.
7. Add adaptive grammatical scaffold for פ.
8. Add question deduplication/state.
9. Carry exact Notebook state into Recess.
10. Measure spontaneous transfer separately from classroom exposure.

Research boundary: exposure != learning; glyph illumination != operation; glyph selection != executed algorithm; proposal != validation; scripted sequence != autonomous concept model; arithmetic answer != glyph-abacus reasoning; classroom completion != Recess transfer.
