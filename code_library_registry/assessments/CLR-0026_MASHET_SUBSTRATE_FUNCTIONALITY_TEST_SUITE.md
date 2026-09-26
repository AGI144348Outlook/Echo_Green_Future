# CLR-0026 — Mashet Substrate Functionality Test Suite

## Classification
Historical validation scaffold / March 2026 / companion to CLR-0025.

## Purpose
Tests concept→substrate lookup, project-defined letter→substrate mappings, deterministic generation, and placeholders for substrate interaction validation.

## What it actually validates

### Concept mapping
The expected answers are authored from the same keyword/substrate assumptions implemented by CLR-0025. Passing therefore establishes conformance to the specified lookup table, not independent semantic accuracy.

### Letter coverage
The expected Hebrew-letter sets are likewise authored from the same project mapping. These tests detect accidental implementation drift, but cannot validate the linguistic truth of those mappings.

### Reproducibility
This is a legitimate determinism test. With fixed dictionary insertion order and deterministic sorting/greedy selection, repeated calls should normally produce identical selections (timestamps aside).

### Interaction rules
The suite explicitly acknowledges that interaction validation is not implemented. It prints one expected interaction but performs no compatibility/prerequisite assertion.

## Critical test-harness defects

1. **Concept result success is recorded incorrectly.**
For a positive case, the harness can print FAIL for missing expected substrates, then still call `generate()` and append `success: True` merely because generation did not throw. The summary therefore counts generation completion rather than mapping correctness.

2. **Letter-count failures do not fail the recorded test.**
The harness prints a failed letter-count check but still stores `success: True`.

3. **Negative case is omitted from summary results.**
When no substrates are identified for Test 7, the printed result is PASS but nothing is appended to `results['concept_mapping']`. The denominator therefore does not represent all declared concept tests.

4. **Complex test conflicts with CLR-0025 defaults.**
Test 6 expects 4–5 letters, but `MashetGenerator.generate()` calls `find_letters_for_substrates()` with default `max_letters=4`. Five can never be generated through that path.

5. **Interaction test suite does not test its declared cases.**
Only `INTERACTION_TEST_CASES[:1]` is iterated, and even that is documentation output only. Incompatibility and prerequisite cases are never executed.

6. **Reproducibility compares letter sets, not ordered sequences.**
Two words with the same letters in different order would be reported letter-consistent despite order being essential to a linguistic/operator sequence. Compare tuple/list sequence and full structural signature.

7. **Determinism is not semantic validation.**
Three identical outputs prove reproducibility, not correctness, grounding, coherence, or transfer.

8. **JSON export is operationally useful but evidence metadata is missing.**
Future results should include implementation commit/hash, registry version, seed where applicable, environment, test-spec version, timestamp, exact assertions, observed values, and pass/fail derived from assertions.

## Recommended validation layers

### Layer A — Registry conformance
Does implementation reproduce the declared mappings exactly?

### Layer B — Internal structural validity
Are exclusions, prerequisites, domain/codomain, phase permissions, TC/TI/TA capabilities, and composition laws satisfied?

### Layer C — Linguistic validation
Do constructed forms satisfy the project's declared Hebrew morphology/phonology rules? Independent linguistic claims require external evidence.

### Layer D — Behavioral validation
Does an admitted operator produce the predicted state transformation on held-out tasks?

### Layer E — Generalization/transfer
Does a structural signature learned/tested in one environment transfer under controlled transformations without contamination or retraining?

## Strong modern test record
`TestSpec -> implementation_ref -> registry_ref -> inputs -> expected structural properties -> observed properties -> assertion results -> evidence status -> provenance`.

Do not let UI/log strings determine pass/fail. Assertions should produce machine-readable outcomes first; prose should render those outcomes second.

## Relation to Echo Notebook
This is a direct ancestor of the Notebook's experiment/audit role. A modern Notebook can query a RegistryObject, instantiate a candidate composition in an NVE, execute a TestSpec, retain the trace/evidence, and only then submit the candidate to the Governor for admission.

## Status
Assessed / Historical validation scaffold / Candidate for reconstruction. Valuable primarily for defining the validation categories and exposing what was not yet tested.
