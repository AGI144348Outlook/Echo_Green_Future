# Exact-source test observations — 2026-11-10 05Z
Pretest Issue #386 posted 05:06Z BEFORE source commit c16d95d and execution. Source: `ring27-queue-drain-20261110-05z.js`, Git blob `ef888682763bd02a76c1e0acba61ede469829261`. Exact GitHub-fetched source executed via isolated V8 Function; proposed Node runtime was NOT used. Four seeds, ten preregistered types per seed: **40/40 predicates true**. See same-thread post-test comment #6759520196.
| seed | initial occupied | queued | drained | final pending | forward L1 | reverse L1 | shifted topology L1 | mass error | predicates |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
|10501|27|27|27|0|9.3433343665|0.9343334367|2.7502061690|4.9738e-14|10/10|
|10502|27|27|27|0|7.5875517513|0.7587551751|3.2398692043|3.1974e-14|10/10|
|10503|27|27|27|0|8.5817691360|0.8581769136|3.0148145735|3.5527e-14|10/10|
|10504|27|27|27|0|7.8259865207|0.7825986521|3.1808879687|3.5527e-14|10/10|
No failures. All 54 unique IDs accounted for; 27-seat capacity respected; zero-coupling identity, deterministic replay, nonnegative mass held. Interpretation: synthetic FIFO batch-drain accounting only, not learning or physics. Limitations: deliberately uniform two-per-seat arrivals, simultaneous release, no incremental service, fixed cyclic shift rather than randomized topology, and no genuine semantic evaluation. Research first: Lu et al. bioRxiv posted Nov 3 2026 DOI 10.64898/2026.10.29.762761; Clark et al. Nature Neuroscience Oct 14 2026 DOI 10.1038/s41593-026-02452-4. Neither validates Echo.
