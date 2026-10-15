# Layer Z order — Addendum 1 (2026-10-15T17:00Z, Claude)

`STRUCTURE.md` lists 27 Layer Z branches (Z01–Z27). A full `git ls-remote --heads` at 17Z shows 42 branches; six Layer Z branches were never in the Z order. Repository events (REST) show they were pushed on 2026-10-12/13 by Timothy, after the Z order was fixed; earlier upkeep runs re-checked only the 27 listed heads, so this was missed until now (finding, recorded here; nothing earlier is changed).

They are appended to the Z order (existing numbers unchanged):

| Z | Branch | Head | Paths | Base | Note |
|---|---|---|---|---|---|
| Z28 | `bytebytego-hub` | 8c315e2 | 30 | library-shared f6ecce6 | Hub catalog first (canonical selection catalog by its own convention) |
| Z29 | `bytebytego-claude` | bd9e94e | 30 | library-shared f6ecce6 | 29/30 blobs equal Z28 |
| Z30 | `bytebytego-gpt` | 95cdd9d | 30 | library-shared f6ecce6 | 29/30 blobs equal Z28 |
| Z31 | `bytebytego-user` | a87a677 | 30 | library-shared f6ecce6 | 29/30 blobs equal Z28 |
| Z32 | `experiment-echo-graphql-canvas-000` | 9b2ad00 | 33 | main 9459934 | 18 blobs already decided elsewhere, 15 new (Issue #24 experiment) |
| Z33 | `personal-library-pwa` | 87760bf | 56 | main 0ba3301 | 21 blobs already decided, 35 new incl. `core-lexicon/` and a vendored Pyodide runtime |

Branches that are not Layer Z (participant or Library branches): `main`, `library-shared`, `mirror-claude`, `mirror-chatgpt`, `mirror-chatgpt-root`, `contract-000-gpt-team`, and the three Library sources. Upkeep runs now compare the full `ls-remote` branch list with this order, not just the listed heads.
