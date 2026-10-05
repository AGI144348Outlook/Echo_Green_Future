# Dev Suite and the Canvas Keyboard

A Pyodide notebook (Python 3.12 running in the browser) built on a gridded canvas,
and a symbol keyboard with a canvas terminal. Everything runs on a phone.

## Run it

| File | How |
|---|---|
| `dist/dev-suite.html` | Open in Chrome or Brave. Self-contained (Python packed in), works offline. About 10 MB. |
| `dist/canvas-keyboard-terminal.html` | Open in Chrome or Brave. Loads Python from the jsDelivr CDN on first use. About 95 KB. |

Saved work lives in the browser: `echo-devsuite-v1` (Suite) and `ckt:*` (Keyboard).

## What's inside

**Dev Suite** (`suite/`)
- Gridded canvas with an underside: `%` steps down, `-%` lifts up; every item can open its own §Canvas.
- Items: Node, Matrix, Link, Gate, § Presence, Symbol, Registry, Note. Matrices bracket, file, reopen and index crossing links.
- Matrixed Files as windows on the surface: §Echo§, Genesis Echo, mini§ר§, Keyboard Terminal, Python library files.
- Filing & storage in the 27 glyph matrices (א … ת, ך ם ן ף ץ); DSL Registry; mapped logics; (?) help.
- Genesis Echo: the ECHO skeleton mapped (classes, methods, flow maps on demand), and **Sandbox ECHO** running it:
  glyph-aware tokenizer, a real evolution loop, the Dictionary (5,000 WordNet definitions, most general first),
  and Vocabulary Homework (READ, SLOTS, LATERAL, VERTICAL, ANALOGICAL, TRANSCRIBE, FILTER, PRESENTIATE) shown live on a task canvas.
- Symbol strip: the symbol keyboard augments every text box in the Suite.

**Canvas Keyboard and Terminal** (`keyboard/`)
- Terminal grid with numbered lines: Insert, Place (drop anywhere), Link (arrows between symbols).
- 12 keyboards, 623 keys, plus ★ Mine. `%` turns keys to logic cards (uses), `%` again to examples to try.
- Brackets open as empty pairs. Block audit with the hinge rule. ◫ frame / operation view (% as mirror inversion).
- ⇅ dual display: linear lines and the compact line per block, both editable.
- ▾ folds the keyboard; Aa opens the phone's keyboard for words.
- The substrate (`keyboard/src/substrate_data.py` and the Python in `page.html`) defines every keyboard, use,
  example and check: edit it to customize.

## Build

```
npm install          # pyodide 0.26.4 into node_modules
python build.py      # writes dist/canvas-keyboard-terminal.html and dist/dev-suite.html
```

The build never modifies sources. It fills placeholders in `suite/src/app_part.html`:
`__DATA_*__` from `suite/src/data/`, `__PY_*__` from `suite/python/`, and `__BUILD_KEYBOARD_B64__`
with the keyboard built from `keyboard/src/`. So: code in `suite/src/*.html`, data in `suite/src/data/`,
Python in `suite/python/`, keyboard in `keyboard/src/`, generated output only in `dist/`.

## Source map

| Path | What it is |
|---|---|
| `suite/src/head_part.html` | Suite page structure and styles |
| `suite/src/loader_part.html` | Serves the packed Pyodide files from memory |
| `suite/src/app_part.html` | The Suite application: code only, with placeholders for data (about 170 KB) |
| `suite/src/data/genesis_skeleton.py` | The Genesis ECHO skeleton source (Sandbox ECHO and the flow maps) |
| `suite/src/data/dictionary.json.gz.b64` | The 5,000-word dictionary, gzip + base64 |
| `suite/src/data/echo_matrices.json.gz.b64` | ECHO's matrices (lobby agents, VGM, WordNet chains, numbers, algorithms), gzip + base64 |
| `suite/src/data/registries.json` | LHEA glyph registry, glyph legend, grammar, formula symbols, formulas |
| `suite/src/data/genesis_structure.json` | Genesis classes, functions, constants and the algorithm list |
| `suite/src/data/latin_registries.json` | Latin roots, prefixes, suffixes; syntax tree registry |
| `suite/src/data/symbols.json` | mini§ר§ symbol registries (straight, curved, hybrid) |
| `suite/python/echo_loader.py` | Sandbox ECHO: loader, tokenizer, Evolution, Dictionary, Homework |
| `suite/python/libmap.py` | Maps Python modules and the skeleton into flow maps |
| `suite/python/build_dict.py` | Builds the dictionary from WordNet (needs nltk) |
| `suite/python/symbols.py` | The three symbol registries with Unicode identities |
| `keyboard/src/page.html` | Keyboard page and its Python substrate (functions) |
| `keyboard/src/substrate_data.py` | KEYBOARDS, USES, EXAMPLES |
| `keyboard/src/app.js` | Keyboard and terminal behavior |
| `build.py` | The build |
