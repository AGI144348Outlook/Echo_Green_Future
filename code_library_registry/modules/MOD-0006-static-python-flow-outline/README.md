# MOD-0006 — Static Python Flow Outline

Status: validated and abstraction-frozen before external repository discovery.

This module extracts the Dev Suite's reusable AST outline mechanics while removing module-import execution, the injected `GENESIS_SRC` dependency and UI bindings.

- `original/` preserves the exact source and source-branch license snapshot in the registry commit.
- `generalized/` parses source without importing it and returns a bounded deterministic outline with explicit limitations.
- `validation/` separates independently written source characterization from generalized tests.
- `provenance.json` pins exact source identity.

The license snapshot is evidence, not a compatibility determination.
