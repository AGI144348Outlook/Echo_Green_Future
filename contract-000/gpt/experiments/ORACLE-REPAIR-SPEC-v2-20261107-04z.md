# Echo-GPT oracle repair specification v2 — untested, noncanonical
Prerequisite: Issue #330 prospective protocol, amended before material test changes. No test executed in this run.

## Why
Claude's earlier E100 10/13 mutant detection missed three lifecycle faults: missing final release, an arrival left open at horizon, and an entirely absent arrival lifecycle. An event-only oracle cannot detect a lifecycle removed from its own event stream. The independent arrival census is the separate witness.

## Independent inputs
- `arrival_census`: tuples (arrival_id, tick), generated before the ledger and hashed as canonical sorted JSON.
- `events`: ordered (tick, phase, sequence, arrival_id, kind, seat_id), with explicit phase order.
- `horizon`, `dwell_ticks`, `seat_count`, `expiry_ticks`, `seed`; all pinned.
- `terminal`: admitted/expired/unresolved with mutually exclusive terminal semantics. A horizon-finalized unresolved arrival must have an explicit reason, not silently disappear.

## Verification obligations
1. Every census arrival has exactly one arrival event; no phantom arrivals.
2. Each arrival receives exactly one terminal outcome by horizon, or an explicitly declared pending state if the preregistered model allows it.
3. Every seat admission has one matching release, except a preregistered horizon truncation record with residual occupancy.
4. No seat overlaps at any phase; explicit same-tick release/admit ordering.
5. FIFO and expiry compare against independently replayed waiting queue, not simulator-reported queue.
6. No mutation gets credit unless activated, trace-distinct from baseline, and detected by independent verifier.
7. Oracle itself must not import simulator transition functions; verify code provenance and dependency graph before claiming independence.

## Ten types remain T1–T10 of #330
T1 conservation, T2 duplicate, T3 missing, T4 double admission, T5 FIFO, T6 dwell overlap, T7 expiry, T8 replay, T9 causal dwell ablation, T10 held-out ring prediction. Keep seed range 1106–1135. T9/T10 must use uncoupled, shuffled, no-op controls and report null/negative results. Distinguish ledger integrity from semantic or causal inference. This document is a design artifact, not execution evidence.

## Research consulted before development (2026-11-07 04Z)
- Tasnim/Dwyer/Hossain, TOGBench (2026-07-05), DOI 10.1145/3805760.3814927: oracle diversity; Java tests, not Echo.
- Nasir/Shah/Alam (2026-09-21), arXiv 2609.24230: output-invisible faults require fault-class-matched oracles; quantum compiler context.
- Shulepov (2026-08-27), arXiv 2608.27100: reproducibility mutation blind spots; ML repository context.
- Egashira et al. (2026-10), arXiv 2610.13065: generated tests can be weak despite high reference pass rate; benchmark not an Echo evaluation.

**No run, CI, inference, deployment or repository tests were performed.**
