# Core Formula Algebra Registry

This section catalogs algebraic forms, decompositions, transformations, and implementation interpretations of Echo's historical core structural formula family.

## Purpose
The registry separates three things that historical artifacts sometimes blended:

1. **Algebraic identity/equivalence** — a valid rearrangement or expansion of a stated formula.
2. **Defined specialization** — a formula obtained by explicitly defining operators, kernels, vectors, or discrete-time terms.
3. **Implementation heuristic** — code inspired by the formula but not algebraically equivalent to it.

Every entry should identify its class.

## Canonical historical family
A recurring historical form is:

`S(t) = A + Σ_i(Σ_n F_n(R_i)) + ∫ C(τ)dτ`.

Related later kernel family:

`☉_k = ⊕{⟲ recursion, ⇢ input, ∫ memory, ⧖ coupling, ≋ noise}`

and discrete state family:

`S_k = 𝒜(S_{k-1}) + 𝒇(U_k) + M(S_{<k}) + C_k + ε_k`.

These are related architectural families; the registry must not claim mathematical equivalence unless a mapping is explicitly defined.

## Registry fields
Each algebra entry should contain:
- Formula ID
- Name
- Source artifact(s)
- Formula
- Classification
- Operand/type assumptions
- Derivation or mapping
- Invariants preserved
- Information introduced/lost
- Executable interpretation, if any
- Validation status
- Notes/cross-references

## Rule
Whenever a historical artifact supplies or implies a new manipulation of the core formula, add it here. Speculative mappings should be labeled as such rather than silently promoted to identities.
