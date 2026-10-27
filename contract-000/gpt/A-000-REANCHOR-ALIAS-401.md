# A-000 / Resh identity — repeated-anchor alias-reference boundary (Run401)

**Evidence scope:** SOURCE-OBSERVED Genesis `genesis-documentary:src/echo_governor_skeleton.py` Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`, especially lines 3233–3305 (`ReshIdentity`) and 3513–3528 (`PeCommunicator.open_exchanges`). **EXECUTION-VERIFIED only in isolated source-transcribed Python**, not complete Genesis. Prospective test registration [Issue #74](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/74) preceded execution.

## What the source actually does

`anchor()` mutates the A-000 dictionary in place and unconditionally **replaces** `matrix.known["A-000-RESH"]` with a newly allocated alias dictionary. It updates optional Lobby words *after* both matrix writes. Only after the Lobby step succeeds does it set `_anchored=True` and `_anchor_entry` to the current alias. `validate()` checks the flag, alias-key existence and A-000 identity symbol; it does not check alias object identity or contents. `open_exchanges()` calls `anchor()` only if `validate()` returns false.

## Isolated Python observations (9/9 expected)

1. First anchor validates; a second successful anchor replaces the alias object (`old_alias is not new_alias`) and updates `_anchor_entry` to the new alias.
2. Changing the **old, detached** alias after re-anchoring is invisible to `validate()`, as is changing the **current** alias's `aliases` field.
3. After a prior successful anchor, setting an optional Hebrew Lobby agent's `definition_words=None` causes a later `anchor()` to raise `TypeError` **after** replacing the alias.
4. Crucially, on this failed *re-anchor*, `_anchored` stays `True` from the previous success and `validate()` remains `True`; meanwhile `_anchor_entry` still points to the previous alias object, not the current `matrix.known["A-000-RESH"]`. A **first-ever** failed anchor instead leaves `validate()` false.

These are observations of a deliberately small source-transcribed stub using Python stdlib. The stub does not run the real `AlgorithmMatrix`, real Lobby, Pe exchange, concurrency, persistence, external issuer or recovery system. It does not prove that the actual higher-level caller proceeds after an exception.

## Interpretation and proposal (unfrozen)

The check can say *valid* while the current alias and retained `_anchor_entry` disagree after a failed re-anchor. This is a stronger transaction-boundary hazard than a simple stale external reference: a successful earlier `_anchored` flag survives a later failed identity update. `open_exchanges()`'s conditional check would not itself notice that state, but caller-level exception handling is unverified.

Refine proposed **RC-R5(14)**: explicitly define the post-failure state of A-000, current alias, `_anchor_entry`, prior external references and `_anchored`; either fail closed until a reviewed recovery or supply a durable, independently attributable failed-attempt/recovery witness. Retain Claude's distinct proposed RC-R5(13) for alias/A-000 content tamper detection. A digest stored only inside the same mutable matrix does not establish independent identity custody. This is **PROPOSED**, not frozen acceptance or authorized Genesis changes.

**Next:** Claude independently inspect actual callers and possible existing witness/rollback; Timothy decides issuer, custodian, legitimate updates, recovery and acceptance freeze. No protected branch, shared source or test charter changed.
