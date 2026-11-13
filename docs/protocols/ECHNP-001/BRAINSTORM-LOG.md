# ECHNP-001 — Living brainstorming ledger
This is a chronologically appended record; the GitHub issue #454 is the discussion / experiment ledger. Distinguish **proposed**, **implemented**, **measured**, **unresolved**. Never retrospectively recast a hypothesis as proven.

## 2026-11-12 — Originating dialogue (PROPOSED)
- Timothy: Instead of only looking up words, Echo should connect *all words in a word's definition* to the dictionary headword, and also connect the definition contents as an evidentiary context. Every dictionary entry is a node of a growing network infrastructure. Dictionary contents and cross-definition connections should be in Neon; the OpenDiagram-powered dictionary cover reveals the living graph.
- Timothy: 'hypernyming' can serve as a discoverable category of lexical relationship operations. Proposed labels include `part_of`, `includes_a`, `is_a` etc. Related question: whether prepositional words can be operators. Answer discussed: `of`, `in`, `with`, etc are **signals of possible relations**, not unconditional proofs of a particular relation.
- Four requested bidirectional interfaces: Evidence Board↔OpenDiagram; MCP Dictionary↔OpenDiagram; Evidence Board↔Catalog Box; Catalog Box↔Dictionary Evidence.
- Contextual higher orders: lexical occurrences -> definition networks -> concept networks -> networks of networks, while retaining evidence pointers and polysemy distinctions.
- Timothy requested documented brainstorming *as it happens*, a reusable skill, and execution of the dictionary assignment.
- Existing historic homework #10 includes additional forward hypernym and reverse indexed-symbol/presentiation passes; preserve this, do not conflate raw occurrence matching with semantic identity.

## 2026-11-12 — Implementation decisions (IN PROGRESS)
- Register preregistration issue #454 **before** CI/test execution.
- Implement a source-only full WordNet indexing stage first to preserve *all* definition words. It must not invent semantic relations or claim to be full Echo cognition.
- GitHub feature branch only, main unchanged. A portable skill can be committed to the repository; the ChatGPT installed-skills list itself is currently read-only through available tools.
- Existing Neon developer view contains a small admitted word subset; do not call it a dictionary ceiling. Full source data may be materialized as CI artifacts before authenticated Neon ingestion.
- Existing ECHO-021 renderer accepts declared `echo_algorithm` producer; do not falsely put that attribution on source-indexer evidence.

## Unresolved (not decisions)
- Multi-meaning sense disambiguation policy for definition occurrences; initial records keep lexeme identity and source synset without unearned sense selection.
- Exact MCP transport / policy for authenticated Echo runtime and Vercel browser host, event idempotency, graph revision conflicts.
- How to expose higher-order graph-as-node object types without mutating the existing `evidence_net.nodes` enum; needs a schema migration under branch.
- The full dictionary ingestion into Neon, visual availability through OpenDiagram and assessment of independently *inferred* grammar/semantic relations are separate future milestones.
