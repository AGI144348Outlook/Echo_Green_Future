# Core Formula Algebra Registry — Initial Entries

## CFA-0001 — Canonical Nested-Ray Form
**Sources:** CLR-0013, CLR-0014  
**Classification:** Canonical historical form

`S(t) = A + Σ_i(Σ_n F_n(R_i)) + ∫ C(τ)dτ`

Interpretation: anchor plus aggregate recursive/fractal ray contributions plus accumulated feedback.

---

## CFA-0002 — Ray-Sum Flattening
**Sources:** canonical form  
**Classification:** Algebraic equivalence, assuming finite/convergent sums

`Σ_i(Σ_n F_n(R_i)) = Σ_i Σ_n F_n(R_i)`

Therefore:

`S(t) = A + Σ_i Σ_n F_n(R_i) + ∫ C(τ)dτ`.

If index domains permit reordering under the relevant convergence assumptions:

`Σ_i Σ_n F_n(R_i) = Σ_n Σ_i F_n(R_i)`.

---

## CFA-0003 — Geometric Fractal Ray Specialization
**Source:** CLR-0013  
**Classification:** Defined specialization

If:
`F_n(R_i;c) = λ^n m_n(c)R_i`

then:

`Σ_n F_n(R_i;c) = R_i Σ_n λ^n m_n(c)`.

CLR-0013 uses:
`m_n(c)=1+0.1c sin(0.5n)`.

This factorization separates ray direction from scalar recursive magnitude.

---

## CFA-0004 — 1D Action Interpretation
**Source:** CLR-0013  
**Classification:** Implementation heuristic, NOT equivalent to CFA-0001

Let:
`G_i = Σ_n F_n(R_i)`
and error sign `q=sign(target-A)`.

The code constructs:
`w_i = exp(qG_i) / Σ_j exp(qG_j)`

then:
`a = (Σ_i w_i R_i)(1+B)`

and:
`A_{t+1}=clip(A_t+ηa,0,50)`.

The historical code does not explicitly compute `S(t)=A+Σ_iG_i+B`; it converts ray terms into action-selection weights.

---

## CFA-0005 — Decayed Spatiotemporal Feedback Kernel
**Source:** CLR-0013  
**Classification:** Defined specialization

Historical feedback can be written:

`B_t = β Σ_m e_m exp(-α_t Δt_m) exp(-α_x |A_t-A_m|)`.

CLR-0013 uses approximately:
- `α_t=0.05`
- `α_x=0.1`.

This turns the integral notation into a discrete kernel-weighted memory sum.

---

## CFA-0006 — 2D Vector Ray Specialization
**Source:** CLR-0014  
**Classification:** Defined specialization

For context vector `c` and unit ray `R_i`:

`F_n(R_i;c)=λ^n[1+0.2<R_i,c>sin(0.3n)]R_i`.

Then:
`G_i(c)=Σ_n F_n(R_i;c)`.

Target-aligned aggregate:
`V(c)=Σ_i max(0,<R_i,c>)G_i(c)`.

This introduces vector-valued operands and context alignment.

---

## CFA-0007 — 2D Gaussian Feedback Field
**Source:** CLR-0014  
**Classification:** Defined specialization

For memory `m`:
- remembered position `x_m`,
- success `s_m`,
- normalized remembered target direction `d_m`,
- temporal age `Δt_m`,

`B_t = β Σ_m d_m s_m exp(-α||x_t-x_m||²) exp(-γΔt_m)`.

Historical parameters:
- `β=0.08`
- `α=0.1`
- `γ=0.02`.

---

## CFA-0008 — 2D Normalized State-Action Update
**Source:** CLR-0014  
**Classification:** Implementation heuristic

`u_t = V(c_t)+B_t`

`a_t = u_t / ||u_t||` when `||u_t||>0`

`x_{t+1}=x_t+ηa_t`, with historical `η=0.3`.

Again, this is an action interpretation of the architectural formula, not a direct algebraic equality to CFA-0001.

---

## CFA-0009 — Structural-Invariant Feedback Generalization
**Sources:** assessment of CLR-0013/CLR-0014  
**Classification:** Proposed modernization / not historical equivalence

Replace raw-coordinate similarity:
`K(x_t,x_m)`

with structural-signature similarity:
`K(φ(z_t),φ(z_m))`

where `φ` extracts invariant relational features.

Then:
`B_t = β Σ_m d_m s_m K(φ(z_t),φ(z_m))T(Δt_m)`.

This is the algebraic direction needed to test transfer under translation or other surface transformations. It is a proposed generalization, not evidence that the historical agents implemented it.

---

## CFA-0010 — Discrete Core-State Family
**Source:** later Echo formula program  
**Classification:** Related canonical family; mapping not yet proven

`S_k = 𝒜(S_{k-1}) + 𝒇(U_k) + M(S_{<k}) + C_k + ε_k`.

Potential correspondence to the earlier formula:
- anchor/current-state contribution ↔ `𝒜(S_{k-1})`
- ray/input contribution ↔ `𝒇(U_k)`
- feedback integral ↔ `M(S_{<k})`
- explicit coupling ↔ `C_k`
- stochastic residual ↔ `ε_k`.

This is a candidate semantic mapping and should not yet be labeled strict algebraic equivalence.

### CFA-0015 — Context-Weighted Operator Mixture
**Source:** CLR-0016. **Classification:** defined operator specialization.
`W_c(t)=sum_i alpha_i(t) W_i(t)`; executable update is `S(t+1)=tanh(W_c(t)S(t))`. This upgrades scalar weighting into a state-transforming operator mixture.

### CFA-0016 — Rank-One Operator Adaptation
**Source:** CLR-0016. **Classification:** implementation heuristic.
`W_i <- W_i + eta alpha_i (g tensor S)`, with `g=0.1(target-S_next)`. This is a local outer-product adaptation rule, not a demonstrated exact gradient of the full recurrent objective.

### CFA-0017 — Basis Decomposition of Learned Operators
**Source:** CLR-0016. **Classification:** proposed algebraic representation.
`W_i=sum_j c_ij ell_j`. If the `ell_j` form a chosen operator basis/frame, learned transformations can be represented by coefficients over registry-addressable primitive operators. Basis completeness/independence must be specified.

### CFA-0018 — Ordered Glyph-Operator Composition
**Source:** CLR-0016. **Classification:** proposed compositional algebra.
`O_word=ell_i1 ell_i2 ... ell_ik`. Operator order is generally significant because `ell_i ell_j != ell_j ell_i`. The commutator `[ell_i,ell_j]=ell_i ell_j-ell_j ell_i` becomes a direct diagnostic of order sensitivity.

### CFA-0019 — Operator-Basis Vectorization
**Source:** CLR-0017. **Classification:** exact linear representation within the chosen span.
Let `L=[vec(ell_1) ... vec(ell_22)]`. Then `vec(W_hat)=Lc`, with least-squares coefficients `c=L^+vec(W)`. For d=8, 22 elements span at most a 22-dimensional subspace of the 64-dimensional full matrix space.

### CFA-0020 — Gram-Corrected Coefficient Update
**Source:** CLR-0017 assessment. **Classification:** proposed correction.
For a non-orthonormal operator frame, coefficient geometry is governed by `G=L^T L`. A projected operator-space update `delta_w` can be mapped by `delta_c=L^+ delta_w=(L^T L)^+L^T delta_w` when appropriate. Using only `L^T delta_w` assumes orthonormal-coordinate geometry.

### CFA-0021 — Orthogonal-Activation Degeneracy
**Source:** CLR-0017. **Classification:** exact diagnostic result.
If every glyph operator is orthogonal, `ell_j^T ell_j=I`, then `||ell_j S||_2=||S||_2` for all j. Therefore `argmax_j ||ell_j S||` cannot provide meaningful state-dependent glyph selection. A discriminative readout must depend on direction, task consequence, prediction, or a non-isometric transform.

### CFA-0022 — Glyph Composition Commutator Test
**Source:** CLR-0017. **Classification:** diagnostic algebra.
`[ell_i,ell_j]=ell_i ell_j-ell_j ell_i`. Nonzero commutator identifies order-sensitive operator pairs and provides a direct test for whether glyph sequence can encode distinct transformations.

### CFA-0023 — Task-Operator Alignment Objective
**Source:** CLR-0019. **Classification:** defined supervised operator objective.
For external task operator `T`, internal composite `W_c=sum_i alpha_i W_i`, and transition `f_W(S)=tanh(W_c S)`, define `L_T(S)=||f_W(S)-TS||_2^2`. T is an externally specified target transformation, not a reward scalar and, in the executable implementation, is not multiplied into the forward dynamics.

### CFA-0024 — Exact One-Step Operator Gradient Through Tanh
**Source:** CLR-0019 assessment. **Classification:** derived correction.
Let `y=tanh(W_c x)`, `y*=Tx`, and `delta=2(y-y*) elementwise (1-y^2)`. Then `dL/dW_i=alpha_i(delta outer x)` for the one-step squared alignment loss. The source update omits the tanh derivative.

### CFA-0025 — Persistent-Excitation Operator Identification
**Source:** CLR-0019 assessment. **Classification:** experimental criterion.
A contracting task can make trajectory error vanish as `S->0` without identifying T. Evaluate over a probe distribution `x~D`: `E_T=E_x ||f_W(x)-Tx||^2`. For linear diagnostics also measure `||W_c-T||_F` and/or induced operator norm.

### CFA-0026 — Factorial Operator/Context Ablation
**Source:** CLR-0019 assessment. **Classification:** experimental decomposition.
Separate adaptation axes: fixed/learned `W` x fixed/learned `alpha`. This yields four core conditions and identifies whether alignment gains arise from operator adaptation, mixture adaptation, or their interaction.

### CFA-0027 — Operator Signature Map
**Source:** CLR-0020. **Classification:** diagnostic map.
Define `phi(W)=(tr(W), det(W), rho(W), ||W||_F, symmetry(W), rotation(W), damping(W))`. The components have different invariance classes: trace/determinant/spectrum are similarity invariants; Frobenius norm is invariant under orthogonal basis changes but not arbitrary similarity; symmetry/threshold scores are representation-dependent diagnostics.

### CFA-0028 — Deterministic Legibility Pipeline
**Source:** CLR-0020. **Classification:** architectural mapping.
`W -> phi(W) -> ConceptToken(phi, rule_id) -> CompositionRecord -> HumanRenderer`. Human language is a terminal rendering of a provenance-bearing intermediate representation, not the operator substrate itself.

### CFA-0029 — State-Conditioned Operator Attribution
**Source:** CLR-0020 assessment. **Classification:** proposed attribution metric.
For mixture `W_c=sum_i alpha_i W_i`, replace norm-only influence with `I_i(x)=||alpha_i W_i x||`, or intervention attribution `Delta_i(x)=||f_W(x)-f_{W\\i}(x)||`. Aggregate over held-out `x~D` for global attribution.

### CFA-0030 — Additive Mixture vs Sequential Operator Syntax
**Source:** CLR-0020 assessment. **Classification:** structural distinction.
Mixture: `W_mix=sum_i alpha_i W_i`. Sequential syntax: `W_seq=W_k ... W_2 W_1`. In general `W_2W_1 != W_1W_2`; therefore order-sensitive operator language must preserve product order rather than infer syntax from mixture weights.

### CFA-0031 — Block-Duplication Lift Intertwining Law
**Source:** CLR-0021. **Classification:** exact algebraic identity.
For `Phi(S)=[S;S]` and `F'=diag(F,F)`, `F'Phi(S)=Phi(FS)`. This commuting/intertwining relation is the primary structural preservation law for the lift.

### CFA-0032 — Block Lift Spectral and Determinant Laws
**Source:** CLR-0021. **Classification:** exact algebraic identities.
`spec(diag(F,F))=spec(F) multiset-union spec(F)`, hence `rho(F')=rho(F)`; `det(F')=det(F)^2`; `rank(F')=2 rank(F)`.

### CFA-0033 — Duplication Lift State Covariants
**Source:** CLR-0021. **Classification:** exact transformation laws.
For Euclidean norm, `||Phi(S)||_2=sqrt(2)||S||_2`; for coordinate sum, `1^T Phi(S)=2(1^T S)`. Dynamic sum conservation requires the separate base condition `1^T F=1^T` and is not implied by the lift.

### CFA-0034 — Governed Structural Transition Gate
**Source:** CLR-0021 assessment. **Classification:** proposed governance schema.
A structural transition `(X,F) --Phi--> (X',F')` is admissible only when declared preservation/covariance laws commute within tolerance, stability constraints hold, target schema is valid, and audit/rollback metadata exists. This generalizes scaling from a hard-coded resize into a Registry-addressable governed transformation.

### CFA-0035 — Token Capability Predicates
**Source:** CLR-0022. **Classification:** defined authorization algebra.
Let `TC(x)`, `TI(x)`, and `TA(x)` denote create, issue, and admit capabilities. The prototype's admission rule is `Admit(r,t) iff TA(r) AND Carried(t)`. Modernization should resolve these predicates through Governor-managed scoped capabilities rather than mutable booleans.

### CFA-0036 — Domain-Bounded Composition Rule
**Source:** CLR-0022. **Classification:** exact rule implemented by prototype.
For domain `d` with carried operand set `K_d`, a requested combination `C` is constructible only if `TC(d) AND C subseteq K_d`. This is a bounded compositional-generation rule, not proof that the result has novel semantic meaning.

### CFA-0037 — Create-Issue-Admit Transition Chain
**Source:** CLR-0022 assessment. **Classification:** proposed typed protocol.
`Symbol=Compose_d(C)`; `Token=Issue_i(Symbol)`; `Admit_r(Token)`. Each arrow has independent capability, schema, provenance, and environment constraints. Separating Symbol from TokenInstance resolves the source artifact's carried=false admission contradiction.

### CFA-0038 — Scoped Governor Authorization Relation
**Source:** CLR-0022 assessment. **Classification:** proposed governance generalization.
`Permit(subject, action, object, environment, constraints)`. TC/TI/TA become action-specific projections of this relation. This allows the same authorization algebra to govern Registry queries, operator/glyph composition, NVE admission, structural transitions, and executable Notebook ActionRequests.
