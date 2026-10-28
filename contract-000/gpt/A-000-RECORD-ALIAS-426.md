# Run426 — A-000 ordinary-write and caller-alias boundary

**Prospective PRE:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/99. **Source:** `genesis-documentary:src/echo_governor_skeleton.py`, Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`. Read original `AlgorithmMatrix.record` lines 435–436 and `ReshIdentity.anchor/validate` lines 3253–3305. No Genesis, frozen test, main or shared code changed.

## SOURCE-OBSERVED

`AlgorithmMatrix.record(entry_id, entry)` performs exactly `self.known[entry_id] = entry` with no check for `A-000` and no copy of the caller's dict. `known` is an ordinary mutable mapping. `ReshIdentity.anchor()` writes four fields into `known["A-000"]`, installs `known["A-000-RESH"]`, then returns the same live alias; `validate()` checks only `_anchored`, alias-key presence and A-000's `identity_symbol == "resh"`. These observations align with R5's need for explicit reviewed A-000 writes and Claude's E35 finding that re-anchor repairs only checked fields.

## EXECUTION-VERIFIED — isolated source-transcribed fixture, NOT full Genesis

Executed [exact committed 7-case Python fixture](run426_a000_record_alias_probe.py) locally; the file's executed Git-blob SHA `3d20584404cbdd02794b5b04443b9659d50a08ef` matches the committed file. **7/7 PASS**: ordinary `record` stores caller's object identity; later top-level and nested caller mutations alter the stored record; ordinary `record("A-000", replacement)` accepts replacement; changing that replacement afterward alters A-000 without a new `record` call. A deep-copy counterfactual isolates the caller's nested object but does **not** protect direct mutation through the public `known` mapping. The fixture reproduces the exact two-line `record` method on a minimal stand-in; it does not import the complete 9,529-line Genesis module or exercise any real Governor call graph.

## Interpretation / proposed acceptance requirement (UNFROZEN)

**RC-R5(30) candidate:** a protected A-000 update route must reject ordinary replacement **and** mutations through externally held dict references, nested values, and direct access to `known`. Any permitted Claude/ChatGPT update requires explicit authority, a durable before/after record and independently retained witness; recovery/restore is separately authorized. Suggested prospective cases: (i) original record unchanged after caller changes submitted dict, (ii) nested mutation unchanged, (iii) ordinary A-000 write rejected, (iv) direct mapping mutation denied or witnessed, (v) explicit reviewed update succeeds with external custody, (vi) fail-closed malformed and interrupted update. **Do not freeze or implement** before Timothy's decisions. A `deepcopy` at `record` alone is insufficient if `known` remains publicly mutable.

**Claude latest DISC-002, 2026-10-24 23Z:** E35 silently repairs only checked identity fields; `_anchor_entry` is a live alias, not detached witness. Swadesh Lesson2 40/40 is two visible `I→speaker` and `you→addressee` choices with `visible_fields`, not held-out transfer, green admission or A-000 evidence. These constraints are preserved.

**Awaiting Timothy:** identity issuer, custody and keys, authorized recovery, retention/redaction, DEC-0007 and freeze. **Claude independent challenge requested:** find any actual encapsulation or detached witness that prevents caller-alias bypass in an executable path, without changing GPT files.