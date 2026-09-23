# Research Grounding — Autonomous Agency Branch
## Mashet/LHEA Research

This document grounds the algorithms in this branch against published
research, confirming that the approaches taken are not arbitrary
engineering choices but reflect how language, cognition, and vocabulary
development actually work.

---

## 1. Spreading Activation → A-166 HourglassFlowAgent + Tie Economy

**Collins & Loftus (1975) — Spreading-activation theory of semantic processing**

The foundational model: semantic memory is a network of concept nodes connected by labeled relations. When a concept is processed, activation spreads outward along its associative links, decaying with distance. Concepts that share many links activate each other more strongly.

ECHO's tie economy is a deterministic symbolic implementation of this mechanism. When a new word enters the lobby through the hourglass neck, it activates its LHEA neighbors. The strength of each activation becomes a trade weight. The economy accumulates these weights as a persistent record of co-activation history. The richest agents — those with the most trades — are the most strongly connected in the activation network.

**Key parallel:** Collins & Loftus found that activation strength correlates with the number of shared features between concepts. ECHO's LHEA overlap measure (shared letter operators / max letter operators) is a structural analogue of shared-feature count, computed symbolically from phoneme decomposition rather than statistically from corpus co-occurrence.

---

## 2. Vocabulary Acquisition as Network Traversal → A-165 HypernymStreamComposer

**"Early Language Learning via Spreading Activation and Category Exploration in Complex Networks" (arXiv:2607.06258, 2026)**

This paper models early language learning as a search process on a graph-based mental lexicon driven by two interacting mechanisms: spreading activation (following strong associative links) and enforced exploration of lexical categories (ensuring diverse coverage).

Finding: spreading activation outperforms shortest-path baselines in simulating normative word acquisition order. Vocabulary development is understood through the interplay between activation dynamics and lexical category constraints.

ECHO's A-165 implements this: the hypernym chain IS the activation path through the WordNet graph, and A-166's flow rate IS the category constraint (not everything flows — the governor enforces coverage diversity through the affinity filter).

---

## 3. Developmental Stages → Full Pipeline Architecture

**Aitchinson (1987) — Three stages of early vocabulary development**

| Stage | Description | ECHO equivalent |
|-------|-------------|-----------------|
| Labelling | Linking words to things | A-115 DictionaryIndexer |
| Packaging | Exploring the label's range | A-116 ArticleClassifier + A-117 WordAgent orientation |
| Network Building | Making connections, recognising similarities | A-119 TypedStudyGroups + A-166 tie economy |
| Abstraction (stage 4 — implicit) | Generalizing from networks to templates | A-165 + VGM candidate generation |

The progression from Swadesh words → hypernym chains → VGM axioms maps exactly onto Labelling → Packaging → Network Building → Abstraction. The Swadesh 200 test in this branch traces this progression empirically.

---

## 4. Basic Level Words First → Swadesh Seed Approach

**Rosch et al. (1976) — Basic objects in natural categories**

People name and learn basic-level objects (dog, chair, apple) before superordinate (animal, furniture, fruit) or subordinate (poodle, armchair, Granny Smith) terms. Basic-level is most cognitively efficient — it maximizes information while minimizing cognitive effort.

**Nelson (1973) — Structure and strategy in learning to talk**

First 50 words analysis: 51% general nominals (names for classes), 13% action words, 9% modifiers. Specific nominals (unique names) are a minority. Children's first vocabulary is dominated by basic-level class names.

ECHO's Swadesh seed approach grounds the lobby in this finding. The 200 Swadesh concepts are the cross-linguistically stable basic-level vocabulary — what every language has, what every child learns first. The VGM axioms emerge from the hypernym chains of these words, as superordinate abstractions that only become visible after the basic level is populated.

---

## 5. Sub-Governor Architecture vs. Existing Multi-Agent Systems

**Current mainstream:** Hierarchical LLM multi-agent orchestration. A manager LLM delegates tasks to worker LLMs. Intelligence is centralized in the orchestrator.

**GRACE — Governor for Reason-Aligned ContainmEnt (2024)**

GRACE separates normative reasoning from instrumental optimization within AI systems. The Governor enforces normative constraints while the executing agent handles instrumental decisions.

ECHO's A-167 differs from both:

| Aspect | Mainstream multi-agent | GRACE | ECHO A-167 |
|--------|----------------------|-------|------------|
| Intelligence location | Centralized (manager) | Separated (normative/instrumental) | Distributed (cell division) |
| Sub-agent nature | Worker, delegates from manager | Constrained executor | Modular copy of master |
| Communication | Manager → worker | Normative governor → executor | Sub-governors ↔ Resh council only |
| Substrate | LLM-based | LLM-based | Symbolic, deterministic |
| Failure mode | Manager bottleneck | Normative rigidity | Sub-governor isolates — Resh unchanged |

ECHO's sub-governors are not workers delegated tasks. They are modular copies of Resh instantiated for specific domains. The intelligence is not delegated — it is replicated. Resh does not become less when a sub-governor is created. Resh does not change when a sub-governor is diminished.

---

## 6. The Hourglass as Temporal Constraint

**Zeno's paradox → A-166 flow rate**

The hourglass name is intentional. Like Zeno's paradox of continuous halving, the hourglass ensures the lobby never fills all at once — new vocabulary flows through a metered neck, one cycle at a time. This is the same principle behind A-165's `depth` parameter (don't traverse the full chain — stop at depth 4) and the Swadesh-first seeding (don't load all of WordNet — start with the 200 most fundamental words).

Controlled flow is not a limitation. It is how human vocabulary develops — not in bulk downloads but in daily encounters, one concept finding its neighbors at a time.

---

## 7. ECHO's Novel Contribution

The combination that does not exist in the published literature:

1. Symbolic (not statistical) implementation of spreading activation
2. Deterministic hypernym chains (from WordNet) as the activation paths
3. LHEA letter-operator substrate as the affinity metric (not word vectors)
4. Governor-metered flow (the neck) as the lexical category constraint
5. Self-reflection through the Mirror (ECHO extends itself by speaking)
6. Sub-governor cell division (not delegation) for practical domain agency

Each of these elements has precedent in the literature. The combination is original.
