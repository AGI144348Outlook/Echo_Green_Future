# Run397 — A-000 / Genesis anchor failure atomicity

**Prospective and actual test thread:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/70. **SOURCE-OBSERVED:** `genesis-documentary:src/echo_governor_skeleton.py` Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`, `ReshIdentity.anchor()` and `validate()`, lines 3253–3305. **EXECUTION SCOPE:** isolated source-transcribed JavaScript behavior probe, *not* the complete Python Genesis runtime, not a frozen race.

## New boundary: partial anchor on Lobby failure

The Python source writes `A-000` identity fields, then overwrites `A-000-RESH`, and only **after both matrix mutations** tries to extend the optional Resh Lobby agent's `definition_words` using `definition_words + [eight words]`. It sets `_anchored=True` only **after** that optional hook. If `definition_words` is `None` or another incompatible type, the addition raises a `TypeError` after matrix writes, with no source-visible rollback or failure receipt. This is a code-order inference; no real Lobby error was injected into full Genesis.

[Isolated source-transcribed probe](A-000-ANCHOR-ATOMICITY-PROBE-397.js) uses a stub matrix/Lobby with the same write ordering. **7/7 expected cases passed:** baseline, partial matrix write on failed Lobby hook, retry after fixing Lobby, missing resh agent, preserved foreign status, stale alias reference on re-anchor, and missing-A-000 bootstrap. The stub's `concat` error is analogous to Python's list-addition error, not the same executable implementation.

**OBSERVATION:** after a simulated failure, matrix contains the new A-000 identity fields and alias while the instance reports `_anchored=false`; subsequent retry validates without a failure receipt. **INTERPRETATION:** current anchoring lacks a transaction boundary. This differs from the previously documented typed-alias and mutable-pointer weaknesses: even an authorized caller can leave a partially changed identity record if a downstream optional hook fails.

## Proposed unfrozen RC-R5 case 14

Begin with an existing A-000 and an optional Lobby agent whose `definition_words` cannot be concatenated with a list. Invoke anchor and assert either (a) no identity mutation occurred, or (b) an explicit versioned failed/partial transaction is retained with a separately held recovery witness; `validate()` must not silently promote a partial state. Retry after repairing the Lobby; verify that an attributable recovery event exists and no unrelated metadata or learning record was lost. Include a no-Lobby control and a normal-Lobby control. A guard must not rewrite Timothy's R5 authority: deliberate GPT/Claude updates remain possible through an explicit logged reviewed path.

**Limits:** a synthetic stand-in cannot prove Python exception behavior across the full Genesis graph, threading, persistence, or a real Governor deployment. No issuer, independent custodian, rollback policy or frozen acceptance suite has been approved. The observed source order supports the failure hypothesis; the actual full-system failure remains **UNVERIFIED**. No production code modified.
