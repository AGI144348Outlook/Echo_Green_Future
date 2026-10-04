# MOD-0004 — Safe Relative Entry Writer

Status: validated and abstraction-frozen before external repository discovery.

This module isolates the workbench's nested browser-file writing mechanism without claiming its `unzip()` stub can parse or extract an archive.

- `original/` preserves the exact browser script and source-branch license snapshot.
- `generalized/` adds an explicit fail-before-mutation relative-path policy and a dependency-free streaming writer.
- `validation/` separates independently written source characterization from generalized tests.
- `provenance.json` pins the source identities.
- `ABSTRACTION_LOCK.json` records validated pre-search hashes.

The source license snapshot is evidence, not a compatibility determination.
