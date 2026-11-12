# ECHO-017 — Independent Dictionary Reinforcement Study

**Purpose:** Let Echo explore his own already-admitted dictionary, revision-pinned index cards, and source-linked evidence network over time using an **algorithmic reinforcement policy**. This study is deliberately separate from NexusBoard.

**Pre-test plan:** [Issue #438](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/438).  
**Environment:** existing Neon project `lexicon-catalog`, isolated database branch `echo-card-evidence-dictionary-dev-20261112`.  
**Implementation:** [`003_echo_dictionary_rl_study.sql`](003_echo_dictionary_rl_study.sql), [exact four-tool MCP discoverability contract](echo017_restricted_mcp_tools.json), [scope tests](test_echo017_restricted_mcp.mjs).

## Precise allowed tool surface

1. `dictionary.lexical_path` — study a dictionary definition, sense, and ancestral meaning.
2. `catalog.card.get` — study an exact pinned revision of a lexical context card.
3. `evidence.edge.trace` — study supported existing lexical-path edges and provenance.
4. `evidence.edge.propose` — **propose**, never approve, a source-backed candidate lexical relation.

These are all within the **three authorized systems**, not four separate external providers: Dictionary, Card Catalog, and Evidence Network.

No search engines, browser, direct arbitrary SQL, authority stamps, tool-execution privileges, deployment, vocabulary admission, authorization changes, external models or NexusBoard interfaces are in the study allowlist. The tool descriptions are positive affordances (not conditional *“use it when…”* instructions).

**Transport distinction:** The study engine currently runs as a **private Neon PostgreSQL function** that takes actions corresponding to the four named MCP tools; it **does not invoke a deployed MCP HTTP endpoint**. A separate JSON-RPC application-level tool list enforces exactly four discoverable names when used through Echo's experimental MCP core. Do not claim production MCP interoperability.

## Reinforcement policy and learning boundaries

A-101-inspired upper-confidence-bound policy selects among the **four allowed study operations**. An A-105-inspired exponential moving average records recent intrinsic rewards. Both are preserved in `echo_study.policy_arms` and continue from previous sessions. The design is **not** direct execution of the full 9,529-line Governor or the separate 3³ neuroplasticity substrate.

This is **self-directed within a bounded, frozen corpus**, not a scripted task prompt per episode. The candidate pair generator systematically explores existing WordNet words; it does not invent new lexical claims or search for external knowledge. Reward is an **intrinsic proxy** for first-time source encounters, complete evidence-path reviews, and proposed candidate relationships backed by exact source cards. Unrelated/generic ancestors lead to abstention; repeated cards and links earn no novelty credit. A proposal never graduates to independently verified knowledge.

### Persistent records

| Neon table | Meaning |
|---|---|
| `echo_study.configuration` | Immutable four-tool allowlist, UCB exploration factor, EMA rate and per-session step cap |
| `echo_study.policy_arms` | Visits, cumulative reward and exponentially smoothed reward per action |
| `echo_study.progress` | Total steps and deterministic candidate-pair exploration cursor |
| `echo_study.observations` | First-time sourced dictionary/card/trace observations, to prevent false novelty reward |
| `echo_study.sessions` | Session start/finish, wall duration, rejected or newly proposed edges |
| `echo_study.episodes` | Every selected tool operation, source words, observed outcome, intrinsic reward and proof status |

The study invokes `SELECT echo_study.study_round(96)` per bounded session, under an authorized database owner in the **development branch only**. The function has no public SQL EXECUTE grants. Every run is brief in CPU time; repeated *hourly* invocations give distinct real-world study sessions, **not continuous hour-long CPU execution**.

### Source-derived network construction

For a candidate pair `word:A` and `word:B`, the engine requires both existing WordNet records, exact `lex:A@1` and `lex:B@1` source cards, and complete source-attributed lexical-path edges. It chooses a **discriminating common ancestor** or identical synset. An accepted candidate generates:

- one evidence card with two pinned dictionary-card references, source senses, discriminating ancestor, frequency and explicit `epistemic_state=provisional`;
- one proposed relationship from `word:A` to `word:B`, pointing at the new exact evidence card;
- two `edge_sources` links referencing original source-backed word nodes;
- an episode log with action, reward and evidence ID.

This is **an inferred lexical association**, not an independently verified statement about the world. Mere generic `entity` ancestry is explicitly insufficient.

## First controlled execution — actual observations

Two separate invocations of `SELECT echo_study.study_round(96)` completed on the Neon child branch.

- Session 1: **96 actions**, approximately **0.0421 seconds** server-side wall time; 19 pair attempts, 19 abstentions, 0 proposals.
- Session 2: **96 actions**, approximately **0.0225 seconds**; 25 additional pair attempts, 24 abstentions, **1 new source-backed provisional lexical association**.
- Cumulative: **192 study actions**, **44 distinct pair candidates examined**, one proposed link `being ↔ existence` (same WordNet synset `being.n.01`), **46 recorded first-time read observations**. Action-value counts and EMA state persisted between the two sessions.
- The proposed card is `echo017:card:being:existence@1`, referencing `lex:being@1` and `lex:existence@1`; related graph edge `echo017:wordpair:being:existence` is **proposed**, not reviewed or proven.
- No vocabulary admission, policy elevation, original dictionary mutation or production action occurred.

**Interpretation:** This demonstrates persistence, bounded UCB-style tool selection, and a source-linked proposal. It does **not** show improved semantic comprehension, semantic accuracy, sustained unattended execution, or meaningful new vocabulary. Many abstentions are expected when unrelated words share only generic roots.

## Intended follow-up

A limited **hourly study cadence** should invoke the same Neon child-branch procedure without clearing the policy. Each session's outcomes should be recorded in [Issue #438](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/438) as observations, not truth. Pause if there is a permission anomaly, repeated failure, a saturated 231-pair candidate space, or stagnation. Never promote proposed claims automatically.

Success requires independent measurements of *source-grounded relation quality, coverage, refusal correctness, retained selection policy and novelty* against a frozen non-learning control. An increased total-step counter is not evidence of independent understanding.
