# Applications and limits

## Meaningful applications

- admit or reject agent-issued commands before a canvas, dashboard or desktop adapter mutates UI state;
- protect human-owned resources while still permitting non-mutating focus;
- validate registered resource kinds and finite positive geometry before rendering;
- provide stable denial codes for audit logs and tests;
- apply the same boundary to notebook panels, media tiles or other owned workspace resources.

## Contract

The module accepts a command, a read-only resource registry and a collection of registered kinds. It returns a frozen decision and never performs the command or mutates registry state.

Principals are limited to \`human\` and \`agent\`. An agent cannot close, move, resize, dock, minimize, maximize or bind a human-owned resource. Opening requires a registered kind. Move and resize geometry must be finite, with positive dimensions.

## Limits

This is admission logic, not authentication or authorization infrastructure. The caller must establish principal identity, protect the registry from tampering, apply allowed commands safely and audit actual outcomes. It does not render DOM, manage pointer events, persist layouts, resolve bindings or make untrusted content safe.
