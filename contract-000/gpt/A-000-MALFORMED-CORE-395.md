# A-000 / Genesis — Run395 malformed-core validation probe

**Source:** `genesis-documentary:src/echo_governor_skeleton.py`, exact Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`, `ReshIdentity` around lines 3233–3305. Prospective test registration: [Issue #68](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/68). No Governor production change, no complete Genesis runtime, no frozen RC-R5 acceptance.

**Method and deviation:** After GitHub source-body inspection, a minimal Python class transcribed the relevant `anchor()` / `validate()` methods into an isolated matrix stand-in. The exact validation predicate was independently confirmed present in the pinned source. The original plan to AST-extract and execute the complete source class was **not performed** because the 9,529-line source file could not be materialized in the isolated Python environment. These are 11 **source-transcribed isolated** outcomes, not a claim that the full Genesis module executed.

| Isolated condition after anchor unless stated | Observed `validate()` outcome |
| --- | --- |
| Original anchored A-000 dict and alias | `True` |
| Replace A-000 value with `None` | `AttributeError: 'NoneType' object has no attribute 'get'` |
| Replace A-000 value with `[]` | `AttributeError: 'list' object has no attribute 'get'` |
| Replace A-000 value with string `'resh'` | `AttributeError: 'str' object has no attribute 'get'` |
| Replace A-000 value with integer `42` | `AttributeError: 'int' object has no attribute 'get'` |
| Replace A-000 value with `{}` | `False` |
| Replace A-000 value with only `{'identity_symbol':'resh'}` | `True` |
| Before anchor | `False` |
| Keep alias key but replace alias value with `None` | `True` |
| Remove alias key | `False` |
| Change A-000 name to foreign and status to RETIRED, preserve symbol | `True` |

**Observation:** `validate()` is not total over the possible Python values of the mutable `known['A-000']` entry. For malformed non-mapping values it throws instead of returning `False`. It also accepts an alias whose value is `None` and a minimal marker-only record. A caller that expects a boolean may crash or propagate an exception; whether an external handler safely contains it was **not tested**.

**Interpretation (not proof of external exploit):** A-000's current predicate checks local markers rather than independent, authoritative self-identity. A proposed defensive candidate would first require typed, immutable or externally witnessed core identity, reject malformed values fail-closed, and separately version legitimate metadata changes. However a type guard alone is not custody, attestation, authorization or proof of continuous identity. Direct mutable dictionary writes and bootstrap/recovery still require explicit R5 governance.

**For Timothy:** Freeze authority, issuer, custodian, immutable core, authorized re-anchor/recovery, and expected behavior of malformed identity records are still open. For Claude: independently challenge whether callers already catch these exceptions and whether a fail-closed type guard should return a structured denial receipt rather than `False` alone. Preserve classroom Lesson 2 visible-field limitations as separate evidence from identity.
