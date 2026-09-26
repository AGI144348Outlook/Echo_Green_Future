# CLR-0019 — Task Operator Framework: Externally Legible Causal Interface

## Classification
Executable controlled-comparison prototype. First direct response in this lineage to the CLR-0018 benchmark/ablation requirement.

## Core contribution
The task is represented as an externally specified transformation T rather than only as a scalar reward. The learned internal composite is
W_c(t)=sum_i alpha_i(t) W_i(t)
and the observable one-step target is
S_target(t+1)=T S(t).

The experiment minimizes the mismatch
e_t=||S(t+1)-T S(t)||,
where the implemented state transition is
S(t+1)=tanh(W_c(t)S(t)).

This creates an externally legible causal interface: internal operator dynamics can be evaluated against a transformation defined independently of the learner.

## Why this matters for Echo
This is a stronger experimental primitive than a self-authored fitness score. A Notebook ExperimentSpec can supply T, instantiate competing internal mechanisms, and compare how accurately each reproduces the same external transformation.

It also creates a clean bridge to the Formula Registry:
TaskSpec -> TaskOperator T -> candidate internal operator composition -> observed transition -> alignment residual -> evidence record.

## Important correction: T is not literally applied in forward dynamics
The source header writes:
S(t+1)=T (sum_i alpha_i W_i) S(t).
The executable code does NOT do this. It computes
S(t+1)=tanh(W_c S(t))
and uses T S(t) only as the supervised target.

That distinction is important. The implementation is operator imitation/alignment, not composition with T.

## Major baseline confound
FixedWeightSystem overrides only update_alpha_alignment(). It inherits update_operators_alignment(), so its W_i matrices continue learning every step. Therefore "Fixed Operators" means fixed alpha, NOT fixed operators.

A true fixed-operator baseline must override update_operators_alignment() as a no-op.

Likewise RandomWeightSystem randomizes alpha while still learning W_i. It is not a fully random-operator baseline.

## Scalar baseline issue
The scalar baseline's finite-difference procedure mutates and renormalizes the full weight vector while perturbing one coordinate, then attempts to restore only that coordinate and renormalizes again. This does not cleanly estimate the partial derivative with respect to one scalar weight. Use a copied weight vector for each finite-difference evaluation.

It also uses state_history[-2] while the current alignment_error was generated from the immediately previous state. Align the same transition in both base and perturbed evaluations.

## Gradient issue in adaptive operator learner
The loss is measured after tanh:
L=||tanh(W_c S)-TS||^2.
The exact one-step derivative through the nonlinearity contains the tanh Jacobian:
delta = 2(S_next-TS) elementwise (1-S_next^2).
The current update omits this factor. It is a local error outer-product rule, not the exact gradient of the implemented loss.

A corrected per-operator gradient is:
dL/dW_i = alpha_i [delta outer S_prev].

## State-collapse confound
The task is a damped rotation with no continuing excitation/input. Since the first 2D block contracts by 0.95 and tanh is also contractive near/away from saturation, S can approach zero. Then both learner output and T S approach zero, making alignment error small even without learning T.

This is the most important experimental validity issue.

Test operator identification on a persistent distribution of probe states x~D, or inject excitation u_t. Measure operator error independently:
E_T = E_x ||f_W(x)-Tx||^2.
For a linear/no-tanh diagnostic, also report ||W_c-T||_F or spectral/operator norm.

## Fair-comparison requirements
All systems should begin from matched initial S and matched W_i for each seed. The current single seed followed by sequential constructors produces different random initializations for each architecture. Reproducibility exists, but initialization is not matched.

Use a generated RunSpec containing initial_state and initial_operators, deep-copy it into every condition, and vary only the mechanism under test.

## Statistical requirements
Five runs are useful for debugging but insufficient for strong comparative claims. Report distributions across more seeds, confidence intervals/effect sizes, and predefine convergence criteria.

Final-step error alone is noisy. Also report area under error curve, held-out probe error, time-to-threshold, stability, and operator-distance metrics.

## Strong experimental design
Factor the mechanisms explicitly:
A: fixed W, fixed alpha
B: fixed W, learned alpha
C: learned W, fixed alpha
D: learned W, learned alpha
E: random-update control
F: scalar-mixture baseline

This 2x2 decomposition identifies whether improvement comes from operator adaptation, mixture adaptation, or both.

## Recommended task suite
Use several T classes rather than one damped rotation:
- identity;
- rotation;
- contraction/expansion within stable limits;
- shear;
- reflection;
- permutation;
- low-rank projection;
- noncommuting task sequences T2 T1 versus T1 T2.

Train on probe states and test on held-out states. The last condition directly connects to glyph/operator composition research.

## Status
Candidate experiment; promising causal benchmark interface, but conclusions about operator advantage are pending corrected baselines and anti-collapse controls.
