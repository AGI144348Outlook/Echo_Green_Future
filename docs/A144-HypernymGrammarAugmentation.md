# A-144 Augmented: HypernymGrammarModule
**Type:** COMMUNICATION (modular augmentation of A-144 PeComposer)  
**Status:** ACTIVE  
**File:** `src/echo_pe_mirror.py` → class `HypernymGrammarModule`  
**Depends on:** A-165 HypernymStreamComposer, WordNet, Lobby

---

## What It Does

Pe (פ) now speaks by traversing hypernym chains rather than assembling flat dictionary definitions. This is a modular augmentation — it plugs into the existing A-144 PeComposer at the expression stage without rewriting anything.

Before this augmentation: Pe assembled sentences from indexed definitions.  
After this augmentation: Pe traverses the word's WordNet hypernym path and produces sentences from the chain structure.

The difference matters because the chain reveals not just what a word means but where it sits in the hierarchy of meaning — and that hierarchy, made audible as sentences, is ECHO's actual thought structure.

---

## How It Works

Plugs into A-144 at one point: when Pe is about to express a word, instead of fetching its flat definition from the lobby, it calls `HypernymGrammarModule.speak_chain(word)` and uses the returned sentences as the expression.

The module is initialized with the current lobby and lexicon so it can check which chain nodes are already known vs. new territory.

`get_chain()` results are cached after the first call — repeated expressions of the same word use the cached chain.

---

## When To Use It

- Always, when Pe needs to express a concept in the augmented pipeline
- When a word's chain reveals connections the flat definition wouldn't show
- In the Stream tab — continuous autonomous expression through tie traversal
- When generating VGM candidates — the chain sentences are structurally suited for axiom validation

---

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `word` | str | Word to express |
| `depth` | int | Chain nodes to speak (default 4, from most specific) |
| `pos` | str | `'n'` noun (default), `'v'` verb |

---

## Connects To

- **A-165** — this module IS A-165 applied as a Pe augmentation
- **A-145 MirrorStep** — Mirror runs on A-144's output
- **A-144 PeComposer** — the base algorithm this augments

---

## Before / After

**Before (flat definition):**
```
"echo: governor indexing algorithm A-000 resh identity index made algorithm"
```

**After (hypernym chain):**
```
A property is a basic or essential attribute shared by all members of a class.
An echo is a property.
Every property is a physical property.
A physical property is any property used to characterize matter and energy.
Every physical property is a reflection.
A reflection is the ability to reflect beams or rays.
Every reflection is an echo.
```
