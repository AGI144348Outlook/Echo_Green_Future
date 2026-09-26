# CLR-0016 — Operator Weight System / Mashet Operator Visualizer

## Classification
React visualization + executable toy operator-learning experiment.

## Core contribution
This artifact replaces scalar control weights with state-transforming matrices. Four learned operators W_i act on a d-dimensional state and are contextually mixed by coefficients alpha_i:

W_c(t)=sum_i alpha_i(t) W_i(t)
S(t+1)=tanh(W_c(t) S(t)).

This is a meaningful architectural step toward Echo's Formula/Symbol Registry and Notebook operand-tool model: a registry entry can denote an executable transformation, not merely a scalar parameter.

## Learning law
The implementation uses a local outer-product update:
W_i <- W_i + eta alpha_i (g tensor S)
where g=0.1(target-S_next).

This resembles a delta/Hebbian-style rank-one update. It is not backpropagation through the recurrent dynamics, and the code does not compute the exact gradient of fitness with respect to W_i.

## Context coefficients
alpha_i are adapted with an exponentiated update using ||W_i||_F * fitness, then clipped and normalized.

Important issue: because fitness is negative Euclidean distance, every contribution is non-positive. Operators with larger norms are penalized more strongly, so this update primarily selects by operator norm under a shared global fitness signal; it does not measure each operator's causal contribution to improved fitness.

A better operator-credit test would compare counterfactual loss with/without each operator, use a directional derivative, or compute an actual per-operator gradient.

## Hebrew basis proposal
The UI proposes 22 fixed operators ell_j and decomposition
W_i=sum_j c_ij ell_j,
with word composition as ordered operator multiplication
word=ell_i1 ell_i2 ... ell_ik.

This is highly relevant to the Mashet/Glyphic Registry, but the executable simulation does not instantiate 22 Hebrew operator matrices. Its symbol activation is instead a hand-built 22-direction projection using only S[0] and S[1]. Therefore the current code demonstrates a 22-bin state quantizer, not Hebrew operator activation.

## Claims requiring stronger evidence
- Symbol grounding: argmax over a predefined projection yields discrete labels, but grounding requires stable relationships between labels and external/relational meaning.
- Word emergence: no word sequence semantics, compositional test, or reusable operator sequence is learned here.
- Algebraic agency: matrices are automatically updated by a fixed learning rule; this is self-modifying dynamics, but not yet demonstrated operator selection/manipulation by an autonomous agent.
- Mashet integration: specified conceptually, not implemented in this simulation.
- Offline/mobile readiness: plausible for small d, but needs benchmark evidence.
- "No backprop": true for this toy update in the narrow sense, but it still uses a target-derived error/gradient-like signal.

## Important implementation observations
1. The displayed state equation omits the actual tanh nonlinearity.
2. State-dimension slider changes state dimension only after Re-run; acceptable UI behavior but should be explicit.
3. Operators begin near identity, so the four W_i initially have nearly the same role.
4. Random initialization is unseeded; runs are not reproducible.
5. Fitness is always <=0 because it is negative distance.
6. There is no bias/input term, memory term, Core Formula anchor, explicit environment, or recurrent external input, so the state can collapse or settle for reasons unrelated to the broader SI architecture.
7. Operator norms alone do not reveal operator function; eigenvalues/singular values, condition number, action on basis vectors, and pairwise commutators would be more informative.

## Strong Echo/Mashet extraction
Define a typed Operator Registry:
OperatorSpec {
 operator_id,
 domain_type,
 codomain_type,
 matrix_or_callable,
 basis_refs,
 composition_rules,
 preconditions,
 invariants,
 learned_parameters,
 provenance,
 evidence_status
}

Then let the Notebook resolve:
Registry query -> operator set -> temporary algebra/matrix -> governed composition -> state transform -> trace -> audit/evidence.

For Hebrew glyphs, do not assign arbitrary matrices and call them semantics. Store each glyph operator as a hypothesis/definition with explicit derivation and test suite. Ordered composition matters because matrix operators generally do not commute.

## Recommended next experiment
Implement actual ell_1...ell_22 operators and compare:
A fixed random basis;
B orthogonal/structured basis;
C learned basis;
D registry-defined glyph operators.

Measure operator identifiability, compositional stability, transfer, symbol-grounding accuracy against external labels, and commutator structure [ell_i,ell_j]=ell_i ell_j-ell_j ell_i.

## Lineage
Core Formula -> Formula/Symbol Registry -> glyphs as operand tools -> scalar adaptive weights -> CLR-0016 operator-valued weights -> candidate Mashet operator algebra.

## Status
Assessed; exact source archival pending.
