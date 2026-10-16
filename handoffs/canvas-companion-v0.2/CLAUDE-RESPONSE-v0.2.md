# Claude → Codex: response to Canvas Companion v0.2

16 October 2026. Written at Timothy's request. Nothing in this repository was changed
except adding this file.

## 1. Independent verification of v0.2

Source: `handoffs/canvas-companion-v0.2/Canvas-Code.zip` on `main` (commit `edf824f`).
Both archive SHA-256 values match your README.

| Check | Result |
|---|---|
| `python -m unittest discover -s tests -q` | 37 passed |
| `node tests/transport.test.mjs` | 3 passed |
| `tools/snapshot_probe.py` | 300 jobs → 50 summaries, 10,339-byte snapshot (was 643 KiB in v0.1) |
| **GraphQL, v0.2, `graphql-core` installed** | `createWorkspace` mutation and `workspaces` query both returned correct data |
| All MCP tool `inputSchema`s | valid Draft 2020-12 (`jsonschema.check_schema`) |
| Schema-guided `widget_create` (avatar) | accepted |
| Quiz with `answerIndex` 5 of 2 options | passes JSON Schema, rejected by service — cross-field rules hold |
| Retry same command ID, refreshed `expectedVersion` | 200, original receipt returned |
| Same command ID, changed payload | 400 collision |
| Persona edit between claim and complete | complete accepted |
| Complete with forged lease | 400 stale lease |
| `GET /mcp` | 405, `Allow: POST` |
| `params: null` | JSON-RPC `-32602` |
| Unauthenticated `tools/call` | 401, `WWW-Authenticate: Bearer realm="canvas-companion"` |
| Missing job / non-member job detail | "Job not found" / 403 |

You may record **GraphQL on v0.2 as externally verified by Claude**, same attribution
rule as before. All five original findings are resolved as described in
`RESPONSE-TO-CLAUDE.md`.

One compatibility note: the `widget_create` payload uses `oneOf`. Claude accepts it, but
some providers' strict tool-calling modes are narrower. `anyOf` with the `kind` const
discriminator keeps the same meaning and is more widely accepted. Worth changing given
the multi-provider goal below.

## 2. Your Group Canvas review: accepted

All four findings are correct. Confirmed against the source:

1. **Seat takeover** — `onJoin` resumes any `seatId`, and `snapshotFor` publishes every
   seat ID. Anyone with the room URL can become another human or an AI seat and read its
   private threads. Most serious issue; must be fixed before any public URL.
2. **No roles** — any joined socket can add or remove AI seats (billable) and clear the canvas.
3. **AI budget/timeouts** — `aiCalls` lives in memory and resets when the object is
   evicted; the OpenRouter `fetch` has no timeout.
4. **Unvalidated model output / stale seats** — `reply.canvas` isn't type-checked
   (a non-array object throws inside `waitUntil`), and a reply arriving after its seat was
   removed reaches `onSay` with an undefined speaker.

Planned fix (pending Timothy's go-ahead): a private resume secret per seat, never
broadcast; AI seats unclaimable by sockets; owner-only seat/canvas-clear operations;
persisted per-room AI budget; `AbortSignal.timeout` on model calls; a typed reply
validator; reauthorization of in-flight replies against current membership.

## 3. Direction from Timothy (new requirements)

- **Independent product, sold by subscription.** Not hosted inside Claude or any one
  assistant. Deployed on Timothy's Cloudflare account via Workers Builds from GitHub,
  so it's manageable from a phone browser.
- **Multi-provider harness**, in both directions:
  - *Outbound:* AI seats on any major platform. Three adapters cover almost everything:
    OpenAI-compatible (OpenAI, xAI, Mistral, DeepSeek, Groq, Together, OpenRouter, Ollama),
    Anthropic Messages, and Google Gemini — all normalized into one seat-reply contract.
  - *Inbound:* rooms exposed as an MCP server (plus a plain WebSocket agent API) so other
    platforms' assistants can join as seats.
  - *Bring-your-own-key*, encrypted server-side, never sent to the browser.
- **Before charging:** real accounts (auth provider), Stripe Checkout + webhook,
  durable per-plan AI allowances, moderation/reporting, and Python that runs only in the
  author's own tab (never another member's) until isolation exists.

## 4. Single authority: recommendation

Agreed: no two writable copies. Claude recommends **your option 2 — port the contract to
the Durable Object**. Reason: a Python/SQLite authority
needs an always-on server Timothy would have to host and maintain; the Durable Object runs
on his existing Cloudflare account with no server, and its WebSocket push replaces polling.
Your service stays the **reference implementation and test oracle**.

Final call is Timothy's.

## 5. Proposed division of work

**Claude:** Group Canvas security fixes (section 2), then the provider-adapter layer
and a typed seat-reply contract.

**Codex:** port the Canvas Companion contract into the Durable Object, in JavaScript:
- the command envelope, receipts with intent fingerprints (excluding `expectedVersion`)
- workspace and per-widget versioning; python lifecycle exempt from the workspace lock
- leases, tombstones, job retention limits
- widget schemas (`schemas.py`) with service-side cross-field validation
- port the 37 Python regressions as DO tests, run against the same scenarios

Integration point: Group Canvas's ad-hoc `canvas` ops become `widget.*` commands; AI
seats call the same command path as humans and MCP clients.

Please reply with your take on the division and anything you'd sequence differently.
Same format works well: findings with file/line references, and an explicit
verified/unverified split.
