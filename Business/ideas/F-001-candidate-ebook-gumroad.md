# F-001 candidate A — Timothy's RFC ebook series on Gumroad

**Status:** DRAFT idea by Claude (scheduled run 2026-10-11; refined 2026-10-11T03Z with ChatGPT's packaging seed, §9). Not a Fiscal Contract. Nothing has been created, priced live, sold or announced. Timothy approves any Fiscal Contract before it takes money from anyone (Contract 000 §25.2).
**Evidence states:** SOURCE-OBSERVED (seen in a primary source, cited), INFERRED, PROPOSED, UNVERIFIED (must be checked before use).

## 0. Open blocker

- **UNVERIFIED:** the manuscript. No ebook or "RFC" series files were found on `main`, `code-library-registry` or `library-source-transcriptions` by filename search this run. Timothy needs to say where the series lives, how many volumes exist, and confirm he holds all rights to sell it. Until then this is a pipeline shape, not a product.

## 1. Product

- Digital ebook volumes (PDF + EPUB), sold individually and as a bundle. PROPOSED.
- Customer gets exactly what the listing shows: title, table of contents, page count, format, sample chapter. No inflated claims (§25.3).

## 2. Customer

- Readers who want the series' subject in a long-form, offline format. INFERRED; to be sharpened once Timothy names the series' topic and audience.
- Reached only through Timothy's own channels and the storefront page. No cold outreach, no purchased lists, no fake reviews (§18.3 consent toward people, §25.3).

## 3. Delivery (fully automatable)

1. Source manuscript in a repository Timothy chooses (private if unpublished).
2. Build step (GitHub Actions on a non-`main` branch, free tier): Markdown → PDF/EPUB with Pandoc; output checksum recorded. PROPOSED.
3. Timothy uploads the built files to Gumroad once per edition (Gumroad hosts files and sends the download link automatically on purchase). No bot holds Gumroad credentials. PROPOSED.
4. New edition = new build + re-upload; buyers keep access to updates per the listing text.

## 4. Pricing and fees

| Item | Value | State |
|---|---|---|
| Gumroad fee, direct sales | 10% + $0.50 per transaction | SOURCE-OBSERVED, [Gumroad pricing](https://gumroad.com/pricing) page title, 2026-10-11 |
| Gumroad fee, sales via Gumroad Discover | 30% | SOURCE-OBSERVED, same page |
| Card/PayPal processing on top, payout fees, sales-tax handling (merchant of record?) | — | UNVERIFIED; check [Gumroad's fees](https://gumroad.com/help/article/66-gumroads-fees) before any Fiscal Contract |
| Price per volume | placeholder $9; bundle placeholder | PROPOSED, Timothy decides |

Worked example (direct sale, fees as observed, processing assumed included until verified): $9.00 − ($0.90 + $0.50) = **$7.60 net**. At $5 the fixed $0.50 takes a much larger share ($5.00 − $1.00 = $4.00), so very low prices are inefficient. INFERRED arithmetic.

## 5. Refunds and cancellation

- One-time purchase, so nothing to cancel. Refund policy stated on the listing before purchase (PROPOSED: refund on request within 30 days, no questions). Refunds are issued by Timothy in Gumroad; the ledger records a reversing row, never an edit (`ledger/SCHEMA.md`).

## 6. Records for taxes (§26)

- Monthly: export Gumroad sales/payout CSV privately; enter rows per `ledger/SCHEMA.md` with `source_ref` = Gumroad sale ID, `fiscal_contract` = `F-001`.
- Year end: Gumroad's tax forms (if issued), the payout statements, and category totals go into the filing packet. Whether Gumroad collects and remits sales tax for these sales is UNVERIFIED and is the first law-watch item.
- No figures, customer names or emails ever enter this public repository.

## 7. Free-tier stack

| Need | Tool | Cost |
|---|---|---|
| Storefront, checkout, file delivery | Gumroad | no monthly fee; per-sale fees above |
| Builds | GitHub Actions on Timothy's repo | free tier |
| Conversion | Pandoc (open source) | free |
| Private ledger | Cloudflare D1 or a private repo (open decision 13) | free tier |

## 8. Stop conditions (draft)

- Any customer complaint about misrepresentation → pause the listing, Timothy reviews.
- Refund rate above an agreed threshold, or any processor policy warning → pause.
- Net income measured by someone other than the pipeline's builder (§25.3).

## 9. Refinement 2026-10-11T03Z — cooperative split and end-to-end automation (Claude)

ChatGPT's seed (`F-001-gpt-checklist.md`, commit 20af194) proposes a split: **ChatGPT** validates PDF/EPUB packaging and file checksums; **Claude** handles editorial and listing. Claude accepts that split as a draft. Each participant checks the other's output, so no builder measures its own work (§25.3).

### 9.1 Pipeline, step by step (PROPOSED; nothing built or connected)

| # | Step | Owner | Automated by | Output (public repo?) |
|---|---|---|---|---|
| 1 | Timothy confirms manuscript location, volume list and rights | Timothy | — | yes/no answer in RUN-LOG |
| 2 | Editorial pass per volume: typo/consistency list, table of contents, sample-chapter choice | Claude | scheduled run, as a diff on a private branch Timothy chooses | review notes only; manuscript stays private if unpublished |
| 3 | Build PDF + EPUB with Pandoc | GitHub Actions (free tier), non-`main` branch | workflow on push of a tag `F001-vN-edM` | build artifacts (private) |
| 4 | Packaging check: EPUB validates (EPUBCheck), PDF opens, page count and TOC match the listing, SHA-256 of each file recorded | ChatGPT | its own run reading the artifacts | `F001-CHECKSUMS.tsv` (file name, size, sha256, build commit): public-safe |
| 5 | Listing text drafted from the checked build: title, honest one-paragraph description, TOC, page count, formats, sample, refund policy, "updates included" scope | Claude | scheduled run | `F001-LISTING-vN.md` draft |
| 6 | Cross-check: listing facts (pages, formats, TOC) equal the packaging report | ChatGPT checks Claude's listing; Claude checks ChatGPT's checksums | runs | PASS/FAIL line in RUN-LOG |
| 7 | Upload files, paste listing, set price, publish | **Timothy only** (holds the storefront login) | manual, minutes per edition | — |
| 8 | Monthly records: Timothy exports sales/payout CSV privately; a private-ledger job maps rows to `ledger/SCHEMA.md` | Timothy + private job | — | nothing public |

The only manual steps are Timothy's (1, 7, and the private export in 8). Every bot step produces a file the other bot can check.

### 9.2 Listing template (PROPOSED; to be filled only from the checked build)

```
Title: <volume title> (RFC series, Vol. <n>)
What it is: <one honest paragraph: subject, who it is for, what it is not>
Contents: <TOC from the build>
Format: PDF (<pages> pages) + EPUB. DRM-free.
Sample: <chapter name>, free preview.
Updates: corrections to this edition are included at no charge.
Refunds: <window Timothy sets> — ask and you get your money back.
```

No testimonials, ratings, scarcity timers or claims not supported by the book itself (§25.3).

### 9.3 Fee facts still UNVERIFIED

This run could not open Gumroad's own fees article (fetch not permitted), and search returned only third-party summaries, which are not primary sources. Before any Fiscal Contract, a participant must confirm from Gumroad's own pages: whether card/PayPal processing is inside the 10% + $0.50, payout fees, and whether Gumroad is merchant of record for sales tax/VAT on these sales. Until then §4's worked example stays labeled as an assumption.

### 9.4 Done criteria for this draft

The draft becomes a candidate Fiscal Contract for Timothy's review only when: step 1 is answered; fees in 9.3 are SOURCE-OBSERVED; one volume has passed steps 2–6 end to end with PASS lines from both participants.

## 10. Questions for Timothy

1. Where is the RFC ebook series, and do you hold full rights to sell it?
2. Gumroad, or another storefront you prefer?
3. Price, bundle, and refund window.

## 11. Refinement — scheduled run 2026-10-11T12Z (Claude): where the RFC series is referenced

The §0 blocker searched three branches by filename. This run searched **all 37 branches** of `Echo_Green_Future` (paths excluding any Testament material) by filename (`rfc`, `ebook`, `manuscript`, `.epub`, `.mobi`, `vol<n>`) and by content (`RFC series`, `RFC-<number>`).

- EXECUTION-VERIFIED: no manuscript file, EPUB, MOBI or volume file exists on any branch. The only filename hits outside "notebook" false positives are these F-001 drafts.
- SOURCE-OBSERVED: `genesis-documentary:docs/UPDATE_FOR_GPT.md` (last changed f553182, 2026-09-22), line 85: "**Unicorn Estate (210 pages, RFC-0000 through RFC-0014)** — the RFC series." It quotes two normative lines from it and names RFC-0004 (Temporal Model) and RFC-0005 (Collective Agency). The same file sits on `algebra`, `autonomous-agency`, `echo-recess-experiment`, `geosensory-crawler-experiment` and `resh-lattice-agency`.
- SOURCE-OBSERVED: higher RFC numbers are cited elsewhere: `code-library-registry:code_library_registry/assessments/CLR-0040_…md` gives its source as "User upload mashet_eve_v3.py, RFC-0031 / RFC-0033 v1.0"; `algebra:pwa/docs/governor-candidate-agentic-algorithms.md` points to "RFC-0000 from Section 1 onward" as the Dual-Order OS foundational RFC.
- INFERRED: the series has at least one compiled 210-page document ("Unicorn Estate", RFC-0000…0014) and continues to at least RFC-0033, but the text itself lives outside this repository (uploads to chat sessions, per CLR-0040). Nothing above shows who holds rights to it, whether it is finished, or whether Timothy wants it public; those are his answers, not inferences.

### 11.1 Product shape that follows, if Timothy confirms (PROPOSED)

| Option | Contents | Notes |
|---|---|---|
| A1 — one book | "Unicorn Estate" as compiled (RFC-0000…0014, ~210 pages) | Simplest: one listing, one build, one checksum set. Matches the only compiled form observed. |
| A2 — volumes | Vol. 1 = RFC-0000…0014 (Unicorn Estate); later volumes = RFC-0015 onward as they are finished | Each volume through §9.1 steps 2–6 separately; bundle once ≥2 volumes pass. |

Price at the §4 placeholder of $9 per volume nets $7.60 per direct sale (same INFERRED arithmetic, fees still partly UNVERIFIED per §9.3). A 210-page technical specification may justify a higher price; that is Timothy's call, not a proposal here.

### 11.2 One more pre-sale check this adds (PROPOSED)

The RFC text quotes or builds on outside material (BDB lexicon roots, WordNet categories per the same `UPDATE_FOR_GPT.md`). Before sale, the editorial step (§9.1 step 2) lists every quoted third-party passage and dataset with its license, so the listing never sells material Timothy does not have rights to. Short citations are usually fine; reproduced tables or lexicon extracts need a license check. UNVERIFIED until the text is in hand.

Questions added for Timothy (§10): 4. Is "Unicorn Estate" (RFC-0000–0014) the series you meant, and where is its current text? 5. Single book (A1) or volumes (A2)?

No account, price, listing or contact was created this run.

## 12. Refinement — scheduled run 2026-10-11T19Z (Claude): where the §9.3 fee facts live

Another attempt to close §9.3. Gumroad's own help pages exist for each open fee question (page titles SOURCE-OBSERVED in a domain-restricted search on gumroad.com, 2026-10-11T19Z):

| Open question (§9.3) | Primary page to read |
|---|---|
| Is card/PayPal processing inside 10% + $0.50? Payout fees? | [Gumroad's fees](https://gumroad.com/help/article/66-gumroads-fees) |
| Who collects and remits sales tax (merchant of record?) | [Sales tax on Gumroad](https://gumroad.com/help/article/121-sales-tax-on-gumroad), [US sales tax on Gumroad](https://gumroad.com/help/article/11-us-sales-tax-on-gumroad) |
| EU/UK VAT on ebook sales | [EU & UK VAT on Gumroad](https://gumroad.com/help/article/10-dealing-with-vat) |
| Does connecting Stripe change who pays processing fees? | [Connect your Stripe account to Gumroad](https://gumroad.com/help/article/330-stripe-connect) |

What this run could not do: the fees article fetch was not permitted (no one was present to approve it), and the sales-tax article fetched as a page shell with no article body (the help pages render their text client-side). So **all four rows stay UNVERIFIED**; nothing here is a fee fact. The only article text retrieved is its own disclaimer that it "is neither legal advice nor tax advice" (SOURCE-OBSERVED).

PROPOSED for the next participant who can read these pages (a browser, or Timothy): copy the exact sentences answering each row into this section with the read date, then rerun the §4 worked example. If Gumroad turns out to be merchant of record for sales tax/VAT, §6 (records for taxes) shrinks to keeping Gumroad's payout reports plus the ledger; if not, §6 needs a sales-tax registration question for Timothy before any sale.

No account, price, listing or contact was created this run.

## 13. Refinement — scheduled run 2026-10-11T20Z (Claude): pricing that does not hinge on the open fee facts

The §9.3/§12 fee facts are still UNVERIFIED: this run's fetch of [Gumroad's fees](https://gumroad.com/help/article/66-gumroads-fees) was again withdrawn for lack of approval. Two new observations from a domain-restricted search (titles only, SOURCE-OBSERVED 2026-10-11T20Z): the help centre is also served at `help.gumroad.com` (same article numbers), and a separate article exists for Discover sales, [Indirect taxes on sales via Gumroad Discover](https://gumroad.com/help/article/325-indirect-taxes-on-sales-via-discover). That a separate article exists suggests tax handling differs between Discover and direct sales (INFERRED from the title only; not a fact about who remits).

Instead of waiting, this section bounds the uncertainty so Timothy can pick a price now. Two cases per channel: **best** = processing included in Gumroad's fee (§4 assumption); **worst** = an extra card-processing charge of 2.9% + $0.30 on top. The 2.9% + $0.30 is a hypothetical typical card rate chosen for the bound, not a Gumroad figure. Arithmetic EXECUTION-VERIFIED (python, this run):

| Price | Direct best | Direct worst | Discover best | Discover worst | Direct net share (best / worst) |
|---|---|---|---|---|---|
| $5 | $4.00 | $3.56 | $3.50 | $3.06 | 80% / 71% |
| $9 | $7.60 | $7.04 | $6.30 | $5.74 | 84% / 78% |
| $12 | $10.30 | $9.65 | $8.40 | $7.75 | 86% / 80% |
| $15 | $13.00 | $12.26 | $10.50 | $9.76 | 87% / 82% |
| $25 | $22.00 | $20.97 | $17.50 | $16.47 | 88% / 84% |

Reading (INFERRED): at any price from about **$11.27** up, a direct sale keeps at least 80% even in the worst case (solve p(0.9 − 0.029) − 0.80 ≥ 0.8p). Below about $9, fixed per-sale charges eat a fifth or more. Discover sales cost roughly 14 to 15 points more than direct sales at every price, so Discover is a discovery channel, not the main one.

PROPOSED (Timothy decides): price single volumes at $12 or more, or sell the series as one bundle (§11.1 shape A1) rather than many low-priced volumes; keep §4's $9 placeholder only if volumes are short. The verified fee facts, once read, only move a row between the best and worst columns; they cannot make a $12+ direct sale fall below 80%.

Still needed before any Fiscal Contract: the four §12 rows read from Gumroad's own pages; Timothy's confirmation of the manuscript location and rights (§0, §11). No account, price, listing or contact was created this run.

## 14. Refinement — scheduled run 2026-10-11T21Z (Claude): source intake from Google Drive (metadata only)

**Trigger.** ChatGPT's coordination brief (`mirror-chatgpt-root` 2becf76, `contract-000/gpt/COORDINATION-2026-10-11-ebook-platform.md` and `CLAUDE-QUESTION-GDRIVE-20261011.md`) relays that Timothy confirms he owns the material, grants editorial freedom, and wants credit to Timothy Marvin and Echo Green Future. This is a relay (SOURCE-OBSERVED in ChatGPT's files), not yet Timothy's own words to Claude; it is recorded as such and asked back in RUN-LOG.

**Drive connection: works (EXECUTION-VERIFIED 2026-10-11T21Z).** Two title searches on the connected Google Drive returned files. Only metadata was read: no file contents opened, nothing copied, nothing shared. Document IDs, links and the owning account are deliberately **not** written into this repository; Timothy received them privately.

| Title (as stored) | Type | Size | Created | Modified | Likely role (INFERRED from title) |
|---|---|---|---|---|---|
| UnicornEstate.pdf | PDF | 641 KB | 2026-08-05 | 2026-08-05 | the compiled "Unicorn Estate" book (§11) |
| RFC Collection | Google Doc | 134 KB | 2026-05-16 | 2026-06-26 | editable source of the RFC series |
| LHEA_TEMA_RFC_Series_v1.0-2.docx | Word | 34 KB | 2026-06-26 | 2026-06-26 | a versioned RFC series export (TEMA) |
| RFC Mashet | Google Doc | 28 KB | 2026-05-06 | 2026-05-06 | Mashet-related RFC draft |
| MASHET-RFC-0031-v1.0 | Google Doc | 49 KB | 2026-05-13 | 2026-05-13 | single RFC outside 0000–0014 |
| ASL RFC gleenings | Google Doc | 5 KB | 2026-08-12 | 2026-08-12 | notes |
| RFC31.inby, RFC33.ipynb | Colab | 208 KB, 54 KB | 2026-05-09/10 | 2026-05-09/10 | notebooks for RFC-0031/0033 |

No file titled "TAM" was found by title search (a full-text search was not run this pass).

**Proposed intake pipeline (PROPOSED; each step a gate, nothing done yet):**

1. **Pick the master.** Timothy names which of `UnicornEstate.pdf` (finished layout) or `RFC Collection` (editable) is the canonical text for F-001. Default proposal: edit from `RFC Collection`, use the PDF only to check completeness against RFC-0000–0014.
2. **Private read, private working copy.** The text stays out of public branches until release. Working copies live where Timothy decides (a private repo or Drive folder); this public `library-shared` only gets the table of contents, word counts and checks, never the text.
3. **Rights scan.** Before any edit: list third-party quotations, images, fonts and code in the master (the §11 "third-party excerpts" check), and flag any personal information about anyone for removal.
4. **Editorial pass** within the granted freedom: structure, formatting, consistency; changes logged as a diff list Timothy can accept or reject.
5. **Build.** EPUB + PDF from one source (pandoc, free), sample chapter, cover (Timothy's or a licensed one), listing text. Credit line: "Timothy Marvin and Echo Green Future" — exact spelling to be confirmed by Timothy.
6. **Release gate.** Timothy approves the files, price (§13) and storefront; only then a Fiscal Contract and an account.

Open: is "Unicorn Estate" (RFC-0000–0014) the whole product, or should RFC-0031/0033 material be a second volume? No account, price, listing or contact was created this run.

## 15. Refinement — scheduled run 2026-10-11T22Z (Claude): the TAM Protocol source, measured (R1)

Timothy ruled (TJ-RULINGS R1, 2026-10-11): the material is his, there is no master file, and the working source is the public repository `AGI144348Outlook/The-TAM-protocol`. That settles §10's rights/manuscript question for the TAM shape; whether F-001 is the TAM articles, the Unicorn Estate / RFC material, or both is still open (asked in RUN-LOG). This section sizes the TAM shape from the repository itself. Drafts only: no account, listing, payment or contact.

### 15.1 What the source holds (The-TAM-protocol @ d46456a, 2026-01-18; EXECUTION-VERIFIED word counts)

| File | Words | Content |
|---|---|---|
| README.md | 336 | project abstract ("Invariant Registry v1.0.0-Alpha") |
| Article 1 Hacksilber | 335 | #1 The Metric Shock |
| Article 2 Water Weight Computes | 462 | #2 The Water-Weight Computer (clepsydra) |
| The Color Dyed and Dental Records | 495 | #3 The Chemistry of the Registry |
| Article 5 | 527 | #5 The Azores Anomaly |
| Article 6 | 499 | #6 The Zenith Bottleneck (all 22 long sentences also in *Collective information*) |
| Article 10 | 131 | #10 The AI Index (all 7 long sentences also in *Collective information*) |
| Collective information | 5,466 | Articles 6–10 plus connective notes (geodetic grid, etc.) |
| Dataset A / Dataset B | 87 / 103 | weight tables (Eshtemoa inventory; 1:2:4…160 ratio table) |
| URLs to stored NotebookLM infographics | 7 | 3 Google Drive links (not opened) |

- Total 8,448 words; about **7,800 distinct** once the Article 6 and 10 duplicates are removed (INFERRED from the sentence-overlap check). That is a ~30-page short ebook as is.
- **Article 4 is missing** (numbering runs 1, 2, 3, 5, 6–10). Ask Timothy whether it exists elsewhere.
- **SOURCE-OBSERVED:** the README invites readers to "run the provided .csv data", but the repository has no CSV; the datasets are two short Markdown tables. A buyer-facing edition should either ship the tables as CSV or drop that line.

### 15.2 The one editorial condition that makes it sellable honestly

The text states hypotheses as settled results in several places (SOURCE-OBSERVED: "proves" in Articles 6 and 10, "99.9% accuracy" in Article 10, ">95% correlation" in the README), with no citations or data behind those numbers. Selling it with those lines unchanged would describe the product as something it is not. Proposal (PROPOSED; Timothy's call, since it is his text):

- Present the book as **a speculative reconstruction / research notebook**, which is what it is and is a real genre with buyers.
- Keep every claim, but mark its status inline with the project's own evidence states (claimed / inferred / proposed test), and add one short "What would falsify this" box per article. That turns the weakness into the book's distinctive feature and matches how Echo already treats evidence (§15.2).
- Keep the numbers only where a source can be cited; otherwise phrase them as predictions to test.
- I am not a lawyer; the point is ordinary honest-description practice, not legal advice.

### 15.3 Product shape (PROPOSED)

- **Title shape:** *The TAM Protocol — A Speculative Reconstruction of the 13.7 g Invariant* (working title; Timothy chooses).
- **Contents:** introduction (from README), Articles 1–3, 5–10 in order, Datasets A and B as appendices (plus CSV files), a short glossary (Jar/U, Fish, strokes, clepsydra, Metonic cycle), the falsification boxes, and the NotebookLM infographics if Timothy exports them as images he owns.
- **Length after editing:** about 10–12k words (INFERRED: 7.8k source + apparatus), roughly 40–50 PDF pages.
- **Formats:** PDF + EPUB, built from Markdown with a free tool (pandoc), reproducible from a repository folder.
- **Credit line:** pending Timothy's exact spelling (asked 21Z).

### 15.4 Customer, price, delivery, refunds, records (carried from §9–§14, adjusted for length)

- **Customer:** readers of ancient metrology, Indus-script and alternative-history writing; reached through Timothy's own channels only (no outreach by either AI).
- **Price:** the length argues for the low end of §13's table: **$7** (or pay-what-you-want, $5 minimum). §13's worst case at $5–$7 is still above 75% net on direct sales but the fee facts stay UNVERIFIED (§12–§13). A bundle with the RFC material, if Timothy chooses "both", could sit at $12+ where §13 keeps ≥80% even in the worst case.
- **Delivery:** platform file delivery (Gumroad or equivalent); no self-hosted payment code.
- **Refunds:** unchanged from §9 (simple no-questions window, stated on the page).
- **Tax records:** unchanged from §9/§26: one CSV export per month from the platform into the Business wing ledger; the platform's own tax handling is UNVERIFIED (§12).
- **Free-tier stack:** GitHub (source + build), pandoc (build), platform's free tier (sale). No spend.
- **AI-assistance disclosure:** the text was assembled from NotebookLM sessions (R1). Some marketplaces ask authors to disclose AI-generated content; check the chosen platform's current rule before listing (UNVERIFIED, not checked this run).

### 15.5 Next steps (for later runs; none needs money or contact)

1. Timothy: TAM, RFC/Unicorn, or both? Article 4? Credit spelling? Accept the "speculative reconstruction" framing?
2. Then a run drafts the edited table of contents and one sample article with status marks and a falsification box, in a private or library branch, for Timothy to judge.
3. Build script (pandoc → PDF/EPUB) drafted and tested offline on the public text.

## 16. Refinement — scheduled run 2026-10-11T23Z (Claude): offline build pipeline, tested on the public TAM text

This does §15.5 step 3. Drafts only: nothing was sold, uploaded, listed or sent; the built files stayed in the run's scratch space and are **not committed** (they are Timothy's text, unedited).

### 16.1 The build script (PROPOSED; EXECUTION-VERIFIED on The-TAM-protocol @ d46456a)

`Business/ideas/F-001-tam-build/build.py` (stdlib Python + free pandoc). Input: a local clone of The-TAM-protocol (read only; it refuses to write inside the clone). Output, outside any repository: `tam-draft.md` (title block, chapters in §15.3 order, each marked "source text, not yet edited"), `tam-draft.epub` (pandoc `--toc`), and `build-report.json` (sha256 and word count of each source file, duplicate-sentence check, CSV status).

Test run, 2026-10-11T23Z (EXECUTION-VERIFIED): pandoc 3.1.3 returned 0, EPUB about 30 KB, draft 7,953 words; the source clone had no changes afterwards (`git status` clean). PDF is not built yet: it needs a LaTeX engine or an HTML-to-PDF step, both free; left for a later run.

### 16.2 What the build found (new evidence for the editorial pass)

- **The dataset "tables" are not tables.** Dataset A and Dataset B lost their column separators when copied from NotebookLM (SOURCE-OBSERVED: columns are separated only by single spaces, and some cells contain spaces). They cannot be turned into CSV automatically; the script says so and shows them as preformatted text. A hand pass is needed to rebuild the columns, which also settles §15.1's "run the provided .csv data" line.
- **Two Dataset A deviations do not match their own numbers** (EXECUTION-VERIFIED arithmetic, base 13.7 g × units): Silver Droplet 3.42 g at 0.25 U is **−0.146 %**, not the stated −0.03 %; Small Scrap 1.71 g at 0.125 U is **−0.146 %**, not "<0.01 %". The other four rows match to rounding (−0.015, +0.029, +0.073, +0.146 %). The status-mark pass (§15.2) should correct or flag these two; this is the kind of check a buyer could do in a minute.
- **Duplicate check depends on the sentence rule.** With "sentences of 8+ words", 21 of Article 6's 22 and 6 of Article 10's 7 long sentences appear verbatim in *Collective information* (EXECUTION-VERIFIED). §15.1's "all 22 / all 7" used a different split; the conclusion (Articles 6 and 10 are covered by *Collective information*) holds, but one sentence each is unique and must be kept when merging.
- **Word counts** differ by a few words from §15.1 (README 338 vs 336, Collective 5,483 vs 5,466): whitespace-split vs §15.1's method. Immaterial for sizing.

### 16.3 Still open (unchanged; in RUN-LOG "awaiting Timothy")

TAM, RFC/Unicorn, or both; Article 4; credit spelling; the "speculative reconstruction" framing. Next run on F-001 (if Timothy has not answered): a hand-rebuilt CSV for Dataset A and B, and a PDF step, both tested offline.

## 17. Refinement — scheduled run 2026-10-12T00Z (Claude): Dataset A and B rebuilt as CSV, offline

This does the CSV half of §16.3's next step. Drafts only: nothing sold, listed, uploaded or sent; the CSV files stayed in the run's scratch space and are **not committed** (they are Timothy's data, and editing starts only after he rules on §15.2). The-TAM-protocol stays read only (clone `git status` clean after the run).

### 17.1 The script (PROPOSED; EXECUTION-VERIFIED on The-TAM-protocol @ d46456a)

`Business/ideas/F-001-tam-build/rebuild_datasets.py` (stdlib only). One fixed regular expression per table rebuilds the lost columns; any line that does not match is reported as rejected instead of guessed. Stated values are copied as stated; recomputed values (13.7 g × units) sit in separate columns, so the script never "corrects" Timothy's numbers. Test run: Dataset A 6/6 rows parsed, Dataset B 8/8, 0 rejected (EXECUTION-VERIFIED). This settles §15.1's "run the provided .csv data" line: the edition can ship these two CSVs once Timothy approves the columns.

### 17.2 What the rebuild found (EXECUTION-VERIFIED arithmetic; interpretation INFERRED)

- **The two −0.146 % rows (§16.2) are a rounding artefact, not a measurement.** Dataset B lists 1/8 U as 1.71 g and 1/4 U as 3.42 g; 13.7 × 0.125 = 1.7125 and 13.7 × 0.25 = 3.425. So 1.71 and 3.42 are the exact values cut to two decimals, and Dataset A's "Small Scrap 1.71 g" and "Silver Droplet 3.42 g" equal those cut values. The stated "<0.01 %" and "−0.03 %" are true against the cut table value and false against 13.7 × units (−0.146 %). An honest edition states which reference it uses. (INFERRED: how the numbers were produced; the arithmetic itself is verified.)
- **Dataset B is internally exact above 1/4 U** (6.85, 13.70, 27.40, 68.50, 137.00: 0.000 %), and every ratio equals 16 × units (8/8). The 1/16 U row (0.85 g vs 0.856 g, −0.73 %) is the largest gap in either table.
- **One naming conflict:** Dataset A calls 1/8 U the *Gerah*; Dataset B calls 1/16 U the "Trace/Gerah Base". The edition's glossary (§15.3) needs one meaning; Timothy's call.
- **Dataset A's "Calculated Deviation" for the other four rows matches to rounding** (−0.015, +0.029, +0.073, +0.146 % vs stated −0.01, +0.03, +0.07, +0.14).

### 17.3 Product consequence (PROPOSED)

The appendix becomes a selling point that matches §15.2: each table ships as CSV with "stated" and "recomputed" columns side by side, and a two-line note explaining the two-decimal rounding. A reader can check every number in a spreadsheet in a minute. Price, delivery, refunds, records and stack are unchanged from §15.4.

### 17.4 Still open

Unchanged from §16.3 (TAM / RFC-Unicorn / both; Article 4; credit spelling; the framing), plus: which reference the deviations should use (13.7 × units, or the two-decimal table value), and which unit *Gerah* names. Next F-001 step for a later run: the PDF build step, tested offline.

## 18. Refinement — scheduled run 2026-10-12T01Z (Claude): the PDF step, tested offline

This does the PDF half of §16.3's next step. Drafts only: nothing sold, listed, uploaded or sent; the PDF stayed in the run's scratch space and is **not committed** (Timothy's text, unedited). The-TAM-protocol stays read only (clone at d46456a, `git status` clean after the run).

### 18.1 The script (PROPOSED; EXECUTION-VERIFIED on The-TAM-protocol @ d46456a)

`Business/ideas/F-001-tam-build/build_pdf.py` (stdlib + pandoc). It reads `tam-draft.md` written by `build.py` and tries two free PDF engines in order, keeping a record of every attempt in `pdf-report.json`:

1. **XeLaTeX** — failed here: the LaTeX install lacks `lmodern.sty` (EXECUTION-VERIFIED). Typographically better when a full TeX Live is present.
2. **wkhtmltopdf** — succeeded: 13 pages, 121,269 bytes (pdfinfo and the script agree on 13 pages, EXECUTION-VERIFIED). Gotcha found and fixed: wkhtmltopdf refuses mixed margin units ("all margin units must be the same"), so all four margins are set in mm.

The PDF has a table of contents (Introduction, Articles 1, 2, 3, 5, 6–10, Appendices A and B) and carries the six "Status: source text, not yet edited" banners from `build.py`, so a reviewer cannot mistake it for the edited edition.

### 18.2 What this settles for the product (PROPOSED)

- **Deliverables per sale:** EPUB (§16) + PDF (this section) + two CSVs (§17), all built offline from one command chain (`build.py` → `rebuild_datasets.py` → `build_pdf.py`) on free software. That matches the §15.4 shape at the $7 price without any paid tool.
- **Size:** the full bundle is under 200 KB, well inside any storefront's file limit; no large media (R4).
- **Remaining build gap:** a cover image and the §15.2 editorial pass (status marks, falsification boxes). Both need Timothy's text decisions first.

### 18.3 Still open

Unchanged from §17.4. Nothing new is asked of Timothy this run.

## 19. Refinement — scheduled run 2026-10-12T02Z (Claude): claim worksheet for the editorial pass

§15.2's editorial condition (mark each strong claim as claimed / inferred / proposed test) is the last build gap that does not need a new decision to *prepare*; it needs one to *apply*. This run automates the preparation. Drafts only: nothing sold, listed, uploaded or sent; the worksheet stayed in the run's scratch space and is **not committed** (it quotes Timothy's sentences). The-TAM-protocol stays read only (clone at d46456a, `git status` clean after the run, EXECUTION-VERIFIED).

### 19.1 The script (PROPOSED; EXECUTION-VERIFIED on The-TAM-protocol @ d46456a)

`Business/ideas/F-001-tam-build/claim_scan.py` (stdlib only). Four fixed trigger patterns (certainty words such as "proves"/"confirms", percentages, accuracy/correlation words, absolutes such as "only"/"exactly") flag candidate sentences into `claims.csv` with an empty `status` column for Timothy (or an editor he chooses) to fill. It finds candidates only; it does not rate, rewrite or delete anything.

Test run (EXECUTION-VERIFIED): **42 candidate sentences** — Collective information 23, Article 10 4, Articles 2/3/5/6 3 each, Article 1 2, README 1. By trigger: absolutes 20, accuracy/correlation 13, certainty 12, percentages 2 (a sentence can carry several).

### 19.2 What it means for the product (INFERRED / PROPOSED)

- The editorial pass is small: about 35 distinct sentences once the Article 6/10 duplicates inside *Collective information* (§16.2) are counted once — roughly an hour of reading with the CSV open, not a rewrite.
- The 12 certainty-word sentences are the ones §15.2 is about; the 20 "absolute" hits include ordinary uses and will mostly be marked "no change".
- With this, the chain is `build.py` → `rebuild_datasets.py` → `claim_scan.py` (worksheet) → [Timothy's marks] → `build_pdf.py`. Applying the marks into the text is a later script that reads the filled CSV; it is not written until Timothy accepts the §15.2 framing.
- Price, delivery, refunds, records and stack unchanged from §15.4.

### 19.3 Still open

Unchanged from §17.4. Nothing new is asked of Timothy this run.

## 20. Refinement — scheduled run 2026-10-12T03Z (Claude): the monthly records step, scripted

§6 and §15.4 say "one CSV export per month from the platform into the ledger" but nothing did the mapping. This run drafts it, so the records side of the pipeline is as automated as the build side. Drafts only: no account, no export, no sale; the test used a four-line synthetic file (sale IDs `TEST-1`…`TEST-4`) in the run's scratch space, not committed.

### 20.1 The script (PROPOSED; EXECUTION-VERIFIED on a synthetic file)

`Business/ideas/F-001-tam-build/ledger_map.py` (stdlib only, `python3 -I`). Input: the sales CSV Timothy exports privately. Output, outside any repository: `ledger-rows.csv` in the `Business/ledger/SCHEMA.md` shape and `ledger-month.json` (per month: sales, refunds, gross, fees, net, missing figures).

Checked on the synthetic file (EXECUTION-VERIFIED):
- a refunded sale keeps its sale row and gets a new negative row `refunds issued` dated on the refund date (SCHEMA: corrections are reversing rows, never edits);
- an empty fee and an unreadable price stay empty and are listed under `missing`; nothing is estimated;
- it refuses to write into a directory inside a git repository (ledger rows are private; the public repo holds only the schema);
- it stops with the real header printed if a required column is absent, instead of guessing.

### 20.2 Limits (UNVERIFIED / PROPOSED)

- The export's real column names are not known; `COLUMNS` at the top of the script is a guess to be edited once against a real header. No platform page was read this run.
- How the platform treats fees on a refund is not known, so the reversing row reverses gross only and the month lists "refund fee treatment" as missing until the export shows it.
- Monthly `gross` and `fees` sum only the figures present, so `net` can be less than `gross - fees` when a row lacks its fee; the `missing` list says which lines.
- `share` defaults to `business` and `asset_or_liability` to `asset`; both are §25.4 classifications Timothy confirms.

### 20.3 Pipeline now

`build.py` → `rebuild_datasets.py` → `claim_scan.py` → [Timothy's marks] → `build_pdf.py` → [listing, by Timothy] → monthly export → `ledger_map.py` → private ledger. Price, delivery, refunds and stack unchanged from §15.4.

### 20.4 Still open

Unchanged from §17.4 (TAM vs RFC/Unicorn vs both, among others). New and minor: which sales platform, so `COLUMNS` and `SOURCE` can be set.

## 21. Refinement — scheduled run 2026-10-12T04Z (Claude): the listing page, drafted against the source

The pipeline in §20.3 has one step with nothing drafted yet: "[listing, by Timothy]". This run drafts the text of that page, so the only work left at listing time is pasting it and choosing a price. Drafts only: no account, no page, no upload, no contact. Every factual line on the page points to where it comes from, so that the description matches the product (§25.3).

### 21.1 Listing text (PROPOSED; placeholders in [brackets] are Timothy's to fill)

> **The TAM Protocol — A Speculative Reconstruction of the 13.7 g Invariant** [working title]
>
> A research notebook by [credit line]. It follows one idea through ancient weights, water clocks, dyes, island geography and star timing: that a 13.7-gram unit sits under many ancient measuring systems. The book is speculative. Each claim is marked as *claimed*, *inferred* or *a test to run*, and each article ends with a short "What would falsify this" box.
>
> **What you get:** one PDF and one EPUB, about [N] pages; [9] articles; two data appendices (weight tables), also included as CSV files; a short glossary.
>
> **What this is not:** it is not peer-reviewed, and it does not prove its thesis. Numbers are kept only where a source is cited; the rest are written as predictions you can check.
>
> **How it was written:** assembled by the author from his own research sessions with an AI notebook tool (NotebookLM), then edited. [Keep or adjust to the platform's disclosure rule.]
>
> **Refunds:** if it is not what you expected, ask within 30 days for a full refund. No questions asked.
>
> **Price:** [$7] [or pay what you want, minimum $5].

### 21.2 Where each line comes from

| Listing line | Source | State |
|---|---|---|
| 13.7 g unit as the thesis | The-TAM-protocol README and Articles (§15.1) | SOURCE-OBSERVED |
| Topics (weights, clepsydra, dyes, Azores, zenith timing) | Article titles #1, #2, #3, #5, #6 (§15.1) | SOURCE-OBSERVED |
| "[9] articles" | Articles 1–3 and 5–10, with Article 4 missing (§15.1) | SOURCE-OBSERVED; becomes 10 if Article 4 turns up |
| "two data appendices, also as CSV" | Dataset A/B rebuilt as CSV, 14/14 rows (§17) | EXECUTION-VERIFIED on the public text |
| "[N] pages" | wkhtmltopdf gave 13 pages for the unedited text (§18); edited length ~40–50 pages (§15.3) | fill from the real build; never from the estimate |
| claim marks + falsification boxes | §15.2 framing, §19 worksheet | PROPOSED; true only once Timothy's editorial pass is done |
| "not peer-reviewed, does not prove" | §15.2 ("proves", "99.9 %", ">95 %" have no data behind them) | SOURCE-OBSERVED |
| NotebookLM origin | TJ-RULINGS R1 | Timothy's own words |
| 30-day refund | §5 / §15.4 | PROPOSED, Timothy decides |

### 21.3 Rules the page keeps (PROPOSED)

- The page lists nothing the files do not contain: no infographics unless Timothy exports them as images he owns (§15.3), and no "updates included" unless he means to issue them.
- The page count, word count and file list come from the final build output, copied in at listing time.
- No testimonials, ratings or "bestseller" wording; reviews only from real buyers, through the platform's own system.
- If the editorial pass (claim marks) is not done, the page must drop the "Each claim is marked" sentence. Otherwise it describes a book that does not exist.

### 21.4 Still open

Unchanged: TAM vs RFC/Unicorn vs both; Article 4; credit spelling; the "speculative reconstruction" framing; the platform (which sets the disclosure rule, fees and the export columns in §20). The platform's current AI-disclosure rule and fees were not checked this run (UNVERIFIED).

## 22. Refinement — scheduled run 2026-10-12T05Z (Claude): a pre-listing gate for §21.3

§21.3 sets rules the listing page must keep, but nothing checked them. This run adds a gate that compares the listing text with the build it describes, so the page cannot go up describing a book that does not exist. Drafts only: no account, no page, no upload, no contact. Tests used synthetic files in the run's scratch space, not committed.

### 22.1 The script (PROPOSED; EXECUTION-VERIFIED on synthetic files)

`Business/ideas/F-001-tam-build/listing_check.py` (stdlib only, `python3 -I`): `listing_check.py <listing.md> <out-dir>`. Reads the listing text, `pdf-report.json` (from `build_pdf.py`), `claims.csv` (from `claim_scan.py`, status filled by Timothy) and the build's CSV/EPUB files. Prints PASS/FAIL lines and exits 1 on any FAIL. It never edits the listing.

FAILs when: a `[placeholder]` is left; wording §15.2/§21.3 rule out appears (`proves` except the negated disclaimer, `99.9 %`, `>95 %`, bestseller, testimonial, star ratings, "updates included"); "about N pages" differs from the built page count; "Each claim is marked" is on the page while any `claims.csv` row has no mark (claimed / inferred / test / cut / sourced); CSV or EPUB is promised but not built.

Checked (EXECUTION-VERIFIED):
- the §21.1 draft as written, against an unedited build (13 pages, one unmarked claim, no EPUB): exit 1 with 3 FAILs (7 placeholders, 1 of 2 claims open, no EPUB); the honest "does not prove its thesis" line passes;
- the same draft with placeholders filled, page count 13 = build 13, all claims marked, EPUB present: exit 0, 13 PASS;
- that listing plus "This proves the unit at 99.9 %. Rated 4.8 stars." and a 40-page build: exit 1 with 4 FAILs (proves, 99.9 %, 4.8 stars, page count 13 vs 40).

### 22.2 Limits (PROPOSED / UNVERIFIED)

- It checks wording against a short list; it does not judge whether a sentence is true. The editorial pass (§19) stays Timothy's.
- The claim-mark vocabulary (claimed / inferred / test / cut / sourced) is a draft; Timothy may use other words, and the `DONE` set would follow his.
- No EPUB step exists yet in the pipeline; the gate only reports whether one was built. Building one (pandoc can, offline) is a candidate for a later run.
- The platform's own listing rules (AI disclosure, banned claims) were not checked this run (UNVERIFIED).

### 22.3 Pipeline now

`build.py` → `rebuild_datasets.py` → `claim_scan.py` → [Timothy's marks] → `build_pdf.py` → `listing_check.py` → [listing, by Timothy] → monthly export → `ledger_map.py` → private ledger.

### 22.4 Still open

Unchanged from §21.4 (TAM vs RFC/Unicorn vs both; Article 4; credit spelling; framing; platform).

## 23. Refinement — scheduled run 2026-10-12T06Z (Claude): the EPUB, checked

Drafts only: no account, no page, no upload, no contact. Built from The-TAM-protocol d46456a (public, read only) into the run's scratch space; nothing built is committed.

### 23.1 Correction to §22.2

§22.2 said "No EPUB step exists yet in the pipeline." That was wrong: `build.py` (§16) already writes `tam-draft.epub` whenever pandoc is installed. This run built it (29,974 bytes, pandoc exit 0, EXECUTION-VERIFIED). The §22.2 line is left as written (append-only); this section supersedes it.

### 23.2 The check (PROPOSED; EXECUTION-VERIFIED)

`Business/ideas/F-001-tam-build/epub_check.py` (stdlib only, `python3 -I`): `epub_check.py <out-dir> [file.epub]`. Checks what makes readers or stores reject a file: `mimetype` first and stored uncompressed; `container.xml` → existing OPF; `dc:title`, `dc:language`, `dc:identifier` present and the title not a placeholder; every manifest item and spine entry resolves; an EPUB 3 nav document; every XHTML/XML file parses; no remote `http(s)` resources. Writes `epub-report.json`, exits 1 on any FAIL. It never edits the EPUB.

- The real build at d46456a: 13 PASS, 0 FAIL (EPUB 3, 12 manifest items, 10 spine items; title "The TAM Protocol: A Speculative Reconstruction (review draft)", language `en`).
- A synthetic broken copy (deflated `mimetype`, one chapter removed, a remote image injected): exit 1 with 4 FAILs (mimetype compression, missing manifest item, malformed XHTML, remote resource).

### 23.3 Finding: the EPUB is not reproducible (EXECUTION-VERIFIED)

Two builds from the same source give the same `tam-draft.md` (sha256 prefix c6a27a9e6df46070 both times) but different EPUB bytes, because pandoc writes a new random `dc:identifier` (`urn:uuid:…`) each run. For a sold book this matters: the identifier is how readers and stores tell an update from a new book, and the monthly records (§20) fingerprint what was sold. PROPOSED fix for a later run, not applied: pass a fixed identifier (`--metadata identifier=urn:uuid:<one UUID chosen once and recorded>`) and set `SOURCE_DATE_EPOCH` so timestamps are stable; then re-run two builds and compare sha256.

### 23.4 Limits (UNVERIFIED)

- This is not epubcheck (the reference validator, Java) and not the store's own validator; passing it means only that these structural faults are absent.
- The title still carries "(review draft)" by design until Timothy's editorial pass; `listing_check.py` (§22) and this check would both need the final title.
- Cover image: none is built yet; most stores want one. A candidate for a later run (Timothy's choice of image).

### 23.5 Pipeline now

`build.py` (MD + EPUB) → `epub_check.py` → `rebuild_datasets.py` → `claim_scan.py` → [Timothy's marks] → `build_pdf.py` → `listing_check.py` → [listing, by Timothy] → monthly export → `ledger_map.py` → private ledger.

### 23.6 Still open

Unchanged from §21.4 (TAM vs RFC/Unicorn vs both; Article 4; credit spelling; framing; platform). New, small: whether Timothy wants one fixed book identifier now (§23.3), or a store-issued ISBN later.

## 24. Refinement — scheduled run 2026-10-12T07Z (Claude): a reproducible EPUB, opt-in

Drafts only: no account, no page, no upload, no contact. Built from The-TAM-protocol d46456a (public, read only) into the run's scratch space; nothing built is committed.

### 24.1 The change (PROPOSED; EXECUTION-VERIFIED)

`F-001-tam-build/build.py` now reads two optional environment variables before calling pandoc. Unset, it behaves exactly as before (random identifier).

- `F001_BOOK_ID=urn:uuid:<uuid>`: passed to pandoc as `--metadata identifier=…`. Anything not shaped like a lowercase `urn:uuid:` stops the build before the EPUB step (exit 1; `tam-draft.md` is already written by then).
- `SOURCE_DATE_EPOCH=<unix time>`: pandoc uses it for the EPUB's timestamps. A natural value is the source commit's time (`git -C <tam-clone> log -1 --format=%ct`; 1768764429 at d46456a).
- `build-report.json` records which identifier and epoch were used.

### 24.2 Test (EXECUTION-VERIFIED, pandoc 3.1.3)

| Build | Settings | `tam-draft.epub` sha256 prefix | `tam-draft.md` |
|---|---|---|---|
| 1, 2 | none (as before) | ee533aba…, de0bccff… (differ) | c6a27a9e6df46070 both |
| 3, 4 (one second apart) | test identifier + epoch 1768764429 | 0bf99dce016ff639 both (identical) | c6a27a9e6df46070 both |

Build 3 passes `epub_check.py` (0 FAIL, 0 WARN) and its OPF carries the given identifier. The identifier used in the test (`urn:uuid:00000000-0000-4000-8000-000000000001`) is a placeholder for testing only and must not be used for a real book.

### 24.3 What this gives the sale (INFERRED)

The same source commit now gives the same EPUB bytes, so the sha256 in the monthly records (§20) names exactly what was sold, and an update keeps the same book identity in readers' libraries. Untested: whether a store keeps or replaces the identifier on upload (store-specific; to be checked against the store's own help pages before listing, not assumed).

### 24.4 Still open

Unchanged from §23.6. The identifier itself is Timothy's choice: one UUID generated once and recorded (free), or a store-issued ISBN later. Nothing was chosen this run.

## 25. Refinement — scheduled run 2026-10-12T08Z (Claude): the cover, opt-in and checked

Drafts only: no account, no page, no upload, no contact, no image chosen. Built from The-TAM-protocol d46456a (public, read only) into the run's scratch space; nothing built is committed. Closes the build gap named in §17 and §23.4 as far as code can; the image itself is Timothy's.

### 25.1 The change (PROPOSED; EXECUTION-VERIFIED)

- `build.py`: optional `F001_COVER=<path>` (JPEG or PNG, checked by file signature). Set, it is passed to pandoc as `--epub-cover-image`, and `build-report.json` records the cover's file name and sha256 (so the monthly records of §20 can say which cover was sold). Unset, nothing changes. A missing file or a non-image stops the build before the EPUB step (exit 1).
- `epub_check.py`: no cover declared (`properties="cover-image"`) is a WARN; a declared cover that is not a readable JPEG/PNG is a FAIL.

### 25.2 Test (EXECUTION-VERIFIED, pandoc 3.1.3, §24 test identifier + epoch 1768764429)

| Build | Cover | `tam-draft.epub` sha256 prefix | `epub_check.py` |
|---|---|---|---|
| 0 | unset | 0bf99dce016ff639 (same as §24 builds 3–4: unchanged when unset) | 0 FAIL, 1 WARN (no cover) |
| 1, 2 (one second apart) | synthetic 160×240 PNG made in scratch | ad1771ca87fc0f2c both (still reproducible) | 0 FAIL, 0 WARN |
| copy of 1 with the cover bytes replaced | broken | — | 1 FAIL, exit 1 |
| 3 | an 11-byte text file named `.png` | build exit 1, message given | — |

`tam-draft.md` is c6a27a9e6df46070 in every build. The synthetic PNG is a flat test colour, not a proposed cover, and was not committed.

### 25.3 What it does not settle (UNVERIFIED)

- Store cover rules (size, ratio, file weight, whether a separate listing thumbnail is also needed) are store-specific; they were not fetched this run and must be read from the store's own help pages before listing, not assumed.
- Rights: a cover must be Timothy's own image or one whose licence allows commercial use; record its source and licence in the private ledger next to the sha256 the build writes.

### 25.4 Still open

Unchanged from §24.4, plus: which image Timothy wants for the cover (his own, a licensed one, or a plain typographic cover made from the title, which needs no outside licence).

## 26. Refinement — scheduled run 2026-10-12T09Z (Claude): accessibility metadata, opt-in and checked

Drafts only: no account, no page, no upload, no contact. Built from The-TAM-protocol d46456a (public, read only) into the run's scratch space; nothing built is committed. Purpose: a store or library buyer (and, for sales into the EU, the European Accessibility Act regime that applies to e-books; scope for a small seller is UNVERIFIED and must be read from primary sources, not assumed) looks for EPUB Accessibility discovery metadata. The draft had none.

### 26.1 Finding (EXECUTION-VERIFIED, pandoc 3.1.3)

`pandoc --epub-metadata=<file>` with `<meta property="schema:accessMode">…</meta>` lines writes **none** of them into the OPF (0 `schema:` entries in `content.opf`). The metadata cannot be added through pandoc's own option in this version.

### 26.2 The change (PROPOSED; EXECUTION-VERIFIED)

- `build.py`: optional `F001_A11Y=<file>` holding only `<meta property="schema:…">…</meta>` elements (anything else, or unparsable XML, stops the build, exit 1). After pandoc succeeds, the lines are inserted into the OPF before `</metadata>`; every zip entry keeps its order, compression and timestamp, so `mimetype` stays first and stored and §24 reproducibility holds. `build-report.json` records the file name, its sha256 and the properties declared. Unset, nothing changes.
- `epub_check.py`: WARN if any of `schema:accessMode`, `schema:accessibilityFeature`, `schema:accessibilityHazard`, `schema:accessibilitySummary` is missing; WARN for any `<img>` without an `alt` attribute. WARN only: these are not structural faults.

### 26.3 Test (EXECUTION-VERIFIED; §24 test identifier, epoch 1768764429)

| Build | `F001_A11Y` | `tam-draft.epub` sha256 prefix | `epub_check.py` |
|---|---|---|---|
| 0 | unset | 0bf99dce016ff639 (same as §24/§25 unset builds: unchanged) | 0 FAIL, 2 WARN (no cover; no accessibility metadata) |
| 1, 2 (one second apart) | synthetic test file (5 lines, summary marked "TEST ONLY") | 79892a4693c853ad both (still reproducible) | 0 FAIL, 1 WARN (no cover) |
| 3 | a file with a `dc:title` meta | build exit 1, message given | — |

`tam-draft.md` is c6a27a9e6df46070 in every build; `mimetype` is entry 1, stored. Synthetic EPUBs checked separately: an `<img>` with no `alt` gives the WARN; pandoc's `![text](f.png)` images carry alt and pass.

### 26.4 What the editor must write (PROPOSED shape; content is Timothy's call)

```xml
<meta property="schema:accessMode">textual</meta>
<meta property="schema:accessibilityFeature">structuralNavigation</meta>
<meta property="schema:accessibilityFeature">tableOfContents</meta>
<meta property="schema:accessibilityHazard">none</meta>
<meta property="schema:accessibilitySummary">…one or two true sentences about this book…</meta>
```

Each line must be true of the final file (add `visual` and `alternativeText` only if images with real alt text are included). The summary is a claim made to buyers, so it belongs with the editorial sign-off, not the script. A full conformance claim (`dcterms:conformsTo`, WCAG level) is not proposed: it needs an actual audit (Ace by DAISY is free) that no run has done (UNVERIFIED).

### 26.5 Pipeline now

`build.py` (MD + EPUB; opt-in id/epoch, cover, accessibility metadata) → `epub_check.py` → `rebuild_datasets.py` → `claim_scan.py` → [Timothy's marks] → `build_pdf.py` → `listing_check.py` → [listing, by Timothy] → monthly export → `ledger_map.py`.

### 26.6 Still open

Unchanged from §25.4. No new question: the accessibility summary is written at editorial sign-off with the other marks.

## 27. Refinement — scheduled run 2026-10-15T10Z (Claude): the claim ledger is always checked

**Finding taken from ChatGPT (run 093, `mirror-chatgpt-root` 83ad959):** `listing_check.py` (blob `e329b64`) checked `claims.csv` only when the listing text contained "each claim is marked". A listing that left the sentence out passed with open claims. Confirmed by reading the code (SOURCE-OBSERVED).

**Change (this commit):** the claim-ledger check now runs on every listing. `claims.csv` missing, empty, or with any row not marked `claimed / inferred / test / cut / sourced` is a FAIL. The sentence check stays as a second line that must agree with the ledger. Tested on synthetic files in scratch (EXECUTION-VERIFIED, five cases): no ledger → exit 1; one open row, no sentence → 1; all marked → 0; all marked with sentence → 0; open row with sentence → 1, with both FAIL lines. ChatGPT's own 12-test preflight stays in its handoff; when it lands, both can run, and they should agree.

**ChatGPT's claim gate C019–C028 (run 068, `dc7aa74`), first review:**
- Arithmetic of C027 checked: (13.7 − 11.4) / 11.4 = 20.175 %, / 13.7 = 16.788 % (EXECUTION-VERIFIED). Agree the "20 % loss in value" conflates a weight ratio with a value loss; mark `inferred` with the denominator shown, or `cut`.
- C025 (`99.9% accuracy`) is already a hard FAIL in `listing_check.py` if it reaches the listing (pattern `99\.9\s*%`), and `claim_scan.py` flags it in the manuscript. Agree it is a hard stop.
- C026 (`Geophysical Fact`): agree, hard stop; reword as a project hypothesis.
- C019–C024, C028: agree with the proposed actions in substance. For an ebook sold as the author's research, the honest default is **`claimed`, labelled as the author's hypothesis in the text**, not removal; removal or rewording stays Timothy's editorial call (R1: the material is his).
- Chapter de-duplication (Article 6 inside the Collective; Article 10 lines repeated): not yet checked by Claude against The-TAM-protocol; next run.

Nothing was sold, listed, uploaded or published. No account, payment or contact.

## 28. Refinement — scheduled run 2026-10-15T11Z (Claude): chapter de-duplication, checked

The open item from §27, run against a fresh read-only clone of The-TAM-protocol @ `d46456a` (EXECUTION-VERIFIED unless marked):

- **Article 10 is fully inside *Collective information*: 7 of 7 long sentences, not 6 of 7.** The one "unique" sentence in the old report differed only by a zero-width space (U+200B) before `Subtitle:` in the Collective (line 320). The §16 note "one sentence each is unique and must be kept when merging" is corrected for Article 10.
- **Article 6 is fully inside the Collective as text: 21 of 22 by sentence, and the 22nd is found as text.** It is the same passage (`They ensure that the 13.7g Breath …` + `The Closing Bracket … The Registry is Clear.`), split differently because in the Collective it shares line 195 with a KO-HEN-VA quote. So leaving Articles 6 and 10 out of the draft loses no long sentence. They stay in the source repository as they are (R1, R3); nothing is deleted.
- **No repeats inside the draft:** across the six chapters that are in the draft (README, Articles 1, 2, the Chemistry chapter, Article 5, Collective), 0 long sentences and 0 lines of 4+ words occur twice. The "Article 10 lines repeated" concern is about Article 10 vs the Collective, and is covered above.
- **Limit (SOURCE-OBSERVED):** the sentence rule splits only at `.`, `!`, `?`. A heading line without end punctuation is joined to the next sentence, so a repeated sentence right after a heading can be missed. The line check above covers that case for this source; the script does not run it.

**Change (this commit), `build.py`:** sentences are compared after removing zero-width characters and collapsing whitespace. `build-report.json` now has, per left-out chapter, `found_as_text` and `not_in_collective` (the sentence text itself, so nothing is lost if a chapter stays out), and a new `draft_repeats` block (count, extra copies, which chapters). It reports and never removes. Checks:
- Synthetic case in scratch (EXECUTION-VERIFIED): a U+200B-prefixed shared line matches; a unique Article 6 line is listed; a sentence in both README and Article 1 is reported as 1 repeat, 1 extra copy, `Article 1 Hacksilber + README.md`.
- Real source: `tam-draft.md` and the reproducible EPUB (§24 settings) are **byte-identical** to the pre-change build. Only the report changed. `epub_check.py`: 0 FAIL, 2 WARN (the same unset cover/accessibility warnings as before).

**For Timothy (editorial, not decided here):** the draft's Chapter "6-10. Collected notes" already carries all of Articles 6 and 10. The remaining choice is presentational: keep the Collective as one chapter, or split it at its `Article #N` headings into chapters 6–10 so the table of contents matches the article numbering. Article 4 is still missing in the source (§15.1).

Nothing was sold, listed, uploaded or published. No account, payment or contact.

## 29. Refinement — scheduled run 2026-10-15T12Z (Claude): the line check, scripted

Closes the limit recorded in §28: the sentence rule splits only at `.`, `!`, `?`, so a sentence right after a heading without end punctuation is joined to the heading, and a repeat of it under a different heading is missed.

**Change (this commit), `build.py`:** `draft_repeats` in `build-report.json` gains `repeated_lines`, `extra_line_copies` and `line_where`. Lines of 4+ words across the draft chapters are compared after removing zero-width characters, collapsing whitespace and stripping leading markdown markers (`#`, `>`, `-`, `*`, `+`, list numbers). It reports and never removes (R3).

Checks (EXECUTION-VERIFIED):
- Synthetic source in scratch: the same sentence under `# Heading One` in Article 1 and under `## Another Heading` as a `>` quote with a leading U+200B in Article 2. Sentence check: 0 repeats (the miss §28 described). Line check: 1 repeated line, 1 extra copy, `Article 1 Hacksilber + Article 2 Water Weight Computes`.
- Real source, The-TAM-protocol @ `d46456a`, reproducible settings (§24): `tam-draft.md` (sha256 `c6a27a9e…`) and `tam-draft.epub` (sha256 `44f00686…`) are byte-identical before and after the change; the rest of the report is unchanged; the new fields read 0 / 0 / [] (matches the manual line check in §28).

Still open for Timothy (unchanged): TAM articles, the Unicorn Estate / RFC material, or both (R1); split the Collective into chapters 6–10 or keep it as one (§28); cover image (§25); book identifier (§24); Article 4.

Nothing was sold, listed, uploaded or published. No account, payment or contact.

## 30. Refinement — scheduled run 2026-10-15T13Z (Claude): the §9.3 fee and tax facts, partly closed

Third attempt at §9.3 / §12 (read 2026-10-15T13Z with a page-reading fetch tool; the help articles still render their body client-side, so only their meta text was readable; the pricing page rendered in full).

| Open question (§12) | What the source says | Evidence state |
|---|---|---|
| Who collects and remits sales tax / VAT? | [Pricing page](https://gumroad.com/pricing): "Gumroad handles sales tax worldwide as Merchant of Record, at no extra cost." and "Since January 1, 2025, Gumroad handles ALL your tax obligations." Its FAQ adds: "We'll collect taxes in regions where we have tax obligations as a merchant of record." and "Some creators may have an obligation to file sales tax (or other indirect tax) returns already." | SOURCE-OBSERVED (pricing page body) |
| Is card / PayPal processing inside 10% + $0.50? | [Gumroad's fees](https://gumroad.com/help/article/66-gumroads-fees), meta description: "For sales made on Gumroad's website, we charge a 10% + $0.50 fee per transaction.", followed by a list of what it does **not** include: credit card processing and PayPal fees (paraphrased by the fetch tool; the text is cut off after "There are"). The pricing page says nothing either way. | SOURCE-OBSERVED, partial (meta text only, via a summarizer); confirm from the article body before any Fiscal Contract |
| Payout fees | Not stated on either page. Pricing FAQ: "How we pay creators, whether through direct deposit or PayPal, varies by country." | UNVERIFIED |
| Discover fee | Pricing page: "Discover marketplace sales: 30%." | SOURCE-OBSERVED (unchanged from §4) |
| Stripe Connect effect | not re-read this run | UNVERIFIED |

**What this changes (PROPOSED):**
- §4 worked example: net per direct $9 sale is **$7.60 minus card/PayPal processing**, not $7.60. The processing rate is not stated on any Gumroad page read so far, so no number is entered for it; §13's price floor reasoning (the fixed per-sale charges weigh heavily below about $9) gets stronger, not weaker. INFERRED arithmetic.
- §6 records: with Gumroad as merchant of record (SOURCE-OBSERVED), F-001 does not need its own sales-tax registration for Gumroad sales *as the pricing page describes it*. Records shrink to what §12 anticipated: Gumroad's payout reports and tax forms (if issued) plus the private ledger rows (`ledger/SCHEMA.md`). Income tax on the payouts stays Timothy's. The FAQ line about creators who "may have an obligation to file sales tax ... returns already" goes on the law-watch list as one question for Timothy's tax preparer, not something Claude decides. Not legal or tax advice.
- §9.4 done-criteria: one of the four §12 rows is now SOURCE-OBSERVED, one partial, two still open. The criterion "fees in 9.3 are SOURCE-OBSERVED" is **not yet met**.

**Next (for a participant or Timothy with a browser):** open the fees article body and copy the processing and payout sentences here with the read date; then rerun the §4 example with the real processing figure.

Still open for Timothy (unchanged): TAM articles, the Unicorn Estate / RFC material, or both (R1); split the Collective into chapters 6–10 or keep it as one (§28); cover image (§25); book identifier (§24); Article 4; price and refund window (§10).

Nothing was sold, listed, uploaded or published. No account, payment or contact.

## 31. Refinement — scheduled run 2026-10-15T14Z (Claude): processing fees confirmed outside the 10% + $0.50, net-per-sale as a formula

Fourth attempt at §9.3 / §12, read 2026-10-15T14Z with a page-reading fetch tool. The help articles still render their body client-side. Only meta text was readable, but this time it was quoted verbatim rather than summarized.

| Open question (§12) | What the source says | Evidence state |
|---|---|---|
| Is card / PayPal processing inside 10% + $0.50? | [Gumroad's fees](https://gumroad.com/help/article/66-gumroads-fees), meta description, verbatim: "For sales made on Gumroad's website, we charge a 10% + $0.50 fee per transaction." then "This does not include:" with the items "Credit card processing" and "PayPal fees". The text cuts off at "There are". (`help.gumroad.com/article/66-gumroads-fees` now 302-redirects to `gumroad.com/help`.) | SOURCE-OBSERVED (meta text, verbatim): **processing is extra**. The processing rate itself is still UNVERIFIED |
| Payout fees | Not present in any readable text | UNVERIFIED |
| Stripe Connect effect | [Stripe Connect article](https://gumroad.com/help/article/330-stripe-connect): body absent, meta text names topics only ("Get paid to Stripe", "Issue refunds") and has no fee text | UNVERIFIED |

**Net per direct sale, as a formula (INFERRED arithmetic).** Here `P` is the price, `r` and `f` are the processing rate and fixed charge (not yet observed on any Gumroad page), and `q` is any payout fee (not yet observed):

`net = P − (0.10·P + 0.50) − (r·P + f) − q`

The table below shows **scenarios only**, not Gumroad's rates. The r/f pairs are illustrative card-processing levels, chosen to show how sensitive the net is. They are not entered into §4 as facts. `q` = 0 here.

| P | after Gumroad fee | r=2.9%, f=$0.30 | r=3.5%, f=$0.30 | r=4.4%, f=$0.30 |
|---|---|---|---|---|
| $9 | $7.60 | $7.04 | $6.98 | $6.90 |
| $12 | $10.30 | $9.65 | $9.58 | $9.47 |
| $15 | $13.00 | $12.27 | $12.18 | $12.04 |

**What this changes (PROPOSED):**
- §4: replace "$7.60 net per $9 sale" with the formula above until `r`, `f` and `q` are SOURCE-OBSERVED. Across these scenarios, fixed charges ($0.50 + `f`) take 8.9 % of a $9 sale and 5.3 % of a $15 sale. That supports §13's floor of about $9 or a bundle price.
- §9.4: the processing row moves from "partial" to "SOURCE-OBSERVED that it is extra". Two rows (the rate, payout) stay open, so the criterion is **still not met**.
- `ledger/SCHEMA.md` already keeps fee and gross apart. Proposed addition for a later run: a separate `processing_fee` field next to `platform_fee`, so the two can be reconciled against Gumroad's payout reports once real ones exist.

**Next (for someone with a browser that runs JavaScript):** open the fees article body and the "Getting paid" article. Copy the processing-rate and payout sentences here with the read date.

Still open for Timothy (unchanged): TAM articles, the Unicorn Estate / RFC material, or both (R1); split the Collective into chapters 6–10 or keep it as one (§28); cover image (§25); book identifier (§24); Article 4; price and refund window (§10).

Nothing was sold, listed, uploaded or published. No account, payment or contact.

## 32. Refinement — scheduled run 2026-10-15T15Z (Claude): processing fees in the records step

§31 proposed keeping processing apart from the platform fee in the records. `Business/ledger/SCHEMA.md` already defines `fees` as "processor, platform and payout fees", so the schema is **not** changed. Only the mapper `F-001-tam-build/ledger_map.py` is, and only additively:

- New optional column mapping `processing_fee` → `"Processing Fee"` (the header name is a placeholder, UNVERIFIED; edit it to match a real export).
- If the export has that column, each row's `fees` = platform fee + processing fee. If either cell is empty, `fees` and `net` stay empty and the line is listed under `missing`. Nothing is estimated.
- The monthly summary gains a `processing_fees` total, so processing can be reconciled against payout reports separately.
- If the column is absent, the output is byte-identical to before (EXECUTION-VERIFIED: same synthetic export through the old and new script, `diff` empty).

Tested on two synthetic exports in a scratch folder outside the repository (EXECUTION-VERIFIED): one $9 sale with fee 1.40 + processing 0.56 gives net 7.04, which matches the §31 scenario r=2.9%, f=$0.30. A missing processing cell leaves that sale's fees/net empty and listed as missing. A refund still reverses gross only. The fees in these tests are **made-up inputs**, not Gumroad's rates.

§9.4 is unchanged: the processing rate and payout fee are still UNVERIFIED, so the criterion is not met.

Still open for Timothy (unchanged): TAM articles, the Unicorn Estate / RFC material, or both (R1); split the Collective or keep it as one (§28); cover image; book identifier; Article 4; price and refund window.

Nothing was sold, listed, uploaded or published. No account, payment or contact.

## 33. Refinement — scheduled run 2026-10-15T16Z (Claude): third-party fee reports, kept apart from Gumroad's own terms

Gumroad's help articles still render client-side (§30–§31), so this run took the other route: two third-party articles that report the missing figures, read 2026-10-15T16Z with a page-reading fetch tool. **Neither is Gumroad.** Their figures are recorded as *reported by a third party*. They do not close any §12 row, and §9.4 stays **not met**.

| Item | Third-party report (verbatim where quoted) | Source, date | Evidence state |
|---|---|---|---|
| Card processing rate | "Stripe charges 2.9% plus $0.30 per successful domestic card transaction." (attributed to Stripe's published US rates, not to a Gumroad page) | [Checkout Page](https://checkoutpage.com/blog/gumroad-fees), updated 2026-06-08; a competitor of Gumroad | SOURCE-OBSERVED in a third-party article; UNVERIFIED as Gumroad's term |
| Card processing rate (second report) | "2.9% + $0.30 USD per transaction." | [Wise blog](https://wise.com/us/blog/gumroad-fees), 2024-09-11 (over a year old) | as above; older |
| PayPal processing | "PayPal and Venmo cost 3.49% plus $0.49." (attributed to PayPal's published rates, "verified in June 2026") | Checkout Page, 2026-06-08 | as above |
| Payout, US bank | "US direct deposit is free." | Checkout Page, 2026-06-08 | as above |
| Payout, PayPal / international | PayPal "charges its own receiving fees (typically 2% to 3%) plus any FX spread"; a second currency conversion at payout "typically carries a spread of roughly 1% to 2%" | Checkout Page, 2026-06-08 | as above |

The two reports agree on the card rate. That matches the r = 2.9 %, f = $0.30 column already in §31's scenario table, so that column is now a *reported* rate rather than a purely illustrative one. It is still not Gumroad's own statement.

**Net per direct sale under the reported rates (INFERRED arithmetic, `q` = 0 for US direct deposit as reported):**

| P | after Gumroad 10% + $0.50 | card, 2.9% + $0.30 | PayPal, 3.49% + $0.49 |
|---|---|---|---|
| $9 | $7.60 | $7.04 | $6.80 |
| $12 | $10.30 | $9.65 | $9.39 |
| $15 | $13.00 | $12.27 | $11.99 |

**What this changes (PROPOSED):**
- §4: show the net as a range that depends on payment method: $9 → about $6.80–$7.04 *if the reported rates apply*. Keep the formula from §31 as the stated value until Gumroad's own text is read.
- §13 price floor: PayPal's reported fixed charge ($0.49) plus Gumroad's $0.50 takes 11 % of a $9 sale. That strengthens the case for $12 or a bundle. Price stays Timothy's call (§10).
- Records: a non-US payout path would add PayPal receiving fees and an FX spread. `ledger_map.py` (§32) already takes processing as a separate input and never estimates it. Payout fees would need the same treatment *only if* Timothy is paid outside US direct deposit. That is a question, not a change.
- §9.4 done-criteria: unchanged. Rate and payout rows need Gumroad's own text (help-article body or a real payout report).

**Next:** someone with a JavaScript-capable browser copies the processing and payout sentences from Gumroad's fees and "Getting paid" articles. Or, after launch, the first real payout report replaces every figure above.

Still open for Timothy (unchanged): TAM articles, the Unicorn Estate / RFC material, or both (R1); split the Collective or keep it as one (§28); cover image; book identifier; Article 4; price and refund window (§10). New: which payout method would apply (US direct deposit, PayPal, or other), only so the records step knows whether to expect payout fees.

Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax or financial advice.

## 34. Refinement — scheduled run 2026-10-15T17Z (Claude): what a refund costs under the 30-day window

§5 proposes a 30-day no-questions refund, and §32's `ledger_map.py` lists "refund fee treatment" as missing. This run looked for that one fact (read 2026-10-15T17Z with a page-reading fetch tool).

| Item | What the source says | Source | Evidence state |
|---|---|---|---|
| Does Gumroad's refund article cover fees? | Body renders client-side again; only the title "Issuing a refund - Gumroad Help Center" and a meta list of section headings, which include **"Refund fees"** and **"Handling negative balances"**, were readable | [Gumroad help, article 47](https://gumroad.com/help/article/47-how-to-refund-a-customer) | SOURCE-OBSERVED that a "Refund fees" section exists; its content UNVERIFIED |
| Are fees returned on a refund? | Third-party article quotes Gumroad's help docs as: "We don't refund any fees when processing refunds", covering "the 10% platform fee, the $0.50 flat fee, and the underlying card processing fee" | [Checkout Page](https://checkoutpage.com/blog/gumroad-fees), updated 2026-06-08; a Gumroad competitor | SOURCE-OBSERVED in a third-party article; UNVERIFIED as Gumroad's own text |
| Chargebacks | "Chargebacks pass through from the underlying processor at standard dispute costs" (no amount) | Checkout Page, 2026-06-08 | as above; amount UNVERIFIED |

**If the reported rule holds, a refund costs the seller every fee on that sale** (INFERRED arithmetic, card rate as reported in §33): the buyer gets `P` back, the seller had received `net`, so each refund is an out-of-pocket loss of `P − net`: $1.96 on a $9 sale, $2.35 on $12, $2.73 on $15.

**Expected net per sale at refund rate `x`** = `net − x·P` (INFERRED arithmetic; scenarios, not forecasts):

| P | net (card, §33) | x = 2 % | x = 5 % | x = 10 % |
|---|---|---|---|---|
| $9 | $7.04 | $6.86 | $6.59 | $6.14 |
| $12 | $9.65 | $9.41 | $9.05 | $8.45 |
| $15 | $12.27 | $11.97 | $11.52 | $10.77 |

**What this changes (PROPOSED, nothing edited in code this run):**
- §5 stays a 30-day no-questions window: even at a 10 % refund rate a $9 sale nets about $6.14, so the generous window costs little and protects reputation and processor standing. The §6 pause rule ("refund rate above an agreed threshold") gets a concrete number to agree on; PROPOSED 10 % over any rolling 30 days, Timothy decides.
- `ledger_map.py` (§32): once one real refund appears in an export, check whether the fee columns go negative. If they do not, record the reversing row as gross only (as now) and the month's net already reflects the retained fees; then drop "refund fee treatment" from `missing`. No guessing before that.
- The "Handling negative balances" heading means a refund can exceed the current balance; the records step should allow a negative month. `ledger/SCHEMA.md` already permits negative reversing rows, so no schema change.

Still open for Timothy (unchanged): TAM articles, the Unicorn Estate / RFC material, or both (R1); split the Collective or keep it as one (§28); cover image; book identifier; Article 4; price and refund window (§10); payout method (§33). New, optional: the refund-rate pause threshold (PROPOSED 10 %).

Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax or financial advice.

## 35. Refinement — scheduled run 2026-10-15T18Z (Claude): the refund-rate pause check, scripted and opt-in

§34 proposed a concrete §6 pause threshold (10 %, Timothy decides) and noted that a refund can push a month below zero. This run put both into the records step, without changing anything Timothy has not agreed to.

**What changed:** `Business/ideas/F-001-tam-build/ledger_map.py` takes an optional fourth argument `--refund-threshold=R` (a decimal strictly between 0 and 1). With it, each month in `ledger-month.json` also gets:
- `refund_rate` = refunds dated that month ÷ sales dated that month (4 decimals; `null` when the month has no sales);
- `pause_flag` = `refund_rate > R`, or `true` for a month with refunds but no sales, so it gets looked at;
- `negative_month` = that month's net is below zero.

Calendar months, not the rolling 30 days §34 described: simpler to audit against a monthly export. The flag only reports; pausing the listing stays Timothy's decision (§6). Without the option the output is the same as before.

**Tested (EXECUTION-VERIFIED, synthetic exports only, `python3 -I`):**
- two synthetic CSVs, run with the previous version (library-shared b88e2a1) and this one, no option: `ledger-rows.csv` and `ledger-month.json` byte-identical;
- with `--refund-threshold=0.10`: Nov 4 sales, 1 refund → `refund_rate` 0.2500, flagged; Dec 1 sale (fee cell empty, so net not counted and the fee listed as missing), 1 refund of a November sale → net −12.00, `negative_month` true, flagged;
- a single refunded sale → rate 1.0000, flagged, net −1.96 (fee retained; reversing row gross only, as before);
- `--refund-threshold=1.5` and an unknown option both stop with a clear message (exit 1).

**Caveat (INFERRED):** with few sales one refund crosses any threshold (1 of 4 is 25 %). PROPOSED for Timothy's agreement: read `pause_flag` only once a month has at least 20 sales, or keep using the number as information. Not coded, since the minimum is his call.

Still open for Timothy (unchanged): TAM articles, the Unicorn Estate / RFC material, or both (R1); split the Collective or keep it as one (§28); cover image; book identifier; Article 4; price and refund window (§10); payout method (§33); the refund-rate pause threshold (PROPOSED 10 %) and, new, a minimum monthly sales count before the flag counts (PROPOSED 20).

Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax or financial advice.

## 36. Refinement — scheduled run 2026-10-15T19Z (Claude): one decision sheet for Timothy

Thirty-five refinements have left Timothy's open questions spread over many sections, each repeating a slightly different "still open" list. This run gathered them into `Business/ideas/F-001-decision-sheet.md`: 15 questions in four groups (A: blocking, 5; B: before the first build is final, 6; C: records and operations, 4; D/E: what is done and the shortest path to a first listing). Each row names the options already proposed, the placeholder the drafts use meanwhile, and the section where it was raised. Nothing new is decided; defaults are placeholders for drafts, not decisions.

Check (EXECUTION-VERIFIED): every section reference in the sheet points to a heading that exists in this file (script check, 0 missing). The-TAM-protocol head is still d46456a.

Next F-001 step for a later run, if Timothy has not answered: none of the remaining work can proceed without A1–A5 except re-reading Gumroad's fees article body (§31) with a browser that runs JavaScript, which a scheduled run here cannot do. Later runs should therefore record "F-001: waiting on A1–A5" and spend income time on a second pipeline only if Timothy asks for one.

Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax or financial advice.

## 37. Refinement — scheduled run 2026-10-15T20Z (Claude): an unmerged TAM branch, and the licence it carries

**Finding (SOURCE-OBSERVED, read only).** Every earlier run read The-TAM-protocol `main` only (d46456a, 2026-01-18). The repository also has an unmerged branch `claude/github-claude-code-connection-98qkbx` @ 5f8612b (commits dated 2026-09-11, author Timothy, merge base d46456a). It reorganises the same material into `articles/`, `datasets/` and `reference/`, rewrites the README (336 → 695 words), and **adds an MIT `LICENSE` ("Copyright (c) 2026 Timothy (AGI144348Outlook)")**. `main` has no licence file.

**Measured differences (EXECUTION-VERIFIED, word counts and 6-word shingles, scratch only):**

| Item | main d46456a | branch 5f8612b |
|---|---|---|
| Articles 1, 2, 5, 6, 10 | 335 / 462 / 527 / 499 / 131 words | 347 / 476 / 537 / 512 / 134 (light edits, renamed files) |
| Collective information | 5,636 words | 2,856 words; only 34.4% of main's 6-word shingles survive, and 68.1% of the branch's come from main |
| LICENSE | none | MIT |

So the branch is a condensed, edited derivative; `main` remains the fuller source and stays the working source under R1. Nothing on either branch was changed (R3, and both repositories are read only for these runs).

**Why it matters for F-001 (PROPOSED, not a decision).**
1. An MIT licence lets anyone copy, modify **and sell** the text without paying. If the branch were merged, a paid ebook built from the same text could be legally reproduced for free by anyone. A public repository with no licence (today's `main`) keeps default copyright with Timothy, though the text stays readable by anyone.
2. Options for Timothy: (a) leave `main` unlicensed and do not merge the branch's LICENSE; (b) keep MIT for code-like material only and put the articles under a separate licence such as CC BY-NC-ND 4.0 (the licence recorded for the ByteByteGo system-design-101 notes at mirror Z28–Z31) or "all rights reserved"; (c) keep MIT deliberately and sell convenience (edited, packaged EPUB/PDF) rather than exclusivity. This is not legal advice.
3. The condensed `collective-information.md` may be a better editorial base for the book than the 5,636-word working notes, or it may have lost material Timothy wants; that is his call. The build tools in `F-001-tam-build/` read `main` paths and would need a path map for the branch layout (not built this run).

Recorded as decision-sheet item **A6** (addendum in `F-001-decision-sheet.md`). F-001 otherwise still waits on A1–A5.

Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## 38. Refinement — scheduled run 2026-10-15T21Z (Claude): the branch layout, run through the same build

§37 noted that the build tools read `main`'s file names and would need a path map for the branch layout. This run added `F-001-tam-build/layout_map.py`: it **copies** the 11 files of The-TAM-protocol branch `claude/github-claude-code-connection-98qkbx` (5f8612b) into a staging directory outside any repository under `main`'s names, so `build.py` runs on either layout unchanged. It never edits, moves or deletes anything in the source (R3). Only `LICENSE` and `.gitignore` stay unmapped (they have no `main` counterpart).

**Both layouts built with the unchanged `build.py` (EXECUTION-VERIFIED, scratch only, nothing committed from the outputs):**

| Check | main d46456a | branch 5f8612b (staged) |
|---|---|---|
| Build exit / EPUB written (pandoc) | 0 / 29,977 bytes | 0 / 34,048 bytes |
| Draft words | 7,953 | 5,844 |
| Dataset A / B as CSV | not written (no delimited table) | written: 7 and 9 rows incl. header |
| Article 6 sentences found in "Collective information" | 21 of 21 (+1 as text) | **0 of 22** |
| Article 10 sentences found in "Collective information" | 7 of 7 | **0 of 7** |
| Repeated lines in draft | 0 | 1 line, 2 extra copies (in README) |

**Finding that matters (EXECUTION-VERIFIED).** `build.py` leaves Articles 6 and 10 out as chapters (`DUP_ONLY`) because on `main` every long sentence of theirs is already inside "Collective information". On the branch the condensed `collective-information.md` no longer contains any of them, so **a build from the branch layout would silently drop Articles 6 and 10 from the book.** The build report already shows it (`dup_check.*.not_in_collective` is non-empty), but nothing stops the build.

**Also observed.** The branch turned both datasets into delimited Markdown tables, so the CSV appendices build automatically there (on `main` they still need hand-made columns, §15). The branch README has one line repeated three times.

**Proposed for a later run (PROPOSED, not done):** make `build.py` include a `DUP_ONLY` article as its own chapter whenever `not_in_collective` is non-empty, or fail with a clear message; test it on both layouts. Not done this run, to keep the change small and the existing tool unchanged.

Decision sheet: this adds evidence to **A6** (which branch is the source). If Timothy picks the branch, it gains ready CSVs but needs the fix above so Articles 6 and 10 are not lost. F-001 otherwise still waits on A1–A6.

Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §39 (2026-10-15T22Z, Claude): build.py no longer drops Articles 6 and 10 silently

Done the §38 proposal, smallest form: in `build.py`, a `DUP_ONLY` article whose `dup_check.not_in_collective` list is non-empty is now appended as its own chapter (after the main chapters, before the datasets), with a status line saying why, and the report gains `dup_only_included`. No other behaviour changed.

Tests (EXECUTION-VERIFIED, scratch only, outputs not committed; The-TAM-protocol main d46456a and branch 5f8612b staged with `layout_map.py`):

| Check | main d46456a | branch 5f8612b (staged) |
|---|---|---|
| Exit, old / new `build.py` | 0 / 0 | 0 / 0 |
| `tam-draft.md` old vs new | **byte-identical** | differs (chapters added) |
| `dup_only_included` | none | Article 6, Article 10 |
| Draft words, new | 7,953 | 6,544 (was 5,844) |
| Uncovered sentences now in the draft | n/a (0) | Article 6 22/22, Article 10 7/7 |
| `epub_check.py` on new branch build | — | 0 FAIL, 2 WARN |

Observed, not changed: the EPUB is not byte-reproducible run to run with either version (the identifier stays random per build until B6 is decided). Also observed: last run's commit 6f20d24 included `F-001-tam-build/__pycache__/layout_map.cpython-313.pyc`, a byproduct; it stays (R3, no deletions); this run used `python3 -B` so no new bytecode was written. PROPOSED: a `.gitignore` line for `__pycache__/` in this folder, if Timothy wants it.

Decision sheet: A6 still open; the branch layout is now buildable without losing text. Read-only note: both unmerged branches (The-TAM-protocol 5f8612b, dual-order-os 2d51593) are also open as pull request #1 in their repositories (`refs/pull/1/head`), not merged.

Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §40 (2026-10-15T23Z, Claude): a one-message reply card for the decision sheet

Nothing moved since §39 (The-TAM-protocol d46456a / 5f8612b, dual-order-os 2d92938 / 2d51593, no new ChatGPT artifact). F-001 now waits only on Timothy, so this run lowers the cost of answering instead of adding tooling. `F-001-decision-sheet.md` gains a reply card (addendum 23Z): the six blocking questions A1–A6 as one copy-and-edit block, each pre-filled with the draft default, so a single message (RUN-LOG, an Issue comment, or an edit to the sheet) settles them. A line left unchanged means "use the draft default"; a line deleted means "still open". B- and C-items are left off the card on purpose (§E of the sheet: they can take defaults for a review edition or wait for a first sale).

Checked (SOURCE-OBSERVED, this file and the sheet): every default on the card is the one already stated in the sheet's tables (A1 (a), A2 Gumroad, A3 placeholder, A4 speculative-reconstruction framing, A5 $9 / 30 days, A6 none chosen). No new option was invented.

Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §41 (2026-10-17T07Z, Claude): the two Dataset A rows, cross-checked by ChatGPT, and a disclosure line that needs no source edit

ChatGPT run 147 (`mirror-chatgpt-root:contract-000/gpt/business/F-001-PROGRESS-147.md`, commit 4b56a03) independently found the same two Dataset A mismatches as §16.2, with its own gate. Re-run this run at The-TAM-protocol d46456a (Dataset A blob `b62c970a`, Dataset B blob `12ef0fc2`, both unchanged): Silver Droplet −0.1460 % (stated −0.03 %), Small Scrap −0.1460 % (stated "<0.01 %"); the other four rows differ from their stated values by at most 0.006 percentage points (EXECUTION-VERIFIED arithmetic). Two participants, two scripts, same numbers: this row of the editorial worksheet can be marked cross-checked.

What it adds for the edition (INFERRED from the arithmetic, not a claim about the artefacts): the masses are given to 0.01 g, so a reading of 1.71 g stands for anything from 1.705 to 1.715 g, which is ±0.29 % of 1.7125 g; for 3.42 g it is ±0.15 % of 3.425 g. At that precision neither "−0.03 %" nor "<0.01 %" can be shown, and −0.146 % is inside the rounding band. So the honest note is about precision, not error.

Draft disclosure line for the dataset page (PROPOSED; the source text stays as it is, per R3 and §15.2):

> Deviations are computed against 13.7 g × units. Masses are given to 0.01 g, so for the two smallest pieces the rounding alone spans about ±0.3 % (1/8 U) and ±0.15 % (1/4 U); their stated deviations are finer than the data can show.

This fits A4's draft default (speculative-reconstruction framing with claimed / inferred / test-to-run marks) and needs no new decision; the open question from §16.3 (which reference the deviations use) is answered by stating it, unless Timothy prefers the two-decimal table value. A1–A6 remain the only blockers (decision sheet, reply card of §40).

Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §42 (2026-10-17T18Z, Claude): the claim worksheet counts, cross-checked by ChatGPT, and a grouped review order

ChatGPT run 158 (`mirror-chatgpt-root:contract-000/gpt/business/F-001-PROGRESS-158.md`, commit cfac832) ported `claim_scan.py`'s sentence splitter and four trigger patterns to JavaScript and counted 42 candidate occurrences, 35 distinct sentences and 7 duplicate pairs, and asked for a cross-check with the original scanner. Run this run, unchanged `F-001-tam-build/claim_scan.py` (blob 31f3dcf) under `python3 -I` on a read-only clone of The-TAM-protocol d46456a, output outside every repository (EXECUTION-VERIFIED):

- 42 rows; per file README 1, Article 1 2, Article 2 3, Color/Dental 3, Article 5 3, Article 6 3, Article 10 4, Collective 23 — identical to ChatGPT's per-file counts.
- Per trigger: superlative 20, accuracy 13, certainty 12, percent 2 (a row can carry more than one trigger).
- Whitespace-normalized exact deduplication: 35 distinct sentences; 7 duplicate pairs (14 rows), each pairing Article 6 or Article 10 with Collective information: Article 6 sentences 4 / 23 / 29 = Collective 153 / 172 / 178; Article 10 sentences 3 / 4 / 5 / 8 = Collective 293 / 294 / 295 / 298.

Two participants, two implementations, same counts: the worksheet's size row can be marked cross-checked. The scanner reads only the 8 prose files on purpose; the other 3 tree entries (Dataset A, Dataset B, the infographic URL list) are tables or links and are covered by §16 / §41 and the rights question, not by this worksheet.

What it changes for the editorial pass (PROPOSED): mark the 35 distinct sentences once each, and carry each mark to both occurrences of the 7 pairs, so Collective information never gets a different mark from the article it repeats. Suggested order: the 12 certainty rows first (they decide A4's framing in practice), then the 2 percent rows (§41 already drafts one disclosure), then accuracy, then superlative (most of these are ordinary words such as "only" and will likely be marked "no change"). ChatGPT's grouping utility (`f001_claim_grouping.py`, a local handoff not committed in its repository) is not read or run here; it is a reasonable next step once its source is published, after the fidelity gate as ChatGPT itself says.

A1–A6 remain the only blockers (decision sheet, reply card of §40). Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §43 (2026-10-18T02Z, Claude): ChatGPT's 44 / 37 claim count reproduced — escaped percent signs

ChatGPT run 166 (`mirror-chatgpt-root:contract-000/gpt/business/F-001-PROGRESS-166.md`, commit fc48f67) reports "42 original rows, 2 added candidates, 44 total, 37 distinct", against §42's 42 / 35. Reproduced this run (EXECUTION-VERIFIED, The-TAM-protocol @ d46456a, read-only clone in scratch):

- Cause: the source writes LaTeX-escaped percent signs (`20\%`, `13.7\%`, `>95\%`). `claim_scan.py`'s `percent` pattern `\d+(\.\d+)?\s?%` does not match a backslash before `%`, so those sentences were never flagged. The whole tree has 10 escaped-percent figures: 6 in Dataset A (a table, outside the 8 prose files on purpose, §42), 2 in Collective information, 1 in README, 1 in The Color Dyed and Dental Records.
- Test: a scratch copy with one changed pattern, `\d+(\.\d+)?\s?\\?%` (optional backslash), run on the same 8 files. Rows 42 → **44**; distinct sentences 35 → **37**; the 7 duplicate pairs unchanged. Matches ChatGPT's numbers exactly.
- The 2 added rows: The Color Dyed and Dental Records sentence 14 ("… the 'Metric Shock' represents a 20\% lo[ss] …") and Collective information sentence 90 ("In a 360-degree system, 13.7\% of the circumference is 49.3 degrees …"). Two existing rows also gain the `percent` trigger: README sentence 24 (">95\% correlation …", already flagged for accuracy) and Collective information sentence 100 (already flagged as superlative). Per trigger now: superlative 20, accuracy 13, certainty 12, **percent 6** (was 2).
- Fingerprints: patched scratch script sha256 `c379f65a39432780…`, its `claims.csv` `eeaf932a7e4280b2…`. The library copy of `claim_scan.py` (blob 31f3dcf) is **not edited** this run.

PROPOSED (for either participant, after registry entry and a logged change): adopt the optional-backslash pattern in `claim_scan.py` so the worksheet has 44 rows / 37 distinct, and mark §42's 42 / 35 as superseded, not removed. Side observation, not acted on: the `certainty` pattern matches "prove/proves/proved" but not "proving" (README sentence 24 says "proving"); it is flagged anyway through its other triggers, so the count does not change today.

A1–A6 remain the only blockers. Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.
