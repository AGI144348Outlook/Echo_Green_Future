# Neon Notebook Card Window — Implementation Status

Status: **frontend reference prototype implemented; live Neon retrieval not yet end-to-end**  
Branch: `feat/neon-card-reference-window`  
Base: `docs/neon-notebook-frontend-assessment`

## Implemented in the Echo Dev Suite

- Added a `Notebook card` placement item to the existing canvas menu.
- Added rectangular sizing, hit testing, and a canvas label showing its canonical card ID.
- Added a read-only reference panel with card-ID validation (`C-00000` format), API-origin configuration, load/refresh, and a link to the Notebook Console.
- Added an adapter expecting `GET /api/cards/:id` returning either a card object or `{ card }`.
- Card projection is cached only in the page's in-memory map. The persisted `DS` workspace stores the card ID, item name, and geometry; it does not persist the fetched claim or provenance.
- No notebook mutation or AI-provider generation is invoked by the reference UI.

## Verified existing API boundary

The current Notebook Console source at `Open_Diagram/notebook-console/app/api/cards/route.ts` implements `GET /api/cards` with `q`, `status`, `box`, and `limit` parameters. It returns a list/search projection. It does **not** implement an exact-card `GET /api/cards/:id` route.

The console's Vercel project has SSO protection enabled for all deployment URLs. The inspected route does not set cross-origin response headers. Therefore the Echo browser app cannot currently retrieve a canonical card projection from that console through the new exact-card request. This is an integration blocker, not a frontend success.

## Required next integration step

Add an authenticated exact-card read endpoint to the Notebook Console, with an explicit origin allowlist or same-origin authenticated proxy, and return only the approved `notebook.card` projection. Do not expose `DATABASE_URL` or any database credential to the browser. This supporting change is outside this Echo-only branch and has not been made.

## Verification status

- Source-level edits committed on this isolated branch.
- Not run: full Pyodide build, browser interaction, hosted deployment, or end-to-end Neon retrieval.
- Existing localStorage workspace schema remains backward-compatible; no schema or permission changes.
