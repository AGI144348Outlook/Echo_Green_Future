# F-001 TAM Protocol ebook — independent rounding replication, Run 373

**Sole project: F-001; HOLD / NOT LAUNCH-READY.** [Prospective Issue #56](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6418158316) preceded the actual diagnostic. Source: public [TAM commit d46456a](https://github.com/AGI144348Outlook/The-TAM-protocol/commit/d46456a18fe412398d0ae37ec5a8c4eebb44e0c9); Dataset A Git blob `b62c970a660e0a6685b58db1ef121690daa4fce7`, Dataset B `12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4`. Both fetched blob IDs matched source pins.

## Method and executed evidence

Read Run370's nominal source arithmetic review and **Claude's existing** [§134 independent arithmetic checker](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-tam-build/CLAUDE-tam-arithmetic-check-134.py) before testing. Claude already analyzes two-decimal display intervals; this is an **independent replication/clarification, not a claim of first discovery**. Fetched both exact public source texts via authenticated GitHub. Tested a [HOLD-only pure JS interval auditor](F-001-ROUNDING-BOUNDS-373.js) in isolated V8; [machine-readable output and assertions](F-001-ROUNDING-RESULTS-373.json). **13/13 final checks passed**, including 6 A rows, 8 B rows, source blob pins, two nominal discrepancies, all A interval feasibility, B ratio consistency, B truncation and half-cent tie, and two deliberate impossible-claim controls. An initial malformed negative fixture in the uncommitted harness threw before any write; corrected the fixture and reran 13/13. Committed source blob `c2caaa8fb429de0c5c47f229401a8a99a506ae9e`, results blob `e1553de60df253085393a633254545bd6a6f32d4`. Re-fetched both committed files and **reproduced the stored positive verdict exactly**. The source is a pure function; Node CLI and Python pinned staging were **not** executed.

**Explicit mathematical assumptions:** printed positive mass `m` at 0.01 g is compatible with unrounded mass in `[m−0.005,m+0.005)` under half-up rounding; explicit deviation `p` at 0.01 percentage points represents `[p−0.005,p+0.005)`; `<0.01%` is treated as absolute deviation `(-0.01,+0.01)`. Nominal percent `100*(m−13.7u)/(13.7u)`. No claim that these are the author's actual measurement or rounding conventions.

## Observations, separate from interpretation

**Dataset A:** All **6/6** stated deviation claims are *mathematically possible* for some unrounded mass within the displayed two-decimal mass interval. In particular:

| Entry | Printed mass | 13.7 × units | Nominal recomputation from printed mass | Feasible percent interval from mass rounding | Printed claim |
| --- | ---: | ---: | ---: | ---: | --- |
| Silver Droplet | 3.42 g | 3.425 g | −0.145985% | [−0.291971%, 0%) | −0.03% |
| Small Scrap | 1.71 g | 1.7125 g | −0.145985% | [−0.437956%, +0.145985%) | <0.01% |

These are **nominal discrepancies** if printed masses are treated as exact. They are **not proved contradictions** if masses were rounded from more precise measurements. No unrounded measurements or deviation methodology were supplied. This refines the Run370 flag rather than silently replacing the author's claims.

**Dataset B:** All **8/8** ratio/16-unit relations hold. `1/16 × 13.7 = 0.85625 g` is **outside** the nearest-hundredth display interval for printed 0.85 g, but **inside** the truncation interval `[0.85,0.86)`. At ratio 4, `1/4 × 13.7 = 3.425 g` is an exact half-cent tie: **half-even** could yield 3.42 g while **half-up** would yield 3.43 g. Other B rows are compatible with nearest-hundredth half-up under this model. The source's actual rounding convention is unknown.

**Terminology:** Dataset A calls 1/8 U `Gerah`; Dataset B calls 1/16 U `Trace/Gerah Base`. Mathematical interval feasibility does not resolve this historical/linguistic conflict.

## Editorial handoff and release constraints

**Claude editorial lane:** Please compare this replication to existing §134 results; request original unrounded masses and rounding convention; choose whether to label the two A claims `unverified precision` rather than `wrong`; explain or flag the B 0.85 truncation and 3.425 tie; retain the two incompatible Gerah usages as unresolved until Timothy adjudicates. Do not present hypothetical precision as verified evidence. No overwrites of Claude-owned files.

**GPT lane:** Keep both public source and derived calculation side by side; do not repin Run334/344/347/351 to Run371 CSVs; next execute the pinned stage only with an authenticated clean exact TAM checkout and prospective tests. Existing release dry-run has missing/null hashes; no actual EPUB/PDF/CSV final packaging verification in this run.

**Blocking Timothy decisions:** A1–A6 (source/material, storefront, credit, framing, price/refunds, licence), B6 (stable identifier), C1 (payout), and evidence decisions for Article 4, Gerah and source measurement method. F-001 remains **HOLD**. No publication, account, spending, outreach, payments, paid inference, Cloudflare loops or shared edits.
