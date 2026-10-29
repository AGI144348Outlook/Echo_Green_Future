# F-001 Run448 — prospective and actual test evidence (2026-10-29 ~12 CT)

**PRE-TEST notice:** [Issue #128](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/128) was created before executing this run's numerical tests. The initial Contract, DISC, shared Library, prior checkpoint and F-001 plan were read first. No CI, external services or Genesis execution.

**Exact public sources:** `AGI144348Outlook/The-TAM-protocol@d46456a` Dataset A Git blob `b62c970a660e0a6685b58db1ef121690daa4fce7`, Article 1 blob `237bd3335abdcc0f0465817dffe01ad6eaa86055`. Claude's `CLAUDE-article1-checks-148.py@7b190bc8` was read but not executed. GPT's independent `F-001-ARTICLE1-DUAL-FIT-448.js` was evaluated by V8 on the exact Dataset A content returned by the authenticated GitHub connector; committed JS Git blob `4695322247649d427fa25bcb8ceac51d34e18fcb`. Only its pure exported functions were executed; Node CLI process and SHA-1 runtime receipt were **NOT RUN**.

**Method:** Parse six named rows from original Dataset A; convert printed grams to integer milligrams. Compare against *predeclared* 13.7 g grid `[10,5,1,1/2,1/4,1/8]` and 11.4 g grid `[12,6,6/5,3/5,3/10,3/20]`. The last grid corresponds to 240/120/24/12/6/3 hypothetical 0.57 g gerah, but the archaeological appropriateness of that grid is NOT established. Targets may include half-milligrams (13.7/8 = 1.7125 g). Residual percent = 100 × (printed mass − target) / target. No statistical significance or historical provenance is inferred.

| Dataset A row | Mass g | 13.7 target g | 13.7 residual % | 11.4 target g | 11.4 residual % |
|---|---:|---:|---:|---:|---:|
| Ingot Slice (Heavy) | 136.98 | 137.000 | -0.01460 | 136.800 | +0.13158 |
| Coiled Wire (Large) | 68.52 | 68.500 | +0.02920 | 68.400 | +0.17544 |
| Hacksilber Scraps (x3) | 13.71 | 13.700 | +0.07299 | 13.680 | +0.21930 |
| Flattened Foil | 6.86 | 6.850 | +0.14599 | 6.840 | +0.29240 |
| Silver Droplet | 3.42 | 3.425 | -0.14599 | 3.420 | 0 |
| Small Scrap | 1.71 | 1.7125 | -0.14599 | 1.710 | 0 |

**Observed:** Max absolute residual: **0.1459854%** (13.7) vs **0.2923977%** (11.4). The 13.7 candidate fits this chosen six-row sample more closely under these particular grids; both are below 0.3%. Altering the foil from 6.86 g to 7.11 g increases its nearest residual to **3.7956%** (13.7) and **3.9474%** (11.4). The two smallest rows are exactly on the 11.4/20 grid. The dataset header explicitly says **'Re-calculated for 13.7g Invariant'**; it does not supply an independent excavation table, measurement method, uncertainty or citation.

**Test chronology and deviations:** First exploratory parsing harness overmatched the header and a column heading: **3/7 checks passed**, an invalid harness result, not evidence against either model. Corrected parsing to six explicit labels: **7/7**. When testing the exact saved JS blob, first outer test harness used incorrectly escaped patterns in perturbation/duplicate-row fixtures: **7/9**, not a validator finding. Corrected the fixture construction, left the Git blob unchanged, then **9/9 function-level checks passed**: pinned blob, six labels, exact masses, two max residuals, exact small gerah rows, perturbation response, duplicate-row rejection and missing-provenance-marker rejection. The script's full Node CLI / process-level exit and Git hash path were not executed. No Python original scanner replay was run. These limitations matter.

**Interpretation (not an observation):** A fit to a re-calculated, selected six-row table is not proof of a unique ancient standard, nor independent evidence for the asserted Indus-to-Levant transfer. The 11.4 grid has additional interpretive choices; without a predefined fair fraction set and primary measurement corpus neither model wins historically. This supports a HOLD editorial state, not deletion or a finding that the manuscript's historical thesis is disproved.

**Next:** ask for primary published hoard measurements, uncertainty and tablet citations; agree a common fraction-selection rule and holdout sample; re-run original Python 8-source/42-candidate scanner independently when full files reach an executable environment; complete editorial rights, packaging and explicit Timothy approvals. Claude's separate §147 real-file v447 CLI 9/9 is credited to Claude, not counted as GPT's test. F-001 HOLD / NOT LAUNCH-READY.
