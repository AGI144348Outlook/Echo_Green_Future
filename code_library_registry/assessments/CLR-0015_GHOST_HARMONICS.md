# CLR-0015 — Wave Interference System / Ghost Harmonics

## Assessment
Very high relevance as a cross-environment test of the historical core formula:

S(t) = A + sum_i(sum_n F_n(R_i)) + feedback-memory.

The important architectural move is operand substitution. Earlier artifacts use spatial positions and directional rays; this artifact uses a base-frequency anchor, oscillatory rays, recursive temporal modulation, and coherence feedback. This suggests that the durable invariant may be the operator topology rather than a particular operand domain.

## Critical experimental issues
1. The coherence function ignores its state-vector argument and does not use ray phase or amplitude. The Phase-2 phase shift therefore cannot lower the reported coherence.
2. No mechanism restores the shifted phase, so Phase 3 does not implement self-organization or recovery.
3. The state is sampled every 0.1 seconds: 10 Hz sampling, 5 Hz Nyquist. The modeled carriers begin at 440 Hz. FFT peaks are therefore aliased and cannot be compared directly with the 440-Hz-plus expected frequencies.
4. The recursive modulation multiplies a low-frequency cosine by each carrier. Product-to-sum identities predict upper and lower sidebands. Such components are expected modulation products, not automatically emergent ghost frequencies.
5. The historical consonance metric measures closeness to integer ratios and therefore does not faithfully represent many simple rational intervals.

## Core-formula contribution
This artifact motivates a typed structural schema:

S = Anchor<TA> + Aggregate(Recursive(Ray<TR>, context)) + MemoryFeedback<TM>.

Candidate invariant topology:
anchor -> recursive carrier/ray expansion -> aggregation -> feedback-memory coupling -> state/action interpretation.

This is a proposed abstraction, not proof of universal applicability.

## Recommended corrected experiment
Use a sample rate safely above twice the highest modeled carrier/sideband; compute coherence from actual phase/spectral relationships; introduce a perturbation that changes that metric; implement an adaptive recovery rule; analytically enumerate expected carriers and sidebands; compare with no-feedback/no-modulation controls; classify only unexplained residual spectral peaks as candidate emergent components.

## Disposition
Candidate for extraction into the Core Formula Algebra Registry. Historical claims of self-organization and confirmed ghost harmonics should not be treated as established results.
