# Neuroplasticity → Systems: Candidate Algorithms

**Status:** Proposed. Nothing here is confirmed or implemented yet.
**Compiled:** 2026-10-06, from a discussion between Timothy, Claude and GPT.
**For:** the Echo design library.

## How to read this file

- Every mechanism below was translated from neuroplasticity into systems terms by one or more of us. The **Source** line on each mechanism says who.
- Each mechanism has **three candidate algorithms**. These are alternatives, so pick one to prototype, or combine them deliberately.
- The biological side is an analogy. We copy the *function* of a brain mechanism, not its physics. For example, wires do not myelinate; what gets built is the *effect* of myelination, a cheaper path.
- All numbers are starting guesses meant to be tuned, not findings.
- Labels follow the environment guide. **Defined** means stated by Timothy. **Reading** means an interpretation that has not been confirmed yet. Everything else is **Proposed**.

---

## 0. Shared model

Every candidate below uses the same small model, so they can be compared and combined.

```
Node    { id, kind, payload_ref, status, provenance }
        status ∈ active | dormant | archived | tombstoned

Link    { a, b,
          w          strength, 0..1
          H          traversal count
          last_used  time of last traversal
          wins       times it led to a good result
          losses     times it led to a bad result
          protect    0..1, how locked it is against change
          tag        cheap "maybe keep" mark, set while awake }

Budget  { M memory, C compute, E energy, T time }   each has usage and cap

Clock   tick  = one awake step (streaming thought)
        rest  = one offline maintenance cycle (sleep)
```

---

## A. Budgets and the resource envelope

### A1. Resource envelope

**Source:** GPT. A skull and a metabolism become a hard capacity ceiling. **Function:** hard ceilings on memory, compute, energy and time, so the environment itself governs growth.

- **A1-a: Hard caps with deferral.** Estimate each operation's cost before running it. If usage plus cost would exceed the cap, defer the operation to the next rest cycle.
  - *Strength:* simple and predictable.
  - *Weakness:* growth can stall when the system is busy.
- **A1-b: Token buckets.** Each budget refills at a fixed rate per tick, up to its cap, and every operation spends tokens from it.
  - *Strength:* allows short bursts while holding the long-run rate.
  - *Weakness:* the refill rates need tuning.
- **A1-c: Pressure bands.** A soft threshold, around 80%, triggers early decay and consolidation. A hard threshold of 100% triggers eviction.
  - *Strength:* degrades gracefully.
  - *Weakness:* more moving parts.

### A2. Activation cap (sparse activation)

**Source:** Claude. The brain uses about 20% of the body's energy, so only a few neurons fire at once. **Function:** only a few nodes are active per tick.

- **A2-a: Top-k.** Each tick, score the nodes by relevance × w and activate only the top k. Everything else stays dormant.
  - *Strength:* fixed cost per tick.
  - *Weakness:* can starve nodes that fall just below the cut.
- **A2-b: Threshold with global inhibition.** Activate any node above a threshold θ. If too many fire, raise θ until the count fits under the cap.
  - *Strength:* adapts to context.
  - *Weakness:* the threshold can oscillate.
- **A2-c: Energy auction.** Each candidate node bids its expected value minus its cost, and the budget is filled greedily by value per unit cost.
  - *Strength:* economically clear.
  - *Weakness:* needs good cost estimates.

### A3. Bounded working set

**Source:** Claude and GPT. Human working memory holds roughly 4 items; the systems equivalents are cache and active state. **Function:** a small active set, with everything else streamed to dormant.

- **A3-a: Fixed slots with LRU.** Keep k slots, around 4–7. A new item pushes out the least-recently-used item, which goes dormant, not deleted.
  - *Strength:* trivial to build.
  - *Weakness:* ignores importance.
- **A3-b: Weighted slots.** Each item costs slot-weight in proportion to its size, and the set must fit a total weight W.
  - *Strength:* large items count more.
  - *Weakness:* sizes have to be estimated.
- **A3-c: Chunk-aware slots.** A consolidated concept token occupies one slot no matter how many parts it stands for.
  - *Strength:* rewards consolidation directly.
  - *Weakness:* depends on F2 and F3.

### A4. Wiring cost (link pricing)

**Source:** Claude. Axons take space, so the brain is mostly local connections with a few long-range bridges. **Function:** every link has a holding cost, and long-range links cost more.

- **A4-a: Flat rent plus a domain multiplier.** Each link pays rent per rest cycle. Cross-domain links pay rent × m, with m around 3. A link whose value falls below its rent gets decayed.
  - *Strength:* simple.
  - *Weakness:* "domain" has to be defined.
- **A4-b: Distance-priced.** Rent scales with the graph distance between endpoints, measured before the link existed.
  - *Strength:* no domain labels needed.
  - *Weakness:* distance is costly to compute on a large graph.
- **A4-c: Bridge quota.** Each domain may hold at most q outbound bridges. A new bridge must outscore the weakest existing one to replace it.
  - *Strength:* guarantees a small-world shape.
  - *Weakness:* the quota is a hard edge.

### A5. Fan-out cap with competition

**Source:** Claude. Synapses are finite, and neighbouring synapses compete. **Function:** each node holds at most F links, and new strong links displace weak ones.

- **A5-a: Evict the weakest.** At capacity, a new link replaces the existing link with the lowest w, but only if the new link's initial w is higher.
  - *Strength:* simple.
  - *Weakness:* new links start weak and rarely win.
- **A5-b: Probation slots.** Reserve p of the F slots for newcomers. A newcomer must prove itself within N ticks or leave.
  - *Strength:* gives new links a fair trial.
  - *Weakness:* there are now two classes of slot.
- **A5-c: Competitive depression.** When one link strengthens by Δ, the node's other links weaken by Δ/(F−1). The weakest fall out naturally.
  - *Strength:* biologically faithful.
  - *Weakness:* the change spreads to every link on the node.

### A6. Normalization (synaptic scaling)

**Source:** Claude, and GPT under "homeostatic plasticity". **Function:** keep each node's total outgoing strength roughly constant, which prevents runaway.

- **A6-a: Divisive normalization.** After updates, divide each of the node's link weights by the node's total, so they sum to 1.
  - *Strength:* exact.
  - *Weakness:* strong links stay dominant, only rescaled.
- **A6-b: Multiplicative scaling at rest.** During rest, multiply every link by s < 1. Then restore any protected links by their protect value.
  - *Strength:* matches downscaling during sleep.
  - *Weakness:* the scale factor s needs tuning.
- **A6-c: Target-sum controller.** Each node has a target total S*. A small controller nudges all its weights toward S* over several cycles.
  - *Strength:* smooth.
  - *Weakness:* slow to correct.

---

## B. Strengthening

### B1. Traversal counters → priority

**Source:** GPT and Claude. Ordinary recursion strengthens nothing; strengthening only happens if a traversal changes stored state. **Function:** every pass from A to B updates that link, and future choices read from the updated values.

- **B1-a: Count plus recency.** On each traversal, H += 1 and last_used = now. Priority P = log(1+H) × exp(−λ × age).
  - *Strength:* cheap.
  - *Weakness:* counts popularity, not success.
- **B1-b: Outcome-weighted.** P = (wins+1)/(wins+losses+2), multiplied by the recency term. This is Laplace smoothing.
  - *Strength:* rewards routes that work, not just routes that are used.
  - *Weakness:* outcomes have to be labelled.
- **B1-c: Saturating counter.** A small counter between 0 and 3, like a CPU branch predictor. It steps up on success and down on failure, and the route is taken when the counter is ≥ 2.
  - *Strength:* tiny and stable.
  - *Weakness:* coarse.

### B2. Hot-path promotion (functional myelination)

**Source:** Claude and GPT. Myelination maps to JIT compilation, caching, indexing and data locality. **Function:** frequently used, successful routes become cheaper, and the promotion reverses with disuse.

- **B2-a: JIT-style tiers.** A route starts interpreted (Tier 0). After N uses it is cached (Tier 1). After M uses with a good success rate it is compiled into a direct route or concept token (Tier 2). If it goes unused for D rest cycles, it demotes one tier.
  - *Strength:* proven pattern.
  - *Weakness:* three thresholds to tune.
- **B2-b: Adaptive cache (ARC-style).** Balance recency and frequency lists automatically, and promote whatever stays in the frequency list.
  - *Strength:* self-tuning.
  - *Weakness:* more complex.
- **B2-c: Materialized index.** During rest, precompute the answers to the most-asked lookups, and drop each index when its hit rate falls.
  - *Strength:* good for read-heavy systems.
  - *Weakness:* the indexes go stale.

### B3. Stability–plasticity protection

**Source:** Claude. Elastic Weight Consolidation (EWC) gives each weight its own protection. **Function:** important, consolidated links resist being overwritten, while new learning stays possible.

- **B3-a: Per-link protect factor.** The effective update is Δw × (1 − protect). Protect rises with consolidation and with use.
  - *Strength:* simple.
  - *Weakness:* protect can lock links in permanently unless it also decays.
- **B3-b: Anchor penalty.** An update is accepted only if (gain from the change) − λ × protect × (Δw)² > 0.
  - *Strength:* principled.
  - *Weakness:* needs a gain estimate.
- **B3-c: Frozen core, plastic shell.** The top p% of links by importance are read-only, and everything else learns freely. The core is re-ranked every rest cycle.
  - *Strength:* easy to reason about.
  - *Weakness:* the cut between core and shell is abrupt.

---

## C. Balance (Timothy's four terms, Defined)

### C1. Homeodynamic (−,+): recursive return with a time limit

**Source:** Timothy. Return, practice, let go temporarily, continue, return. **Function:** regulated change through alternating release and reinforcement.

- **C1-a: Time-sliced return.** Each topic gets a time quantum. At the end of the quantum, checkpoint the topic, release its resources and mark it dormant. A scheduler returns to it later.
  - *Strength:* fair.
  - *Weakness:* can interrupt a topic just before it resolves.
- **C1-b: Return with backoff.** After each return that brings no progress, the next return is delayed ×2. After a return that does bring progress, the delay resets.
  - *Strength:* spends less on stuck topics.
  - *Weakness:* can neglect a topic for too long.
- **C1-c: Release–reinforce pulse.** Alternate two phases: an active phase that strengthens with (+), and a release phase that decays and goes dormant with (−). The ratio between the phases is adjustable per topic.
  - *Strength:* mirrors the (−,+) pair directly.
  - *Weakness:* the ratio has to be learned.

### C2. Heterostatic (±,−): mitigating runaway one-track bias

**Source:** Timothy. In systems terms this is starvation or scheduler capture. GPT's rule: "priority ≠ unlimited residency". **Function:** stop any single pathway from monopolizing resources.

- **C2-a: Aging.** Every waiting topic's priority rises a little each tick until it gets served. This is the classic cure for starvation.
  - *Strength:* proven.
  - *Weakness:* low-value topics eventually get served too.
- **C2-b: Residency cap.** No path may hold more than r% of compute over a window. When it hits the cap, it is forced dormant for one cycle.
  - *Strength:* a hard guarantee.
  - *Weakness:* can interrupt genuinely urgent work.
- **C2-c: Diminishing returns.** The effective priority is P / (1 + β × recent_share), so the more a path has had recently, the less it wins next time.
  - *Strength:* smooth.
  - *Weakness:* β needs tuning.

### C3. Homeostasis (−,±): the bounded resulting state

**Source:** Timothy. Homeostasis is the result of homeodynamics. **Function:** keep key quantities, such as budget use, active count and total weight, near their setpoints.

- **C3-a: Setpoint with a dead band.** Correct only outside a band around the setpoint, for example 70–85% budget use.
  - *Strength:* stable, with no constant fiddling.
  - *Weakness:* responds late to sharp spikes.
- **C3-b: PID controller.** A standard proportional–integral–derivative controller drives decay and promotion rates toward the setpoint.
  - *Strength:* responsive.
  - *Weakness:* can overshoot if poorly tuned.
- **C3-c: Hysteresis switches.** Enter maintenance mode above a high mark, and leave it below a lower mark.
  - *Strength:* no flapping between modes.
  - *Weakness:* coarse, all-or-nothing.

### C4. Heterodynamics (+,+): integrated synthesis

**Source:** Timothy. Polymathically integrated homeostasis, or knowledge synthesis. GPT: X + Y + Z → G. **Function:** combine strong structures from different domains into a new generalization G, without any one absorbing the others.

- **C4-a: Bridge search.** During rest, compare pairs of strong structures from different domains. Where they share a pattern, propose G as a candidate (see D2).
  - *Strength:* direct.
  - *Weakness:* checking every pair across domains is expensive.
- **C4-b: Analogy scaffold.** Use the Indices shape (?):(?)::(?):(?) as the template, fill slots from separate domains, and keep only the fillings that hold up under testing.
  - *Strength:* uses the existing notation.
  - *Weakness:* slot filling needs a way to score candidates.
- **C4-c: Co-activation merge.** When structures from different domains are repeatedly active together and each stays strong, create G over them. The parts are kept, not consumed.
  - *Strength:* cheap, since it piggybacks on activity.
  - *Weakness:* co-activation does not prove a real relation.

---

## D. Trial and error

### D1. Explore/exploit ratio

**Source:** Timothy (the balancing ratio) and Claude (explore/exploit, learning rate). **Function:** keep trying new options while using the ones that work.

- **D1-a: ε-greedy with decay.** Explore with probability ε, otherwise take the best option. ε shrinks as confidence grows.
  - *Strength:* simplest.
  - *Weakness:* explores blindly.
- **D1-b: UCB1.** Choose the option with the highest mean + c√(ln N / n), so options that have been tried less get a bonus.
  - *Strength:* principled, with no randomness.
  - *Weakness:* assumes conditions stay fixed.
- **D1-c: Thompson sampling.** Keep a Beta(wins+1, losses+1) distribution per option, draw one sample from each, and choose the highest draw.
  - *Strength:* adapts well.
  - *Weakness:* random by nature, so runs are harder to replay.

### D2. Candidate lifecycle

**Source:** GPT. candidate → trial → comparison → reinforce, retain, refine, suspend or discard. **Function:** nothing becomes knowledge until it has been tested.

- **D2-a: State machine with thresholds.**
  - Reinforce if score ≥ θ_hi.
  - Refine if θ_mid ≤ score < θ_hi.
  - Suspend if the score is undecided after N trials.
  - Discard if score < θ_lo.
  - *Strength:* auditable.
  - *Weakness:* the thresholds are arbitrary.
- **D2-b: Tournament.** Candidates for the same problem compete head-to-head, and their ratings are updated Elo-style. The bottom fraction is suspended every rest cycle.
  - *Strength:* compares candidates against each other, not against a fixed bar.
  - *Weakness:* needs matched problems to compare on.
- **D2-c: Evidence accumulator.** Each trial adds log-odds for or against the candidate. Decide only once the evidence crosses a boundary in either direction (sequential testing).
  - *Strength:* uses the fewest trials needed to reach a decision.
  - *Weakness:* needs a probability for each trial outcome.

### D3. Weakening with salvage

**Source:** Timothy. A weakening candidate is searched for generalizations before it is gone, because weakening is gradual, not instant. **Function:** recover what is still useful from a failing candidate, within a budget.

- **D3-a: Fixed decay window.** The candidate enters a window of R rest cycles. Each cycle runs one abstraction search. If an abstraction is found, keep it and tombstone the specifics. If not, tombstone everything when the window closes.
  - *Strength:* bounded.
  - *Weakness:* R is fixed regardless of value.
- **D3-b: Cost-gated search.** Search only while (expected value of an abstraction) > (holding cost + search cost). Stop as soon as it is not.
  - *Strength:* budget-honest.
  - *Weakness:* needs value estimates.
- **D3-c: Gist extraction by fading.** Decay the details first and the structure last. Fine-grained fields expire, and whatever pattern survives the window becomes the abstraction. This is like episodic memory fading into gist.
  - *Strength:* no explicit search needed.
  - *Weakness:* what survives may not be useful.

---

## E. Forgetting (Timothy's two kinds, Defined)

### E1. Temporally displaced forgetting (dormant, not deleted)

**Source:** Timothy, with GPT's ACTIVE → DORMANT → ACTIVE. **Function:** release the working budget while keeping enough to reconstruct the item later.

- **E1-a: Status flip.** Set the node to dormant. Its payload stays in storage, but it costs no working budget and is skipped by activation.
  - *Strength:* instant to restore.
  - *Weakness:* still occupies storage.
- **E1-b: Tiered storage.** Items move from active to dormant to archived, with archived items compressed into cold storage. Each step down lowers the cost and raises the time needed to reactivate.
  - *Strength:* scales to large stores.
  - *Weakness:* slow to restore deep items.
- **E1-c: Checkpoint and summary.** Keep a summary plus a reference to the full payload, and rehydrate on demand.
  - *Strength:* the cheapest to keep.
  - *Weakness:* the summary may miss the detail that is needed later.

### E2. Obliviously discarded forgetting (with anti-repetition)

**Source:** Timothy, plus GPT's tombstone: hash, reason and time. **Function:** actually delete, but without relearning the same failure later.

- **E2-a: Tombstone record.** Delete the payload and keep {hash, reason, time, pointer to any salvaged abstraction}. Check new candidates against the tombstones before trying them.
  - *Strength:* exact.
  - *Weakness:* the tombstones themselves grow over time.
- **E2-b: Bloom filter.** Add the hashes of discarded items to a compact Bloom filter. A match means "probably tried before", so check further before retrying.
  - *Strength:* tiny.
  - *Weakness:* gives occasional false positives and cannot store reasons.
- **E2-c: Expiring tombstones.** Tombstones are kept, but they expire after a long horizon, so ideas can be retried once conditions may have changed.
  - *Strength:* allows a second chance.
  - *Weakness:* may repeat some failures.

---

## F. Consolidation and concept tokens

### F1. Tagging and capture (two-phase consolidation)

**Source:** Claude. In the brain, lasting memory needs protein synthesis, so cheap tags are set while awake and only some tagged items are later captured. **Function:** tag cheaply while streaming, and spend the consolidation budget only during rest.

- **F1-a: Tag, then a budgeted commit.** While awake, set tag = 1 on salient links. At rest, rank tagged links by importance and consolidate the top items within the budget. Clear the remaining tags.
  - *Strength:* matches the biology.
  - *Weakness:* "importance" has to be scored.
- **F1-b: Repetition-captured.** A tag is captured only if the link is traversed again before the tag expires.
  - *Strength:* filters out one-offs.
  - *Weakness:* misses important events that happen only once.
- **F1-c: Reward-captured.** A tag is captured only if a good outcome follows within a time window.
  - *Strength:* learns what actually pays off.
  - *Weakness:* rewards can arrive late.

### F2. Concept token formation ({A,B,C} → X)

**Source:** Timothy ({A,B,C} → X, abstractions of generalizations) and Claude (BPE-style merging). **Function:** fuse sequences that keep recurring into a single token.

- **F2-a: BPE-style pair merge.** At rest, find the most frequent adjacent pair (A, B), create a token AB, and repeat up to a merge budget.
  - *Strength:* proven in tokenizers.
  - *Weakness:* merges pairs only, building up larger tokens one step at a time.
- **F2-b: Frequent subgraph.** Find small subgraphs that recur at least s times and replace each occurrence with token X.
  - *Strength:* captures structure beyond simple sequences.
  - *Weakness:* subgraph mining is expensive.
- **F2-c: Validated merge.** Propose X from co-occurrence, but adopt it only if it passes D2 testing: X must predict as well as its parts while costing less.
  - *Strength:* safe.
  - *Weakness:* slower.

### F3. Concept token economics (hot token, cold provenance)

**Source:** GPT. A token costs less than traversing its parts and keeps a reversible pointer to its provenance. **Function:** the token is what gets executed, and the original parts sit in cold storage.

- **F3-a: Pointer token.** X = {cost, ref → [A, B, C, relations, experiences]}. Execution uses X. Audits follow ref.
  - *Strength:* simple.
  - *Weakness:* the referenced parts can go missing if the cold store is pruned.
- **F3-b: Expand on doubt.** Use X by default. If confidence in the result drops, expand X back into its parts and re-check them.
  - *Strength:* self-correcting.
  - *Weakness:* expansion takes extra time.
- **F3-c: Cost-accounted swap.** Keep X only while cost(X) + upkeep < cost(traversing the parts) × use rate. Otherwise dissolve X back into its parts.
  - *Strength:* budget-honest.
  - *Weakness:* the accounting itself has overhead.

### F4. Attention as compute scheduling

**Source:** Claude (attention allocates focus) and GPT (attention maps to compute scheduling). **Function:** split the per-tick compute among active items.

- **F4-a: Softmax shares.** share_i = exp(s_i/τ) / Σ exp(s_j/τ). A lower temperature τ gives sharper focus.
  - *Strength:* smooth.
  - *Weakness:* every item gets at least a sliver.
- **F4-b: Top-k plus round-robin.** The top k items get full compute, and one rotating slot goes to the rest.
  - *Strength:* focused, without starving anything.
  - *Weakness:* the rotating slot is thin.
- **F4-c: Weighted fair queuing.** Each item gets compute in proportion to its weight, with guaranteed minimums.
  - *Strength:* fairness is guaranteed.
  - *Weakness:* more bookkeeping.

### F5. Routing to specialists (reuse and multiplexing)

**Source:** Claude (mixture-of-experts routing) and GPT (neural reuse maps to reusable primitives). **Function:** send each input to a few specialist modules, and reuse primitives rather than duplicating them.

- **F5-a: Top-2 router.** Score every module for the input and run only the top 2.
  - *Strength:* cheap.
  - *Weakness:* the router has to be learned.
- **F5-b: Load-balanced router.** Same as F5-a, plus a penalty on modules that are overused.
  - *Strength:* avoids a single module capturing everything.
  - *Weakness:* sometimes routes to a module that isn't the best fit.
- **F5-c: Primitive library.** Modules are built from shared primitives, and a new module must reuse existing primitives wherever they fit.
  - *Strength:* less duplication.
  - *Weakness:* a design discipline, not automatic.

### F6. Recursive consolidation with presentiated refinement

**Source:** Timothy (Presentiated Refinement of Recursive Consolidation, the balancing of ratios as the abstraction → generalization process), GPT (the loop: experience → comparison → recurrence → abstraction → generalization → refinement → recomparison) and Claude (presentiation means refining *in place*, not by copying). **Function:** keep re-testing whether an abstraction still represents its experiences, and adjust its weight accordingly.

- **F6-a: Loop with in-place update.** Each rest cycle, check each abstraction against a sample of its source experiences. If the fit is good, raise its resolve. If the fit is partial, refine it in place, keeping the same id. If the fit is poor, lower its resolve, and on repeated failure send it to D3.
  - *Strength:* matches the Presentiation definition (not a copy).
  - *Weakness:* in-place edits need version history.
- **F6-b: Shadow and promote.** Refine a shadow copy and swap it in only if it beats the original.
  - *Strength:* safe.
  - *Weakness:* this is a copy, so it departs from presentiation. It is included for comparison.
- **F6-c: Adaptive ratio.** Each abstraction carries its own learning rate, which is the "ratio". The rate rises when the abstraction's fit drifts and falls when the fit is stable, so experience sets how much representation each abstraction deserves.
  - *Strength:* the ratio itself becomes plastic.
  - *Weakness:* a rate per abstraction adds tuning surface.

---

## G. Rest and repetition

### G1. Rest maintenance cycle

**Source:** Claude, from sleep's three jobs (downscaling, interleaved replay, clearance), and Timothy (rest and repetition go hand in hand). **Function:** an offline pass that downscales, replays and cleans up.

- **G1-a: Fixed three-phase pass.**
  1. Downscale all links (A6-b).
  2. Replay tagged and dormant items interleaved with older ones (F1, F6).
  3. Garbage-collect and compact (E2).
  - *Strength:* clear.
  - *Weakness:* the same work every cycle.
- **G1-b: Prioritized replay.** Replay items in order of surprise, meaning the error between expected and actual results, plus importance, until the replay budget runs out.
  - *Strength:* spends effort where learning is.
  - *Weakness:* can neglect calm, stable knowledge.
- **G1-c: Pressure-triggered rest.** Rest runs when budget pressure, a backlog of tags or accumulated surprise crosses a threshold, not on a fixed clock.
  - *Strength:* adaptive.
  - *Weakness:* irregular timing.

### G2. Higher-order recursive return (topic-scale audit)

**Source:** Timothy, Defined. A syntax auditor makes a few passes within one sentence: generalization → root → morphology of the root → root placements → specialized → complete grammar-checked sentence. Rest-cycle return runs the same passes at a higher magnitude, across streams of topics laid dormant. **Function:** multi-pass refinement of dormant topics, spread across rest cycles.

- **G2-a: One level per cycle.** Each dormant topic advances one audit level per rest cycle: general → root → morphology → placement → specialized → complete.
  - *Strength:* steady.
  - *Weakness:* slow for urgent topics.
- **G2-b: Interleaved levels.** In each rest cycle, run different levels on different topics, mixed together, so no single topic monopolizes rest. This is the topic-scale form of interleaved replay.
  - *Strength:* protects against overwriting old learning.
  - *Weakness:* progress is harder to track.
- **G2-c: Return to the failing level.** If a later pass fails, drop back to the deepest level that failed. Topics that stay coherent skip ahead.
  - *Strength:* effort goes where it's needed.
  - *Weakness:* needs a pass/fail check at every level.

### G3. Spaced repetition

**Source:** Claude. Repetition spaced out by rest beats the same amount crammed together. **Function:** schedule returns at growing intervals.

- **G3-a: Leitner boxes.** Items sit in boxes 1–5, and box n is reviewed every 2ⁿ cycles. Success moves an item up a box, and failure sends it back to box 1.
  - *Strength:* dead simple.
  - *Weakness:* coarse.
- **G3-b: SM-2 style.** Each item's interval is multiplied by an ease factor that adjusts with recall quality.
  - *Strength:* proven in flashcard systems.
  - *Weakness:* designed for recall, not reasoning.
- **G3-c: Forgetting-curve scheduler.** Model each item's retention as exp(−t/S) and schedule the return just before retention falls below r*. Each successful return increases S.
  - *Strength:* principled.
  - *Weakness:* S has to be estimated per item.

---

## Dependencies at a glance

```
A1 envelope ─┬─ A2 activation cap ── F4 attention scheduling
             ├─ A3 working set ───── E1 dormant
             └─ C3 homeostasis ───── A6 normalization

B1 counters ── B2 hot paths ── F2 concept tokens ── F3 hot/cold economics

D1 explore/exploit ── D2 lifecycle ── D3 salvage ── E2 tombstones

F1 tagging ── G1 rest cycle ─┬─ G2 topic-scale audit
                             ├─ G3 spaced repetition
                             └─ F6 recursive consolidation ── C4 synthesis

C1 homeodynamic return + C2 anti-capture  →  wrap every scheduler above
```

## Suggested first prototype set

This is one coherent pick to start from, and every choice is open to change:

- A1-c, A2-a, A3-a, A6-b
- B1-b, B2-a
- C1-a, C2-a
- D1-c, D2-a, D3-a
- E1-a, E2-a
- F1-a, F2-c, F3-a, F6-a
- G1-a, G2-a