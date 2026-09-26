# CLR-0031 — Mathematical Substrate System: Core Formula Exercise Platform

## Classification
Historical mathematical-carrier prototype / Core Formula workbench ancestor / Dual glyph-math curriculum ancestor / Assessed.

## Architectural role
This artifact deliberately transfers the substrate-carrier pattern from project-defined Hebrew glyph mappings to conventional mathematical notation.

Historical mapping:
concept -> mathematical substrate label -> mathematical symbol -> formula template -> executable numerical operation.

It also provides a concrete Core Formula exercise:
B(t) = A + sum_i F_n(R_i) + integral C(tau) d tau + feedback(B_current).

## Strong contribution

### 1. Operand-carrier abstraction
The important architectural move is not the specific substrate labels; it is recognizing that the carrier can be exchanged while preserving a common registry/interface pattern.

Hebrew/Glyph carrier:
glyph -> declared operator/substrate metadata -> composition.

Mathematical carrier:
symbol -> established mathematical operation -> typed operands -> composition.

This is a direct ancestor of a dual-learning representation in which Echo can inspect a project glyph/operator and a mathematically explicit analogue side-by-side.

### 2. Executable symbol registry
MathematicalSymbol already approximates a useful Symbol Registry record:
symbol, name, substrate tags, operations, domain_type.

Modernize to:
SymbolSpec {
  symbol_id,
  notation,
  operator_kind,
  arity,
  domain,
  codomain,
  operand_types,
  semantics_ref,
  implementation_ref,
  laws,
  preconditions,
  provenance,
  evidence_status
}.

### 3. Core Formula as an executable decomposition
The artifact decomposes the historical Core Formula into independently inspectable components:
anchor,
ray transformation,
summation,
context integration,
feedback.

This supports the later Formula Registry / executable dependency graph concept.

## Mathematical audit

### A. Integration/differentiation “dimension effect” comments are incorrect
Integration does not generally reduce dimension by 1 and differentiation does not generally increase it by 1.

For physical dimensions/units:
if [f] = U and [x] = X,
[d f / d x] = U / X,
and
[integral f dx] = U * X.

Vector-space/domain dimension changes depend on the particular operator and spaces, not on a universal +/-1 rule.

### B. Partial derivative implementation is actually a one-variable forward derivative
The ∂ executable:
(f(x+h)-f(x))/h
is a forward finite-difference derivative for a scalar variable. It does not implement a partial derivative unless a multivariable function and selected coordinate are supplied.

### C. Gradient is forward finite difference
_gradient computes coordinate-wise forward differences. This is a numerical approximation, not the mathematical gradient operator itself. Central differences would normally give better truncation accuracy:
(f(x+h e_i)-f(x-h e_i))/(2h).

### D. Tensor product does not imply quantum entanglement
Tensor products provide the state-space structure used for composite quantum systems, but a tensor-product state can be separable. Entanglement is a property of states that cannot be factored into a product of subsystem states.

### E. The “fractal transform” is recursive, not demonstrated fractal
F_d(x) = x + 0.1 F_{d-1}(0.8x), F_0(x)=x.
This is a finite recursive scalar transformation. Recursion/self-similarity in source code does not by itself establish fractal geometry, fractal dimension, or scale invariance.

Indeed it can be unfolded:
F_d(x) = x * sum_{k=0}^d 0.1^k 0.8^k
       = x * sum_{k=0}^d 0.08^k.
Thus it is simply a depth-dependent scalar multiplier.

Closed form:
F_d(x) = x (1 - 0.08^(d+1)) / (1 - 0.08).

This is an especially useful archival finding: the historical “fractal” ray operator is algebraically reducible to linear scaling.

### F. Feedback is contemporaneous algebraic augmentation, not a temporal feedback loop
feedback = 0.1 tanh(current_behavior)
is calculated once from the partial current result and then added. There is no recurrence B_{k+1}=G(B_k,...) or delayed output-to-input path. It is better called a nonlinear self-dependent correction term in this exercise.

### G. Concept-to-formula generation is templated routing
Natural-language keywords select at most two symbols. For multiple symbols, _construct_formula returns strings such as:
∫(Σ operation)
without typed operands, bounds, indices or executable composition.

Furthermore _create_executable uses only symbols[0], so a displayed multi-symbol formula is not actually executed as that composition.

Therefore:
RenderedFormula != ExecutedOperator
for multi-symbol generated operations.

### H. Registry incompleteness
MATHEMATICAL_SUBSTRATES defines ∫, Σ, ∂, ∇, ∏, lim, ∘, ⊛, ⊗, but MATHEMATICAL_SYMBOLS instantiates only the first five. Concept analysis can request composition_substrate, but no ∘ MathematicalSymbol exists, so “recursive self-similar transformation” can produce no selected symbol and fall back to f(x).

## Core Formula normalization

The historical exercise is best represented as:

B = A + S_R + I_C + H(B_partial)

where
S_R = sum_i F_d(R_i),
I_C = integral_a^b C(tau) d tau,
B_partial = A + S_R + I_C,
H(z) = 0.1 tanh(z).

With the supplied recursive ray transform:
F_d(r) = r * (1 - 0.08^(d+1))/0.92.

Therefore the whole demonstrated computation can be written explicitly:

B = A
  + k_d * sum_i R_i
  + integral_a^b C(tau) d tau
  + 0.1 tanh(A + k_d sum_i R_i + integral_a^b C(tau)d tau),

where k_d=(1-0.08^(d+1))/0.92.

That makes the actual mathematics much clearer than the “fractal” label.

## Modern Echo reconstruction

### Separate established semantics from project metadata
For mathematical symbols, conventional mathematical semantics should be authoritative. Project substrate tags can be secondary metadata.

MathSymbol
-> formal semantics
-> typed signature
-> algebraic laws
-> executable implementation(s)
-> project analogies/substrate tags.

Do not let project analogies redefine ∫, ∂, ∇, etc.

### Dual representation
A future Echo curriculum/Notebook can expose:

Project Glyph Operator <-> Structural Role <-> Mathematical Operator

but the middle relation must state its status:
exact equivalence,
restricted equivalence,
analogy,
heuristic,
or hypothesis.

This prevents “Mem = integral” style analogies from silently becoming mathematical identities.

### Formula Registry
Represent the Core Formula as an AST/dependency graph rather than a string:

FormulaNode(add)
  anchor(A)
  aggregate(sum)
    ray_transform(F_d)
    rays(R_i)
  integrate
    context(C)
    interval(a,b)
  correction(H)
    partial_state

Each node can point to Symbol Registry definitions and executable implementations.

## Recommended experiments

1. Replace F_d with several genuinely distinct operator families and test which Core Formula behavior is invariant.
2. Compare recursive source form against its closed-form scalar multiplier to determine whether recursion contributes anything beyond representation.
3. Convert feedback into an actual discrete recurrence and study stability.
4. Require generated multi-symbol formulas to compile to the same operator graph they display.
5. Build exact/analogy links between Glyphic Registry entries and Math Symbol Registry entries rather than conflating their semantics.

## Lineage
CLR-0001 Mathematical Substrate System
-> historical Core Formula work
-> CLR-0031 mathematical carrier/exercise platform
-> current Symbol Registry + Formula Registry + dual glyph/math curriculum.

Related:
- CLR-0027 Mashet Ontological Framework
- CLR-0028 Mashet integrated substrate generator
- CLR-0030 interactive Notebook/platform ancestor
- CFA registry for normalized Core Formula algebra.

## Status
Assessed / High-value mathematical carrier ancestor / Formula Registry reconstruction candidate.
