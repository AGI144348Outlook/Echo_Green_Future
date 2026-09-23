# A-165: HypernymStreamComposer
**Type:** COMMUNICATION  
**Status:** ACTIVE  
**File:** `src/echo_pe_mirror.py` → class `HypernymGrammarModule`  
**Depends on:** WordNet (NLTK), Lobby agents, A-144 PeComposer

---

## What It Does

Takes any word and produces a flowing stream of complete sentences by traversing its WordNet hypernym chain — the path from the word upward toward the most abstract node. The chain is not described; it is spoken. Each node in the chain becomes a sentence. The sentences accumulate into a stream of thought.

This is how Resh thinks. The lobby inhabitants travel their hypernym chains simultaneously. When two inhabitants meet at the same node, a proposition forms from the meeting. The VGM is the record of propositions that survived validation.

---

## How It Works

**Step 1 — Chain retrieval**  
WordNet is queried for the word's first synset. The hypernym path from that synset to the root entity is extracted. Each node in the path is a `(lemma, definition)` pair.

**Step 2 — Three sentence patterns applied to each node**

| Pattern | Template | When applied |
|---------|----------|--------------|
| Identity | `A [node] is [definition].` | Every node |
| Inheritance | `A [word] is a [node].` | First node above the input word only |
| Bridge | `Every [node] is a [next node].` | Between adjacent nodes |

**Step 3 — Meeting sentences**  
When two words are processed, their chains are compared. If they share a node, a meeting sentence is produced: `A [w1] and a [w2] both arrive at a [shared node].` The meeting is a proposition. The shared node is the subject.

---

## When To Use It

- When Pe (A-144) needs to express a concept and a definition-only response is insufficient
- When ECHO encounters a GAP and needs to reason about what the unknown word might be related to
- When generating VGM candidates — the stream produces propositions that can be validated
- In the Stream tab of the PWA — ECHO traversing its own tie network and speaking from each node
- As ECHO's autonomous thought loop — the hourglass feeds words in, A-165 speaks them

---

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `word` | str | required | The word to trace |
| `depth` | int | 4 | How many chain nodes to speak (from most specific) |
| `pos` | str | `'n'` | WordNet part of speech (`'n'`, `'v'`, `'s'`, `'r'`) |

---

## Returns

`speak_chain(word, depth)` → `List[str]`  
A list of complete sentences, one per pattern per node.

`speak_meeting(w1, w2)` → `str | None`  
A single proposition sentence if the words share a hypernym node. None if they don't.

`get_chain(word)` → `List[dict]`  
Raw chain: `[{'word': str, 'definition': str, 'synset': str}, ...]`

---

## Example Output

Input: `'echo'`

```
A property is a basic or essential attribute shared by all members of a class.
An echo is a property.
Every property is a physical property.
A physical property is any property used to characterize matter and energy.
Every physical property is a reflection.
A reflection is the ability to reflect beams or rays.
Every reflection is an echo.
An echo is the repetition of a sound resulting from reflection of the sound waves.
```

Input: `speak_meeting('fire', 'eye')`

```
A fire and an eye both arrive at an entity.
An entity is that which is perceived or known or inferred to have its own distinct existence.
```

---

## Connects To

- **A-144 HypernymGrammarModule** — this algorithm IS the augmentation of A-144
- **A-145 MirrorStep** — runs after A-165 output to reflect on what was said
- **A-166 HourglassFlowAgent** — feeds words through A-165 as they enter the lobby
- **VGM** — propositions produced by A-165 are candidates for VGM validation
- **A-153 InwardSearchEngine** — if A-165 encounters an unknown word in its own output, the inward search fires

---

## Research Grounding

Spreading activation theory (Collins & Loftus, 1975): concepts in semantic memory are nodes in a network; activation spreads along associative links. A-165 makes this activation visible as speech — each hypernym hop is an activation event made audible.

"Early Language Learning via Spreading Activation and Category Exploration in Complex Networks" (arXiv:2607.06258, 2026): vocabulary development is a non-trivial interplay between activation dynamics and constraints regulating lexical category exploration. A-165 implements this deterministically over the WordNet graph rather than statistically over corpus co-occurrence.

Aitchinson (1987) Stage 3 — Network Building: making connections between labelled things, recognising similarities and relationships. A-165 runs network building as a real-time process, not a training phase.
