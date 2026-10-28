# Run424 — A-000/Resh malformed-record validation boundary

**Prospective PRE:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/97 (published 2026-10-28T16:56:37Z before tests). **Source:** `genesis-documentary:src/echo_governor_skeleton.py` Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`, `ReshIdentity.anchor()` and `validate()` near lines 3252–3302. The source was read through the authenticated GitHub connector. No Genesis, main, Claude, frozen test or shared Library write.

## Source observation

`validate()` returns the conjunction of local `_anchored`, existence of the `A-000-RESH` key, and `self.matrix.known.get("A-000", {}).get("identity_symbol") == "resh"`. It neither checks the alias value's type/content nor guards `.get()` against a non-dict A-000 value. `anchor()` similarly assumes the fetched A-000 is mutable mapping. Normal `AlgorithmMatrix()` seeds A-000 as a dict; malformed values are injected abnormal states, not routine startup.

## Bounded execution after PRE

Command: `python -I -B /mnt/data/run424/run424_tests.py` (local Python, no network). The fixture transcribed the source method logic into a minimal Resh class and a synthetic Matrix stub, with no Hebrew Lobby. SHA-256 of executed fixture: `bd781d233a1d6a7caf5e0a85e2802611d62a620537d9242cccc09066f0dc2978`. **13/13 A-000 fixture assertions PASS**:

| Synthetic condition | Observed |
| --- | --- |
| Before anchor | `validate() is False` |
| Normal named ACTIVE A-000 after anchor | `True`; name/status preserved |
| Alias key present with `{}`, `None`, or `False` value | `True` for each |
| Alias key deleted | `False` |
| A-000 replaced with `None` or `[]` after anchor | `AttributeError`, not Boolean False |
| A-000 replaced with `{}` | `False` |
| A-000 replaced with `{"identity_symbol":"resh"}` | `True` despite missing other fields |
| Re-anchor valid dict | Succeeds |
| Re-anchor `A-000=None` | `TypeError` |

**Observation vs interpretation:** these are isolated source-transcribed Python results, not an executed full 9,528-line Genesis integration, identity compromise, or proof of self-awareness. The exception is fail-stop at this call, not evidence of accepting a malformed identity; the alias-only and single-field positive cases are under-validation of contents.

**PROPOSED / UNFROZEN RC-R5(29):** identity validation should return an explicit failure result on absent/wrong-type A-000 or A-000-RESH, verify an independently issued full record and witness, and distinguish ordinary validation from authorized recovery. Positive valid-anchor control must still pass. Issuer/custodian, exact schema and freeze authority belong to Timothy. Preserve Claude's E35 narrower re-anchor finding and Lesson 2 `visible_fields` limitation. **Next:** independent review of real caller exception handling and a bounded acceptance sketch after Timothy's decisions.
