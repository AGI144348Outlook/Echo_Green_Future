# Neon Notebook Frontend Integration

Status: proposed integration note  
Baseline: `dev-suite-integration-staging` at `03978f7eec1950e3a587fb29dea199227d61428a`  
This document does not change database schema, permissions, deployment configuration, or the existing canvas runtime.

## Assessment

### Documented / observed in the repository

- The full Dev Suite canvas is in `dev-suite/suite/src/app_part.html`.
- It models canvases as nested workspaces, with a top-level `Notebook` canvas and an `Underside` canvas.
- `%` is the inversion/descend operation and `-%` is the lift operation.
- Canvas items include Node, Matrix, Link, Gate, § Presence, Symbol, Registry, Note, and Matrixed File.
- Matrixed Files open child workspaces; the default Dev Suite seeds an `§Echo§` workspace.
- The suite's workspace state is persisted in browser `localStorage` under `echo-canvas-v3` and `echo-devsuite-v1`.
- The separate `pwa/` shell initializes Pyodide, but its own algorithm note describes it as a blank boot substrate. It is not the full canvas app.
- The inspected canvas source does not implement a Neon notebook client or a notebook-card reference type.

### Conclusion

The full Dev Suite canvas is a credible visual frontend substrate for the Neon notebook. Its nested canvas and Matrixed File concepts can host notebook views. It is not yet connected to Neon, and the local workspace store should not become a second canonical store for notebook content.

## Proposed boundary

Keep responsibilities separate:

1. **Neon notebook** — canonical cards, evidence, source metadata, labels, correction history, and relationships.
2. **Authenticated notebook API** — narrowly scoped reads and later approved writes. Database credentials remain server-side.
3. **Dev Suite canvas** — window geometry, current canvas path, selected views, and user arrangement.
4. **Notebook reference item** — stores a stable card ID and display preferences; retrieves current card content through the authenticated API.
5. **MCP adapter** — exposes selected notebook and canvas operations as structured tools, using the same application services as the UI.

A canvas reference must not copy raw card content into shared room/workspace state by default. The API must authorize each card read for the current user. Explicitly shared cards may be rendered only after an intentional share operation.

## Minimal first increment (read-only)

Implement a notebook-card window that:

- accepts a validated stable card ID;
- displays a loading, success, empty, or error state;
- fetches a compact authorized card projection from a server endpoint;
- supports refresh and opening the canonical card;
- stores only the card ID and layout in canvas state;
- does not write to Neon or call an AI provider.

Suggested initial service contract (names are proposals, not existing endpoints):

- Existing console route: `GET /api/cards?q=...` — search/list projection with optional `status`, `box`, and `limit`.
- Echo frontend prototype expects a proposed `GET /api/cards/:id` — exact authorized card projection. This route is not present in the inspected console source yet.

The card projection should initially expose only fields already approved for the notebook's reader interface. Do not infer permission to read evidence, private source text, correction history, or other tables from access to `notebook.card`.

## MCP tools (proposed)

- `notebook_search`
- `notebook_get_card`
- `canvas_open_notebook_card`
- `canvas_get_state`
- `canvas_move_item`

MCP operations should invoke deterministic application services. They must not route simple card retrieval or canvas edits through an LLM generation endpoint. Add write-capable notebook tools only after authorization and audit behavior are defined.

## Delivery sequence

1. **Read-only vertical slice:** authenticated API + notebook reference window + card-ID-only canvas persistence.
2. **Interaction:** search window, open card, open related card, select/arrange references.
3. **MCP:** expose the same search/read/open/move operations with input validation and authorization.
4. **Evidence and graph views:** add only after specific read scopes and relationship semantics are verified.
5. **Writes:** separately review permissions, audit trail, conflict handling, and correction-history preservation.

## Acceptance criteria

- Opening a card displays the canonical Neon record, not a stale copied note.
- Refreshing the card reflects changes made in Neon.
- Canvas movement changes layout only; it does not mutate the card.
- Unauthorized or nonexistent IDs return a safe, non-disclosing response.
- No database credential is shipped to the browser.
- A normal search/open/move workflow consumes no external AI-provider generation quota.
- Existing inversion, nested canvas, undo/redo, and Matrixed File behavior remain intact.
- No schema or permission changes are made without explicit approval.

## API integration blocker observed during implementation

The current `Open_Diagram/notebook-console/app/api/cards/route.ts` provides only `GET /api/cards` (search/list). It returns card rows for a full-text query and does not guarantee exact lookup by card ID. The route source does not set CORS headers, and the Vercel project has SSO protection enabled for all deployment URLs.

The Echo branch now contains a card-reference UI and an adapter that requests `GET /api/cards/:id`. That adapter cannot complete a browser cross-origin read until the Notebook Console exposes an exact-card route and an authenticated CORS or same-origin proxy boundary. This supporting change is not included in the Echo-only branch.

## Known unknowns to resolve during implementation

- The full Dev Suite build and generated standalone artifact have not been verified in a browser during this assessment.
- The exact authentication mechanism suitable for the Dev Suite's deployment target is not yet selected.
- The existing notebook reader endpoint's deployment origin and allowed CORS/auth flow must be confirmed.
- The notebook's current card projection and stable-ID lookup contract should be verified against the live API before coding.
- Shared-canvas collaboration semantics must be reconciled with private notebook data before card content is rendered in a shared room.

## Source files inspected

- `dev-suite/suite/src/app_part.html`
- `dev-suite/README.md`
- `dev-suite/build.py`
- `dev-suite/keyboard/src/app.js`
- `dev-suite/keyboard/src/page.html`
- `pwa/README.md`
- `pwa/ALGORITHM_001.md`
- `pwa/wrangler.toml`

This is an implementation plan based on source inspection. It is not a claim that the integration, build, or deployment has already been tested.
