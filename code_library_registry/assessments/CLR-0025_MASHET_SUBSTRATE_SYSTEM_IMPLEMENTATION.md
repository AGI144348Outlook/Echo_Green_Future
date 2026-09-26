# CLR-0025 — Mashet Substrate System: Complete Python Implementation

## Classification
Historical executable prototype / Mashet semantic-substrate generator. March 2026. Implements concept-keyword mapping, project-defined Hebrew letter/substrate mappings, greedy letter selection, word construction, derived metadata, explanation, logging, and CLI.

## What the code actually computes
The executable pipeline is:
`concept string -> substring keyword matches -> required substrate set -> greedy Hebrew-letter coverage -> concatenated glyph string/transliteration -> union/count of assigned substrates -> generated explanation`.

This is substantially narrower than the theoretical claim "meaning emerges through substrate intersection." The implementation performs deterministic registry lookup, set union/counting, greedy coverage, and templated prose generation.

## Data model
### Substrate Registry
Each named substrate stores:
- description;
- properties;
- enables;
- prohibits.

These are project-defined semantic assertions. The code does not execute or validate most of these fields.

### HebrewLetter
Stores glyph, name, transliteration, gematria, substrate set, and description.

The letter-to-substrate mappings are Mashet definitions/hypotheses, not established intrinsic Hebrew computational semantics.

### MashetWord
Stores generated glyph sequence, transliteration, selected letters, all/dominant substrates, generated meaning string, source concept, timestamp.

This is useful provenance and should be retained in a modern RegistryObject.

## Important algorithmic findings

### 1. "Intersection" is mostly union
`derive_meaning()` collects:
`all_substrates = union_i substrates(letter_i)`.
Dominance is based on frequency. It does not compute a semantic intersection as described in the surrounding theory.

A true common intersection would be:
`I = intersection_i S(letter_i)`.
A richer composition should retain union, intersection, ordered sequence, rule activations, exclusions, prerequisites, and domain typing separately.

### 2. Dominance threshold bug/ambiguity
Comment says substrates appearing in >50% of letters, but code uses:
`count >= len(letters)/2`.
For 4 letters, 2/4 = 50% is accepted, not >50%. For 3 letters, count >=1.5 means 2, correctly >50%.

### 3. Greedy selector can add irrelevant semantics
Selection scores overlap with required substrates, but once a letter is selected, `covered_substrates.update(letter.substrates)` includes every substrate assigned to that letter. Generated `all_substrates` therefore contains properties never requested by the concept. This is semantic leakage by construction.

The selector also uses `new_substrates = letter.substrates - covered_substrates`, not `(letter.substrates & required_substrates)-covered_required`, so unrelated substrate novelty can influence selection while filling minimum letters.

### 4. Minimum-three-letter requirement can fabricate excess structure
If one/two letters cover the requirements, the forced `min_letters=3` causes extra letters/substrates to be introduced. The word's derived meaning can therefore be driven by formatting constraints rather than conceptual requirements.

### 5. No phonological validation
Despite theory discussing Hebrew phonological/morphological constraints, `construct_word()` simply concatenates consonants and transliterations. No vowels, roots, binyanim, final-letter forms, phonotactics, morphology, or Hebrew lexical validation are implemented.

### 6. Silent/guttural transliteration collapses information
Aleph and Ayin transliterate to empty strings, so distinct Hebrew sequences can map to the same Latin transliteration. Transliteration is therefore not an injective identifier.

### 7. Keyword analysis uses substring matching
`if keyword in concept_lower` can generate accidental matches inside unrelated words and has no tokenization, negation, morphology, phrase disambiguation, or contextual semantics.

### 8. Registry constraints are descriptive only
Fields such as `prohibits`, `enables`, and `properties` are never enforced by generation. No compatibility, exclusion, prerequisite, domain, or Governor checks occur.

### 9. No executable operation generation
Unlike the preceding theoretical document, this artifact generates MashetWord metadata only. It does not create executable Mashet functions, prove correctness, perform self-modification, or demonstrate cross-domain transfer.

## Strong surviving architecture
This is nevertheless a useful early Registry prototype:
`Natural-language request -> semantic feature extraction -> registry lookup -> candidate operator/glyph selection -> composition record -> provenance/explanation`.

That pattern maps well to the modern Notebook and Generalization/Glyphic Registries if the project-defined semantic mappings are explicitly typed and evidence-scoped.

## Modernization
Replace single substrate labels with typed registry relations:
`GlyphRef --participates_in{source,evidence,status,version}--> Primitive/ActionRef`.

Replace greedy word construction with a constrained composition problem:
- cover required action/features;
- minimize unrequested features;
- satisfy domain/codomain;
- satisfy composition rules;
- enforce exclusions/prerequisites;
- preserve order;
- retain ambiguity/candidate alternatives;
- require Governor admission before executable use.

Recommended objective:
`argmin_C [lambda_1 MissingRequired(C) + lambda_2 ExtraFeatures(C) + lambda_3 RuleViolations(C) + lambda_4 Complexity(C)]`.

Do not call the resulting string a Hebrew word unless it independently satisfies the project's chosen Hebrew linguistic criteria. "Mashet glyph sequence" or "constructed Mashet form" is safer by default.

## Relation to current architecture
This prototype is an ancestor of:
- Glyphic Registry;
- Generalization Registry;
- Operator Registry;
- Notebook query-to-temporary-matrix workflow;
- deterministic translation/explanation records;
- TC/TI/TA-governed operator construction.

Modern flow:
`ConceptSpec -> typed Registry query -> candidate glyph/operators -> constrained composition -> temporary expression/matrix -> NVE test -> evidence -> Governor admission -> optional persistence`.

## Status
Executable historical prototype / Assessed / Candidate for reconstruction, not direct reuse. Preserve source separately when archival fidelity is desired.
