# MOD-0001 — Verified Resource Gate

Status: abstraction frozen before external repository discovery.

This module separates a reusable mechanism from ECHO's Algorithm Matrix boot experiment: a deterministic, ordered gate that authorizes a target, grants creation, instantiates a fixed resource layout, verifies the layout, and only then exposes storage.

- `original/` preserves the two source files exactly as found at the pinned source revision.
- `generalized/` contains domain-neutral code with no Hebrew, ECHO, Governor, matrix, or PWA assumptions.
- `validation/` contains independent tests.
- `provenance.json` records source identity and the abstraction boundary.
- `ABSTRACTION_LOCK.json` records the pre-search content hashes.

This is process-local governance. Actor strings and hashes are not authentication, hostile-code isolation, or tamper resistance against code running in the same interpreter.

Distribution or upstream contribution remains pending resolution of the repository licensing audit. Internal preservation and validation do not assert outbound license compatibility.
