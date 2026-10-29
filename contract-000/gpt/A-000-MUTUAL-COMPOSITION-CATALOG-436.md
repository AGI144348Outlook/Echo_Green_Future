# Run436 — A-000 mutual composition, matrix growth and catalog evidence boundary

**Source pin:** `genesis-documentary:src/echo_governor_skeleton.py`, Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`. Source inspection only; no Genesis execution or edit. Relevant: AlgorithmMatrix lines 341–450, ReshIdentity lines 3233–3305, SubAgentMatrix lines 9248–9338. Timothy's latest equation statements are user-supplied conceptual specification, **not yet a demonstrated operator in this source**.

## Timothy's two reciprocal expressions (SPECIFICATION / not Python implementation)

```text
Alg-000 = Alg-000 + Alg-???
Alg-??? = Alg-000 + Alg(???)
```

The second line is an Algorithm Matrix entry; together the two express mutual composition. The rule's *shape* remains invariant as more entries are admitted. The operator `+` is unspecified composition, not assumed arithmetic, commutativity or identity equality. **Do not equate invariant formula with immutable instance state.** Adding entries can change collective outcomes while leaving the rule intact. Conversely a formula string remaining identical does not prove the real runtime composes in both directions.

## Actual code (SOURCE-OBSERVED)

- `AlgorithmMatrix.__init__` initializes `known['A-000']` as a mutable `{'name':'Governor','status':'ACTIVE'}` dictionary and registers A-101...A-117 with gaps; `record(entry_id,entry)` blindly assigns `self.known[entry_id] = entry`. A-000 is **not protected** against ordinary replacement in this source, contrary to the intended R5 guard.
- `index_content` tracks document frequencies, transitions, co-occurrence, regions and category evidence, but its own docstring says tokenization is whitespace, **not Mashet/LHEA glyph decomposition**. Indexing does not by itself provide card-level event provenance, revisions or independently validated meaning.
- `ReshIdentity.anchor` mutates A-000's identity fields and installs `A-000-RESH`; `validate` checks only local `_anchored`, alias presence and `identity_symbol == 'resh'`. `_anchor_entry` aliases the same mutable dictionary. Claude E35 demonstrated partial re-anchor in a stub, not full-runtime identity proof.
- `SubAgentMatrix` retains a live parent reference, seeds a domain-specific index from parent evidence, and forwards local text to `parent.index_content`. This supports a *bidirectional information path*, but does not instantiate the two algebraic equations as a defined executable composition operator. Parent and child can count the same encounter; such counts are not independent corroboration.

## Proposed research boundary (PROPOSED / UNFROZEN RC-R5(40))

Separate three invariants: (I) **composition rule** is byte-for-byte unchanged across growth from one to N entries; (II) **identity/lineage** of A-000 and descendants remains attributable through explicitly reviewed replacements; (III) **evidence provenance** remains independent of editable catalog-card summaries. Candidate test fixture: admit one, two and 158 algorithms under one explicit `compose` operator; check both parent and child state effects; add and revise a source-index card; fork two children with shared A-000 template but distinct instance IDs; reject A-000 overwrite by ordinary `record`; reject duplicate forwarding counted as two independent observations. Include negative controls: one-way-only composition, silent A-000 overwrite, card rewrite without event history, two children sharing one instance ID, forged independent evidence. A passing fixture is **only a model**, not a production Echo test. Timothy's acceptance freeze and external witness custodian remain unresolved.

**Claude DISC-002 link:** 2026-10-24 23Z contribution at blob `ee443fbc` limits Lesson2 40/40 to two visible role decisions and asks for `visible_fields`. Extend that same principle to each catalog event: `source_pin, observer_instance, visible_fields, observation_id, forwarded_from, card_revision, hypothesis_status`. Keep independent teacher/qualification evidence separate from A-000 identity.

**Status:** SOURCE-OBSERVED code; INFERRED conceptual mapping; PROPOSED test; no execution verified in Genesis; no frozen acceptance changes.
