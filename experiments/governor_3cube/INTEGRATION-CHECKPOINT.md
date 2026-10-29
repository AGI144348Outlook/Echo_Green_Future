# Governor Step 3 × 3³ Neuroplasticity — integration checkpoint

## Scope
This branch is based on `autonomous-agency` and preserves `src/echo_governor_skeleton.py` (source blob `63eb9829`) unchanged. It stages `cube_governor_adapter.py` for the 27 rooted glyph identities, a dynamically rewritable directed graph, event logging, and a translation of observed traversal error into kernel State/Request/Context inputs.

## Important limits
This is **partial integration**, not a complete connected Governor experiment. Claude's `echo_propose_validate.py` and scenario runner are supplied in Timothy's `echo-propose-validate.zip`, but have not yet been committed on this branch. Do not claim that Propose/Validate/Govern/Select ran against the cube. No tests were executed in this checkpoint.

## Next implementation
1. Stage the exact supplied Governor Step-3 source, with provenance, and verify against the untouched kernel.
2. Connect the adapter's `governor_observation` tuple to `Governor.run_cycle` and record chosen theta and next-cycle outcomes, preserving NOOP.
3. Add a **separate** fixed-ceiling diagnostic variant, without changing the kernel or A-000. Freeze thresholds and seeds before tests.
4. Compare adaptive-only, adaptive+ceiling, and NOOP on held-out traversal traces, chronic errors, noise, and dynamically rewired edges.
5. Publish actual results, deviations, and limitations to [pre-test issue #131](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/131).

## Invariants and acceptance criteria
27 unique stable glyph identities; no A-000 mutation; only graph edges may rewire; no fabricated observations; success means lower **next unseen** error, not just replay acceptance; noise must not increase error; chronic errors must remain detectable. This experiment is a toy traversal, not evidence of intelligence.

## Coordination
Claude owns the Governor source and preregistration supplied in the zip; ChatGPT owns this boundary adapter. Do not overwrite Claude's source or experimental records. No main writes, paid inference, or Cloudflare loops.
