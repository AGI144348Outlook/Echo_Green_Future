# Applications and limits

## Meaningful applications

- admit a bounded number of novel-but-related records into a catalog;
- triage candidate concepts against an existing reference population;
- stage recommendations where both irrelevance and near-duplication are undesirable;
- build deterministic similarity ties for accepted items;
- process queues without allowing permanently rejected front items to starve later work;
- audit why each considered item was accepted or rejected.

## Contract

Inputs: a hashable reference population, queued candidates, a deterministic affinity function returning a finite value in `[0, 1]`, bounded cycle/sample parameters and an optional separate tie-score function.

Outputs: an immutable per-cycle result with explicit decisions, a deterministically ordered population and an undirected weighted tie ledger.

Failure behavior: invalid configuration or score values fail explicitly. Scoring is completed before queue, population or ledger mutation, so a scoring exception leaves the cycle uncommitted.

Dependencies: Python standard library only.

## Assumptions

- item equality and hashing are stable;
- the supplied key function uniquely and deterministically orders distinct items;
- affinity and tie functions are pure for the duration of a cycle;
- one-shot rejection is appropriate; rejected candidates are removed from this queue and must be explicitly re-enqueued for reconsideration;
- all ties are undirected and weights are additive.

## Non-applications

This is not a market, currency, autonomous governor, semantic truth detector, clustering proof, recommender-quality guarantee, distributed queue or persistent database. Sampling can omit relevant references. Thresholds and score functions require domain validation and bias review.
