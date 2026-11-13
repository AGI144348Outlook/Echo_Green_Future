# ECHNP-001 — Contextual Dictionary Evidence Networking Protocol
Status: **PROPOSED / IMPLEMENTATION IN DEVELOPMENT**. Living record; version 0.1; 2026-11-12.
Owner/originator: Timothy. Research thread: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/454
Earlier context: dictionary homework #10 (recursive forward hypernyming and reverse occurrence-matching/presentiation); OpenDiagram experiment #450.

## User intent and assignment (do not silently narrow)
Echo should traverse **the full available dictionary**, preserving the words in **every definition entry**, including grammatical words, connecting every occurrence to its headword/sense and connecting words to one another through the definition as a shared evidential context. Echo can then discover and propose explicit, source-attributed semantic links. Existing concept networks should become addressable evidence-network components in higher-order networks. Neon is authoritative; OpenDiagram is the dictionary's interactive visual cover; the MCP dictionary is the discoverable lexical source. No arbitrary vocabulary fixture, 22-item cap, preset dictionary subset, diagram count or fixed upper order of network composition.

## Four interfaces
1. Neon Evidence Board <-> OpenDiagram: a versioned graph snapshot renders the source graph; explicitly submitted *semantic* UI edits become proposals, while rearrangement is only layout.
2. MCP Dictionary <-> OpenDiagram: source-grounded WordNet sense/definition/hypernym records are navigable as diagrams; **renderer must not invent relations**.
3. Neon Evidence Board <-> Neon Catalog Box: evidence nodes/edges reference exact immutable catalog card revisions and provenance.
4. Neon Catalog Box <-> Dictionary Evidence: record original dictionary, synset identity, source digest, definition, symbol occurrences and sense-ambiguity status.

## Levels and identities
- Word surface/occurrence: `occ:{source-synset}:{position}`; includes articles/prepositions/conjunctions.
- Lexeme key: `word:{normalized-orthography}`; shared *spelling*, NOT inherently one meaning.
- Sense identity: `wn:{synset.name()}` and source vocabulary/version; stable for the pinned WordNet release.
- Definition record: `def:wn:{synset.name()}`; preserves exact original gloss.
- Contextual graph: versioned set of linked lexical senses, definitions and evidence, not automatically a proof.
- Recursive graph-as-node: an addressable snapshot with stable graph ID, revision, membership and explicit typed inter-network links. Source chains remain dereferenceable.
- Existing homework #10 distinguishes raw symbolic occurrence, a lexical index route, and *optional* semantic presentiation. Pattern equality alone must not confer sense identity.

## Relation types and epistemic states
**Definition occurrence** is always grounded as `definition_contains_occurrence` (and an inverse `occurs_in_definition`), including headword/sense->definition->occurrence->lexeme. This links all words to the entry through shared context **without creating O(n²) guessed pairwise facts**.
**Source-native sense relations:** hypernym/is_a, instance_hypernym/instance_of, part_meronym/has_part, part_holonym/part_of, member and substance meronym/holonym, other WordNet-native edges only when explicitly sourced and named.
**Candidate grammatical cues:** `of`, `with`, `in`, `for`, `through`, `between`, articles/conjunctions. They are indexed first as occurrences. They may cue a *proposal* but do **not** entail `part_of`, `is_a`, `causes`, etc without independent disambiguation.
States: observed source occurrence; source-native semantic edge; proposed interpretation; contested; reviewed; rejected. Preserve both underlying source and reviewer state.

## Discoverable MCP tools (proposed, not deployed)
- `dictionary.sense.resolve`: lexical surface->candidate synsets and source references, no blind first-sense selection.
- `dictionary.definition.occurrences`: all token occurrences and positions for a selected synset.
- `dictionary.hypernym.trace`: cited WordNet hypernym paths.
- `context.relations.propose`: validate explicit source evidence, store provisional proposals only.
- `context.network.compose`: create versioned graph-as-node reference with membership and evidence.
- `evidence.network.commit_proposal`: idempotently commit a sourced proposal via authenticated restricted Neon service; no arbitrary SQL or status promotion.
- `diagram.network.open`: render a committed revision without adding semantic assertions.
- `diagram.network.propose_edit`: emit typed proposed semantic changes separately from canvas layout.

Each MCP tool needs concrete JSON schema, trusted actor binding and audited result; registration does not itself provide autonomy or model capabilities.

## First execution phase
An Echo-repository dictionary indexer will stream source-only WordNet definitions/occurrences and native WordNet semantic edges to compressed, reproducible evidence files with SHA-256 manifest. This is **source reconstruction**, not proof that Echo's entire Governor/3³ has inferred relations or that Neon was written. No `producer:echo_algorithm` attribution on deterministic indexer output.
Future integration: source-batch ingestion into an isolated Neon schema with transaction IDs/idempotency and graph revision checks; then a Vercel authenticated MCP service + OpenDiagram visual projection. Do not claim these exist before verified.

## Success evidence
Reconcile full dictionary enumeration, token counts, stable IDs, function-word preservation, referenced native edges, artifact availability, and execution provenance; then independently score semantic discovery against held-out source-grounded tasks.
Follow pre-test, run and post-test protocol in issue #454. Each future brainstorm appends a dated addendum; never overwrite an earlier proposal as though it had always been established.
