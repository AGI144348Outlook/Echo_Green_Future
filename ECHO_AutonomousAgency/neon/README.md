# Echo — dictionary + Neon Index Card Catalog + Evidence Card Network

**Development status (2026-11-12):** two additive schemas deployed in an isolated Neon development branch; dictionary view connected to the existing WordNet table; **22 pinned lexical cards**, **73 nodes**, **124 candidate lexical-path edges**; algorithmic comparative experiment and MCP application-handler tests passed. This is **not** a deployed MCP listener or a demonstration of independently learned language.

## Exactly three systems

1. **Dictionary** — already present as \`genesis.wordnet_chain\` and \`core_lexicon.*\` in existing Neon project \`lexicon-catalog\`. The new **read-only view** \`echo_dictionary.wordnet_context\` preserves the existing source of lexical entries and sense/chain records. Echo's separate \`EchoDictionary.require_lobby\` admission constraint remains binding; a dictionary tool may not read a word the trusted runtime has not admitted.
2. **Revisioned Index Card Catalog** — additive \`card_protocol.*\` tables using stable \`card_id\`, exact revision and inert typed context, compatible in concept with the [Dual Order OS CatalogBox](https://github.com/AGI144348Outlook/dual-order-os/tree/feature/contextual-card-protocols).
3. **Evidence Card Network** — additive \`evidence_net.*\` graph tables tracking sourced lexical paths, provisional associations and distinct assertion/review states. Neither \`lexical_path\` nor mere shared universal ancestry establishes a factual proposition.

**Database:** existing Neon project \`lexicon-catalog\`. **Child branch:** \`echo-card-evidence-dictionary-dev-20261112\`. Original \`genesis\`, \`core_lexicon\`, legacy \`public.card\` and production Echo state untouched. This branch is separated from NexusBoard.

## Repository implementations

- [Additive two-system Neon schema](001_card_evidence.sql)
- [Echo-only read-only dictionary bridge](002_dictionary_bridge.sql)
- [Eight MCP tool contracts](card_evidence_dictionary_mcp_tools.json)
- [Scope-bound application RPC](card_evidence_rpc.mjs)
- [Parameterized Neon data adapter](neon_pg_adapter.mjs)
- [Offline protocol tests](test_rpc.mjs)
- [Algorithmic comparison 015](../src/card_evidence_dictionary_015.py)
- [Comparison unit tests](../tests/test_card_evidence_dictionary_015.py)

The six shared tools are \`catalog.card.get\`, \`catalog.configuration.resolve\`, \`catalog.card.propose\`, \`evidence.node.get\`, \`evidence.edge.trace\`, and \`evidence.edge.propose\`. Echo adds two **read-only** operations: \`dictionary.lexical_path\` and \`dictionary.network.compare\`. They are **not** in NexusBoard. The two new tools must check trusted Lobby admissions before use, and cannot directly expand vocabulary or promote knowledge.

## MCP routing and preserving Agent individuality

\`\`\`text
Echo authenticated Agent / school-day governor
       |
       | mission, bounded vocabulary, authorized tool subset
       v
Echo-only MCP function (deployment pending, no public endpoint)
       |
       +--- read-only dictionary bridge: admitted words / senses
       +--- versioned card catalog: exact context references
       +--- lexical evidence network: source-backed relation paths
       |
       v
Candidate relations / explanations / questions
       |
       v
Existing Homework/Classroom validation and knowledge governance
        (no auto-admission, no self-promoted truth)
\`\`\`

The repo contains an **application-level RPC handler**, not a Streamable HTTP server. To expose it, a future trusted gateway or Neon Function must authenticate the operator and Echo Agent, bind mission context and admitted vocabulary, check per-callee authorization, validate MCP 2026-07-28 headers/metadata and Origin, and connect the parameterized Postgres adapter to a **least privileged role**. No live endpoint, no private signing secret and no production role policy exist yet.

**No dictionary integration into NexusBoard.** A common protocol-card vocabulary does not require exposing Echo's semantic graph or lexicon to corporate offices.

## Experiment 015 — exactly what improved, and what did not

[GitHub Actions comparison](https://github.com/AGI144348Outlook/Echo_Green_Future/actions/runs/43170950499) used frozen \`matrices/echo_wordnet_chains.json\` with the **same 22 source words** in both arms:

- **Baseline:** A-165-style shared hypernym detection, including universal \`entity\` root.
- **Treatment:** same dictionary + pinned CatalogBox context + proposed evidence-path witnesses, with documented common-ancestor specificity filtering.
- **14 pairs:** baseline reported **13 associations**; treatment returned **6 provisional supported** relations and **8 abstentions**. All six supported relations included pinned source references and path witnesses.
- **33 new lexical terms** were recognizable as *candidates* in existing chains, but **0 words** were actually admitted to Echo's Lobby. The experiment evaluated *traceability and selectivity*, not learned vocabulary growth or correctness against independent semantic ground truth.

These measures are **not** a precision estimate: the evidence graph was constructed from the same WordNet chain data used by the baseline; a stricter treatment necessarily reports fewer associations. Independent adjudication and prospective admission/classroom tests are required before claiming substantive language improvement.

## Research and privacy safeguards

The original \`autonomous-agency\` branch remains intact. Development is on \`feature/autonomous-agency-card-evidence\` descended from it. The original dictionary's source access gate and experimental status are preserved. Do not infer truth from a graph edge, a high confidence metric or a model-generated authority stamp.

- [Pre-test/research Issue #435](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/435)
- [Algorithmic comparison CI](https://github.com/AGI144348Outlook/Echo_Green_Future/actions/runs/43170950499): **7/7 unit tests**, 14-pair comparison.
- [MCP contract CI](https://github.com/AGI144348Outlook/Echo_Green_Future/actions/runs/43171846641): **8/8 unit tests**.
- Neon development branch: two new isolated schemas, **8 RLS-enabled tables**, read-only dictionary view and provisional source-linked graph.
