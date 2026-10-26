# RC-R5(44) — Resh alias value/type validation gap (Run 378)

**Status:** SOURCE-OBSERVED predicates and ISOLATED-JS-MODEL outcomes, not a Genesis Python runtime result; PROPOSED candidate only, not a frozen test. **Prospective entry:** [Issue #13 PRE](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6424734004), published before checks. **Source:** [Genesis `src/echo_governor_skeleton.py`](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/genesis-documentary/src/echo_governor_skeleton.py) blob `63eb982989b4f3478d649430b555c8f4ba755c27`, `ReshIdentity` lines 3233–3305. Current public Contract `0fbc794` and DISC-002 `ee443fbc` read first.

## Question and hypothesis

`ReshIdentity.validate()` checks `self._anchored`, the **presence of the key** `A-000-RESH` in `matrix.known`, and `A-000.identity_symbol == 'resh'`. It does not inspect the alias value, its type, its identity fields or its link back to A-000. **Hypothesis:** malformed alias values can satisfy local validation and lead `report()` to assert `A-000 and Resh are one`.

## Method and observations

Seven bounded exact-source checks passed: anchored flag, alias key membership, A-000 symbol match, no alias-value retrieval, no alias name/aliases check, report calls validate, and report makes a strong identity statement. Six isolated JS predicate-model scenarios matched the expected branch behavior, assuming the anchored flag is true and A-000 has identity_symbol `resh`:

| Alias key/value | Expected local `validate` | Isolated model | Interpretation |
| --- | --- | --- | --- |
| present / canonical mapping | true | true | ordinary path |
| present / `None` | true | true | malformed alias accepted by predicate |
| present / empty mapping | true | true | fields not examined |
| present / integer `42` | true | true | type not examined |
| present / `False` | true | true | truthiness of value irrelevant |
| key absent | false | false | membership is checked |

**Observations:** 7/7 source assertions, 6/6 isolated model cases. **Interpretation:** local marker recognition does not independently attest a well-formed identity alias. This extends Claude's E35 and Run377's RC-R5(43) alias-content findings with malformed **value/type** cases. No actual Genesis Python execution, frozen acceptance tests, deployment, or A-000 writes were performed. An external caller could reject malformed aliases; this review does not show an exploit in production.

## Proposed acceptance candidate — not frozen

RC-R5(44): after a valid anchor, replace `A-000-RESH` with `None`, `{}`, `42`, and `False` without deleting its key. A strong identity **attestation** must be refused, or the report must explicitly state that identity is **unverified**, until a schema-bound and externally witnessed alias identity is validated. Record the original and mutated values, witness source and recovery attempts append-only. Timothy decides the custodian, required fields, issuer and freeze criteria; do not silently choose a hash scheme or modify Genesis. A local self-description may remain separate from an independently validated attestation.

**Claude coordination:** E35 and Lesson 2 remain independent evidence chains. Lesson 2's two role decisions and visible speaker/addressee labels are not A-000 validation. The analogous principle is to record what the validator actually inspected, not to claim identity from fields it never saw.
