# MOD-0003 — Structured Workspace Registry

Status: validated and abstraction-frozen before external repository discovery.

This module extracts the Matrix Dictionary's reusable local workspace mechanism: named collections containing items and relations, optional provider enrichment, external index bindings, detached snapshots and JSON persistence.

- `original/` preserves the exact source and source-branch license snapshot.
- `generalized/` removes Echo, glyph and matrix vocabulary while adding injectable IDs/time, safer identifiers, detached inputs/outputs and atomic save.
- `validation/` distinguishes source characterization from generalized tests.
- `provenance.json` pins exact source identity.
- `ABSTRACTION_LOCK.json` records validated pre-search hashes.

The license snapshot is evidence, not a compatibility determination. Outbound contribution remains blocked by the repository licensing audit.
