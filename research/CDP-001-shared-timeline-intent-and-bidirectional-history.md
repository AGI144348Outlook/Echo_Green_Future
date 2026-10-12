# CDP-001 — Shared timeline, intent-first conversational archaeology

Status: user-directed design specification; no parser implementation authorized in this change. Date: 2026-10-12.

## Governing rules
1. All syntax trees (Dataset, Registry, Matrix, Index, Codex, Algorithm, Logic, and future trees) operate against **one shared timeline**. They cooperate to reconstruct it; none maintains a conflicting independent chronology.
2. After temporal reconstruction, **intent is the second organizing principle**. Timothy's stated intent has priority for interpreting his projects, but never substitutes for actual evidence. Other actors (Julian, Nexus, fictional characters, Claude, GPT) retain their own attributed intents; do not merge them.
3. History is reconstructed as a documentary with **story/plot, people and characters, settings/realms, projects, needs, interruptions, decisions, resumptions, outcomes**. Narrative presentation is a view over source-backed events, not permission to invent causal links.
4. Traverse the same event graph in both directions: **forward** from earliest evidence (origins → developments → present) and **backward** from the current state (current result → dependency → prior need → interruption or deferral → earlier origin).
5. A causal edge ('X led to Y') requires source evidence or an explicit inference flag and confidence. Chronological adjacency alone is not causation.
6. Maintain immutable source provenance, original timestamp/timezone, import timestamp, uncertain dates, message branches, speaker/actor attribution, contradictory testimony, and revision histories.
7. Distinguish real people, assistant identities, fictional characters, and in-world agents. Separate factual documentary events from fiction, roleplay, hypotheses, and generated narrative.

## Event schema (draft)
```json
{
  "event_id":"stable source-scoped identifier",
  "source_refs":[{"dataset_id":"...","conversation_id":"...","message_id":"...","offset":0}],
  "time":{"start":null,"end":null,"precision":"unknown","timezone":null,"confidence":0.0},
  "actors":[{"id":"Timothy","role":"proposer","kind":"real-person"}],
  "intent":{"owner":"Timothy","goal":"...","type":"architecture|design|framework|business|worldbuilding|character|other","status":"proposed|approved|deferred|revised|tested|completed|unknown","evidence_refs":[]},
  "setting":{"project":null,"realm":null,"context":null},
  "content_types":["algorithm","decision"],
  "edges":[{"type":"depends_on|responds_to|revises|interrupts|resumes|motivated_by|caused_by","target":"event_id","basis":"explicit|inferred","confidence":0.0}],
  "classification":{"dataset_tree":[],"registry_tree":[],"matrix_tree":[],"index_tree":[],"codex_tree":[],"algorithm_tree":[],"logic_tree":[]},
  "interpretation_status":"candidate"
}
```

## Joint temporal inference procedure
- Ingest all raw sources losslessly, preserving conversation branches and edit/revision records.
- Extract explicit dates and temporal relations; build partial-order constraints without manufacturing missing times.
- Ask each syntax tree for evidence-bearing events and links; merge into one event graph, retaining disagreements.
- Attribute intent from user statements, explicit plans, choices, pauses, and changes; mark inferred motives separately.
- Identify project arcs, actors, settings/realms, conflicts, dependency chains, and outcomes.
- Generate forward documentary and backward why-chain views from the same graph; both must point to original messages.
- Test chronology conflicts, mistaken speaker attribution, fabricated causal claims, and story/fiction vs documentary confusion.

## Example backward question
'Why did we pause the automated story world?' → identify explicit pause event → cited blocking need → work started to satisfy that need → prior requirement → earliest available origin. If evidence stops, say 'unknown' instead of inventing a bridge.

## Acceptance criteria for first prototype
- Exact round-trip to source messages and branches; no source alteration.
- One timeline used by every syntax tree; consistent event IDs in forward/backward traversal.
- Timothy's intent clearly attributed and distinguished from assistant proposals.
- Tests with contradictory timestamps, unclear intent, paused/resumed project, fictional character intention, and cross-conversation dependency.
- Source-linked narrative output; unsupported inferences visibly labeled.

## Boundaries
This is a separate shared parser project, not an automatic import into Timothy's personal Lexicon. Do not write to main or ingest private exported conversations without his explicit direction.
