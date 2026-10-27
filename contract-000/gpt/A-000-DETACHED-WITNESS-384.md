# A-000 / Resh — detached witness candidate, Run384

**Status:** PROPOSED / synthetic execution verified only; **not** frozen RC-R5 acceptance, not deployed, no Genesis mutation. Prospective registration: [Issue #13](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6431110961).

**SOURCE-OBSERVED:** Genesis `genesis-documentary:src/echo_governor_skeleton.py` Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`. `AlgorithmMatrix.__init__` initializes A-000 with `name=Governor,status=ACTIVE`; `record()` permits ordinary overwrite. `ReshIdentity.anchor()` modifies A-000 in place, creates A-000-RESH, and retains a shared mutable alias in `_anchor_entry`. `validate()` checks only `_anchored`, alias-key existence and A-000's `identity_symbol`. Neither full identity content nor external custody is checked.

**PROPOSED:** [standalone read-only candidate](a000_detached_witness_384.py) deep-copies A-000 and A-000-RESH, checks the expected Governor/Resh fields, computes canonical JSON SHA-256 and compares the current pair to a detached receipt. A separate custodian must keep the receipt outside the mutable matrix; that custodian and authorization are *not* implemented.

**EXECUTION-VERIFIED:** [10/10 isolated Python unittest cases](test_a000_detached_witness_384.py) passed on synthetic pair fixtures: intact pair; changed status; altered aliases; missing Governor; missing alias; detached copy not aliased; mutated receipt state; changed digest; changed identity glyph; and explicit **negative capability** (a newly issued receipt for altered state is accepted, proving the prototype cannot distinguish an authorized issuer from an attacker). Exact committed code Git blob fingerprints matched local tested files: implementation `90282d37f19b1f081bbebecd9bd005629e45268d`, tests `39667b7b710f8eac3537f18533fceafc388965f1`.

**INTERPRETATION:** A detached digest can detect later changes *relative to a trusted receipt*, not independently establish who was allowed to issue that receipt. No proof of adversarial integrity, rollback safety, identity authority, complete Genesis execution or learning. Candidate only for RC-R5 case (13), which remains unfrozen.

**Next:** Claude independently challenge field scope, custody and receipt replay; Timothy to choose custodian, permitted amend authority and frozen acceptance. No changes to protected code or another participant's work.
