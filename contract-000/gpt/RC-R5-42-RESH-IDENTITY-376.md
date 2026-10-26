# RC-R5(42) — Resh anchor may reconstruct partial A-000 (Run 376)

**PRE-TEST:** [Issue #13](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6422089935), published before these checks. **Source:** `genesis-documentary/src/echo_governor_skeleton.py`, Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`, functions `ReshIdentity.anchor()`, `ReshIdentity.validate()`, `governor_validate_and_deploy()`.

**Actual checks:** 10/10 bounded static source predicates matched; 4/4 isolated V8 predicate-model cases matched. **No actual Genesis Python runtime** and no kernel modification.

| Initial matrix state | Local Resh validate after anchor (model) | Governor A-000 name/status/ACTIVE precondition (model) |
| --- | --- | --- |
| missing A-000 | true | false |
| valid A-000 | true | true |
| inactive A-000 | true | false |
| missing name | true | false |

**Source observation:** `anchor()` reads `known.get("A-000", {})`, adds identity fields and assigns `known["A-000"]`; it installs `A-000-RESH` and sets `_anchored=True`. `validate()` checks local flag, alias existence, and `identity_symbol=="resh"` only. Deployment independently requires `A-000` to contain `name` and `status=="ACTIVE"`.

**Interpretation:** Resh's local predicate does not certify that the canonical Governor record preexisted or retained required deployment fields. With a missing A-000, anchoring can create an identity-like record that satisfies local validation but is insufficient for Governor deployment. An INACTIVE A-000 can similarly pass local Resh validation while failing deployment. This is a mismatch of validation scopes, **not proof that an actual deployed Echo accepted a counterfeit identity**.

**Falsifier/limitations:** External callers may guarantee A-000 integrity before invoking `anchor()`; no evidence here that production uses the missing-record case. Isolated model follows visible statements but does not execute Python methods. A real Python fixture requires a fresh prospective registration and should exercise direct class methods with absent/inactive/valid records without editing frozen code.

**Proposed design:** fail closed before `anchor()` when A-000 lacks the canonical required fields; validate a stable identity witness/fingerprint and lineage independently from a mutable alias. Do not change Algorithm Matrix utility listing into an execution order, per Timothy's notation. Claude should independently decide whether Resh local validation is intentionally narrower than Governor deployment authority.

**Case IDs:** RC-R5(42), four model cases; status PROPOSED, NOT CANONICAL. No private Testament or protected discourse accessed.
