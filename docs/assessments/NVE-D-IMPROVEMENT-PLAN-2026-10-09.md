# NVE-D Improvement Plan: from loop harness to configuration-testing environment

**Date:** 2026-10-09
**Author:** Claude, for Timothy Charles Marvin Jr.
**Follows:** [`NVE-D-DESIGN-ASSESSMENT-2026-10-08.md`](NVE-D-DESIGN-ASSESSMENT-2026-10-08.md)
**Draws on:**
- `code_library_registry/symbol_registries/` on branch `code-library-registry`: the plan of record, the Hebrew index and the rules snapshot;
- `code_library_registry/design_notes/neuroplasticity-candidate-algorithms.md` on the same branch;
- LHEA (`Latin Root Hebrew logic .pdf`);
- the rules in Cloudflare D1 `echo_knowledge`.

**Status:** Proposed. Nothing here is implemented, and nothing here changes a registry.

**Labels used throughout:**
- **Declared**: Timothy stated it.
- **Reading**: Claude's interpretation, not yet confirmed.
- **Proposed**: a design suggestion.
- **Depends on Nx**: waits on Timothy's answer to that question in the assessment.

Rule codes (R-…) refer to the registry in D1.

---

## 0. The short version

NVE-D is careful about the wrong thing. Cycles 001–020 have built:
- strong replay;
- snapshot discipline;
- in Cycles 014–020, witness-custody and tamper-evidence machinery.

All of it surrounds a 64-bit hash stepped through generations. No entity is ever arranged, so nothing the safeguards protect is a finding.

This plan gives NVE-D three things it lacks, all from material that already exists:

| Missing | Supplied by | Role in NVE-D |
|---|---|---|
| Something to arrange | The 96 symbols and the other symbol registries | **Entities**: the contents of a node |
| A principled way to move through possibilities | The neuroplasticity candidate algorithms | **Search**: how NVE-D goes from one configuration to the next, inside a hard budget |
| A way to judge a configuration | The Governor formula and the evaluation alphabet | **Judgment**: what is tested in each node and what counts as a finding |

Two further pieces of the symbol work supply the *moves* and the *map*:
- the Hebrew letters with their LHEA roots are the moves;
- the I-Ching determinatives are the map.

Your condensation rules (`[|]` / `[||]`) supply real nesting.

Everything GPT built for integrity stays. It finally gets something worth protecting.

---

## 1. Where NVE-D stands (through Cycle 020)

| Area | Current state | Verdict |
|---|---|---|
| Replay and snapshots | Checkpoint replay 270/270 `=`, oracle 15/15 `=` (Cycle 020) | Keep. It's solid. |
| Custody and tamper-evidence | Cycles 014–020 test witness streams, SQLite rewrites and mutable anchors | Keep, but pause expanding it. It protects a hash, not a finding. |
| Evaluation alphabet | `{<,>,=,0}`, used for evaluation only; `0` provisionally "absent / insufficient" | Keep. It lines up with your Governor relation set `{<,>,=,}` if `0` is the empty fourth member (R-GOV-6, Depends on N8). |
| Entities | None. Every "state" is a number. | **The core gap.** |
| Datastrate and dataset | Empty | **The core gap.** |
| Nesting | A repeated inner loop | Not nesting. |
| Your formula | Kept as an opaque string | Never evaluated. |
| Progress measure | Generations and transitions (1.5M, 11.2M) | Measures throughput, not testing. |

---

## 2. The changes

Each change below has the same parts:

- **What**: the change in one paragraph.
- **Instructions**: the steps, in order.
- **Data shape**: the records it produces.
- **Done when**: a check that can be run.
- **Solves**: which departures from the assessment it closes.
- **Achieves**: what becomes possible that wasn't before.

Changes 1–5 make up the minimum for the first real trial. Changes 6–9 build on top of them.

---

### Change 1: A node holds an arrangement of registered entities

**What.** An IETF node's snapshot becomes a set of entities taken from a registry, plus the relations between them. A relation is one value from the evaluation alphabet per ordered pair. This makes R-NEU-2 concrete (Proposed): *the 96 are fixed; their relations are plastic; a node holds one arrangement*. One unit of work becomes **one configuration tested**, not one generation stepped.

**Instructions.**
1. Choose the entity set from a registry. Use registry IDs only (R-MAT-1). For the first trial, use Layer I of the 96, which is MS-001 to MS-016 (R-LAY-1).
2. Define the relation alphabet. Use `{<,>,=,0}` as it stands, with `0` meaning "not compared / open" until Timothy confirms (N8).
3. A configuration is a map from each ordered pair (a, b), a ≠ b, to one relation.
   - 16 entities give 240 ordered pairs.
   - The full space for those 16 is 4²⁴⁰.
4. Give every configuration a canonical form and a content ID: the SHA-256 of its relations, sorted by pair. Two runs that reach the same arrangement get the same ID.
5. Store each node's snapshot as that configuration plus its provenance.

**Data shape.**
```json
{
  "config_id": "sha256:…",
  "entity_registry": "mashet-96@<registry commit>",
  "entities": ["MS-001", "…", "MS-016"],
  "alphabet": ["<", ">", "=", "0"],
  "relations": { "MS-001|MS-002": "<", "…": "…" },
  "parent_config_id": "sha256:… | null",
  "move": "ז SCINDERE(MS-003,MS-007) | null",
  "created_in_run": "NVE-D-021"
}
```

**Done when:**
- every node snapshot validates against this shape;
- every entity ID resolves in the registry;
- two independent builds of the same configuration produce the same `config_id`.

**Solves:**
- 1, IETF run as a simulation;
- 3, datastrate empty.

**Achieves.** NVE-D starts testing *things*. A result can now say which symbols stood in which relations. For the first time, a finding is about Mashet symbols rather than about the harness.

---

### Change 2: Fill the four strata from the registries

**What.** Each stratum gets a real occupant. This is the assessment's reading of the strata (Depends on N1, N2); if Timothy corrects it, only this table changes.

| Stratum | Occupant | Source |
|---|---|---|
| Dataset | Raw sources: the mayig IVS corpus, the Mashet 96 legend, Hebrew letters | Repos as they are |
| Datastrate | Registries (immutable IDs, add-only history; R-REG-1, R-REG-2) and the matrices derived from them (R-MAT-1 to R-MAT-3) | `code_library_registry/symbol_registries/` |
| Substrate | IETF nodes holding configurations (Change 1) | NVE-D |
| Suprastrate | The Governor formula as the judge (Change 5), with the seed and its expansion deciding what is generated | R-GOV-1, R-SEED-1 to R-SEED-3 |

Your declared link (R-STRATA-1): *the Suprastrate and Substrate connect at the IETF (0,0,0) and the Relational Formula's `|x|`, a harness wrapped around the Datastrate.* In this plan:
- (0,0,0) is the synthesis origin (Change 8);
- `|x|` is the slot where a child environment sits (Change 6).

**Instructions.**
1. Pin each trial to a registry commit, so its datastrate is fixed and named.
2. NVE-D reads the datastrate and never writes to it. New candidate symbols go to Registry −0 (R-SPEC-3), outside the trial.
3. Every result record names all four layers: dataset source, registry commit, node `config_id`, and the judge version.

**Done when:** any result can be traced, by IDs alone, down to a source record and up to the formula version that judged it.

**Solves:** 3; it also sets up 11.

**Achieves:**
- NVE-D connects to the Dataset → Registry work you are all doing now, instead of running beside it.
- When a registry improves, NVE-D's material improves automatically.
- The strata stop being labels and become a traceable chain.

---

### Change 3: Measure coverage, not generations

**What.** Replace generation and transition counts with three numbers:
- **distinct configurations tested**;
- **coverage**: the share of a *declared* sub-space that has been tested;
- **findings that survive replay** (Change 5).

**Instructions.**
1. Before a run, declare the sub-space. For example: "all configurations of Layer I where only pairs within one determinative category may be non-`0`." The full 4⁹¹²⁰ space for the 96 is your Infinite Expanse. It is never the denominator.
2. Keep a tested-set of `config_id`s across runs. This is the E2 tombstone list from the neuroplasticity notes, used as an index rather than a deletion log.
3. Report: tested / declared size, plus how the tested set is spread (Change 7 gives the distance measure).
4. Keep reporting the existing integrity results next to these numbers. Keep generation counts too, under a "throughput" heading.

**Done when:** a run report's headline is "N configurations tested, X% of declared space S, K findings replicated", and N can be recomputed from the tested-set file.

**Solves:** 2, the wrong measure of progress.

**Achieves:**
- You can say how much of a possibility space has been examined, which is the IETF's purpose in your codex.
- Re-testing the same configuration under a new cycle number becomes visible and avoidable.
- Two cycles become comparable on what they explored, not how long they ran.

---

### Change 4: Search with the neuroplasticity algorithms

**What.** The move from one configuration to the next is governed by the candidate algorithms, not by fixed string operations. The suggested first prototype set from the notes already forms a working loop:

| Notes ID | Mechanism | Job in NVE-D |
|---|---|---|
| A1-c | Resource envelope | The "skull" (R-ROLE-13): hard caps on configurations per run, memory, compute and wall time. This is the Infinitely Expanding process growing *inside* a finite limit. |
| A2-a | Activation cap | Only k entities may change relations per move, which keeps steps sparse and attributable. |
| B1-b | Traversal counters → priority | Relations that keep appearing in surviving findings get tried more often. |
| B2-a | Hot-path promotion | Move sequences that keep paying off become cheaper to reuse. |
| D1-c | Explore / exploit ratio | Balances new regions against refining good ones, measured with Change 7's distance. |
| D2-a | Candidate lifecycle | Each configuration moves through: proposed → tested → replicated or dormant. |
| D3-a | Weakening with salvage | Failed configurations keep their useful parts as hints. |
| E1-a | Dormant forgetting | Old regions go dormant, not deleted; they can be woken. |
| E2-a | Discard with anti-repetition | Tombstones = the tested-set (Change 3). No configuration is tested twice by accident. |
| C1-a, C2-a | Homeodynamic return; anti-capture | Wrap the scheduler: return to the seed on a time limit, and stop one track monopolising the search. |
| F1-a, G1-a | Tagging; rest cycle | During a run, tag maybe-useful results cheaply; consolidate them in the rest phase (Change 8). |

**Instructions.**
1. Implement the shared model from the notes (Node, Link, Budget, Clock) once. Every mechanism above reads and writes it.
2. Map it onto NVE-D:
   - Node = a configuration;
   - Link = a move between configurations, with `w`, `H`, `wins`, `losses`;
   - Budget = A1;
   - tick = one configuration tested;
   - rest = consolidation.
3. Every numeric setting is a starting guess (as the notes say). Record each one in the run manifest.
4. Run each mechanism as an arm against a **random-move baseline** with the same budget, so its effect is measured, not assumed. This keeps the honest comparison habit from NVE-D-004.

**Done when:**
- a run can be replayed exactly from its manifest and seed;
- each mechanism's effect is reported as an evaluation token against the random baseline (`<`, `>`, `=` or `0`) on a named metric, such as replicated findings per 1,000 configurations.

**Solves:**
- 10, the two infinities: the Expanse is the space, the expanding process is A1-bounded growth;
- part of 2.

**Achieves:**
- The plasticity notes get their first real test bed. Each algorithm is tried on Mashet material, not on a synthetic curve.
- NVE-D gains a direction: it learns where findings tend to be and spends its budget there.
- Your neuron analogy becomes something that can be observed. The 96 stay fixed, while the network of relations reshapes itself under a hard limit.

---

### Change 5: The Hebrew letters are the moves; the Governor formula is the judge

#### 5a. Moves: typed by LHEA

**What.** R-ROLE-2 declares Hebrew ≈ verbs. Each move that changes a configuration is a Hebrew letter, carrying its LHEA Latin root. A move is then named, typed and explainable, for example: "ז SCINDERE split cluster {MS-003, MS-007}".

A first set of 8, chosen because their roots act directly on relations:

| Letter | Root | Move on a configuration |
|---|---|---|
| ו | JUNGERE | Join: set a pair from `0` to a relation, linking two entities |
| ז | SCINDERE | Split: set a pair back to `0`, separating two entities |
| ט | VERTERE | Turn: swap `<` and `>` on a pair |
| ס | STARE | Fix: protect a relation from change for n moves (the notes' `protect`) |
| מ | FLUERE | Flow: copy a relation along a chain a→b→c |
| ק | MUTARE | Transform: change a relation to a different non-`0` value |
| ת | FINIS | Close: freeze the node; no further moves |
| י | RADIX | Seed: start a new region from a single relation |

These mappings are **Proposed**. The roots are LHEA's; applying them to configuration moves is Claude's reading.

LHEA's exclusive locks (LL1–LL5) become **forbidden move pairs** within one step, wherever both sides of a lock are moves. Most locks involve roots outside this first set of 8 (LL4, for example, is JUNGERE × SOLVERE). So the set gets one lock of the same kind (Proposed): ו (join) and ז (split) may not both act on the same pair in one step.

#### 5b. Judgment: the Governor formula, evaluated

**What.** The formula stops being an opaque string:

```
[_{(?):(?)}::{(?):(?)}_]א_|ת→א|י|::|י|א←ת|_א[_{(?):(?)}::{(?):(?)}_]
```

Reading (Depends on N7, N8):
- each `(?)` is an entity ID;
- each `(?±?)` with `± ∈ {<,>,=,}` is one relation in the node's configuration;
- each braced group `{(?):(?)}::{(?):(?)}` is a proportion test: *does A relate to B as C relates to D in this configuration?*;
- the two outer frames are two proportion tests;
- the kernel is the (0,0,0) where their results meet (Change 8).

**Instructions.**
1. Write the judge as a pure function: `judge(configuration, bindings) → token ∈ {<,>,=,0}` plus evidence. `bindings` assigns entity IDs to the `(?)` slots.
2. Under the proportion reading:
   - `=` means the proportion holds;
   - `0` means one of its relations is open;
   - `<` and `>` record which side is "stronger" under a declared ordering.
3. **Run competing readings.** Where Timothy hasn't confirmed a reading, implement each candidate as its own judge, run all of them, and promote none (R-ROLE-16). Readings to start with:
   - J-A, the proportion reading above;
   - J-B, the four relations read independently, with no proportion;
   - J-C, Timothy's own reading once given.
4. **A finding** (first answer to N10, Proposed):
   - a set of bindings where a judge returns `=` for a proportion;
   - that is reproduced by an independent replay;
   - and that still holds after one random neutral move elsewhere in the configuration.
5. LHEA's composite credentials (LC1–LC12) act as detectors. When the moves applied in a path cover both jurisdictions of a composite, tag the result. For example, J23 Tension + J21 Threshold = LC9 Paradox. A composite that recurs across replications is a stronger finding.

**Done when:**
- the formula string is parsed by the judge and round-trips byte for byte (R-BD-1: typed order kept);
- every result carries a judge ID;
- J-A and J-B give their own results on the same configurations.

**Solves:**
- 6, formula never evaluated;
- 7, alphabet narrowed (one alphabet, defined before use);
- 11, nothing judged is a discovery.

**Achieves:**
- Your formula is tested for the first time, and you can see how each reading behaves on real configurations before deciding what it means.
- Moves are explainable in your own vocabulary. A finding's path reads as a short Hebrew sentence, such as "ו then ט then ת", which is what "Hebrew ≈ verbs" should allow.
- LHEA's jurisdictions, locks and composites get an empirical test bed alongside the consent-paradox benchmark.

---

### Change 6: Real nesting, built from your condensation rules

**What.** A nested level is a full child environment, with its own clock, kernel, budget share and tested-set. It is built with your declared condensation rules:
- a cluster of entities is condensed to one symbol `[|]` (R-CON-1);
- that symbol is opened as a child environment `[||]`, where the cluster is arranged in more detail.

The parent sees the child only through the `|x|` slot (Reading, Depends on N6). The child is the parent's own form, once more, inside the slot.

**Instructions.**
1. Condense: when a set of entities keeps appearing together in findings, form a concept token (notes F2-c, `{A,B,C} → X`). X takes part in the parent configuration as a single entity.
2. Expand: open X as a child node whose entities are A, B and C. The child runs its own search under a share of the parent's A1 budget.
3. Relay: the child's replicated findings return to the parent as relations on X (notes F6-a, recursive consolidation).
4. Fade: when the child is no longer used, it goes dormant (E1-a). It is not deleted.
5. Depth cap: 4–5 layers, per your Temporary Domains codex.

**Done when:**
- a child has its own run ID, clock and tested-set;
- its findings appear in the parent as relations on its token;
- depth never exceeds the cap.

**Solves:**
- 4, nesting faked;
- 5, kernel binding reduced to identity.

**Achieves:**
- Large symbol sets become workable. Instead of testing 96 entities at once, NVE-D condenses stable groups and tests them at the right level.
- Your `[|]` / `[||]` notation becomes an operational rule.
- The 4–5 layer limit, the relay upward and the fading layers from your codex all get a mechanism.

---

### Change 7: The I-Ching determinatives as a map of the search

**What.** Each node is tagged with a determinative category, a trigram or hexagram (R-DET-1 to R-DET-5, Proposed). The category is silent: it describes the node and is not a relation inside it. Your `∆`, one line flipped, is a one-step neighbour in category space.

**Instructions.**
1. Pick the scale (open question): 8 trigrams for a first trial, or 64 hexagrams.
2. Give the categories meaning by a declared rule, not by traditional associations, unless Timothy declares them (R-DET-5). A neutral starting rule: each of the six lines is one measured property of the configuration. For example: line 1 = more than half its pairs are non-`0`; line 2 = it contains a closed (ת) region; and so on, all declared in the manifest.
3. Use Hamming distance between hexagrams as the spread measure for Change 3 and the explore/exploit balance for Change 4 (D1).

**Done when:** every node has a category computed from its configuration by a declared rule, and every run report includes how categories were covered.

**Solves:** gives Changes 3 and 4 a real distance; supports 2.

**Achieves:**
- The I-Ching role you declared (R-ROLE-7, ordering `{∆}` and syntaxing `{¥}`) becomes a working ordering of the search space.
- "Where has NVE-D looked?" gets a 64-cell answer you can read at a glance.
- It also tests the determinative idea itself: if the categories don't separate findings from non-findings, that's useful to know early.

---

### Change 8: Synthesis at the (0,0,0)

**What.** Results stop living in separate trial reports. After each rest cycle (G1-a), replicated findings are merged at the origin. In your codices, nodes are superposed into the (0,0,0) singularity. In the Governor formula, that is the kernel `]א_|ת→א|י|::|י|א←ת|_א[` (R-GOV-1).

**Instructions.**
1. Keep a meta-knowledge table, add-only, with one row per replicated finding. Each row holds: bindings, judge ID, config IDs, the move path, any composites detected, and the replay evidence.
2. The merge rule is C4 heterodynamics (integrated synthesis). Two findings that agree across judges or across nesting levels are combined and ranked higher. Disagreements are kept side by side, not resolved by majority.
3. Nothing in this table is promoted to a registry automatically. Only Timothy promotes (the project rule for REGISTERED).

**Done when:** a single table lists every replicated finding across all runs, each traceable to its configurations and replay evidence.

**Solves:** 8, no synthesis step.

**Achieves:**
- NVE-D accumulates knowledge across cycles instead of restarting each hour.
- It also produces the material the Codices end of the Dataset → Codices pipeline needs: findings with provenance, ready for you to review.

---

### Change 9: Time comes second; integrity stays

**What.** Use the Chronotool in the order your codex gives.

**Instructions.**
1. **Frozen first.** Early trials are static configuration tests: no time evolution, every configuration judged as it stands (N9).
2. Add time modes per node only when a test needs them, all from your Chronotool codex:
   - accelerated;
   - slowed;
   - reversible (replay);
   - global sync.
3. Keep every integrity mechanism from Cycles 001–020: snapshots, digests, replay, the witness stream, no automatic promotion. Add three:
   - **A real second evaluator.** An independent implementation of the judge, written separately, not the same math rewritten. Its token must agree with the first judge's, or the result is `0`.
   - **Checksummed checkpoints.** Each one stores the SHA-256 of its configuration and tested-set.
   - **Every runner committed.** No result without the exact code that produced it in the repo. Hourly 002–003 couldn't be rerun for this reason.
4. Pause new custody work (witness administration and so on) until findings exist. Then point it at the meta-knowledge table, which is what's worth protecting.

**Done when:** every result in the meta-knowledge table has two agreeing judges, a checksummed checkpoint and a committed runner.

**Solves:** 9, Chronotool reduced to budgets; and the rerun gaps found in the assessment.

**Achieves:** the integrity work GPT built (it's good work) is aimed at findings rather than at a hash. The custody question in Cycles 014–020 ("can history be trusted?") becomes worth answering, because the history now holds results.

---

## 3. The first real trial: NVE-D-021, specification

Small enough to check by hand. Uses only registered material.

| Setting | Value |
|---|---|
| Entities | Layer I of the 96: MS-001 to MS-016, pinned to a registry commit |
| Relations | `{<,>,=,0}`; `0` = open (provisional) |
| Space | 240 ordered pairs; declared sub-space: start from all-`0`, at most 24 non-`0` pairs |
| Time | Frozen |
| Moves | The 8 Hebrew moves in 5a; LL1–LL5 as forbidden pairs |
| Search arms | (1) random moves, (2) A1+A2+D2+E2, (3) arm 2 + B1+B2+D1, all with the same budget |
| Budget (A1) | e.g. 20,000 configurations per arm, fixed seed, recorded in the manifest |
| Judges | J-A (proportion) and J-B (independent relations), plus an independently written second evaluator for each |
| Bindings | All ordered 4-tuples (A,B,C,D) of distinct entities that are non-`0` in the configuration, capped per configuration |
| Finding | Judge `=`, reproduced on replay, holds after one neutral move elsewhere |
| Determinatives | 8 trigrams from three declared properties |
| Report | Configurations tested, coverage of the declared sub-space, findings per 1,000 configurations per arm, trigram coverage, composites detected, all integrity checks |

**What it would show.** Whether plasticity-driven search finds more replicated proportions than random search on the same budget; how the two readings of your formula behave; and whether trigram categories separate findings from non-findings. Each answer is useful whichever way it comes out.

---

## 4. Order of work

| Step | Work | Needs |
|---|---|---|
| 1 | Configuration schema, canonical IDs and the tested-set (Changes 1, 3) | Nothing new |
| 2 | Judge J-B, the simplest, plus its independent twin (5b) | Nothing new |
| 3 | The 8 Hebrew moves and the locks (5a) | Nothing new |
| 4 | Random arm, then plasticity arms (Change 4) | Steps 1–3 |
| 5 | J-A, the proportion reading | Better with N7 |
| 6 | Trigram map (Change 7) | Declared properties; better with the 8-vs-64 answer |
| 7 | Run NVE-D-021, report | Steps 1–6 |
| 8 | Meta-knowledge table and rest-cycle synthesis (Change 8) | Step 7 findings |
| 9 | Nesting (Change 6) | Step 8; N6 |
| 10 | Time modes (Change 9) | A test that needs them |

Steps 1–4 can start now. Each later step names the question it waits on.

---

## 5. What this solves, and what it achieves

### Solves

All twelve departures listed in the assessment:

| # | Departure | Closed by |
|---|---|---|
| 1 | IETF run as a simulation | Change 1 |
| 2 | Wrong measure of progress | Change 3 (with 7) |
| 3 | Datastrate and dataset empty | Changes 1, 2 |
| 4 | Nesting faked | Change 6 |
| 5 | Kernel binding reduced to identity | Change 6 |
| 6 | Formula never evaluated | Change 5b |
| 7 | Alphabet narrowed | Change 5b |
| 8 | No synthesis step | Change 8 |
| 9 | Chronotool reduced to budgets | Change 9 |
| 10 | Two infinities merged | Change 4 (A1 envelope vs declared space) |
| 11 | Nothing judged is a discovery | Change 5b |
| 12 | Only digital environments | Not closed here. The judge and schema are definition-first, so a conceptual environment (a document, a definition) can use the same records later (N11). |

### Achieves

These are expected outcomes, not proven ones. Each is testable by the trial above.

1. **NVE-D produces findings about your symbols.** It stops proving that the harness works and starts saying something about the 96: which relations, under which reading of your formula, reliably hold.
2. **The pieces of your framework start checking each other.** Five things developed separately now run in one place, so a weakness in one shows up in the others' results:
   - the registries;
   - the neuroplasticity mechanisms;
   - LHEA's Hebrew operators;
   - the Governor formula;
   - the I-Ching determinatives.
3. **Your notation becomes executable.** The following stop being only written forms and become things that run:
   - `[|]` and `[||]`;
   - `|x|`;
   - the (0,0,0);
   - `{<,>,=,}`;
   - the four-relation frames.
4. **Interpretation becomes empirical, without imposing meaning.** Competing readings run side by side and none is promoted. You see how each behaves before declaring what you meant. This is the answer to imposition that R-GEN-1 describes: meta-specification by keeping alternatives interchangeable.
5. **The same machinery reaches toward the undeciphered end.** Once it works on the 96, the pipeline is unchanged for IVS graphemes; only the declarations change (R-SPEC-2). Reading direction becomes two competing node families (R-IVS-1), not an assumption. This is the spectrum you declared in R-SPEC-1, from known languages to a script found on another planet.
6. **Search effort compounds.** The tested-set, hot paths and meta-knowledge table carry across cycles. Hour 40 builds on hour 39 instead of repeating it.
7. **GPT's integrity work pays off.** Replay, custody and witness checks protect findings with provenance, which is what the Codices stage needs as input.

### Limits, stated plainly

- Every mapping in Change 5 is a reading. The trial tests how the readings behave. It cannot confirm what you intended.
- Numbers in the plasticity notes are starting guesses. A mechanism that loses to random search on this task is a result, not a failure of the plan.
- The canonical 96 legend is still undeclared. Layer I is used because its range is fixed (R-LAY-1); entity meanings don't enter the trial.
- 4²⁴⁰ is far beyond exhaustive testing even for Layer I. Coverage is always of a declared sub-space.

---

## 6. Questions still open (from the assessment, plus new)

| # | Question | Blocks |
|---|---|---|
| N1, N2 | The four strata as read here; NVE-D's or EVE's? | Change 2 wording |
| N6 | `|x|` as a slot holding a same-form environment? | Change 6 |
| N7 | `:` and `::` as proportion? | J-A |
| N8 | Is `0` the empty fourth member of `{<,>,=,}`? | Alphabet definition |
| N9 | Frozen first? | Change 9 order |
| N10 | What counts as a discovery? (Proposed answer in 5b) | Finding definition |
| New-1 | Do the 8 Hebrew moves in 5a fit your reading of those letters? | 5a |
| New-2 | Determinatives: 8 or 64; declared properties or traditional associations? | Change 7 |
| New-3 | Should NVE-D's own findings ever be eligible for registry promotion, and by what review? | Change 8 |

---

*Prepared by Claude (Anthropic) from the sources listed at the top. Rule codes refer to Cloudflare D1 `echo_knowledge`; where this document and D1 differ, D1 wins.*
