# CLR-0021 — Echo Phase-1 Execution Spec: Algebraic Self-Scaling

## Classification
Structural scaling / governed architecture prototype. Directly related to CLR-0020 legibility and the EVE/NVE scale-transition lineage.

## Core contribution
The durable architecture is a transactional scaling protocol:

`current structure -> proposed lift -> algebraic validation gate -> commit OR abort -> post-lift audit`

This is substantially stronger than treating dimensional growth as an unconstrained mutation. The gate can become a Governor-controlled structural transition.

## Exact result of the supplied main test
For the specified damped 30-degree rotation,
`F = 0.95 R(pi/6)`:
- `rho(F)=0.95`
- `det(F)=0.9025`
- after 20 baseline steps, approximately `S=(-0.024014,-0.4000794)`
- duplicated state sum: `sum(S')=-0.8481868`
- after one lifted step: `sum(F'S')=-0.3405616`
- difference: approximately `0.5076252`

Therefore constraint 3 fails at tolerance `1e-6`, and the supplied main test returns `gamma=0`. The code's SUCCESS conclusion is not reached.

## Why the gate fails
State-sum conservation is not a property of a generic damped rotation. It requires
`1^T F = 1^T`
for all states (column sums equal one), or an equivalent state-specific condition.

The lift itself is structurally correct. The gate asks the lifted dynamics to preserve a quantity the base dynamics never promised to preserve.

## Exact lift laws
With
`Phi(S)=[S;S]`
and
`F'=diag(F,F)`:

1. **Intertwining / dynamics preservation**
   `F' Phi(S)=Phi(FS)`.
   This is the strongest structural invariant in the experiment.

2. **Spectrum**
   `spec(F')=spec(F) union spec(F)`, hence
   `rho(F')=rho(F)`.

3. **Determinant**
   `det(F')=det(F)^2`.
   Determinant is not numerically preserved; its transformation law is preserved.

4. **Rank**
   `rank(F')=2 rank(F)`.

5. **Duplicated-state norm**
   `||Phi(S)||_2=sqrt(2)||S||_2`.

6. **State sum**
   `sum(Phi(S))=2 sum(S)`, but dynamical sum conservation only follows if the base F preserves sums.

These should be expressed as typed lift invariants / covariants rather than the broad statement "invariants preserved."

## Gate redesign
Recommended Phase-1 structural gate:
- dimension/shape law satisfied;
- intertwining error `||F'Phi(S)-Phi(FS)|| <= eps` (preferably test on a probe basis, not only one state);
- `rho(F') <= rho_limit`;
- nonsingularity if invertibility is actually required;
- expected determinant transformation `|det(F')-det(F)^2| <= eps`;
- expected norm scaling for the lift;
- deterministic translation equality under repeated read-only rendering;
- post-lift finite-horizon stability audit.

If conservation of a quantity is desired, define it explicitly as a base-system invariant first and prove/test `q(FS)=q(S)` before requiring its lifted version.

## Stability nuance
`rho(F)<=1` is sufficient for asymptotic decay when strictly below 1 in a fixed linear discrete system, but at rho=1 Jordan structure matters for boundedness. A finite norm threshold of 100 is a heuristic runtime check, not a stability proof.

The source also calls norms below 1e-6 "collapsing" and otherwise "stable"; this should be separated from mathematical stability.

## Self-scaling claim
This demonstrates a candidate mechanism for **self-applied structural dimensional lift**, not autonomous self-scaling in the stronger sense. The lift map, target dimension, block construction, gate criteria, and commit method are externally specified. A later self-scaling claim would require Echo to propose/select a lift from a governed admissible transformation registry and justify it against declared invariants.

## Translation criterion
The translation function is deterministic in code, but Phase-1 does not actually test determinism. Test:
`render(X)==render(X)`
across repeated read-only calls and compare corresponding pre/post lift semantic records.

"Translation preserves meaning across scales" also needs an explicit semantic commutation condition, not merely successful rendering.

## Important architectural connection
This suggests a general Governor transition object:

`StructuralTransition = {source_schema, lift_operator, target_schema, preserved_properties, covariant_properties, admissibility_tests, rollback, provenance}`.

That can live in the Formula/Operator Registry and be invoked by the Notebook when Echo proposes a new structural capacity.

## Status
Candidate structural-transition protocol. Main supplied experiment correctly aborts under its current gate. Replace the mismatched state-sum condition with lift-consistency laws before treating Phase-1 as a positive scaling demonstration.
