# ECHO Notebook PWA

The EVE control surface for ECHO: a touch-first semantic Canvas, widget workspace and
Notebook I/O, with ECHO's Python runtime running locally in the browser through Pyodide.

```
UI · Canvas · Widgets · Notebook I/O            (JavaScript, this folder)
                 │  bridge.js: one JSON seam
              Pyodide 0.26.4 (Python 3.12, WebAssembly)
                 │
          echo/  ECHO runtime
            kernel/     echo_governor_skeleton.py, verbatim (A-000 … A-158)
            operators/  LHEA letter operators, A-174 inversion probe
            matrix/     canonical Registry + local overlay
            canvas/     ECHO as a Canvas actor (IDENTIFY → VALIDATE → OPEN)
            mcw/        MCW envelopes and outbox (no keys, no network)
            bootstrap/  boot() and the entry points bridge.js calls
                 │
Local NVE (IndexedDB): canvas + operation log, layout, overlay, I/O history, outbox
                 │  MCW (when an endpoint is configured)
          Cloudflare gateway → D1 / KV / R2 → GitHub, ChatGPT, Claude
```

Local ECHO and repository ECHO are the same code: `echo/kernel/skeleton.py` is the
repository file unchanged. To update the kernel, replace that file and bump the
version in `echo/manifest.json` and `sw.js`.

## Run it

It must be served over http(s); opening `index.html` as a file will not load Pyodide
or register the service worker.

```bash
python3 -m http.server 8000      # then open http://localhost:8000
```

The first load downloads about 10 MB of Pyodide from jsDelivr. The service worker
caches it, so after that the app, including ECHO's Python runtime, works offline.
For development without the CDN: `?pyodide=/path/to/pyodide/` (URL ending in `/`).

## Deploy

Any static host works. Cloudflare Pages: connect the repository, no build command,
output directory = this folder. GitHub Pages also works because every path is relative.

## Architecture rules this code keeps

- One store, one reducer: `C_{t+1} = Reduce(C_t, O_t)`. The person and ECHO use the same
  operations; every operation is logged with actor, provenance and timestamp. The audit
  widget's *Replay check* rebuilds the Canvas from the log and confirms it matches.
- Semantic resident identity ≠ Canvas Presentiation identity ≠ widget identity. Two
  Presentiations of `dog` share `word:dog`. Closing or moving an Inspector never touches
  the resident or the circle. Changing the renderer (circle ↔ lattice) never changes identity.
- Canonical identity is stable. `teach` only adds new words to a private local overlay,
  marked unvalidated. It can never rewrite a canonical resident.
- ECHO may not move or remove the person's Presentiations or close or rearrange their
  widgets. The reducer enforces this, not just the UI.
- No API keys, tokens or secrets anywhere in this package. MCW messages are queued
  locally and POSTed to the endpoint you set; authentication belongs to the gateway.

## Canvas operations

PRESENTIATE, RESOLVE (read, logged), MOVE, REMOVE, RELATE, SELECT, CLEAR_SELECTION,
SET_RENDERER. Widget operations: OPEN, CLOSE, FOCUS, MOVE, RESIZE, DOCK, MINIMIZE,
MAXIMIZE, BIND, SAVE_LAYOUT, RESTORE_LAYOUT.

## I/O commands (type `help`)

`resolve <w>` · `presentiate <w>[, w]` · `chain <w>` · `hypernyms of <w>` · `hyponyms of <w>` ·
`relate <a> <b> [type]` · `select <w>` · `remove <w>` · `selection` · `equilibrium <a> <b>` ·
`invariant <w>` · `teach <w> is-a <w>[: definition]` · `cycle [text]` · `identify` · `words` ·
`mcw <message>`. Words in ECHO's replies are chips: tap one to select its Presentiation,
or to Presentiate it if it is not on the Canvas.

## Honest limits of v0.1

- The Registry is a curated 59-resident offline seed with hand-set hypernyms, not WordNet
  and not the 1,862-agent D1 lobby. That arrives through MCW.
- The kernel's Propose step is still the single no-op candidate (M-000-NOOP), so `cycle`
  runs a real Governor cycle with a placeholder transformation.
- A-174's complex-phase reading is labelled a hypothesis. Its fixed-point report separates
  the strict involution test from the trivial letter-set test.
- Not in this version: DUPLICATE (new identity), widget tab-stacking, the WidgetSpec /
  WidgetFactory text-to-widget compiler, and live sync with the Cloudflare canonical state.
- The kernel emits one harmless SyntaxWarning (invalid escape at line 6892); it is
  suppressed at import and does not affect behaviour.

## Tests

- `python -m pytest tests` runs the runtime in CPython (suitable for GitHub Actions).
- The package was also verified in real Pyodide 0.26.4 and driven end to end in
  headless Chromium on 360 px and 412 px phone viewports and a desktop viewport: 72/72
  checks, plus an offline reload with the network disabled.
