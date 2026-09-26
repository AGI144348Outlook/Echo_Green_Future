# CLR-0020 — Operator Translation Layer: Making Echo Legible

## Classification
Interpretability / deterministic translation prototype. Direct successor to CLR-0019.

## Core architecture
Three-stage interface:
1. operator -> algebraic signature -> concept token;
2. weighted operator composition -> structural/syntactic representation;
3. concept structure -> deterministic human template.

This is a valuable separation because human wording is downstream of the machine-readable operator record rather than being the internal reasoning substrate.

## Strong contribution
The important object is not the prose renderer but the intermediate typed record:
Operator -> Signature -> ConceptToken -> CompositionRecord -> Rendering.

That record can be stored, queried, audited, and rendered into multiple languages or interfaces without changing Echo's operator dynamics.

## Important mathematical distinction
The source calls all extracted features invariants. Some are similarity invariants (trace, determinant, eigenvalues/spectral radius), while Frobenius norm and the symmetry score are generally basis/coordinate dependent under arbitrary similarity transforms. They can still be useful diagnostics, but should not all be called algebraic invariants.

Recommended split:
- similarity invariants: trace, determinant, spectrum/spectral radius;
- orthogonal-basis invariants: Frobenius norm;
- representation diagnostics: symmetry score and thresholded rotation/damping classifications.

## Classification limitations
- determinant alone does not generally establish contraction/expansion; sign and dimension matter.
- determinant can be negative for orientation reversing maps.
- fraction of eigenvalues below unit magnitude is not a complete stability criterion for non-normal matrices.
- complex eigenvalues indicate rotational/oscillatory components in real systems, but thresholding their fraction is a heuristic.
- symmetric matrices are not generally 'equilibrium-seeking'; that label requires dynamics/objective assumptions.
- trace is not simply 'scaling'.

Concept labels should therefore be treated as defined semantic mappings with confidence/evidence fields, not mathematical identities.

## Rendering bug
render_action_statement() selects the root from the dominant operator by influence, but obtains modality/constraint from composition.concepts[0]. If operator 0 is not dominant, the sentence combines properties from different operators.

The syntax tree should retain the dominant operator index, or rendering should classify the composite itself.

## Composition semantics
The implementation uses an additive mixture:
W_c=sum_i alpha_i W_i.
This is not ordered operator composition. Therefore its 'syntax' captures mixture/importance, not sequential syntax.

True noncommutative syntax requires products such as:
W_word = W_k ... W_2 W_1
and explicit order. This connects directly to the T2T1 vs T1T2 experiment proposed for CLR-0019.

## Influence metric
weight x Frobenius norm measures weighted magnitude, not causal contribution to a particular state transition. Better state-conditioned attribution:
I_i(x)=||alpha_i W_i x||
or intervention:
Delta_i(x)=||f_W(x)-f_{W without i}(x)||.
Use held-out probe distributions for global attribution.

## Honesty claim
Deterministic templates greatly reduce open-ended generation, but 'cannot hallucinate or lie' is too strong. A deterministic system can still produce false or misleading statements when its classifier, thresholds, semantic mapping, or measurements are wrong. Better claim: deterministic, traceable, constrained rendering with explicit provenance.

## speak() side effect
speak() calls compute_alignment(), which advances self.S. Observation changes the system being observed. For an interpretability interface, report generation should normally be read-only. Separate observe/report from step/advance.

## Scalability
The renderer itself is inexpensive, but eigendecomposition/determinant and dense dxd operators are not dimension-free. 'Works at any dimensionality' should be replaced with a measured complexity claim and sparse/structured alternatives for large d.

## Recommended typed record
TranslationRecord {
  operator_ref,
  state_ref,
  signature: {values, invariance_class},
  classifications: [{label, rule_id, confidence}],
  composition: {kind, members, coefficients, order?},
  attribution,
  task_alignment,
  provenance,
  timestamp/turn
}

HumanRenderer should consume this record and never inspect mutable model state directly.

## Echo relevance
Very high. This can become the Notebook's operator-inspection surface and an audit bridge between Formula Registry, TaskOperator experiments, Generalization Registry, and later glyph semantics.

Crucially, glyph meanings should not be declared from these generic threshold labels. The translation layer can provide empirical operator descriptors that are compared against independently specified glyph semantics.

## Status
Candidate interpretability architecture. Preserve the three-layer separation; tighten the mathematics and make reporting read-only/provenance-bearing.
