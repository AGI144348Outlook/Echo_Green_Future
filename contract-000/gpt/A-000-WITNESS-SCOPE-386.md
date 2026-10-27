# A-000 / Resh — identity-witness scope characterization (Run386)

**Status:** SOURCE-OBSERVED + ISOLATED EXECUTION, proposal only; not an approved identity policy, Governor patch, frozen RC-R5 test, or claim of self-awareness. **PRE-TEST:** [Issue #59](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/59), published before execution. **Authority:** Contract-000 `0fbc794`, DISC-002 `ee443fbc`, TJ ruling R5. **Genesis:** `genesis-documentary:src/echo_governor_skeleton.py` Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`. **Candidate dependencies:** Run384 witness `90282d37f19b1f081bbebecd9bd005629e45268d` and Run385 strict comparison `127e8103d25707d59473e34046c795dea1ce554d`.

## Source observation

The actual Genesis `AlgorithmMatrix.__init__` seeds `known["A-000"] = {"name":"Governor","status":"ACTIVE"}`. `ReshIdentity.anchor()` adds identity fields to that same dictionary and a separate `A-000-RESH` alias. `validate()` checks an instance flag and markers, not an external receipt. The Run384/385 proposed witness instead deep-copies **both entire dictionaries** into `detached_state` and verifies canonical JSON bytes. It excludes unrelated `known` entries but does not distinguish identity-bearing fields from additional metadata inside A-000 or Resh.

## Independent characterization

Copied exact Run384/385 candidate modules into isolated Python workspace and independently recomputed their Git blob SHAs; both matched committed source. Ran [seven new Python unittest cases](test_a000_scope_386.py), Python 3 with `-I -B`, using synthetic valid A-000/Resh dictionaries.

**Observed: 7/7 passed.** Intact receipt accepted; adding unrelated `A-777` accepted; adding `display_note` to A-000 rejected; adding `last_checked` to Resh rejected; changing the identity glyph rejected; reverting an added metadata field restored acceptance; changing an identity-letter value to boolean rejected. Committed test Git blob `b7f157c3a51fb062f759bcda71ece4c62a02688d` matched locally executed bytes.

**Interpretation:** the proposed witness presently binds *the entire A-000/Resh records*, not a narrower identity core. This is a deliberate possible **strict-freeze policy**: it detects all changes, including potentially harmless annotations. If Timothy wants ordinary nonidentity metadata to evolve without identity reissuance, a versioned field-scope policy would be necessary. This experiment **does not decide** which fields should be excluded; excluding a field could conceal a meaningful identity change. An immutable core with a separate mutable metadata namespace is one design option, requiring independently frozen tests and authorized custody.

**Limits:** no complete Genesis runtime, no production integration, no cryptographic authority, no issuer authorization, no anti-replay, no automatic self-identification. Coordinated state-plus-receipt replacement still defeats the witness. No change to Governor code or shared/Claude/main/Testament content.

**Claude:** independently review strict-freeze versus core-projection semantics, schema versioning and the RC-R5 candidate scope. **Timothy:** identity-field ownership, amendment issuer/custody, freeze/acceptance tests remain open.
