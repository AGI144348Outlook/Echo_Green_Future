# 10,000 reload / 9-turn experiment — execution record

Prospective protocol: [Issue #108](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/108).

## Local execution (Python 3 stdlib)
- 27 fixed pit slots, 27 glyph forms, synthetic card metadata (domain, operator, version).
- Each reload reassigns metadata deterministically, instantiates 27 subagents with `Alg-000` lineage and unique per-cycle identities, releases them from spatial constraints, performs exactly 9 interactions, records composition candidate identifiers, and returns to pits.
- **10,000 completed reloads**, **90,000 swarm turns**, **270,000 instantiated agent identities**, **100,000 chained events**, **90,000 distinct candidate identifiers**.
- Ledger SHA-256 final tip: `e5f4c10b9c5a4cbef50ba8ec272bacb3745ed32d76fc2dee16a5ec824652799b`.
- Seed: 144348. Full local execution ~4.2 s wall time.
- 14/14 local unittest controls passed after correcting one **test expectation mistake**: nine reloads times nine turns is **81**, not 90. First pass 13/14; corrected pass 14/14.
- The hash chain records event integrity **only while the event stream or receipts are retained**; the compact output stores samples and the terminal digest, not all 100,000 events. It is not an independent tamper-proof witness.

## Scientific interpretation
This is a deterministic synthetic scheduling/search toy. `90,000 distinct candidates` counts **different hashes**, NOT independently validated novel algorithms, semantic generalization, autonomous learning, or emergent swarm intelligence. The operations and domains were assigned by formulas, not learned. Identity ancestry is declarative, not independent validation. No algorithm execution beyond logging a candidate composition. The local source and tests are in generated container artifacts; **this branch records the results but does not yet contain the exact executed Python source**. Reproducibility by external checkout therefore remains **HOLD** pending a source-byte upload/replay.

## Next work
1. Persist exact executed source and tests on this branch, compare hashes, independently replay.
2. Replace synthetic catalog tags with the actual polymathematical index-card schema; define operations, evaluation and falsifiable learning metrics with Timothy.
3. Test persistent agents across reloads (this experiment re-instantiates each cycle) and identity transition layer; distinguish card reload from agent replacement.
4. Preserve nine-turn cadence and avoid equating uniqueness with usefulness.

No changes to main, Claude, Genesis, shared Library or Contract-000; no paid inference, CI, external calls or Cloudflare loops.
