---
name: echo-contextual-dictionary-networking
description: Use for Echo's WordNet definition-occurrence evidence networking, hypernymic/grammatical relationship discovery, recursive graph composition, Neon catalog persistence, OpenDiagram synchronization, and living brainstorm documentation.
---

# Echo contextual dictionary networking — ECHNP-001

Canonical living spec: `docs/protocols/ECHNP-001/README.md`
Chronological brainstorm ledger: `docs/protocols/ECHNP-001/BRAINSTORM-LOG.md`
Experimental / deliberation thread: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/454

## When invoked
1. Read the canonical spec and **latest** ledger and issue discussion before continuing.
2. Maintain three separate categories: **Timothy's proposals**, implemented code/contracts and **measured observations**. Add dated, append-only brainstorm notes during discussion. Do not mutate code/main just because brainstorming occurs.
3. Preserve *all available WordNet definition occurrences*, including prepositions, articles and conjunctions. Identify source synset, headword lemmas, exact definition, occurrence order and original lexical token. Never silently turn a shared definition occurrence into `is_a` / `part_of` / `causes`.
4. Treat WordNet-specific synset relations and raw definition co-occurrence as different evidence types; repeated spellings may represent different senses. Trace original source and revisions. A graph-of-graphs references pinned subgraph versions; it does not transfer truth status automatically.
5. Provide discoverable MCP contracts with clear read/propose/commit/render privileges. Echo picks operations based on context; no canned answers, unintended LLM filling, arbitrary vocabulary cap or fake `producer:echo_algorithm` signatures.
6. Before running **any** GitHub repository tests, experiments or CI, publish a pre-test GitHub Issue/Discussion with Timothy's discussion, problem, hypothesis, method, expected results and falsifiers. After execution, post observed results, limitations, evidence links and next steps **in the same thread**. No private source contents in public issues.
7. For Neon writes, use a development branch and source-pinned, idempotent, permission-scoped operations; keep authoritative evidence and catalog revisions separate from OpenDiagram's non-semantic layout. Do not claim live Neon sync or full Echo Governor operation unless verified.
8. Track full-dictionary passes with resumable progress and reproducible source/manifest digests. Report what actually finished, including failures or incomplete runs. Avoid arbitrary sample/operation ceilings in the scientific objective.

## Tool outputs
- `dictionary.definition.occurrences`: source-only occurrence inventory
- `dictionary.hypernym.trace`: WordNet-native sense graph evidence
- `context.network.compose`: proposed versioned nested concept graph
- `evidence.network.commit_proposal`: authenticated, validated Neon evidence transaction
- `diagram.network.open`: OpenDiagram projection of committed evidence
All listed calls are **proposals** until implemented and advertised by a live MCP server.

## Status
This is a portable repository **skill package**. Committing it does not install it into ChatGPT's managed Skills list or itself implement an MCP server.
