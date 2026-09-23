# A-166: HourglassFlowAgent
**Type:** ACQUISITION  
**Status:** ACTIVE  
**File:** `src/echo_hourglass.py` → class `HourglassGovernor` + `TieEconomy`  
**Depends on:** LHEA phoneme decomposition, Lobby agents, WordNet (optional)

---

## What It Does

The Governor runs in leisure mode — no query to answer, no task to complete. The hourglass turns on its own. New vocabulary flows from an external Dictionary source through the Governor's neck into the Lobby, where existing agents mingle with new arrivals. Ties form through LHEA letter affinity. The tie economy is self-organizing.

This is ECHO's autonomous acquisition loop. When left running, ECHO's lobby grows from encounters it chose, through a filter it applies, at a rate it controls.

---

## How It Works

**The three-chamber structure:**

```
┌─────────────────────────────────┐
│  DICTIONARY  (outside entity)   │  ← new vocabulary waiting
│  hypernym stream, corpus, API   │
└──────────────┬──────────────────┘
               │
           [ר GOVERNOR]               ← the neck
           LHEA affinity filter
               │
┌──────────────┴──────────────────┐
│  ECHO LOBBY  (inhabited world)  │  ← existing agents + new arrivals
└─────────────────────────────────┘
```

**The Governor's filter (the neck):**  
A word passes if its LHEA letter overlap with existing lobby agents falls in the Goldilocks zone:
- Too similar (`> max_affinity`) → already known, skip
- Too foreign (`< min_affinity`) → can't connect, skip
- In range → passes through, enters the lobby

This ensures only words that are *related but novel* enter. Words the lobby already knows by another name don't duplicate. Words from completely foreign domains don't force false connections.

**Tie economy:**  
Every new arrival finds its lobby neighbors by LHEA overlap and (optionally) WordNet similarity. Each meaningful overlap becomes a trade in the economy. The tie weight accumulates with each trade. The richest agents are the ones whose letter substrate connects to the most incoming vocabulary — not the ones with the best definitions.

---

## When To Use It

- As the hourly Cloudflare cron job — ECHO acquiring vocabulary while idle
- As the `run_homework()` loop — ECHO completing its own homework entries
- During sandboxed vocabulary development experiments (see: Swadesh 200 test)
- Any time a new corpus or API stream is available as a Dictionary source
- When a sub-governor needs to populate its domain lobby from an external source

---

## Parameters

**HourglassGovernor:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `existing_lobby_words` | set | required | Current lobby agent names |
| `flow_rate` | int | 6 | Max words per cycle through the neck |
| `min_affinity` | float | 0.05 | Minimum LHEA overlap to pass |
| `max_affinity` | float | 0.90 | Maximum LHEA overlap (already known) |

**TieEconomy:**  
No parameters. Initializes empty. Accumulates through `trade(w1, w2, strength)` calls.

---

## Key Methods

`fill_dictionary(entries)` — load entries into the top chamber  
`one_cycle(economy, phoneme_map, letter_index)` → `List[dict]` — one hourglass turn, returns admitted words with their neighbors  
`governor_filter(word)` → `(bool, float)` — whether a word passes and its affinity score  
`TieEconomy.trade(w1, w2, strength)` — register a co-activation  
`TieEconomy.richest_agents(n)` → sorted list — highest economy participants  
`TieEconomy.strongest_ties(n)` → sorted list — highest weight pairs  

---

## Example Output (6 cycles, Swadesh hypernym stream)

```
Cycle 1: 'classificatory', 'material', 'immaterial' entered
  'classificatory' ties with 'letter' (0.312), 'unit' (0.289)

Cycle 3: 'psychological feature', 'event', 'happening' entered
  'event' ties with 'change' (0.418), 'state' (0.391)

Economy after 6 cycles:
  Richest:  classificatory(7), event(5), material(4)
  Strongest tie: classificatory ↔ letter (0.748)
```

---

## Connects To

- **A-158 GeosensoryCrawler** — provides one of the Dictionary sources (live sensor APIs)
- **A-156 VocabularyAcquisitionAgent** — the predecessor; HourglassFlowAgent is its governed evolution
- **A-165 HypernymStreamComposer** — words entering via the hourglass get spoken via A-165
- **A-160 ActivationEventLogger** — every tie trade is an activation event that should be logged
- **A-167 SubGovernorInstantiator** — each sub-governor runs its own hourglass with its own Dictionary
- **Cloudflare Cron Trigger** — the hourly cron fires `one_cycle()` against the live D1 lobby

---

## The Tie Economy Principle

The LHEA substrate is the draw. Meaning confirms after contact is made. Agents that trade most are not the most correctly defined — they are the most *letterically central*, whose phoneme decomposition overlaps with the widest range of incoming vocabulary.

This is Hebbian learning implemented symbolically: agents that co-activate through shared letter substrate wire together. The economy is the visible record of those wirings.
