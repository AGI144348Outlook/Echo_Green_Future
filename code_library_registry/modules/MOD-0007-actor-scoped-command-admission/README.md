# MOD-0007 — Actor-Scoped Command Admission

Status: validated and abstraction-frozen before external repository discovery.

This module extracts the widget branch's reusable command and ownership boundary while removing DOM rendering, pointer events, layout mutation and Echo-specific names.

- \`original/\` preserves the exact branch source and source-branch license snapshot in the registry commit.
- \`generalized/\` provides pure, deterministic admission decisions.
- \`validation/\` separates source characterization from generalized verification.
- \`provenance.json\` pins the exact branch, commit, path and blob.

The source license snapshot is evidence, not a compatibility determination.
