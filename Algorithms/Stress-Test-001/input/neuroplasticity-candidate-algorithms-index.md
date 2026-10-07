# Neuroplasticity → Systems: Candidate Algorithms — Stress-Test Extraction

**Status:** Proposed. Nothing here is confirmed or implemented yet.
**For:** the Echo design library.

This file is a source-derived compact extraction for Stress Test 001. It preserves the mechanism hierarchy and candidate algorithm definitions needed for registry formation. The complete source remains the canonical document.

## 0. Shared model
Node { id, kind, payload_ref, status, provenance }
Link { a, b, w, H, last_used, wins, losses, protect, tag }
Budget { M memory, C compute, E energy, T time } each has usage and cap
Clock: tick = one awake step; rest = one offline maintenance cycle

## A. Budgets and the resource envelope
### A1. Resource envelope
- **A1-a: Hard caps with deferral.** Estimate operation cost; defer if cap would be exceeded.
- **A1-b: Token buckets.** Budgets refill to caps; operations spend tokens.
- **A1-c: Pressure bands.** Soft pressure triggers decay/consolidation; hard pressure triggers eviction.
### A2. Activation cap (sparse activation)
- **A2-a: Top-k.** Activate only top-k nodes by relevance × w.
- **A2-b: Threshold with global inhibition.** Raise threshold until active count fits cap.
- **A2-c: Energy auction.** Fill budget greedily by expected value per cost.
### A3. Bounded working set
- **A3-a: Fixed slots with LRU.** Evicted active items become dormant, not deleted.
- **A3-b: Weighted slots.** Active set must fit total slot-weight W.
- **A3-c: Chunk-aware slots.** A consolidated concept token occupies one slot.
### A4. Wiring cost (link pricing)
- **A4-a: Flat rent plus domain multiplier.**
- **A4-b: Distance-priced.**
- **A4-c: Bridge quota.**
### A5. Fan-out cap with competition
- **A5-a: Evict the weakest.**
- **A5-b: Probation slots.**
- **A5-c: Competitive depression.**
### A6. Normalization (synaptic scaling)
- **A6-a: Divisive normalization.**
- **A6-b: Multiplicative scaling at rest.**
- **A6-c: Target-sum controller.**

## B. Strengthening
### B1. Traversal counters → priority
- **B1-a: Count plus recency.** H += 1; P = log(1+H) × exp(−λ × age).
- **B1-b: Outcome-weighted.** P uses Laplace-smoothed wins/losses × recency.
- **B1-c: Saturating counter.** Small 0–3 success/failure counter.
### B2. Hot-path promotion (functional myelination)
- **B2-a: JIT-style tiers.** interpreted → cached → compiled/direct; demote with disuse.
- **B2-b: Adaptive cache (ARC-style).**
- **B2-c: Materialized index.**
### B3. Stability–plasticity protection
- **B3-a: Per-link protect factor.** Effective update Δw × (1 − protect).
- **B3-b: Anchor penalty.**
- **B3-c: Frozen core, plastic shell.**

## C. Balance
### C1. Homeodynamic (−,+): recursive return with a time limit
- **C1-a: Time-sliced return.**
- **C1-b: Return with backoff.**
- **C1-c: Release–reinforce pulse.**
### C2. Heterostatic (±,−): mitigating runaway one-track bias
- **C2-a: Aging.**
- **C2-b: Residency cap.**
- **C2-c: Diminishing returns.** Effective priority P/(1+β×recent_share).
### C3. Homeostasis (−,±): bounded resulting state
- **C3-a: Setpoint with dead band.**
- **C3-b: PID controller.**
- **C3-c: Hysteresis switches.**
### C4. Heterodynamics (+,+): integrated synthesis
- **C4-a: Bridge search.**
- **C4-b: Analogy scaffold.** Use (?):(?)::(?):(?) across domains and retain tested fillings.
- **C4-c: Co-activation merge.**

## D. Trial and error
### D1. Explore/exploit ratio
- **D1-a: ε-greedy with decay.**
- **D1-b: UCB1.**
- **D1-c: Thompson sampling.**
### D2. Candidate lifecycle
- **D2-a: State machine with thresholds.**
- **D2-b: Tournament.**
- **D2-c: Evidence accumulator.**
### D3. Weakening with salvage
- **D3-a: Fixed decay window.**
- **D3-b: Cost-gated search.**
- **D3-c: Gist extraction by fading.**

## E. Forgetting
### E1. Temporally displaced forgetting (dormant, not deleted)
- **E1-a: Status flip.**
- **E1-b: Tiered storage.**
- **E1-c: Checkpoint and summary.**
### E2. Obliviously discarded forgetting (with anti-repetition)
- **E2-a: Tombstone record.** Keep {hash, reason, time, pointer to salvaged abstraction}.
- **E2-b: Bloom filter.**
- **E2-c: Expiring tombstones.**

## F. Consolidation and concept tokens
### F1. Tagging and capture (two-phase consolidation)
- **F1-a: Tag, then budgeted commit.**
- **F1-b: Repetition-captured.**
- **F1-c: Reward-captured.**
### F2. Concept token formation ({A,B,C} → X)
- **F2-a: BPE-style pair merge.**
- **F2-b: Frequent subgraph.**
- **F2-c: Validated merge.** Adopt X only if it passes D2: predicts as well as parts while costing less.
### F3. Concept token economics (hot token, cold provenance)
- **F3-a: Pointer token.** X = {cost, ref → [A,B,C,relations,experiences]}.
- **F3-b: Expand on doubt.**
- **F3-c: Cost-accounted swap.**
### F4. Attention as compute scheduling
- **F4-a: Softmax shares.**
- **F4-b: Top-k plus round-robin.**
- **F4-c: Weighted fair queuing.**
### F5. Routing to specialists (reuse and multiplexing)
- **F5-a: Top-2 router.**
- **F5-b: Load-balanced router.**
- **F5-c: Primitive library.**
### F6. Recursive consolidation with presentiated refinement
- **F6-a: Loop with in-place update.** Recheck abstractions against source experiences; strengthen/refine/lower resolve; repeated failure → D3.
- **F6-b: Shadow and promote.**
- **F6-c: Adaptive ratio.**

## G. Rest and repetition
### G1. Rest maintenance cycle
- **G1-a: Fixed three-phase pass.** Downscale; replay; garbage-collect/compact.
- **G1-b: Prioritized replay.**
- **G1-c: Pressure-triggered rest.**
### G2. Higher-order recursive return (topic-scale audit)
- **G2-a: One level per cycle.** general → root → morphology → placement → specialized → complete.
- **G2-b: Interleaved levels.**
- **G2-c: Return to the failing level.**
### G3. Spaced repetition
- **G3-a: Leitner boxes.**
- **G3-b: SM-2 style.**
- **G3-c: Forgetting-curve scheduler.**

## Dependencies at a glance
A1 envelope → A2 activation cap → F4 attention scheduling
A1 envelope → A3 working set → E1 dormant
A1 envelope → C3 homeostasis → A6 normalization
B1 counters → B2 hot paths → F2 concept tokens → F3 hot/cold economics
D1 explore/exploit → D2 lifecycle → D3 salvage → E2 tombstones
F1 tagging → G1 rest cycle → G2 topic-scale audit / G3 spaced repetition / F6 recursive consolidation → C4 synthesis
C1 homeodynamic return + C2 anti-capture wrap the schedulers.
