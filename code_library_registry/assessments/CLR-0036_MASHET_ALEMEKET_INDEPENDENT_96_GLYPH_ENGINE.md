# CLR-0036 — Mashet · Alemeket · Independent — 96-Glyph Engine

## Classification
Recovered executable offline symbolic-engine prototype / 96-glyph runtime / Assessed / High-priority reconstruction candidate.

## Architecture
The source explicitly declares:
1. GLYPH_TABLE — 96 operators as first-class objects.
2. MANIFOLD ENGINE — thesaurus rebarring of a 23x1 substrate at boot.
3. KERNEL — reads glyph table and produces field state S.
4. INTROSPECTION — kernel reads itself and produces symbolic state.
5. SYNTHESIS ENGINE — navigates rebarred domains to produce English.
6. IETF HARNESS — spatial-node testing for synthesis validation.

Each glyph record contains name, category, weight, role and fn(state)->delta. This is materially more executable than the earlier visual 96-glyph legend.

## Strong contribution
This artifact implements the important architectural rule that the kernel reads operator definitions from a registry/table rather than hard-coding every behavior into the kernel.

That is a direct ancestor of the modern Symbol/Formula Registry idea.

## Audit findings
- “No LLM / no API / no network” is genuinely distinct from the earlier API-backed Alemeket PWA.
- Several glyph functions use Math.random(); deterministic/reproducible testing therefore needs seeded randomness.
- Some mathematical names are analogical rather than faithful implementations. Example: an “eigenvalue” glyph that merely scales a vector by magnitude is not an eigenvalue computation.
- Several symbols are identities/placeholders; declared role must remain distinct from implemented transform.
- Symbol collision: ⧫ appears for both binding (id 25) and potential_barrier (id 59) in the recovered code. A JavaScript object cannot retain both keys; the later definition overwrites the earlier one. Thus the claimed 96-addressable operator registry is not actually 96 unique keys as written.
- “Introspection” should be described as structured self-inspection of registered state/code metadata, not subjective self-awareness.
- English synthesis from authored seed domains remains project-defined semantics and needs held-out behavioral validation.

## Modern reconstruction
SymbolSpec -> unique immutable symbol_id -> notation index (non-unique allowed only explicitly) -> typed domain/codomain -> implementation_ref -> laws/tests -> evidence.

Kernel should resolve by symbol_id, not raw Unicode glyph key.

## Status
Assessed / Genuinely new executable family / Very high Echo relevance.
