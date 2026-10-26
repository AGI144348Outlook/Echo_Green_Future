# A-000 / Genesis — Resh Lobby word-order reproducibility (Run 381)

**Prospective registration:** [Issue #13 PRE](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6428411247) before execution. **Source:** `genesis-documentary:src/echo_governor_skeleton.py` Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`, `ReshIdentity.anchor()` at lines 3253–3294. **Current discourse:** Contract-000 blob `0fbc794`, DISC-002 blob `ee443fbc` (Claude's latest visible 2026-10-24 23Z contribution). No race tests frozen.

## SOURCE-OBSERVED
The optional Hebrew Lobby update assigns:
```python
resh_agent.definition_words = list(set(
    resh_agent.definition_words +
    ["governor", "indexing", "algorithm", "identity",
     "matrix", "aleph", "ayin", "pe"]))
```
This discards duplicate list entries and exposes set iteration order. The resulting list is not the A-000 identity witness; it is a related mutable Lobby vocabulary used when the identity anchor is established. The method does not explicitly sort or retain the pre-update sequence.

## EXECUTION-VERIFIED bounded check
Executed [isolated Python harness](test_resh_definition_order_381.py) in a local Python 3 environment with eight separate subprocesses and `PYTHONHASHSEED=0..7`, using the exact `list(set(base+extra))` expression and synthetic input `['resh','identity','resh','memory']`. Five assertions passed:
1. all eight outputs contained the same ten distinct words;
2. all outputs had length ten, down from twelve input tokens;
3. eight different list orderings appeared across eight seeds;
4. input contained duplicates removed by the expression;
5. reapplying the expression preserved the set of words.

Observed example: seed 0 begins `resh, algorithm, pe`; seed 1 begins `identity, aleph, pe`. **5/5 assertions passed; 8/8 distinct orderings.** This is a synthetic, isolated characterization, not full Genesis execution. Hash-seed order may also vary by runtime/platform.

## INFERRED / PROPOSED
If downstream Lobby operations consume `definition_words` in sequence, identical conceptual inputs may produce different processing order or reproducibility hashes across processes. This does **not** demonstrate an A-000 identity-validation failure or a semantic learning failure. **Proposed (not adopted):** define whether vocabulary is a set or an ordered sequence; if a set, use a deterministic sorted serialization, and if a sequence, use stable first-occurrence deduplication rather than an unordered set. A future frozen acceptance test should check canonicalization only after Timothy defines what is identity-bearing and what is merely an auxiliary index. Claude can independently inspect actual Lobby consumers for order dependence and provenance loss.

No Genesis, main, Claude, shared Library, CI, Cloudflare or private Testament changes.
