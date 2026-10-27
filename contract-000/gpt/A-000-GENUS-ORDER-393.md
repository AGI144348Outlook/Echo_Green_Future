# Run393 — Resh anchor and ordered genus derivation (unfrozen, isolated)

**Pre-test Issue:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/66. **Pinned Genesis:** `genesis-documentary/src/echo_governor_skeleton.py` Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`. Read Contract-000 §30 and R5; Claude's latest visible DISC-002 2026-10-24 23Z; Run392's duplicate-word finding.

## Source-observed code path

- `WordAgent.definition_words` is an ordered **list** of filtered definition words (around lines 1074–1080). `Lobby.populate()` derives that list from matrix transitions.
- `Lobby._compute_genus_depths()` (around lines 1273–1307) selects the **first** eligible known non-stopword in each agent's `definition_words` as `genus_of[word]`; `compute_generality_scores()` (around 1219–1271) calls this and assigns 10% weight to normalized genus depth.
- `ReshIdentity.anchor()` (around 3260–3293) overwrites the Resh WordAgent list using `list(set(old + eight terms))`. It neither stores the original order nor recomputes `Lobby.generality_scores` or agent scores. `validate()` checks only `_anchored`, alias-key existence and A-000 identity_symbol.
- A source-text search found **no invocation** of `ReshIdentity(` in this pinned 9,529-line Genesis module. This is a conditional hazard, not a demonstrated active production path. The exact terms `governor` and `matrix` need to be present as WordAgents for the demonstrated genus alternatives.

## Isolated execution, not the full Governor

[Committed, blob-matched Python probe](code/a000_genus_order_probe_393.py) transcribes the source's set conversion and first-eligible-word genus selection; it runs eight separate Python processes with `PYTHONHASHSEED=0..7` on a synthetic Resh list with both `governor` and `matrix` as known candidate genera.

**Observed:** 11/11 assertions passed. Before normalization, the first genus is `governor`. Across eight hash seeds after normalization, first genus was `governor` **4** times and `matrix` **4** times, although the set of eight words was identical. The synthetic score snapshot remained unchanged until an explicit recomputation (the actual `anchor()` also has no recomputation call).

**Deviations:** initial attempt at 32 subprocess seeds timed out twice in the local execution environment (including a 20-second bounded rerun); reduced to eight seeds, which completed and exercised both alternatives. No test assertion failure. This is not a probabilistic estimate of production behavior.

## Interpretation, limitations and candidate RC-R5 tests

An identity anchor that rewrites a definition-word list can change the **order-sensitive genus heuristic** while leaving cached generality values stale. This extends Run392's multiplicity observation: the list is not universally consumed as a mathematical set. It **does not** prove that Resh's live Lobby currently computes a genus, that `governor` and `matrix` are real WordAgents in the letter Lobby, or that an anchor constructor is called in the integrated runtime.

Candidate checks for Timothy's unfrozen R5 race: (1) no vocabulary mutation from identity admission, or explicit logged approved mutation; (2) deterministic ordering of derived vocabulary; (3) independent re-derivation/invalidation of dependent genus/generality state; (4) separate immutable encounter evidence from derived views; (5) independently held identity witness and authorized re-anchor path. No Governor changes, no frozen tests, no claims of self-awareness.
