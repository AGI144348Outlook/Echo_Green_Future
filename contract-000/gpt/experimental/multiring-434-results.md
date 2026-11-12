# Issue #434 — measured outcomes (2026-11-12 04Z)

Pretest: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/434. Source commit: 494b25d93de008cbee74ae90716209075d4b9595.

**Execution:** Four fixed seeds 11,23,37,53; 10 distinct scripted predicates per seed; locally transcribed Python stdlib implementation, NOT independently byte-exact executed from retrieved GitHub blob. Python local execution. **32/40 PASS, 8/40 FAIL.** All four seeds failed both zero-gain and common-phase null tests.

| seed | replay | unique | mass error | min mass | zero-gain L1 | uniform L1 | heterogeneous L1 | triad/pair L1 | shuffle L1 | boundary L1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|11|0|27|0|0.404376|5.861901|1.511774|9.182337|4.874494|28.610270|1.591184|
|23|0|27|0|0.374715|5.728590|1.359749|8.829505|4.710595|34.272148|1.494222|
|37|0|27|0|0.331878|5.176751|1.519320|7.798760|4.534921|29.653304|1.553475|
|53|0|27|1.42e-14|0.395080|5.058419|1.722788|7.174228|4.906940|33.131209|1.706839|

**Observations vs interpretations:** Deterministic replay, uniqueness, mass conservation, nonnegative mass and intervention distinctions passed all seeds. Zero-gain control FAIL is a fixture construction error: shuffled affinity consumes random draws before mass initialization, so compared baselines have different starting states even with gain=0. Uniform-phase null FAIL is a model/design mismatch: radius feedback depends on absolute phase (sin phase), so a uniform frequency shift affects mass. Thus the preregistered expected invariance is not a valid symmetry of this model. Neither failure should be silently changed to PASS. The large shuffled-affinity difference may also be contaminated by initial-state RNG divergence. No independent prediction task was run; no learning or physical precession demonstrated.

**Next:** preregister an amendment before any rerun; decouple RNG streams for initial state and affinity permutation, and either use relative-phase radius feedback or explicitly treat common-phase shift as a positive intervention. Preserve the original failed record. No canonical changes.
