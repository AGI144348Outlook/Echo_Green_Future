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
