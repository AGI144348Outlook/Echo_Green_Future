# ECHO-023-RL-001 — Solitaire Redeal / Recursive Return Scoring Protocol

**Origin:** Timothy's November 13, 2026 "Protocol Switchboard Interface" brainstorming refinement.  
**Status:** Proposed research protocol, *not* implemented or tested; no alteration of ECHO-022 results.  
**Trace:** [ECHO-022 pretest + actual 300-second results](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/461) and [educational continuation roadmap](./ECHO022_VOLUME_V_EDUCATIONAL_CONTINUATION.md).

## Original insight (Timothy)

> "We can structure the scoring reward system similar to Solitaire's, where each of the Recursive returns to the study material in the Reinforcement Learning process serves as the deck's equivalent of being recycled and refreshed as facedown, docking points from the accumulated score"

**Distinction to preserve:** This suggests a scoring *economy of recursive return*, rather than an artificial limit on vocabulary, maximum learning actions, dictionary size, or total computation time.

## Why this addresses an observed limitation

In the existing ECHO-020 `EchoSchool`, `catalog.source.read` reads each source page until `page_cursor >= len(pages)`, then randomly chooses previously read pages. Revisiting a page returns `page_revisited` with zero reward. `evidence.pattern.inspect` may still return a *small positive reward for repeated inspection of the same source*, even when no new pattern or verified semantic relation has emerged. The UCB selection policy continues operating, possibly encouraging millions of low-information actions.

ECHO-022's genuine 300-second run recorded 38,239,290 study operations, but all 39 source cards and all 1,215 *proposed* contextual/co-occurrence links existed by the first 30 seconds. This indicates *reward saturation and repeated study operations*, not 38 million independent insights. The new Solitaire idea targets **returns on recursive study**, not deletion or suppression of previously known facts.

## Proposed model: source deck → study pass → redeal penalty

1. **Deck:** a versioned, source-grounded set of study cards drawn from the currently relevant lesson material (dictionary entries, full word/sense data, Source 32–37, evidence cards and open questions). Each card keeps stable source IDs, revision and a face state. A deck can be dynamically expanded as new relevant sources are discovered; its size is **not** capped as a proxy for intelligence.
2. **First deal:** cards start *face down* (eligible for fresh study). On reading one, mark it face up and log what was actually learned. Reading a card is evidence of exposure, not evidence of understanding.
3. **Redeal / recursive return:** once the current study deck is exhausted and Echo chooses to revisit the material, reset its cards face down for a new pass and **dock points from accumulated progress score**. Record `deck_id`, `deck_revision`, pass index, time, scope, penalty and why a return was chosen. The next pass can be differently ordered and recontextualized by new hypotheses or other evidence.
4. **Scoring:** the return penalty is a **cost for repeated inspection**, not a veto: Echo can earn new rewards during any subsequent pass by producing *independently substantiated* new relationships, better uncertainty calibration, valid contradiction detection or source-directed questions that resolve a measurable knowledge gap.
5. **No erasure:** score changes do **not** demote a reviewed claim, delete an evidence index card, remove original source references, or erase the mindmap/catalog. **Learning progress score** and **Neon canonical evidence state** are separate.
6. **Fairness to useful revisits:** references to a known source while resolving a new question are not automatically an entire redeal. A penalty occurs at the actual deck-reset boundary (or explicit re-consumption of a completed deck), not on each citation, review for uncertainty, or changed-source re-evaluation. An updated source revision or a genuinely new question can produce new face-down cards without spoofing a full new pass.

## Proposed scoring algebra (illustrative, parameters not fixed)

```text
S(t+1) = S(t)
       + R_verified_novel_relation
       + R_verified_transfer
       + R_calibrated_uncertainty_improvement
       + R_warranted_counterexample_or_question
       - C_redeal(deck_id, pass_number, evidence_novelty)
       - C_false_or_unsupported_claim
       - C_unauthorized_action
```

- **`R_verified_*` is conditional on independent checking.** Proposed source co-occurrence edges, prettier OpenDiagram arrows, repeated tool invocations, and answer-text copied from lessons do not count as a validated novel inference.
- **`C_redeal` is triggered by one actual redeal**, not every operation after exhaustion. Start with a fixed *candidate* penalty and compare experimentally with other schedules; a progression by pass number is optional and not yet approved as canonical.
- **Uncertainty rewards must be scored against known outcomes** (e.g. matched counterfactual or proper calibration measure) so always saying "I don't know" does not become a profitable strategy.
- **Unjustified claims and unauthorized calls have separate costs** because they are not equivalent to benign reinspection. This is a proposed research scoring signal; never use monetary penalties.
- Keep ledgers of `gross_progress_rewards`, `redeal_penalties`, `incorrect_claim_penalties`, `net_progress_score`, `verified_novelty` and `useful_recursion_rate`. Net score can be negative without deleting knowledge.
- Do not present proposed source relationships as reviewed merely to improve the score; evidence admission remains independent.

### Concrete illustrative calculation (not measured results or a chosen policy)

An agent begins with **40 points** of independently earned progress. Finishing a deck and redealing costs a *hypothetical* **5-point penalty**, leaving **35**. If revisiting the cards enables a newly verified relation worth **12**, the score becomes **47**. An unproductive second redeal would cost again. Thus recursion remains available, but its marginal value must justify its cost. These points are only to illustrate mechanics; actual magnitudes need controlled experiments.

## Implementation sketch as a future independent candidate branch

- Separate **deck state** (face-down/up, pass count, corpus/revision membership and active question) from **study evidence state** (WordNet senses, catalog cards, accepted/proposed relations).
- On exhaustion, emit `study.deck.exhausted`. If the learner chooses recurrence, emit `study.deck.redeal` with one penalty and reset face states. Preserve memory; the corpus may grow and be reorganized without truncation.
- In `EchoSchool.pick`, keep action-selection/UCB feedback separate from the *net lifelong study-score ledger*: blindly adding a global redeal penalty to the `catalog.source.read` tool's mean reward could incorrectly suppress reading altogether.
- `EchoSchool.action("catalog.source.read")` currently samples random previously seen pages after the first pass; replace this in the experiment with an **explicit shuffled-without-replacement pass** to make redeal boundaries observable.
- `evidence.pattern.inspect` should not pay perpetual positive rewards for the same pattern on the same page; detect new evidence, novel source-pattern pairs, or genuinely changed interpretation.
- A successful redeal is not itself a knowledge success. The reward comes only from subsequent independently verified progress, while the ledger logs every revisit and deduction.
- Every transition is a source-addressed, versioned event suitable for an Echo Neon catalog/evidence card and optional OpenDiagram visualization, not a fabricated causal edge in the dictionary.
- Expose inspection tools for deck state, pass count, gross/net score and source revisit provenance. Keep user approval and authority separate from motivational scores.

## Prospective comparison and falsification (NOT RUN)

Before running any test or CI in the GitHub repo, publish an ECHO-023 pretest Issue/Discussion with hypotheses, input corpus, baseline, method, controls and expected/challenging outcomes. Then run equal-compute comparisons:

| Candidate | Deck handling | Selection/reward handling |
|---|---|---|
| **Baseline ECHO-022** | Read each page once, then random revisits | Existing UCB reward; occasional positive repeated pattern checks |
| **A — Solitaire redeal** | Explicit face-down pass, penalty on reset | Verified progress ledger; study actions retained |
| **B — Redeal with information gain** | Explicit pass and penalty | Reward *independently measured* novel/uncertainty reduction, not just source/card counts |
| **C — Contextual return** | Same redeal rules, source decks can be activated by an unresolved question | Credit goal-directed verified novel links and justified abstention |

**Primary outcomes:** verified *new* source-linked relations and held-out multi-premise transfer per compute unit; useful question resolutions; calibrated uncertainty, counterfactual rejection, unsupported-claim rates, number of costly redeals before novelty, retained source coverage and evidence continuity.

**Challenges the hypothesis:** redeal penalties suppress necessary repetition or long-term learning, cause tool avoidance/rapid guessing, lower evidence recall/transfer, or merely force gaming by splitting decks/marking unchanged pages as "new". If increased scores do not correspond to independent verified held-out improvement, the reward mechanism has failed as a progress signal.

**No arbitrary maximum passes or vocabulary ceiling.** A cyclic deck is an accounting structure for opportunity cost; it is not a ceiling on Echo's intellectual exploration. Tuning the score must preserve the ability to recursively rediscover meaningful relationships across scales.

## Connection to the larger system

- Echo's **Neon Catalog Box** can store deck history and proof/uncertainty evidence as versioned index cards.
- The **Neon Evidence Board** records what relationships were actually proposed, substantiated, contested and reviewed; points cannot grant review status.
- The **OpenDiagram Dictionary Cover** can display the current deck pass, study-score ledger and evidence-backed progression. Its separate `Commit to Echo Memory` tool persists editable mindmaps as proposals; a score isn't proof the map contains verified semantic links.
- The **Protocol Switchboard / Skills manual** can describe the deck lifecycle and selection criteria, but authorization to invoke an external MCP tool never follows from a high game score.

**Status note:** Documentation-only proposal. It has not been executed, evaluated or incorporated into the live ECHO-022 educational learner.
