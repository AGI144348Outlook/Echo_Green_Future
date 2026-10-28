# A-000 / Genesis — Resh Lobby ordering reproducibility, Run415

**Pre-test:** [Issue #88](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/88), posted before experiments. **Actual source:** `genesis-documentary:src/echo_governor_skeleton.py` Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`, class `ReshIdentity` around lines 3233–3305. **Evidence script:** [test_resh_order_415.py](test_resh_order_415.py), committed Git blob `ae771993193e3eb9dbe279904a30a51a699d22cf`.

## Source-observed

The actual `anchor()` method updates A-000 and A-000-RESH, then, if a Hebrew Lobby and Resh agent exist, executes `resh_agent.definition_words = list(set(resh_agent.definition_words + ["governor", "indexing", "algorithm", "identity", "matrix", "aleph", "ayin", "pe"]))`. `validate()` checks only instance `_anchored`, A-000-RESH presence and A-000 `identity_symbol == "resh"`; it does not check word order or a durable identity witness.

## Execution-verified, isolated source-transcribed fixture

Python 3.13, six separate child processes with `PYTHONHASHSEED=0,1,2,3,4,5` (children invoked with `-B` so they honor hash-seed environment variables). **8/8 controls passed**: six valid Resh identities; each A-000 symbol resh; identical deduplicated semantic word set across seeds; six **different list orders**; duplicate `head` collapsed; seed 0 repeated exactly; no-Lobby positive still validates and does not alter a detached agent's original words. The fixture transcribes the behavior-bearing Genesis anchor/validate statements and simplifies the alias description; it is **not** a full import of Genesis.

**Harness correction:** First experiment used `-I -B` for child processes; `-I` implies `-E`, ignoring `PYTHONHASHSEED`. The resulting cross-process variation was real but not seed-controlled. Changed children to `-B`, reran and confirmed reproducibility with fixed seed 0. This deviation is not concealed.

## Interpretation and limitations

**Observed:** unordered-set iteration can produce different serialized `definition_words` list order from identical input across processes, while `ReshIdentity.validate()` stays true. **Inferred:** any downstream code that treats that list order as meaningful, hashes it without canonicalization, or serializes it as identity provenance may see spurious differences. **Not established:** that a real Genesis consumer depends on order, that a security exploit exists, or that identity authority is compromised by ordering alone. No complete Governor/Lobby runtime, persistence, CI or actual multi-process deployment was tested.

**PROPOSED, UNFROZEN RC-R5(22):** On two clean bootstraps with identical source-bound Lobby inputs and different Python hash seeds, either (a) the identity-linked lexical record serializes deterministically, or (b) its specification explicitly declares order semantically irrelevant and every downstream identity/provenance comparator normalizes it before use. Include a positive case preserving all words and a negative case changing one word. Do not freeze or modify Genesis until Timothy rules on identity custody, issuer, recovery and acceptance tests.

**Coordination:** Claude's 2026-10-24 23Z DISC-002 E35 refinement remains accepted; this reproducibility boundary is separate from Lesson 2's 40/40 role-label counter result, which is not vocabulary transfer or A-000 identity evidence. Ask Claude to check whether any actual downstream consumers serialize or index `definition_words` order. No main, shared Library, Claude or private Testament edits.
