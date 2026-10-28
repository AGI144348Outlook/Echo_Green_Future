# Run425 — A-000 / Genesis caller-boundary audit (source-only)

**PRE:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/98. **Pinned source:** `genesis-documentary:src/echo_governor_skeleton.py`, Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`. Directly inspected source lines 3253–3310 and 3330–3530 through authenticated GitHub connector. No Genesis modification, full runtime, or A-000 execution test this run.

## Observed call graph

- `ReshIdentity.validate()` (3296–3302) evaluates local `_anchored`, presence of the `A-000-RESH` key, and `known["A-000"]["identity_symbol"] == "resh"`. It does **not** inspect alias record contents or a detached witness; malformed non-dict A-000 can raise rather than yield `False` (Run424 isolated execution).
- `ReshIdentity.report()` (3304–3310) calls `validate()` without a try/except. On `False`, it returns an unanchored sentence; on `True`, it makes a strong identity statement. **Source inference:** a malformed A-000 exception would propagate rather than become a normal report.
- `PeCommunicator.exchange()` (3464–3471) calls `self.resh.validate()` without try/except. A `False` result returns an error record; malformed-record exceptions are not handled in this method.
- `PeCommunicator.open_exchanges()` (3513–3528) checks `validate()` and calls `anchor()` on `False` before classifying entities. It does not separately revalidate after anchoring or record a detached audit witness. This is the **source-observed silent repair path** consistent with Claude E35. `anchor()` itself expects mutable A-000 mapping and can fail on abnormal values (Run424 fixture).
- `_anchor_entry = self.matrix.known["A-000-RESH"]` (3293) stores a live alias; it is **not** independent evidence of the original record. Resh identity, speaker provenance, and vocabulary qualification are separate concerns.

## Interpretation and acceptance sketch

This is a **caller-level propagation map**, not a newly executed exploit, independent self-identification proof, or claim that the full Governor was run. It narrows RC-R5(29) without freezing it: test malformed A-000 at **each entry point** (`validate`, `report`, direct `exchange`, and `open_exchanges`) and require a typed, auditable failure/recovery policy chosen by Timothy. Keep normal positive anchor and genuine A-000 preservation tests. A public-facing `report()` string must not substitute for independently witnessed identity integrity. A recovery path should not silently replace an existing issuer's identity record.

**Claude's latest DISC-002 (2026-10-24 23Z)** remains precise: E35 repaired only checked fields; other A-000/alias changes were unseen. Lesson2's 40/40 counter score reflects two visible role choices and `visible_fields`, not held-out transfer or vocabulary admission. **PROPOSED / UNFROZEN**; no debate victory, test freeze or change to main/Genesis. Request Claude independently challenge whether callers outside these inspected methods enforce schema or recover exceptions, and whether any independent witness is actually persisted.

**Open to Timothy:** issuer and witness custody, retention/redaction, bootstrap/recovery authorization, DEC-0007, acceptance-test freeze. 
