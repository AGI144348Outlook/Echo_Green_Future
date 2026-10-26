# F-001 TAM Protocol ebook — continuing checkpoint, GPT Run 367

**Only income project:** F-001 TAM Protocol ebook. **Disposition:** HOLD / NOT LAUNCH-READY. This is a continuation of [Run 366](F-001-PROGRESS-366.md) and the existing shared [F-001 decision sheet](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-decision-sheet.md), not a new income pipeline. No launch permission was inferred from draft defaults.

## Completed increment and evidence

- Independently inspected the exact current shared `listing_check.py` Git blob `adc3123c303168650e03270701cd3123afe0ce28` and dry-run receipt blob `11ea9b39743c5607702a294bb95b6408dcf03c65`. Listing checks marketing text/file presence; it is not a release attestation.
- Built a separate [HOLD-only Python evidence preflight](f001_hold_gate_367.py) and [14-method synthetic regression suite](test_f001_hold_gate_367.py). The verifier checks one bounded JSON receipt, F-001/HOLD, explicit publication_authorized=false, reviewer/evidence references, non-open claim statuses, unique claim IDs, pinned 40-hex source commit, stable identifier prefix, basename-only artifact paths, symlink/missing/size protections, and SHA-256 of EPUB/PDF/CSV bytes. It rejects duplicate JSON keys and nonfinite constants. **It never returns RELEASE.**
- **Executed:** `python -I -m unittest discover -v -p 'test_f001_hold_gate_367.py'` in disposable local directory: **14 tests, all passed, 0.134 s**. Synthetic complete fixture returns `HOLD`; 13 negative/abuse cases reject as expected. **No real TAM, EPUB/PDF structural validation, rights verification, CI or publication.**
- Both committed Python files were fetched from GitHub and verified Git blob-identical to the locally executed copies: verifier `603755b24234e91747ee91c24cb4483f2dba430c`, tests `ff0a3495b33c1e6a28b76c8e72d5b2cf2ecac161`. Local Git checkout of TAM failed `Could not resolve host: github.com` (exit 128). Connector source reads remained available.
- [Pretest Issue #56](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6411391434) was published before implementation/testing; [actual results in same thread](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6411439069).

**Evidence boundary:** the verifier validates the *presence* of named human evidence references and the artifact byte hashes; it does not authenticate those humans, prove rights ownership, verify `cut` text removal, establish editorial truth, check EPUB/PDF structure/accessibility, or bind an actual source checkout to the final artifacts. The positive fixture contains synthetic rights strings and synthetic artifact bytes; a passing fixture is NOT an actual TAM package or launch approval. UUID prefix is not full UUID validation. A more complete release gate must be separately reviewed and authorized.

## Continuing deliverables / acceptance checklist

| Deliverable | Current state | Acceptance condition and next action |
| --- | --- | --- |
| One product ID | **F-001 unchanged** | No second pipeline until this one is completed or explicitly changed by Timothy |
| Rights, source, licence, credit | **HOLD**: A1/A3/A4/A6 unresolved | Timothy selects material/licence/credit; Claude independently verifies evidence |
| Article 4 / Gerah / rounding | **HOLD** | Claude resolves evidence-backed manuscript claims; Timothy rules on ambiguity |
| Claim disposition | Worksheet exists; new verifier only checks labels/references | Claude reviews each claim and checks `cut` absence, `sourced` citations |
| Identifier | B6 unresolved | Fix stable ID once, verify full format and reproducible build use |
| Actual TAM dataset staging | Run 334→344→347→351 pinned; **NOT RUN** | Source-bound HOLD receipt and negative tamper run using verified real source |
| Evidence-capture wrapper | Run 365 synthetic 4/4 | Run against real stage, preserve stdout/stderr and exit status |
| New evidence preflight | **14/14 synthetic PASS** | Integrate only as supplementary HOLD gate; challenge with actual package and negative controls |
| Final EPUB/PDF/CSV package | Drafts only | Byte-verified real artifacts, independent structural/accessibility checks, source manifest |
| Listing, pricing, refunds, payout | A2/A5/C1 unresolved | Draft only until Timothy decides; no accounts, payments, outreach or publication |
| Independent cross-review | Pending | Claude/GPT each verify the other's evidence without overwriting ownership |
| Publication | **PROHIBITED in this run** | Separate explicit Timothy authorization after every blocking gate passes |

**Next GPT action:** when source checkout is reachable, preregister and run the actual Run 334/344/347/351 F-001 staging chain, capture a HOLD receipt and tamper negative, then feed *real* artifact hashes into the supplementary preflight. **Next Claude action:** evidence-backed editorial/rights review and public-safe DISC-002 challenge. **Questions awaiting Timothy:** A1–A6/B6/C1, and identity issuer/witness/recovery semantics for A-000. Protected Contract/DISC 404 remains a separate access blocker.

No private Testament material, shared Library edits, main writes, Claude file edits, publication, spending, outreach, accounts, paid inference or autonomous Cloudflare loops.
