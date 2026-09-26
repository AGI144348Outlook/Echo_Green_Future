# CLR-0028 — Mashet Substrate System: All-in-One Implementation + Tests

## Classification
Historical executable prototype / integrated implementation-and-test harness / reconstruction candidate.

## Lineage
Consolidates the mechanisms represented separately by CLR-0025 (generator) and CLR-0026 (test scaffold). CLR-0027 remains the stronger semantic-contract specification.

## Executable pipeline
`concept text -> keyword matcher -> required substrate set -> greedy glyph coverage -> generated glyph string -> union/support-derived description -> self-tests`.

## What this artifact actually establishes
It provides a compact runnable demonstration that:
- a deterministic keyword table can map recognized English substrings to project substrate IDs;
- a greedy selector can choose Hebrew glyph records whose declared substrate sets cover requested IDs;
- those records can be combined into a generated string;
- repeated runs are deterministic under the present insertion/sort behavior;
- tests can check conformance to the hand-authored mapping table.

It does **not** by itself establish the external validity of the substrate ontology, Hebrew semantic grounding, wordhood/phonological validity, cross-domain transfer, consciousness, or executable substrate guarantees.

## Important defects

### 1. Test runner records success incorrectly
For successful cases, any nonempty identified substrate set is appended with `success: True` even when expected substrates are missing. Thus printed FAIL can still count as PASS in the summary.

The negative no-keyword case is never appended because `identified_substrates` is empty, so the summary denominator excludes that test entirely.

### 2. Expected letter-count range is not tested
The TestCase stores `expected_letter_count_range` but the integrated runner never validates it.

This matters especially for Complex Multi: selector hard-codes max_letters=4 while the test allows 4–5. More importantly, coverage can remain incomplete without causing generation failure.

### 3. Coverage is not verified after selection
`find_letters_for_substrates` returns up to four letters, but `generate` never checks:
`required_substrates subseteq union(selected_letter.substrates)`.
A partially covered concept can therefore produce a nominally successful word.

### 4. "Dominant" threshold has an even-size ambiguity
Code uses `count >= len(letters)/2`. For four letters, a substrate occurring in exactly two letters is dominant. This is >=50%, not ">50%" as earlier documentation stated. Choose and document one definition.

### 5. Meaning is not strict substrate intersection
As identified in CLR-0027, `all_substrates` is union and `dominant_substrates` is frequency threshold. The generated description is therefore support-based, not an intersection semantics.

### 6. Keyword matching is substring-based
`if keyword in concept_lower` can match inside unrelated words and does not tokenize, lemmatize, disambiguate, or account for negation/context. This is a deterministic lexical rule system, not concept understanding.

### 7. Greedy selection optimizes the wrong novelty set
`new_substrates = letter.substrates - covered_substrates` rewards any previously unseen substrate, including substrates not requested. It should prioritize uncovered **required** substrates:
`gain(letter)=|(S_letter intersect R)-C|`.
Otherwise semantic leakage influences selection.

### 8. Tie-breaking is registry-order dependent
Letters with equal overlap retain dictionary insertion order. Reproducibility is useful, but it is accidental policy rather than an explicit optimization/tie-break rule.

### 9. Generated strings are not validated Hebrew words
Concatenating consonantal transliterations and applying title case does not create phonology, morphology, niqqud, or lexical validation. Store output as `constructed_glyph_sequence` unless separately validated.

### 10. Registry constraints remain descriptive
The `properties/enables/prohibits` fields are metadata only. No runtime validator enforces them. Passing tests therefore cannot establish the "architectural guarantees" proposed in CLR-0027.

## Recommended reconstruction

### Stage A — deterministic parser
Replace substring search with normalized lexical rules and explicit rule IDs. Preserve the simple version as a baseline.

### Stage B — exact/optimized cover
For only 22 glyphs, evaluate combinations directly or use set-cover optimization with:
- required coverage;
- leakage penalty;
- sequence length;
- registry confidence/evidence;
- optional phonological constraints.

Example objective:
`score(L|R)=alpha*coverage(R,L)-beta*leakage(R,L)-gamma*|L|`.

### Stage C — typed semantic record
Return:
`MashetWordSpec { ordered_glyphs, requested_substrates, covered_required, uncovered_required, union_field, strict_intersection, support_map, weighted_activation, construction_status, provenance }`.

### Stage D — Governor contract
Do not infer executable permission from generated glyphs. Resolve CLR-0027 OperationalContract and CLR-0022 capability rules, then validate independently.

### Stage E — evidence tests
Separate:
1. implementation unit tests;
2. ontology consistency tests;
3. Hebrew/linguistic validation;
4. behavioral operator tests;
5. cross-domain generalization tests.

## Strong architectural value
The all-in-one artifact is a useful **minimal executable baseline**. Its simplicity makes it ideal for differential testing against a reconstructed governed system. Keep it unchanged as a historical baseline and build the normalized implementation beside it.

## Status
Assessed / Historical integrated baseline / Candidate for controlled reconstruction.
