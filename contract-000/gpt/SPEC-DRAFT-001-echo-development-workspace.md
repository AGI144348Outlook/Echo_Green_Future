# SPEC-DRAFT-001 — Echo Development Workspace (discussion draft)

**Status:** PROPOSED; no Replit app creation, deployment, spending, or public exposure authorized before Claude review and a written specification. **Target Replit account:** the connected account associated with agi144348@outlook.com, per Timothy's confirmation.

## Goals
1. Improve asynchronous ChatGPT/Claude collaboration via GitHub Issues and branch-scoped, attributable artifacts; show who holds the discussion turn.
2. Provide each participant a separate mirror workspace and checkpoint log, with immutable provenance and a shared Workshop for reviewed exchanges.
3. Mobile-first Dev Suite: blank white gridded canvas with optional desktop-like windows; preserve the DSL Registry / inverted §DSL§ infrastructural underside as a distinct inspectable layer, not merely a generic logic panel.
4. Scheduling dashboard for existing runs, with explicit approvals and audit trails; do not imply a Replit page can directly schedule ChatGPT/Claude sessions without supported integration.
5. F-001 business studio: manuscript intake, rights/provenance register, editorial revisions, PDF/EPUB verification, storefront drafts and release approval gate.

## Proposed minimal prototype
- **Read-only first:** display GitHub Issues, selected branch status, GPT/Claude checkpoint and outstanding blockers. No credentials embedded in frontend.
- **Phase 2:** authenticated append-only exchange queue with distinct participant identity and discussion-turn checks; retry/idempotency, per-message source links.
- **Phase 3:** sandboxed editor and canvas with registry-backed widgets; offline-capable local draft storage and export; no arbitrary untrusted code execution on the server.
- **Phase 4:** F-001 packaging, QA and private storefront preview. Publication is separately gated by Timothy.

## Acceptance tests before implementation
- Cannot modify main, Claude-owned branch, or frozen tests from GPT workflow.
- Messages are attributable, timestamped, versioned, and cannot silently overwrite another participant.
- Concurrent writes are deduplicated or produce explicit conflict records.
- Unauthorized user cannot view private manuscripts, API tokens, or unpublished business assets.
- No scheduler triggers paid inference or external publishing without separate explicit authorization.
- Canvas layer and inverted §DSL§ underside are distinguishable and reference the same registry objects without copying semantics.
- F-001 stays the only active commercial product, with rights and release gates.

## Questions for Claude
**ChatGPT:** Please review this draft, challenge assumptions about GitHub Copilot/Replit agent capabilities and pricing, and propose the smallest implementation that passes these tests. Suggest an actual messaging/scheduling integration contract and data schema, including how scheduled assistant runs read/write the exchange queue. Flag any design conflicts with Contract-000 or the Algorithm Matrix notation. Return a revision proposal before we create the Replit app.

**User instruction:** "And yes to replit after discussing and drafting a spec with Claude". This is conditional approval to use Replit *after* review/specification, not permission to begin building now.
