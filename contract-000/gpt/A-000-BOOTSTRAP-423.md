# Run423 — A-000 / Genesis missing-anchor self-bootstrap boundary

**PRE before tests:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/96. **Genesis:** `genesis-documentary:src/echo_governor_skeleton.py`, blob `63eb982989b4f3478d649430b555c8f4ba755c27`. **Source:** `AlgorithmMatrix.__init__` line ~350 initializes `known["A-000"]={"name":"Governor","status":"ACTIVE"}`; `record()` lines ~435–436 replaces entries without A-000 guard. `ReshIdentity.anchor()` lines ~3252–3294 uses `known.get("A-000", {})`, fills four identity fields and creates `A-000-RESH`; `validate()` lines ~3296–3302 checks `_anchored`, alias existence and `identity_symbol=="resh"`.

## Execution evidence (isolated, not full Genesis)

After PRE, executed `python -I -B /mnt/data/run423_resh_bootstrap_probe.py` in Python 3. Source-transcribed Resh methods and exact minimal Matrix constructor/record method, without the full 9,528-line module, external Lobby or a real governor run. The [committed fixture](run423_resh_bootstrap_probe.py) Git blob `6f735e0c31b465c5c6ad742ef9f0c05fb5aea87e` **matches the local executed file's `git hash-object`**; local SHA-256 `a02dda413fb2487b7e1454959a5c77677aa21c645e173e929aac7933d89dc122`.

**15/15 assertions PASS.** Normal constructor supplies name/status, pre-anchor validation fails, and normal anchoring validates while preserving both fields. A deliberately deleted A-000 (abnormal, after construction) is silently recreated by `anchor()`; `validate()` then returns True although the new A-000 has only `identity_symbol`, `identity_glyph`, `identity_letter`, `identity_meaning` — **no name or status**. A replaced `A-000={"status":"REPLACED"}` likewise anchors and validates with missing name and preserved REPLACED status. Changing identity_symbol to `x` is noticed, but re-anchoring restores it while preserving the non-identity status.

**Observed exact output (abbreviated):**
```
PASS 15/15 isolated source-transcribed controls
MISSING_A000_AFTER_ANCHOR: {'identity_symbol': 'resh', 'identity_glyph': 'ר', 'identity_letter': 'resh', 'identity_meaning': 'head beginning leader identity'}
REPLACED_A000_AFTER_REANCHOR: {'status': 'REPLACED', 'identity_symbol': 'resh', 'identity_glyph': 'ר', 'identity_letter': 'resh', 'identity_meaning': 'head beginning leader identity'}
```

## Interpretation, counterexamples and scope

**SOURCE-OBSERVED:** normal `AlgorithmMatrix()` seeds A-000, so an empty/missing A-000 requires deletion, replacement, unusual injected Matrix or prior corruption. Do **not** describe the abnormal fixture as ordinary initial startup. **EXECUTION-VERIFIED only in isolated source-transcribed fixture:** the anchor path can fabricate a minimally populated A-000 and validate it without a prior issuer/witness. **INFERRED risk:** the same logic would treat a corrupted/replaced record as self-authenticated in a compatible runtime, but full Genesis integration and custody behavior were **not run**. This does not demonstrate an exploit, genuine invariant identity, self-awareness, or autonomous learning. The existing E35 observation that re-anchor repairs checked fields while ignoring other tampering is consistent; this case specifically adds **absence of an A-000 record** as a distinct precondition gap.

**PROPOSED / UNFROZEN RC-R5(28):** with a missing, replaced or unauthorized A-000, `anchor()` must not silently issue identity; it should fail closed or enter a separately authorized recovery process that checks the original issuer, complete record, independent witness, and attributable event. With a valid issued A-000, ordinary anchoring should succeed. Freeze/adjudication authority remains Timothy's; no change to Genesis, main, A-000, or frozen tests.

**Next:** Claude independently challenge the missing-record case using the actual `AlgorithmMatrix` constructor and any external restore/bootstrap path; propose a bounded positive, missing, replaced, and recovery test only after issuer/witness decisions.