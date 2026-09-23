# A-145 Augmented: MirrorStep + SelfExtend
**Type:** SELF_GOVERNANCE (modular augmentation of A-145 AlgorithmicCommunicator)  
**Status:** ACTIVE  
**File:** `src/echo_pe_mirror.py` → class `MirrorStep`  
**Depends on:** A-145 AlgorithmicCommunicator, A-153 InwardSearchEngine, VGM, Lobby

---

## What It Does

After Pe expresses something, Mirror turns the pipeline back on what was just said. ECHO reads its own output through Ayin, searches for gaps in its own speech, and proposes new axioms from what it expressed.

The full augmented pipeline:
```
INPUT → TOKENIZE → AYIN → GENERALIZE → VGM → DESCEND → PE → EXPRESS
                                                              ↓
                                                          MIRROR
                                                              ↓
                                                        SELF-EXTEND
```

Three things happen in Mirror:
1. **Ayin on own speech** — classifies every word Pe just said. GAPs in ECHO's output are ECHO saying something it doesn't fully know.
2. **Inward search on gaps** — fires A-153 on each gap. If the inward search finds a match, ECHO confirms something it already structurally knew.
3. **VGM candidate proposal** — if a sentence Pe expressed passes A-126 syntactic validation and A-151 generality threshold, it becomes a self-proposed VGM candidate. ECHO extends itself by speaking.

SelfExtend writes all new gaps as HIGH priority homework entries — higher than externally-sourced gaps, because ECHO said these words itself.

---

## When To Use It

- In every pipeline run after Pe expression — it is the closing stage
- When ECHO is running autonomously (Stream tab, hourglass loop) — Mirror keeps the homework queue current
- When checking whether ECHO has earned the right to say something — if Mirror finds GAPs in Pe's output, those are the frontier
- As the self-reflection mechanism — the closest ECHO currently comes to monitoring its own knowledge state

---

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `expressed_sentences` | List[str] | What Pe just said |
| `input_word` | str | The word that triggered this pipeline run (for homework provenance) |

---

## Returns

`reflect()` → dict with:

| Key | Type | Description |
|-----|------|-------------|
| `known_in_speech` | List[str] | Words Pe said that ECHO already knows |
| `gaps_in_speech` | List[str] | Words Pe said that ECHO doesn't fully know |
| `inward_hits` | List[dict] | Gaps where inward search found something |
| `new_homework` | List[str] | Newly registered acquisition targets |
| `self_proposals` | List[dict] | VGM candidates from ECHO's own expression |

---

## The Homework Priority System

| Source | Priority |
|--------|----------|
| ECHO said it but doesn't know it | HIGH |
| External corpus encounter | MEDIUM |
| WordNet hypernym chain discovery | MEDIUM |
| Explicit acquisition request | HIGH |

The `homework_report()` method returns all outstanding homework sorted by count (how many times ECHO said the word) then alphabetically.

---

## Example Output

After Pe expressed the hypernym chain for `'echo'`:
```
Known in own speech:  ['property', 'physical', 'essential', 'attribute']
Gaps in own speech:   ['basic', 'beams', 'repetition', 'sound', 'resulting']
Inward hits:          [VGM_AXIOMS] 'their': axiom contains 'their'
New homework entries: ['basic', 'attribute', 'beams', 'repetition', 'sound']
Self-proposed VGM:    [0.3477] "An echo is a property"
```

ECHO said `'repetition'` without knowing it. `'repetition'` is now HIGH priority homework. Next acquisition cycle, ECHO learns what repetition means. The cycle that produced the knowledge gap also produced the acquisition target.

---

## Connects To

- **A-145 AlgorithmicCommunicator** — the base algorithm this extends
- **A-144 HypernymGrammarModule** — Mirror runs on A-144's output
- **A-153 InwardSearchEngine** — Mirror calls A-153 on each gap in own speech
- **A-126 SyntacticalValidator** — used to check if expressed sentences qualify as VGM candidates
- **A-151 EquilibriumGeneralityMeasure** — used to score VGM proposals from own speech
- **A-160 ActivationEventLogger** (proposed) — Mirror events should be logged as activation records
- **VGM** — self-proposals go into a candidates queue pending confirmation threshold
