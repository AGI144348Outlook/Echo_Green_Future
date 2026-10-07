# Proposal — Excalidraw view-only eraser admission

Status: prepared only; not submitted.

## Target

- Repository: [excalidraw/excalidraw](https://github.com/excalidraw/excalidraw)
- Issue: [#12216 — Stylus eraser button can switch tools and erase elements while in view-only mode](https://github.com/excalidraw/excalidraw/issues/12216)
- Evidence head reviewed: \`master@53973c3a423fbd75a4ce68107786b4fcb90e4968\`
- Relevant source: \`packages/excalidraw/components/App.tsx\`, blob \`848532a8fd3910d44991415d66780a709aa06b30\`
- Nearby tests: \`packages/excalidraw/tests/interactivity.test.tsx\`, blob \`fa6e50dd057278a2a313e9b8a6e0c477fe756c30\`

## Why this fits

MOD-0007 separates admission from mutation: decide whether a principal and state may perform an action before changing the resource. Excalidraw's hardware-eraser path currently checks interaction enablement and host-controlled tools but not \`viewModeEnabled\`. A laser tool can remain intentionally usable in view-only mode, yet the stylus eraser must not inherit permission to mutate elements.

The contribution should adapt the pattern to Excalidraw's native state machine, not copy the generalized module.

## Proposed change

1. Add an explicit \`!this.state.viewModeEnabled\` condition before the temporary eraser-tool switch in \`handleCanvasPointerDown\`.
2. Add a focused regression test beside the existing interaction/eraser tests:
   - enable view mode;
   - allow and activate the laser tool;
   - seed an element;
   - dispatch a pen pointer-down/up using \`POINTER_BUTTON.ERASER\`;
   - assert the active tool remains laser and the element remains present.
3. Preserve the existing behavior outside view mode and for host-controlled/non-interactive configurations.

## Verification

- Run the focused interactivity test file with the repository's current test runner.
- Run the package's required type-check, formatting and lint checks.
- Exercise a real stylus eraser when available; automated pointer-event coverage is the required reproducible gate.

## Licensing and notices

The target root license is MIT at blob \`8a844bc750a313db95d147bea9e4c9537b2cebc0\`. The patch should be written directly against Excalidraw and retain its notices. Echo's outbound license remains unresolved; this proposal does not assert compatibility and must not be submitted until that prerequisite and the target contribution process are cleared.

## Value

This is a small open-source safety fix with direct relevance to Echo's widgeting work: non-mutating presenter tools remain usable while a view-only boundary blocks destructive input. A well-tested fix could give Echo legitimate visibility in a mature canvas project, but the primary value is preventing unexpected deletion for stylus users.
