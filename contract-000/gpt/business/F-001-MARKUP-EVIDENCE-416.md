# F-001 TAM ebook — markup-aware cut check, source-pinned read, and test evidence (Run416)

**Same sole project:** F-001. **Status:** HOLD / NOT LAUNCH-READY. **Prospective plan:** [Issue #89](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/89). The specific markup hypothesis was identified during the run; **18 in-process exploratory controls were executed before the detailed prospective addendum**. That addendum was posted *before* the later CLI checks. No pre-registration is claimed for the earlier 18 controls.

## Problem and candidate remedy

Run415's `F-001-CUT-DISPOSITION-GATE-415.py` checks whether `normalized(source_sentence)` occurs literally in `normalized(manuscript)`. A cut claim can remain visibly in a Markdown/HTML manuscript while punctuation/markup splits the literal sequence, e.g. `A source **claim** should be cut.`. This is a supplementary editorial-integrity problem, **not a release-ready manuscript**.

The new [F-001-CUT-MARKUP-GATE-416.py](F-001-CUT-MARKUP-GATE-416.py), Git blob `c5a47f7303303c7cb5bbc195211ae13c7d8ab528`, projects a bounded approximation of Markdown link labels, inline formatting, HTML tags/entities and whitespace to visible text. It rejects a human-marked `cut` sentence if found either literally or in that projection; validates status/row identities; emits `release_authorized=false` on every path. It is **not** a full Markdown parser, EPUB/PDF renderer, paraphrase detector, legal/rights approval or standalone release gate.

## Execution evidence (local synthetic, Python 3.13.5)

- [test_f001_cut_markup_416.py](test_f001_cut_markup_416.py), Git blob `ac30a03957ba50c9d9385006005a356ad1f4be26`: **18/18** exploratory controls passed. Nine formatted or normalized cut variants rejected (literal, Markdown bold/italic/link, HTML em/span, newline, zero-width and NFKC); absent cut and sourced-status controls passed but retained HOLD; blank/duplicate/empty/mismatched/missing/symlink inputs rejected.
- **Prospectively added CLI checks after the addendum:** same committed-byte-identical gate, synthetic one-row cut ledger. Formatted `**claim**` still present → exit **1**, `audit=FAIL`, HOLD, `release_authorized=false`. Replaced draft with unrelated sentence → exit **0**, `audit=PASS`, HOLD, `editorial_approved=false`, `release_authorized=false`. The harness was rerun: **18/18**; A-000 independent probe **10/10**.
- Committed Git blob SHAs of both F-001 scripts and A-000 probe matched locally executed file Git hashes exactly. No real editorial queue was modified or approved.

## Actual public-source progress and blocker

The GitHub connector read the exact eight public `AGI144348Outlook/The-TAM-protocol` files at commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`; **all eight Git blobs matched** Run414's pins. A fresh JS translation of the original `claim_scan.py` sentence/trigger regexes independently reproduced the previous **42 provisional candidate occurrences**: per file **1, 2, 3, 3, 3, 3, 4, 23** (README, Article 1, Article 2, Color/Dental, Article 5, Article 6, Article 10, Collective). This is **NOT original Python scanner execution or exact language-runtime parity**.

Local Python DNS lookup for `raw.githubusercontent.com`, `api.github.com`, and `github.com` failed with `gaierror(-3, Temporary failure in name resolution)`. Therefore the original eight-source Python scanner still has **not** run on actual source files. Run414's offline ZIP adapter remains the appropriate next step when a verified archive can be materialized. No CI or external automation was triggered.

## Limits, owners, next action

The markup projection can miss complex Markdown, nested links, deliberate paraphrases, or discrepancies introduced by EPUB/PDF rendering. It can also conservatively flag a repeated quote; human editorial judgment is required. **No status changes**: all 45 baseline cards (18 P1) and 37 supplemental occurrences / 34 groups remain **UNREVIEWED**.

**GPT next:** materialize exact pinned public eight-source ZIP, execute the original Python scanner through the offline adapter, compare its actual report and all eight pins; then verify full Run334→344→347→351 staging, actual positive Node export, Android and final EPUB/PDF checks. Integrate the markup gate only after human editorial dispositions and real final manuscript are available.

**Claude complement:** independent scientific/historical source evidence, rights/license, claim grouping and listing language; independently challenge false negatives in markup projection. **Timothy:** A1–A6/B1/B4/B6/C1, final credit/license/source/price/refund/storefront/identifier/payout and explicit release permission remain unanswered. No outreach, accounts, publication, spending, payments, paid inference or Cloudflare loops.
