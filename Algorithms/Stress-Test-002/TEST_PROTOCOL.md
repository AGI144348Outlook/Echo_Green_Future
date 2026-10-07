# Stress Test 002 — Blind Test Protocol

## Phase A — blind structural run
Give the tester only RAW_SYMBOLIC_CORPUS.txt and this protocol section through "Required output". Do NOT provide EXPECTED.md or the semantic declarations during the first pass.

Ask the tester to:
1. Preserve the source exactly.
2. Decompose observable primitives.
3. Classify straight / curved / combination primitives where defensible.
4. Detect recurring structural motifs.
5. Represent nesting/containment recursively.
6. Mark unresolved structures UNKNOWN rather than inventing meanings.
7. Produce machine-readable output plus a human-readable report.

### Required output
- raw integrity hash
- line/character preservation check
- primitive inventory
- geometry classifications with evidence
- recurring motif inventory
- recursive containment representation
- unresolved/ambiguous inventory
- inferred interpretations, if any, explicitly labeled INFERRED
- parser losses/errors

## Phase B — declared-semantics reveal
After Phase A is frozen, reveal DECLARATIONS.md.

The tester must add declarations without rewriting Phase A observations. It must report:
- which Phase A structures align with declarations
- which do not
- whether any earlier inference accidentally anticipated a declaration
- whether any declaration conflicts with observed structure

## Phase C — expected criteria reveal
Only after Phase B is frozen, reveal EXPECTED.md and score the run.

Do not reward semantic cleverness. Reward preservation, provenance, recursive structure, restraint, and auditability.
