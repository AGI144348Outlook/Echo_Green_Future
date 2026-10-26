# F-001 TAM Protocol ebook — real-source claims inventory and scanner gap (Run 378)

**Single continuing project:** F-001 TAM Protocol ebook. **HOLD / NOT LAUNCH-READY.** Prospective [Issue #56 PRE](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6424734750) was published before scans. Prior work: [Run377 source-binding checker](F-001-CLAIM-BINDING-377.md) passed 14 synthetic Python tests but had not been applied to real TAM source.

## Source and method

Read the **eight public files** at `AGI144348Outlook/The-TAM-protocol` commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`. All **8/8 Git blob SHA and UTF-8 byte-size tuples** matched that pinned tree. Translated the exact sentence-split expression and four `claim_scan.py` trigger patterns into JS regex and applied them to these retrieved source strings. This is **not** execution of the Python scanner or Run377 binding verifier; container-side GitHub DNS resolution failed. JS `\b` and Python Unicode boundary handling may differ. [Machine-readable review manifest](F-001-REAL-CLAIMS-378.json) retains file, source blob, sentence index, trigger and short excerpt without marking claims true.

## Observations (source-backed scan)

**42 baseline candidate sentences**, with 47 trigger occurrences: certainty **12**, percent **2**, accuracy **13**, superlative **20**. File distribution:

- `README.md`: 1 baseline; 1 additional gap candidate; source blob `213bcfaf560d`.
- `Article 1 Hacksilber`: 2 baseline; 0 additional gap candidate; source blob `237bd3335abd`.
- `Article 2 Water Weight Computes`: 3 baseline; 0 additional gap candidate; source blob `ec657c3fa0f7`.
- `The Color Dyed and Dental Records`: 3 baseline; 1 additional gap candidate; source blob `b525ad60ab37`.
- `Article 5`: 3 baseline; 0 additional gap candidate; source blob `c8c1bf617c0d`.
- `Article 6`: 3 baseline; 0 additional gap candidate; source blob `662d745f0b9b`.
- `Article 10`: 4 baseline; 0 additional gap candidate; source blob `e82be564872f`.
- `Collective information`: 23 baseline; 1 additional gap candidate; source blob `710ad3cd4fee`.

The baseline scanner's `\d+(\.\d+)?\s?%` pattern misses percent signs escaped as `\\%`, and the certainty pattern misses present participles such as `demonstrating`. Supplemental **read-only** review on the same sources found **three previously unflagged sentences**: `README.md` sentence 8 (`demonstrating`), `The Color Dyed and Dental Records` sentence 14 (`20\\%`), and `Collective information` sentence 90 (`13.7\\%`). Some other escaped percents occur in sentences already captured by different triggers. The combined **editorial review queue is 45 distinct sentences**, not 45 verified claims.

**Nine of nine synthetic JS regex controls matched** expected original/gap behavior (plain and escaped percent, proving/demonstrating/establishing, neutral sentence, unrelated word, ordinary precision, unrelated slash). These controls are not a Python regression suite or a full recall/precision evaluation. A gap-only detector may add false positives; human editorial review is required.

## Interpretation and boundaries

The existing source-ledger workflow is **incomplete as a candidate-finding tool** for at least these three cases under the JS-translated rules. This is a reproducible candidate gap, **not** a claim that the book's historical conclusions are correct or incorrect. No human claim dispositions were made; all 45 records remain `UNREVIEWED`. The JSON manifest is **not** compatible with `claim_scan.py`'s `claims-report.json` or Run377's SHA-256-binding input and must not be passed off as either. No real Python source-scan, pinned Run334→344→347→351 stage, final manuscript inclusion check, EPUB/PDF/a11y validation or release approval occurred.

## Next actions

GPT: with clean source materialization, run the exact shared Python scanner and Run377 binding checker; compare row counts and investigate Unicode differences, then propose an **opt-in**, prospectively tested scanner gap supplement without changing shared code. Claude: independently review the three supplemental candidates and evidence states, Article 4, Gerah, historical precision and rights. Timothy: decide pending A1–A6/B1/B4/B6/C1 editorial and commercial gates. **F-001 remains HOLD.** No new income project, accounts, outreach, spending, payment, publication, CI, paid inference or Cloudflare loops.
