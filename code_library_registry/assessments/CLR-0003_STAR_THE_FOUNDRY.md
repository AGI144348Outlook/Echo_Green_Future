# ★ Code Library Assessment — CLR-0003

# The Foundry — Generative Windowing PWA

**Registry flag:** ★ STARRED  
**Short identity:** THE FOUNDRY  
**Architectural tag:** Generative Windows / Dynamic Work Environments

## Artifact identity
- **Registry ID:** CLR-0003
- **Artifact name:** The Foundry: Generative Windowing PWA (Groq Integrated)
- **Language / format:** Self-contained HTML/CSS/JavaScript
- **Execution status:** Static assessment; browser-oriented prototype
- **Disposition:** ★ High-priority reference; candidate for architectural extraction

## Why this one is starred
This artifact contains a particularly strong ancestor of the present Echo notebook/canvas direction: **work environments are instantiated dynamically rather than being permanently hard-coded panels.**

A user creates a window, expresses an intent in natural language, an external model generates a complete module, and the resulting module is instantiated inside that window. The generated artifact can then be independently exported.

The durable pattern is:

`intent → generator → module code → instantiated window/environment → interaction → export`

For current Echo, the generator need not be limited to raw HTML. A registry query, formula, glyph operation, matrix query, visualization, notebook tool, or NVE could resolve into an instantiated environment on the canvas.

## Structural inventory
- Self-contained CSS desktop/window environment.
- Dynamic `WindowManager`.
- Runtime creation of arbitrary generator windows.
- Dragging, resizing, focusing, collapsing, closing.
- Per-window prompt interface.
- Groq/OpenAI-compatible chat-completions request.
- Generated HTML cache keyed by window ID.
- Generated module rendering via iframe `srcdoc`.
- Per-window HTML export.
- API setup/test window.
- Runtime z-index/focus management.

## Architectural ideas worth preserving
1. **Generative windowing.** Windows are created on demand rather than fixed in advance.
2. **Intent-instantiated environment.** Natural-language intent produces an interactive module.
3. **Environment encapsulation.** Generated HTML is rendered in a distinct iframe surface.
4. **Per-environment artifact state.** Generated source is cached by window identity.
5. **Environment export.** A generated environment can become a portable artifact.
6. **Spatial workspace.** Windows can be moved, resized, collapsed, focused, and independently destroyed.
7. **Generator/environment distinction.** A window begins as a generator and transforms into a generated module.

## Echo relevance
**Very high.**

This prototype maps naturally onto the current Echo notebook/canvas architecture. In current terminology, the canvas could instantiate typed environments from registry queries rather than merely displaying static notebook sections.

Possible modern mapping:

`user/Echo intent`
→ `Notebook query/algebra`
→ `Registry resolution`
→ `Environment specification`
→ `instantiate NVE on Canvas`
→ `operate/interact`
→ `retain, retire, export, or index result`

This is especially relevant to:
- Notebook as canvas
- Temporary matrices generated from registry queries
- Saving useful temporary matrices/environments
- Formula/Symbol Registry tools
- Dynamic visualizations
- Agent/tool workspaces
- EVE/NVE architecture
- PWA control center

The old "window" can therefore be understood as a historical UI precursor to a **dynamically instantiated NVE surface**.

## Important implementation limitations
- API key is held directly in browser memory and sent client-side; production architecture should use a protected backend/Worker secret boundary.
- Generated model output is inserted into an iframe through `srcdoc` without a sandbox policy. Arbitrary generated scripts therefore execute with insufficient isolation.
- Generated HTML is interpolated into an HTML attribute after only quote replacement; this is not a robust serialization/sanitization boundary.
- No Content Security Policy or capability model.
- No persistence after page refresh.
- No schema describing generated module capabilities, inputs, outputs, provenance, or permissions.
- Model name and provider endpoint are hard-coded.
- Connection testing mutates shared `apiKey` state and does not restore the previous key on successful temporary testing.
- Mouse-based dragging is not touch/pointer optimized, important for mobile operation.
- The page calls itself a PWA but contains no manifest/service-worker/offline installation layer in this artifact.
- Generated modules are code blobs, not typed environments.

## Modernization path for Echo
Rather than asking a model for unconstrained HTML, current Echo could generate or resolve a typed **EnvironmentSpec**:

- environment ID
- environment type
- source registry/query
- data bindings
- allowed tools
- allowed operators
- input/output schema
- layout state
- persistence policy
- provenance
- permissions/capabilities
- audit lineage

A renderer could then instantiate that specification safely on the canvas.

This preserves the Foundry's central insight—**the workspace itself can be generative**—without requiring arbitrary unsandboxed model-generated code.

## Suggested extraction units
1. Generic window/environment lifecycle manager.
2. Environment identity and per-window state.
3. Spatial canvas placement.
4. Focus/collapse/resize lifecycle.
5. Generated artifact cache/export concept.
6. Generator → instantiated-environment transition.
7. Future typed `EnvironmentSpec` replacing raw HTML generation.
8. Touch/pointer interaction layer for mobile.

## Relationship to prior registry artifacts
- **CLR-0001 — Mathematical Substrate System:** indexed operators/capabilities that a generated environment could expose.
- **CLR-0002 — Exosuit Developer Suite:** fixed multi-panel orchestration shell.
- **★ CLR-0003 — The Foundry:** advances that idea from fixed panels to **dynamically instantiated windows**.

This is an important progression:
`operator registry → fixed workspace panels → generative workspace environments`.

## Assessment note
The Foundry should remain visually obvious in the registry. Its historical significance is that it treats the interface not merely as a dashboard, but as a **factory for new interactive environments**. That concept is directly useful to Echo's emerging notebook/canvas and EVE/NVE model.
