# Code Library Assessment — CLR-0013

# Structural Intelligence — Ghost Attractor Experiment

**Short identity:** GHOST ATTRACTOR EXPERIMENT  
**Architectural tag:** Anchor/Ray Dynamics / Decayed Feedback Memory / Transfer Experiment  
**Disposition:** Candidate for extraction; experiment requires redesign before its ghost-attractor conclusion is interpretable  
**Current Echo relevance:** Very High

## Executive assessment
This Python experiment is an important ancestor of the current Echo structural formula family. It operationalizes a state/action architecture described as:

`S(t) = A + Σᵢ(Σₙ Fₙ(Rᵢ)) + ∫C dτ`

with:
- anchor/current position,
- directional rays,
- recursively/fractally decayed ray contributions,
- feedback history,
- temporal decay,
- spatial similarity,
- target-driven action selection,
- baseline-controller comparison,
- a three-phase transfer protocol.

The strongest lineage contribution is the attempt to turn the symbolic structural formula into an executable agent with measurable behavior.

## Formula lineage
The artifact clearly anticipates later Echo concepts:
- anchor,
- rays,
- feedback,
- memory/history,
- recursively scaled contributions,
- target/context modulation,
- ghost attractors,
- structural transfer testing.

It should be cross-referenced with the current kernel/formula work rather than treated as an isolated controller experiment.

## Agent dynamics
The agent stores four fixed rays:
`[-1.0, -0.3, 0.3, 1.0]`.

Each ray contribution is accumulated across levels:
`F_n(R) = λ^n · context_modulated(R)`

with a sinusoidal level modulation.

Historical feedback records:
- position,
- error,
- time.

Feedback contribution is weighted by:
- exponential temporal decay,
- exponential absolute-position similarity.

Action weights are softmax-like exponentials of ray contributions aligned to error direction, then the weighted ray action is multiplicatively modulated by accumulated feedback.

## Major experimental validity issue: the proposed ghost transfer is not encoded
Phase 1 trains around x≈10–20.
Phase 3 tests a similar oscillatory pattern around x≈35–45.

However, the memory kernel is:

`spatial_similarity = exp(-0.1 * |current_position - memory_position|)`.

This explicitly privileges **absolute spatial proximity**. When the agent is near x≈40, memories acquired near x≈15 receive a strong distance penalty.

Therefore the mechanism does not encode the key relation required by the stated test: **structural similarity of oscillatory dynamics independent of absolute location**.

If Phase 3 performs differently, the current experiment cannot cleanly attribute that result to a transferred ghost attractor from Phase 1.

To test structural transfer, memory retrieval would need features such as:
- relative target displacement,
- phase/frequency,
- trajectory shape,
- velocity/acceleration signature,
- normalized local coordinates,
- invariant relation patterns,

rather than—or in addition to—absolute position.

A strong redesign would compare:
`similarity(structural signature current, structural signature memory)`
against
`similarity(absolute position current, absolute position memory)`.

## Formula implementation caveat
The code comments say:
`State S(t) = A + rays + feedback`

but the variable `A = self.position` is not subsequently used to calculate action or an explicit S(t) value. The action is computed from ray weights and feedback, and position is then updated.

Likewise, `ray_contributions` are not directly summed into a state; they parameterize action-selection weights.

Thus this is an interpretation inspired by the formula, not a literal numerical implementation of the displayed equation.

A modern implementation should return an explicit trace:
- A,
- each F_n(R_i),
- per-ray sum,
- total ray term,
- feedback integral,
- S(t),
- selected action,
- resulting state.

## Feedback semantics
The stored value is target error. Positive/negative historical errors accumulate through the memory kernel and multiplicatively scale current action.

This can cause feedback magnitude to alter action gain without guaranteeing that the remembered contribution is appropriate to the current structural situation.

Modernization should distinguish:
- error memory,
- state memory,
- action memory,
- outcome/reward memory,
- structural-pattern memory.

## Baseline comparison caveat
The baseline is PID-like but not carefully tuned to the same task constraints. A comparison against one arbitrary controller is not sufficient to establish superiority of the structural architecture.

A stronger experiment would include:
- tuned PID,
- proportional-only,
- no-memory structural ablation,
- temporal-memory-only ablation,
- spatial-memory-only ablation,
- structural-signature-memory variant,
- randomized seeds and repeated trials.

## Ghost score caveat
The score:
`(phase3_early - phase1_late)/(phase1_early - phase1_late)`

is labeled:
- 0 = perfect transfer,
- 1 = complete relearning.

This normalization can become unstable or misleading if the Phase-1 early/late denominator is small, negative, or if Phase-3 performance exceeds either reference range.

Thresholds 0.3 and 0.6 are heuristic and not statistically justified.

A modern experiment should report confidence intervals/distributions across runs and define transfer metrics before observing results.

## Plotting defects
There is a likely indexing error:
`ep_late = 95`
followed by:
`structural_results['phase3']['positions'][ep_late]`.

Each phase contains only 50 episodes, indexed 0–49. This should raise an IndexError when `plot_results()` reaches that line.

The intended Phase-3 early episode may have been index 5 or another value in 0–49.

Plot 6 is explicitly conceptual/synthetic rather than experimental data. It must not be interpreted as measured feedback distribution.

## Reproducibility
The structural dynamics use deterministic target schedules, while some parts are deterministic as written; no explicit random seed framework or multi-run statistical protocol exists.

A modern test harness should record:
- experiment ID,
- configuration,
- code/version hash,
- seed,
- run count,
- raw trajectories,
- derived metrics,
- analysis version.

## Echo extraction candidates
1. AnchorSpec.
2. Ray/OperatorSpec.
3. recursive contribution trace.
4. FeedbackMemory record.
5. similarity-kernel registry.
6. explicit S(t) evaluation trace.
7. ActionSelection policy.
8. transfer-test harness.
9. ablation framework.
10. invariant/structural signature extractor.
11. experiment provenance.

## Strong connection to Generalization
The failed/under-specified ghost-attractor test points toward a very important current Echo problem.

Generalization requires recognizing:
`same relation/pattern under changed surface coordinates`.

Phase 1 and Phase 3 intentionally change absolute position while preserving a related oscillatory form. That is precisely the kind of transformation under which a useful generalized representation should remain recognizable.

A future Echo transfer experiment could deliberately test:
`surface transformation → invariant extraction → pattern retrieval → transfer`.

This connects the old ghost-attractor work directly to the current Generalization Registry and algebraic notebook work.

## Assessment conclusion
This artifact is historically important even if its original ghost-attractor test is not valid as written. In fact, the defect exposes the deeper research question clearly: **what representation lets Echo recognize a learned structure when its absolute coordinates change?**

The answer should not be hard-coded spatial proximity. It should come from extracting and indexing invariant relational structure.
