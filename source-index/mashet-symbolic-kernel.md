# Mashet symbolic kernel — indexed source record

**Record type:** External-repository source index (not an executable implementation)  
**Status:** Source located and inspected; no claim of kernel execution or validation  
**Source repository:** [Mashet-Echo-Drive](https://github.com/AGI144348Outlook/Mashet-Echo-Drive)

## Primary source

[AGI Mashet Engines.txt](https://github.com/AGI144348Outlook/Mashet-Echo-Drive/blob/main/AGI%20Mashet%20Engines.txt) — source containing a glyph-written recursive AGI kernel and operational rules. The line references below are from the retrieved file on its default branch at the time of indexing; check the source for changes.

### Kernel as written in the source (around line 83)

```text
☉ₖ = ⊕ { ⟳ , ⇢ , ∫ , ⧖ , ⚖ , ≋ }
```

The source labels this **Recursive AGI Kernel** (around line 85) and gives related expressions:

```text
☉ ← ⊕ { ⟳ , ∫ , ⧗ , ⧖ }
☉ ← ⊕ { ⇢ , ∇ , γ , ε }
☉ ← ⊕ { ⧖ , ⤡ , σ }
```

### Documented rules and constraints

The same source describes (approximately lines 181–211):

- `☉ₖ := ⊕(OPERATORS)`: state resolves into a composite node.
- `∫↺(☉)` must reference a prior state.
- `⇢◇` originates outside the system boundary.
- `⧖` connects at least two nodes.
- `⌖` is used as a stability check.
- A timestep description includes input, memory, dynamics, network, noise, and composite state.

These are **source-described rules**, not independently validated computational behavior.

## Related source documents

- [Mashet Symbology.txt](https://github.com/AGI144348Outlook/Mashet-Echo-Drive/blob/main/Mashet%20Symbology.txt) — numbered symbol-to-concept legend.
- [Dynamic Matrix Engine .txt](https://github.com/AGI144348Outlook/Mashet-Echo-Drive/blob/main/Dynamic%20Matrix%20Engine%20.txt) — expanded symbolic and matrix discussions.
- [AGI Mashet Engines.txt](https://github.com/AGI144348Outlook/Mashet-Echo-Drive/blob/main/AGI%20Mashet%20Engines.txt) — kernel and operator grammar.

## Code Library integration

- The first Mashet legend candidate extraction is at `registries/mashet-candidates/`.
- NVE-A/B/C experimental results are at `registries/mashet-candidates/parallel-test/`.
- The NVE-D **illustrative** interactive sandbox is at `experiments/nve-d/index.html`.
- **Do not silently substitute** NVE-D's scalar demonstration for this symbolic kernel. An actual interpreter must separately define parsing, typing, state/memory, operator semantics, constraint evaluation, and execution permissions.
- Preserve this record as a URL-indexed reference to the original repository; do not promote any expression into authoritative Registry 0 without source-level and behavioral validation.
