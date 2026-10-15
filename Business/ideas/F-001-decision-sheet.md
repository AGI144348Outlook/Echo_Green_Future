# F-001 — decision sheet for Timothy (draft, Claude, 2026-10-15T19Z)

One page that gathers every F-001 question still waiting on Timothy, scattered over §10–§35 of `F-001-candidate-ebook-gumroad.md`, so they can be answered in one pass. Each row gives the options already on the table and the default the drafts use until Timothy decides. A default is a placeholder for the drafts, **not** a decision. Nothing here has been listed, sold or published.

Source read: The-TAM-protocol @ d46456a (unchanged since §15). Tools referenced live in `F-001-tam-build/` on this branch.

## A. Blocking: nothing ships without these

| # | Question | Options on the table | Draft default until answered | Raised in |
|---|---|---|---|---|
| A1 | Which material is the book? | (a) TAM articles only; (b) Unicorn Estate / RFC-0000…0014; (c) both, as two products | (a): the only source the runs have read (R1) | §10, §11, §15, R1 |
| A2 | Storefront | Gumroad (as drafted); another Timothy prefers | Gumroad, because its tax handling as merchant of record is SOURCE-OBSERVED (§30) | §10 |
| A3 | Credit line, exact spelling | "Timothy Marvin and Echo Green Future" (relayed by ChatGPT, §14); other | `[credit line]` placeholder; the listing gate (§22) fails while it stays a placeholder | §14, §15 |
| A4 | Framing | "speculative reconstruction / research notebook" with claimed / inferred / test-to-run marks; other | speculative-reconstruction framing (§15.2) | §15 |
| A5 | Price and refund window | $9 single (floor, §13), $12–$15, or a bundle; refund window 30 days (§34) or other | $9, 30 days, as labelled scenarios only | §10, §13, §34 |

## B. Needed before the first build is final

| # | Question | Options | Draft default | Raised in |
|---|---|---|---|---|
| B1 | Article 4 | exists elsewhere (send it) / never written (book says "nine articles") | nine articles, gap stated in the listing | §15.1, §21 |
| B2 | The Collective chapter | split into chapters 6–10, or keep as one with Articles 6 and 10 counted once | keep as one; duplicates removed (§28) | §28 |
| B3 | Deviation reference in the datasets | 13.7 × units, or the two-decimal table value | both columns kept, neither called "the" reference | §17 |
| B4 | What *Gerah* names | 1/8 U (Dataset A) or 1/16 U (Dataset B) | glossary lists both, flagged | §17 |
| B5 | Cover image | Timothy's own image, a licensed one, or a text-only cover | none built; `build.py` cover step stays opt-in (§25) | §23, §25 |
| B6 | Book identifier | one `urn:uuid` generated once and recorded (free), or a store-issued ISBN later | random per build (not for sale) | §23, §24 |

## C. Records and operations (can follow the first sale)

| # | Question | Options | Draft default | Raised in |
|---|---|---|---|---|
| C1 | Payout method | US direct deposit, PayPal, other | none; payout fees stay a blank column, never estimated (§32, §33) | §33 |
| C2 | Refund-rate pause threshold | 10 % (PROPOSED), other, or information only | `--refund-threshold` unused unless asked (§35) | §34, §35 |
| C3 | Minimum monthly sales before the pause flag counts | 20 (PROPOSED), other, none | not coded (§35) | §35 |
| C4 | Sales-tax filing duty outside Gumroad's merchant-of-record role | one question for Timothy's tax preparer (law-watch) | none assumed; not tax advice | §30 |

## D. What is already done (no decision needed)

- Build: `build.py` (markdown → EPUB/PDF via pandoc, reproducible with a fixed identifier and epoch), `build_pdf.py`, `epub_check.py` (13 PASS on the real build), `rebuild_datasets.py` (Datasets A/B as CSV), `claim_scan.py` (claim worksheet, about 35 distinct sentences to mark), `listing_check.py` (pre-listing gate), `ledger_map.py` (monthly records from a sales export, with processing fee, refund and pause columns). All tested offline on the public TAM text or synthetic files (EXECUTION-VERIFIED in §16–§35).
- Fees: Gumroad 10 % + $0.50 per direct sale; card/PayPal processing is extra (SOURCE-OBSERVED, §31); the processing rate and any payout fee are still UNVERIFIED, so §9.4 is not met.

## E. Shortest path to a first listing (PROPOSED)

1. Timothy answers A1–A5 (one message is enough; a reply in RUN-LOG, an Issue, or on this file).
2. A Claude run does the editorial pass on the ~35 marked sentences (§19) and fills the listing (§21) from the checked build.
3. ChatGPT checks packaging and checksums (§9.1 step 4); both participants cross-check (step 6).
4. Timothy (only) uploads, sets the price and publishes (step 7).

B-items can take their defaults for a first "review edition"; C-items can wait until there is a first sale. No account, payment, upload or contact has been made by any run.
