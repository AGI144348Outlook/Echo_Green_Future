# Code Library Assessment — CLR-0014

# Structural Intelligence — 2D Ghost Attractor Experiment

**Short identity:** 2D GHOST ATTRACTOR  
**Architectural tag:** Vector Rays / Spatial Feedback Field / Structural Transfer Test  
**Lineage:** CLR-0013 Ghost Attractor Experiment  
**Disposition:** Candidate for extraction; transfer interpretation requires redesign  
**Current Echo relevance:** Very High

## Executive assessment
This artifact extends CLR-0013 from scalar 1D motion to a 2D vector state. It adds:
- a 2D anchor position,
- 12 quasi-even directional rays,
- recursively scaled vector ray contributions,
- Gaussian spatial feedback,
- temporal decay,
- successful-target direction memory,
- circular-path training and translated-circle testing,
- spatial memory-field visualization.

It is a useful formula-development artifact and belongs in the Core Formula Algebra Registry lineage.

## Formula interpretation
Historical displayed form:

`S(t) = A + Σᵢ(Σₙ Fₙ(Rᵢ)) + ∫C dτ`.

This implementation gives the ray term a vector interpretation:
`F_n(R_i;c) = λ^n [1 + <R_i,c>·0.2 sin(0.3n)] R_i`.

The implemented aggregate action is closer to:
`a_t = Normalize( Σ_i max(0,<R_i,c_t>) Σ_n F_n(R_i;c_t) + B_t )`
`x_{t+1} = x_t + η a_t`.

Thus, as in CLR-0013, the displayed S(t) formula is architectural inspiration rather than a literal computed state equation.

## Feedback kernel
For successful memories:
`B_t = β Σ_m d_m exp(-0.1||x_t-x_m||²) exp(-0.02Δt_m) s_m`

where `d_m` is the normalized historical direction from remembered position to remembered target.

This is a useful explicit kernel decomposition for the algebra registry.

## Major transfer-validity issue persists
Training occurs around center (5,5), testing around (15,15), while retrieval is based on absolute Euclidean proximity:
`exp(-0.1||x_t-x_m||²)`.

The center translation is about 14.14 units. At that separation the Gaussian factor is approximately `exp(-20)`, effectively zero for direct Phase-1 influence near the translated Phase-2 region.

Therefore this mechanism does not encode translation-invariant circular structure. Any improved Phase-2 performance cannot, by itself, demonstrate a ghost influence from the distant Phase-1 circle.

Moreover, Phase 2 immediately appends new memories at the test location, so the feedback-memory field visualized after the full experiment mixes training and test memories. It cannot show that the test region was influenced while still unvisited.

## Better ghost-transfer test
Freeze Phase-1 memory before testing and evaluate the first translated episode without writing Phase-2 memories.

Compare:
1. full Phase-1 memory,
2. memory cleared,
3. absolute-position kernel,
4. translation-invariant structural-signature kernel.

A circle signature could include radius, phase-relative tangent, curvature, angular velocity, normalized target displacement, and trajectory periodicity.

Then translated circles can be compared in local coordinates.

## Ray generation
The method name `_fibonacci_sphere_2d` is somewhat misleading. It generates directions on a circle using a golden-ratio angular sequence, not a sphere.

For 2D, equally spaced angular rays would already give exact uniform angular spacing. Golden-angle ordering can still be useful for progressive sampling.

## Success metric
`success = max(0,1-dist/10)` is a hand-designed proximity score. It is not an independent success measurement.

A modern experiment should explicitly distinguish:
- task error,
- reward/success definition,
- memory write weight,
- retrieval similarity.

## Memory-field visualization
The plotted field sums spatial kernels multiplied by stored success. It omits temporal weighting and remembered direction used by the actual feedback computation, so it is not the actual feedback vector field.

It is best classified as a scalar memory-density/success-weight illustration.

## Current Echo relevance
The artifact strengthens the connection between the old formula program and current:
- vector operands,
- glyph/operator rays,
- feedback memory,
- generalized pattern retrieval,
- invariant transformations,
- environment-local coordinates,
- experiment audits.

The translated-circle failure mode is especially useful: generalization requires a representation that survives translation rather than a kernel tied to raw coordinates.

## Suggested extraction
- VectorState/Anchor.
- RaySet.
- RayContribution operator.
- FeedbackKernel.
- MemoryRecord.
- StructuralSignature.
- SimilarityKernel registry.
- frozen-memory transfer protocol.
- ablation harness.
- explicit formula evaluation trace.

## Lineage
`CLR-0013 scalar ghost-attractor test → CLR-0014 vector/spatial-field test`.

Both should feed the Core Formula Algebra Registry, but neither should be recorded as empirical proof of ghost attractors.
