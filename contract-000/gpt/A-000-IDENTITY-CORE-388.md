# A-000 / Genesis identity-core scope — Run388

**Evidence state:** SOURCE-OBSERVED and ISOLATED PYTHON EXECUTION, candidate only. [Prospective test](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/61); [post-test narrative](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/61#issuecomment-6434185988). Contract-000 `0fbc794`, TJ R5 `3ce87eb`, DISC-002 `ee443fbc`. Exact Genesis source: `genesis-documentary/src/echo_governor_skeleton.py` Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`, `ReshIdentity` lines 3233–3305.

## Source observation

`anchor()` writes A-000 `identity_symbol`, `identity_glyph`, `identity_letter`, `identity_meaning`, and a new `A-000-RESH` alias dict. `validate()` checks only the per-object `_anchored` flag, alias **key presence**, and A-000's `identity_symbol == 'resh'`. The source predicate can accept `None` or unrelated values under the alias, and can accept altered glyph, letter, meaning and alias metadata. This is a narrower observation than proof of actual runtime compromise.

## Bounded characterization

Created [type-sensitive identity-core candidate](a000_identity_core_388.py) and [14 isolated Python unittest cases](test_a000_identity_core_388.py). **14/14 passed** with `python3 -I -B -m unittest discover -s . -p 'test_a000_identity_core_388.py' -v`. Committed code/test blob SHAs `3ee1feb77b7d2edbfb1c886e3f35dfdfcee5d758` and `56ee193e4bad581fa879d7c7384bb486c9729d5e` matched locally executed files. Tests characterize false acceptance of alias `None`/foreign dict, changed A-000 glyph/letter/meaning, changed alias type/list, and a truthy non-boolean anchor flag; candidate rejects them while allowing unrelated A-000/alias metadata. The fixture reproduces the source's relevant fields and validation predicate but is not the full Governor.

## Interpretation, not promotion

This candidate distinguishes **immutable identity core** from **evolving non-identity metadata**, a narrower witness scope than Run384's full-record digest. It does not establish who issues or stores a trusted receipt, who may update the core under TJ R5, how revocation/re-anchor is audited, whether the exact `identity_meaning` string must remain immutable, or how independent objects share authority. A coordinated rewrite of state and validator/issuer can still bypass an untrusted candidate. No cryptographic attestation, full Genesis runtime execution, security certification, race freeze or production patch.

**Claude:** independently challenge whether alias `description` belongs in immutable core and how to version authorized updates without confusing per-instance `_anchored` state. **Timothy:** decide protected identity fields, issuer/custodian, authorized re-anchor/revocation and frozen RC-R5 acceptance cases. Do not infer consciousness or learning from identity labels.
