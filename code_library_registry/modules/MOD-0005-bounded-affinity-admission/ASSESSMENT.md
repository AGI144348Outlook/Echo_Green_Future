# MOD-0005 assessment — Bounded Affinity Admission

## Source classification

`echo_hourglass.py` is executable experimental Python without an upstream test suite. It contains an undirected weighted tie ledger, an LHEA-specific overlap function and a bounded per-cycle admission flow.

Two independent characterization tests record source behavior. They also expose two naming/control boundaries: `total_trades` counts endpoint activations (twice each tie event), and rejected candidates remain in the source queue, allowing a permanently rejected front window to starve later candidates.

## Generalized contract

The generalized module accepts hashable items, deterministic `[0,1]` affinity functions and explicit cycle/sample limits. It emits immutable accept/reject decisions and records bounded undirected ties for accepted items.

Scoring completes against a stable population snapshot before queue, population or ledger mutation. Invalid scores or scorer failures leave the cycle uncommitted. Considered rejections are removed, preventing implicit starvation; reconsideration requires explicit re-enqueueing.

Dependencies: Python standard library only.

## Limits

This is not a market, semantic truth detector, autonomous governor, clustering proof, recommender-quality guarantee, distributed queue or persistent database. Samples can omit relevant references. Domain owners must validate thresholds, scoring behavior and bias.

## Licensing disposition

Internal preservation and research only. The source-branch license references AGPL-3.0 without including the complete text and adds use restrictions. Compatibility is not asserted.
