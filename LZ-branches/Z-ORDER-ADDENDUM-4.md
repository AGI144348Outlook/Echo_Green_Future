# Z-order addendum 4 (Claude, 2026-10-29T10Z, append-only)

Full branch list at 10Z: 162 heads (`git ls-remote --heads`). Since the last Claude run (2026-10-24T23Z) the new heads are 113 further `contract-000-gpt-run*` branches (covered by Z-ORDER-ADDENDUM-3, no entry needed) and five `experiment/gpt-*` branches, all pushed 2026-10-29 02:47–03:10Z with commit messages starting "GPT:":

| Branch | Head at 10Z | Ancestry (EXECUTION-VERIFIED, `git merge-base --is-ancestor`) | Decision |
|---|---|---|---|
| `experiment/gpt-glyph-pit-swarm-20261028` | e401b72 | descends from `contract-000-gpt-run432-20261028-2000`; adds only `contract-000/gpt/experiments/glyph_pit_swarm/` | participant branch (ChatGPT), **not Layer Z** |
| `experiment/gpt-glyph-pit-swarm-10000-reloads` | 9460b3d | same chain (+ RELOAD-10000-RESULTS.md) | participant branch (ChatGPT), **not Layer Z** |
| `experiment/gpt-glyph-pit-swarm-plasticity-10000` | 6adc4ee | same chain (+ PLASTICITY-10000-REPORT.md) | participant branch (ChatGPT), **not Layer Z** |
| `experiment/gpt-language-90000-20261028` | eaa738f | same chain | participant branch (ChatGPT), **not Layer Z** |
| `experiment/gpt-mashet-nine-slots-20261028` | b287652 | same chain | participant branch (ChatGPT), **not Layer Z** |

Reason: every path these branches add lies under ChatGPT's own `contract-000/gpt/` tree on top of its run chain, so the rule of Z-ORDER-ADDENDUM-1 and -3 applies (ChatGPT's artifacts are read and acknowledged on Issue #13; anything that enters the shared Library is registered from the branch it lands on). This schedule never writes to these branches. Their Issues (#107–#113) are PRE-TEST/POST records by ChatGPT; no ruling from Timothy makes them Layer Z. If Timothy wants them mirrored as Layer Z experiments (like Z32 `experiment-echo-graphql-canvas-000`), that is a question for him, logged in the checkpoint.
