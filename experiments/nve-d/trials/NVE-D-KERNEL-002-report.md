# NVE-D-KERNEL-002 — Kernel-bound environment test

**Executed in the chat runtime.** The NVE-D test environment was bound to a candidate kernel via an immutable per-node reference:

```python
K_ENV = KERNELS[candidate_name]  # constant for this experimental node
X = K_ENV                      # the candidate |x| is the same callable
assert K_ENV is X
state = K_ENV(state + external_input)
```

This is a **technical binding fixture**, not an assertion that the symbolic syntax `|x|` has a discovered meaning. A candidate is fixed within a node but varies between nodes. The NVE-D evaluator and recorder remain separate from the candidate kernel, avoiding an untestable circular assertion that the evaluator itself is always correct.

**Run:** 4 declared candidate callable hypotheses (identity, rotate, reverse, nested reverse/rotate), 4 generation budgets (250, 1000, 2500, 5000), 2 seeds (7, 31): **32 runs, 70,000 completed generations** in 0.12 s. These Python functions are explicit synthetic hypotheses and are not inferred from Mashet punctuation or the original codices.

**Recorded relational checks:** binding identity `=`; deterministic checkpoint replay `=`; deliberately incorrect kernel binding detected `=`; opaque source expression preservation `=`. Here `=` denotes exact fixture identity under the declared criterion, not validated semantic equivalence. `0` is reserved for unsupported fixture comparisons. No directional evaluation is claimed.

**Document Feedback Evaluation:** (5) earlier IETF-001 validated only replay/isolation; this adds constant candidate binding; (7) binding check and replay share a Python implementation and do not independently establish symbolic meaning; (8) revise with independently implemented runner, kernel composition hypotheses, injected binding mismatches, separate evaluation rule candidates and comparative cross-node behavior. No protected registry promotion.

**Local reproducible artifacts:** `/mnt/data/nve_d/nve_d_kernel_binding_002.py` and `/mnt/data/nve_d/NVE-D-KERNEL-002-results.json`. They are **not committed** by this report. Commit or import the executable runner separately before asserting repository-side reproducibility.
