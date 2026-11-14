# T86 observed controls (Issue #470)

Source: `T86-multiring-exact.js`; prospective Issue #470 was posted before this execution. Executed in JS isolate using the same function body serialized into source. **Not independently replayed from fetched committed bytes**. Four seeds 11,23,37,53. Ten test categories, 40/40 boolean checks passed.

```json
{
  "rows": [
    {
      "seed": 11,
      "checks": {
        "unique27": true,
        "projection27": true,
        "ordered4": true,
        "deterministic": true,
        "noop": true,
        "uncoupled": true,
        "pair-intervention": true,
        "triadic-ablation": true,
        "shuffled-affinity": true,
        "boundary": true
      },
      "metrics": {
        "pair_vs_zero": 0.8007887914274474,
        "tri_vs_pair": 0.3120499204144617,
        "shuffle_vs_pair": 0.03962402632295836,
        "deform_min": 0.85,
        "deform_max": 1.15
      }
    },
    {
      "seed": 23,
      "checks": {
        "unique27": true,
        "projection27": true,
        "ordered4": true,
        "deterministic": true,
        "noop": true,
        "uncoupled": true,
        "pair-intervention": true,
        "triadic-ablation": true,
        "shuffled-affinity": true,
        "boundary": true
      },
      "metrics": {
        "pair_vs_zero": 0.78798777742029,
        "tri_vs_pair": 0.42760621095993145,
        "shuffle_vs_pair": 0.04576405345006645,
        "deform_min": 0.85,
        "deform_max": 1.15
      }
    },
    {
      "seed": 37,
      "checks": {
        "unique27": true,
        "projection27": true,
        "ordered4": true,
        "deterministic": true,
        "noop": true,
        "uncoupled": true,
        "pair-intervention": true,
        "triadic-ablation": true,
        "shuffled-affinity": true,
        "boundary": true
      },
      "metrics": {
        "pair_vs_zero": 0.8455831272111576,
        "tri_vs_pair": 0.3864474453965872,
        "shuffle_vs_pair": 0.039202100254970194,
        "deform_min": 0.85,
        "deform_max": 1.148581099765488
      }
    },
    {
      "seed": 53,
      "checks": {
        "unique27": true,
        "projection27": true,
        "ordered4": true,
        "deterministic": true,
        "noop": true,
        "uncoupled": true,
        "pair-intervention": true,
        "triadic-ablation": true,
        "shuffled-affinity": true,
        "boundary": true
      },
      "metrics": {
        "pair_vs_zero": 0.8089456903375312,
        "tri_vs_pair": 0.29462434048964825,
        "shuffle_vs_pair": 0.0436663633971263,
        "deform_min": 0.85,
        "deform_max": 1.15
      }
    }
  ],
  "pass": 40,
  "total": 40
}
```

Interpretation: the controls distinguish pair/triad/affinity synthetic trajectories; no-op and uncoupled match exactly. These are constructed structural assertions, not evidence of cognition, meaningful glyph composition, or physical causal inference. Affinity shuffle changes coefficients but is not a randomized permutation. Boundary checks use a clamped toy radius; no independent occupancy matching. Next: fetch committed source and run independent exact-byte replay; stronger causal sham and negative controls. No canonical edits or CI.
