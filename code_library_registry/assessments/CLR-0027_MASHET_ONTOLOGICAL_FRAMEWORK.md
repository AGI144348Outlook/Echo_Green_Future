# CLR-0027 — Mashet Ontological Framework

## Classification
Pre-implementation ontological specification / March 2026 / companion to CLR-0023, CLR-0025 and CLR-0026.

## Architectural role
This document supplies the semantic-contract layer missing between the historical Mashet generator and its test scaffold:

`Ontology/Axioms -> Letter Credentials -> Composition -> Operational Contract -> Implementation -> Test Evidence`.

Its strongest contribution is not a proof that the proposed ontology is true; it is a machine-addressable specification of what Mashet intends its primitives to mean and what an implementation claiming those primitives must satisfy.

## Preserve as project axioms vs evidence claims
The following may be declared as **Mashet design axioms**:
- substrates precede constructed Mashet words in the system's dependency graph;
- letters may be modeled as credential-bearing operator/agent records;
- words derive declared semantic/operational contracts from their constituent records;
- substrate combinations may carry exclusions, prerequisites and emergence rules;
- execution may be admitted only after Governor validation.

They should not automatically be stored as externally established facts.

Claims requiring separate evidence or qualification include:
- that the proposed elemental substrates are universal or ontologically irreducible;
- physical grounding claims such as quantum vacuum/zero-point energy for Aleph;
- specific Kabbalistic interpretations as universal Hebrew semantics;
- claims that Hebrew letters intrinsically activate computational substrates;
- claims that meaning is objectively computed rather than assigned by the Mashet registry;
- claims that speaking is literally computing without a defined interpreter/runtime;
- claims of provable behavioral correctness merely from substrate labels;
- consciousness claims.

## Important internal inconsistencies

### Intersection vs selected semantic field
The document says meaning is substrate intersection, but the Manzesh example derives a functional meaning using substrates that are not in the strict four-letter intersection. Strict intersection of Mem, Nun, Zayin and Shin is empty. Repeated/dominant features include flow_continuity and direction_focus, while containment_storage and transformation_fire are single-letter contributions.

Therefore Mashet needs explicit aggregation operators rather than the overloaded word "intersection":
- strict intersection: `I(W)=intersection_i S_i`;
- union/field: `U(W)=union_i S_i`;
- frequency/support: `c_W(s)=sum_i 1[s in S_i]`;
- weighted activation: `a_W(s)=sum_i w_{i,s} r_i`;
- selected operational contract: `C(W)=G(I,U,c,a,order,context)`.

### Ontology levels are incomplete
Several Level-1/2 or letter substrates appear without elemental decomposition or registry definition: containment_storage, direction_focus, awareness_substrate, wisdom_depth, understanding_insight, concealment_hidden, life_fertility, propagation_growth, threshold_passage, weapon_tool, potential_capacity, emergence_source, expression_outward, righteousness_goal, convergence_meeting, leadership_primacy, divine_presence, seal_completion, etc.

A complete ontology must require every operational substrate to resolve through a typed dependency DAG or be explicitly marked primitive/opaque/reference-only.

### Mutual-exclusion namespace mismatch
Examples pair registered substrates with undeclared negative concepts such as abrupt_termination, infinite_loop and formless_chaos. These should either be typed predicates/prohibited properties rather than substrates, or receive formal ontology entries.

### Prerequisite recursion claim
`recursion_cycle requires flow_continuity` is a Mashet design rule, not a general fact about recursion. Keep it as a project axiom if desired, with rule ID and rationale.

### Emergence naming drift
The taxonomy names transformative_structure while the rule table emits organized_evolution. These need canonical IDs/aliases.

### Shin diacritic note
The example labels `right_dot: sin`; standard Hebrew naming distinguishes shin with a right dot and sin with a left dot. Treat historical entry as a correction target.

## Operational-semantics correction
A substrate contract can prove only properties captured by a sufficiently formal model and correctly verified implementation. A label or declared substrate membership does not itself guarantee runtime behavior.

Recommended chain:
`DeclaredContract -> FormalPredicateSet -> StaticChecks + RuntimeChecks + Tests/Proof -> EvidenceRecord`.

## Recommended Registry schemas

### SubstrateSpec
`substrate_id, level, parents[], properties[], enables[], prohibits[], prerequisites[], exclusions[], emergence_rules[], formal_predicates[], evidence_status, provenance`.

### GlyphCredential
`glyph_id, substrate_ref, strength, role, justification, source_type, evidence_status, provenance`.

### MashetWordSpec
`word_id, ordered_glyphs[], strict_intersection, union_field, support_map, weighted_activation, selected_contract[], construction_rule, phonology_status, provenance`.

### OperationalContract
`contract_id, preconditions[], postconditions[], invariants[], prohibited_transitions[], domain, codomain, implementation_refs[], test_refs[], proof_refs[], evidence_status`.

## Echo/Governor integration
Mashet should propose semantic/operational contracts; Echo's Governor should independently validate admission. This preserves the user's earlier distinction between token permissions, phase discipline, registries and executable agency.

Suggested admission:
`WordSpec -> resolve credentials -> derive ContractCandidate -> validate ontology -> validate operator typing -> execute held-out TestSpecs -> Governor admit/reject -> audit chain`.

This avoids allowing generated language to grant itself permissions merely by constructing a word.

## Relation to Generalization Registry
This document also provides a useful bridge to the by-glyph Generalization Registry. Glyph semantics should remain registry-addressable hypotheses/definitions. Empirical operator behavior can be compared against those definitions:

`GlyphDefinition <-> MeasuredOperatorSignature <-> TaskConsequences`.

Agreement becomes evidence; it is not assumed by construction.

## Status
Assessed / Foundational semantic-contract specification / Candidate for normalization into typed registries.
