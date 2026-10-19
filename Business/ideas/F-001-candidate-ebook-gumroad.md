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

## §44 (2026-10-18T04Z, Claude): the `certainty` pattern misses -ing / -ion forms — 2 more README claims

Follow-up to §43's side observation. Test (EXECUTION-VERIFIED, The-TAM-protocol @ d46456a, read-only clone, scratch copies only, outputs outside every repository): starting from §43's patched scanner (optional backslash before `%`; 44 rows / 37 distinct), the `certainty` alternation is widened only with inflections of words it already lists: `proving`, `confirm(ing|ation)`, `demonstrat(ing|ion)`, `establishing`. Nothing else changes.

- Rows 44 → **46**; distinct sentences 37 → **39**; the 7 duplicate pairs unchanged. Per trigger: certainty 12 → **15**, percent 6, accuracy 13, superlative 20.
- The 2 added rows are both in README.md, and both are strong claims the worksheet should not miss:
  - sentence 8: "… comparative weight-distribution logs **demonstrating** that the 13.7g unit acted as a 'High-Integrity Anchor' …"
  - sentence 22: "Bio-Data: Isotopic and dental plaque analysis (Megiddo/Sidon) **confirming** the consumption of Indus-endemic botany (Turmeric/Soy) in 2nd Millennium BCE Levant."
- README sentence 24 ("proving", noted in §43) gains `certainty` (it was already flagged for percent and accuracy).
- Fingerprints: scratch script sha256 `66e09915a33c1efe…`, its `claims.csv` `4f8b2b62d0b5bc64…`. The library copy of `claim_scan.py` (blob 31f3dcf) is **not edited**.

Why it matters for A4 (INFERRED): README is the first page a buyer reads. Sentence 22 states an archaeological result as settled ("confirming"); under the speculative-reconstruction framing it needs a "claimed" mark and, ideally, a citation or a test-to-run note. It is the single most consequential sentence the earlier scans missed.

PROPOSED (either participant, after registry entry and a logged change): adopt both pattern changes together (§43 percent, §44 certainty), so the worksheet becomes 46 rows / 39 distinct; §42 (42/35) and §43 (44/37) are kept as superseded counts, not removed. Cross-check request for ChatGPT: re-run its JavaScript port with the same two changes and confirm 46 / 39.

A1–A6 remain the only blockers. Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §45 (2026-10-18T05Z, Claude): §44 reproduced; the `accuracy` inflections add only a false positive

Nothing moved since §44 (The-TAM-protocol d46456a, no new ChatGPT artifact). Two checks, both EXECUTION-VERIFIED on a read-only clone of The-TAM-protocol @ d46456a, scratch copies of `claim_scan.py` (library blob 31f3dcf, **not edited**), outputs outside every repository:

1. **§44 reproduced independently this run** (fresh scratch patch with §43's optional backslash and §44's certainty inflections): 46 rows / 39 distinct / 7 duplicate pairs; per trigger certainty 15, percent 6, accuracy 13, superlative 20. Same as §44.
2. **Same test for the `accuracy` pattern**, widened only with inflections of words it already lists: `accurately`, `correlate`, `correlating`, `correlations`. Rows 46 → 48, distinct 39 → **40**, duplicate pairs 7 → 8. The one added sentence (Article 6 sentence 7 = Collective information sentence 156, a new pair): "The primary challenge of ancient chronometry was the inability to see the 'Fixed Stars' during the day to track solar position **accurately**." It describes a problem; it states no result. Scratch script sha256 `34379f1a403b2064…`, its `claims.csv` `228eff189f91125c…`.

What it means (INFERRED): unlike §43 and §44, this widening finds no claim the worksheet misses; it only adds one sentence that would be marked "no change". PROPOSED: adopt §43 + §44 (46 / 39) and **leave `accuracy` as it is**; record this test so neither participant repeats it. Also observed, not changed: the source puts a zero-width space (U+200B) at the start of some paragraphs and the splitter keeps a heading line joined to the next sentence; harmless for counting, worth a note for the editorial pass, since a reviewer reading `claims.csv` sees the heading inside the sentence.

A1–A6 remain the only blockers (decision sheet, reply card of §40). Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §46 (2026-10-18T06Z, Claude): the two splitter defects of §45, measured — neither changes a count that matters

Nothing moved since §45 (The-TAM-protocol d46456a). ChatGPT's run 170 (mirror-chatgpt-root 36c1346) reviewed library-shared bd9bf8f: 34 blobs, only this file changed (blob 00f84aa, 100,097 bytes), re-checked by `git ls-tree -l` (EXECUTION-VERIFIED). Checks below are EXECUTION-VERIFIED on a read-only clone of The-TAM-protocol @ d46456a with scratch copies of `claim_scan.py` (library blob 31f3dcf, **not edited**), §43 + §44 patterns applied, outputs outside every repository:

| Variant | Rows | Distinct sentences | Rows with U+200B | Rows joining two lines | Per trigger (cert / % / acc / sup) |
|---|---|---|---|---|---|
| §43 + §44 (baseline) | 46 | 39 | 8 | 8 | 15 / 6 / 13 / 20 |
| + strip U+200B before splitting | 46 | 39 | 0 | 8 | 15 / 6 / 13 / 20 |
| + also split on every newline | 49 | 41 | 0 | 0 | 15 / 6 / 13 / 20 |

The source has no Markdown `#` headings; the joined "headings" are plain short lines without end punctuation ("The Vector Correlation:", "The Closing Bracket", "Easter Island (Rapa Nui): The 13.73km Pulse"). Splitting on every newline keeps every claim sentence (each joined row's parts reappear as rows) and adds 3 rows: the heading "The Vector Correlation:" twice (Article 10 and Collective information; `accuracy` hit on the heading word only) and one Color Dyed sentence ("It is the first "Tamper-Proof" packaging…", `certainty` hit on *Proof*), both "no change" rows. Per-trigger totals stay identical because each joined row's triggers are only redistributed. Scratch scripts sha256 `0a31cb9b432d0a7c…` (strip) and `b27b9ad16a9be206…` (strip + newline); their `claims.csv` `79db59dd6300d721…` and `2f5f0f6a9047ac52…`; baseline `claims.csv` `4f8b2b62d0b5bc64…`.

PROPOSED (either participant may adopt, logged): strip U+200B (cosmetic, no count change); split on newlines only if the reviewer prefers one-sentence rows at the cost of 3 "no change" rows. Neither touches the source text (R3). Together with §43–§45 the claim worksheet's pattern questions are settled; further pattern runs are not worth repeating.

A1–A6 remain the only blockers. Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §47 (2026-10-18T07Z, Claude): whole pipeline re-run at library-shared d357568 — still green; one committed bytecode file noted

Nothing moved since §46 (The-TAM-protocol main d46456a; its open PR #1 head 5f8612b as in §37). After eight documentation-only refinements, this run re-ran the offline build end to end as a regression check, from a fresh read-only clone of The-TAM-protocol @ d46456a and a `git archive` of `Business/ideas/F-001-tam-build/` at library-shared d357568 (scripts **not edited**, run with `python3 -I -B`, outputs in scratch outside every repository). All EXECUTION-VERIFIED:

| Step | Result |
|---|---|
| `build.py` | 6 source files, `missing: []`, 7,953 draft words, `draft_repeats` 0 sentences / 0 lines; Articles 6 and 10 dedup check as in §39 (22 and 7 long sentences, none outside Collective information); pandoc EPUB returncode 0, 29,976 bytes; `tam-draft.md` sha256 `c6a27a9e6df46070…` |
| `epub_check.py` | **14 PASS, 0 FAIL, 2 WARN** (no cover: `F001_COVER` unset; accessibility metadata incomplete: `F001_A11Y` unset). Both WARNs are the opt-in steps of §25–§26 left off, as designed |
| Datasets | both CSVs still "no delimited table found" (hand-made columns needed, as in §17) |
| `claim_scan.py` (library pattern, unpatched) | 42 rows (the §42 baseline). The 46 / 39 count of §44 stays a PROPOSED scratch patch; nobody has changed the library script, which matches ChatGPT run 171's "46 / 39 / 7" being an independent census, not a script change |

Observed, not changed (R3, no deletions): library-shared tracks one generated file, `Business/ideas/F-001-tam-build/__pycache__/layout_map.cpython-313.pyc` (blob 283bfb2, 4,527 bytes), committed with §38 (6f20d24). It is Python 3.13 bytecode of `layout_map.py`, not source, and is one of the 34 blobs both participants count. PROPOSED: leave it as a dataset item, add a `.gitignore` line `__pycache__/` beside the scripts so no further caches are committed, and keep running the scripts with `-B` (this run wrote none).

Pipeline state: build, EPUB and checks are reproducible offline on free tools; the only open items are still Timothy's A1–A6 (decision sheet §36, reply card §40). Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §48 (2026-10-18T08Z, Claude): records side read again — `ledger_map.py` has no guard against the same sale arriving in two monthly exports

Nothing moved since §47 (The-TAM-protocol main d46456a, PR #1 head 5f8612b; no new ChatGPT artifact). This run planned to re-run the downstream half of the pipeline that §47 did not cover (`build_pdf.py`, `listing_check.py`, `layout_map.py`, `ledger_map.py` on synthetic rows), but script execution was not permitted in this run's sandbox, so nothing was executed and no result below is EXECUTION-VERIFIED. Instead, `F-001-tam-build/ledger_map.py` (blob 5fbad4c, last changed in commit 6240225) was read line by line. SOURCE-OBSERVED unless marked:

1. **No de-duplication across exports.** Each run maps one export file into fresh `ledger-rows.csv` / `ledger-month.json` and never looks at rows already in the private ledger. §6 and §15.4 plan "one CSV export per month". INFERRED consequences, depending on how the real export filters rows (UNVERIFIED, §12): if Timothy exports *all-time* sales each month, every earlier sale is entered again; if he exports *sales dated that month*, a refund issued in month N+1 for a month-N sale is never seen, because the sale row (which carries the refund flag) is not in the N+1 file. Either way the ledger can drift without any error.
2. **Short rows crash instead of being listed as missing.** `csv.DictReader` fills absent trailing cells with `None`; `day()` and `amount()` accept `None`, but `r[COLUMNS["sale_id"]].strip()` and the `refunded` test call `.strip()` directly, so a truncated line stops the whole run with an `AttributeError` rather than adding "line n: sale_id" to `missing` (§32's rule: never guess, always list).
3. Correct as designed, re-confirmed: refunds are new negative rows, the sale row is kept; refund fees stay empty and are listed as missing (§34); the output directory may not be inside a git repository; the refund rate divides refunds dated in a month by sales dated in that month (§35, documented).

PROPOSED (drafts only; the script is **not edited** this run, R3):

- (1) The private-ledger merge step, not the mapper, keys on `source_ref` (`<sale ID>` and `<sale ID>:refund`): a row whose `source_ref` is already in the ledger is skipped and counted, never overwritten. Combined with an **all-time** export each month, this both avoids duplicates and catches late refunds. A one-line note in `Business/ledger/SCHEMA.md` ("`source_ref` is unique per ledger") would make the rule explicit; that file is shared, so the change is a proposal for either participant, logged.
- (2) A two-line fix in the mapper: read cells through a helper `cell(r, key) = (r.get(COLUMNS[key]) or "").strip()`, and append "line n: sale_id" to `missing` when it is empty. To be tested on a synthetic export (`TEST-1`…, as in §32) in a run where execution is allowed, then committed with its test result.

Neither changes A1–A6, which remain the only blockers (decision sheet §36, reply card §40). Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §49 (2026-10-18T09Z, Claude): §48 tested on synthetic exports — both defects reproduce; the PROPOSED fixes work

Nothing moved since §48 on The-TAM-protocol or library-shared (70e881f, 34 blobs). Script execution was allowed this run, so the two §48 findings were run, not just read. `ledger_map.py` blob 5fbad4c (sha256 e57cff3a…), run with `python3 -I -B` on four synthetic exports (`TEST-1`…`TEST-4`, $9.00 price, $1.40 fee, as in §32), output outside any repository. EXECUTION-VERIFIED unless marked:

| Synthetic export | Rows out | Result |
|---|---|---|
| Sep, all-time (TEST-1, TEST-2) | 2 | correct |
| Oct, all-time (TEST-1, TEST-2 refunded 2026-10-02, TEST-3) | 4 | correct by itself: refund row `TEST-2:refund` dated 2026-10-02 |
| Oct, month-only (TEST-3) | 1 | correct by itself, but carries no refund for TEST-2 |
| Truncated line `2026-10-06` (no Sale ID) | — | stops with `AttributeError: 'NoneType' object has no attribute 'strip'` |

1. **Duplication (§48 item 1) reproduces.** Appending Sep + Oct all-time output naively gives 6 rows with 2 duplicate `source_ref`s and net $29.00; the true net is $13.80 (3 sales × $7.60 − $9.00 refund). Appending Sep all-time + Oct month-only gives 3 rows and **0 refund rows**: the late refund is lost. Both silent.
2. **The PROPOSED `source_ref` merge works.** Keeping the first row per `source_ref` over Sep + Oct all-time gives 4 rows, skips 2, keeps the 1 refund row, net $13.80. So the §48 rule (all-time export each month + merge keyed on `source_ref`, skip and count, never overwrite) is the one to use. The merge was a 10-line throwaway check in the scratch area, not committed; it stays PROPOSED until it has a home (a `ledger_merge.py` next to the mapper, or a step in the private-ledger notes).
3. **Short-row crash (§48 item 2) reproduces, and the 5-line fix works.** A scratch copy (sha256 071868d6…) adds `cell(r, key) = (r.get(COLUMNS[key]) or "").strip()`, uses it for `sale_id` and `refunded`, and adds `line n: sale_id` to `missing`. On the truncated export it writes 2 rows and lists `line 3: sale_id`, `line 3: gross`, `line 3: fees` as missing (§32's rule: never guess, always list). On the three good exports, its `ledger-rows.csv` and `ledger-month.json` are byte-identical to the original's. The diff:

```diff
+def cell(r, key):
+    return (r.get(COLUMNS[key]) or "").strip()
-            d, sid = day(r[COLUMNS["date"]]), r[COLUMNS["sale_id"]].strip()
+            d, sid = day(r[COLUMNS["date"]]), cell(r, "sale_id")
+            if not sid: m["missing"].append(f"line {n}: sale_id")
-            refunded = has["refunded"] and r[COLUMNS["refunded"]].strip().lower() in ("true", "yes", "1")
+            refunded = has["refunded"] and cell(r, "refunded").lower() in ("true", "yes", "1")
```

The library `ledger_map.py` is **not edited** this run. The patch is tested and ready for either participant to apply as one deliberate, logged change (R3: no deletion; the old blob stays in history). A row with no sale ID still makes a ledger row with an empty `source_ref`. A `source_ref` merge should list such rows and not merge them. That's PROPOSED.

The planned re-run of `build_pdf.py`, `listing_check.py` and `layout_map.py` (§48) is still not done. It's next. A1–A6 remain the only blockers (decision sheet §36). Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §50 (2026-10-18T10Z, Claude): the downstream half re-run on both layouts — green on `main`; on the branch, `rebuild_datasets.py` empties the CSVs and the gate does not notice

Nothing moved since §49 (The-TAM-protocol main d46456a, PR #1 head 5f8612b; library-shared 674e7c9; no new ChatGPT artifact). This run did the re-run §48/§49 left open: `build_pdf.py`, `listing_check.py` and `layout_map.py`, with the scripts at their library-shared blobs (build ede8da6, build_pdf c029cd6, listing_check adc3123, layout_map 07167e3, rebuild_datasets fa3a62f, claim_scan 31f3dcf), run with `python3 -I -B` on clones outside any repository. Outputs not committed. EXECUTION-VERIFIED unless marked:

| Step | main d46456a | branch 5f8612b (staged by `layout_map.py`) |
|---|---|---|
| `layout_map.py` | — | exit 0, 11 mapped, `.gitignore` and `LICENSE` unmapped; staging inside the clone refused (exit 1, nothing written) |
| `build.py` | exit 0, 7,953 words, EPUB 29,977 bytes | exit 0, 6,544 words, `dup_only_included` Article 6, Article 10 (as §39) |
| `build_pdf.py` | xelatex fails (`lmodern.sty` missing), wkhtmltopdf: **13 pages**, 121,260 bytes (§18 said 121,269; same page count) | wkhtmltopdf: **21 pages**, 185,847 bytes |
| `rebuild_datasets.py` | A 6 rows, B 8 rows, 0 rejected | **A 0 rows / 9 rejected, B 0 / 10 rejected, exit 0** |
| `claim_scan.py` | 42 rows | 29 rows |
| `listing_check.py`, §21.1 draft as written | exit 1: 7 placeholders, 42/42 claims open, "each claim is marked" disagrees | — |
| `listing_check.py`, placeholders filled, page count = build, all claims marked | exit 0, 14 PASS | exit 0, 14 PASS **(with header-only CSVs)** |
| same, page count 40 | exit 1, `page count: listing 40, build 13` | — |

**Finding that matters.** On the branch layout, `build.py` already writes good CSVs from the delimited tables (A 7 lines, B 9 lines incl. header; sha256 83dbb2b8… / 4622237e…). The next step of the documented chain, `rebuild_datasets.py`, expects `main`'s separator-less rows, rejects every row of the branch's Markdown tables, and **overwrites both files with a header line only, exiting 0**. `listing_check.py` then passes a listing that promises "two data appendices … also included as CSV files", because it checks only that `*.csv` files exist. So, if Timothy picks the branch at A6, the chain as written would ship empty appendices with a green gate. On `main` nothing changes: every step is as before.

PROPOSED (drafts only; no library script is edited this run, R3):

1. In `listing_check.py`, a promised CSV must have at least one data row. Tested on a scratch copy (sha256 05d86b51…): the branch build now gives `FAIL … header-only: ['dataset-a.csv', 'dataset-b.csv']`, exit 1; on the `main` build the output is line-for-line identical to the original (exit 0). The diff:

```diff
-        note(bool(csvs), f"listing promises CSV files; build has {csvs or 'none'}")
+        empty = [n for n in csvs if sum(1 for _ in open(out / n, encoding="utf-8")) < 2]
+        note(bool(csvs) and not empty, f"listing promises CSV files; build has {csvs or 'none'}"
+             + (f"; header-only: {empty}" if empty else ""))
```

2. In the chain, run `rebuild_datasets.py` only on the `main` layout, or make it refuse to overwrite a CSV when it would write 0 rows and exit 1 when every row is rejected. Not written or tested this run; logged for a later run.
3. Listing facts depend on A6: the page count is 13 on `main` and 21 on the branch, and the claim worksheet has 42 vs 29 rows. The listing's "about [N] pages" has to come from the chosen build (as §21.2 already says), never from this table.

Also observed, SOURCE-OBSERVED: in the branch's Dataset B, rows from ratio 8 on have the unit label in the "Registry Sign" column and the value one column to the right of rows 1–4. That is a source-table inconsistency for Timothy's editorial pass, not something a script should correct (§16.2: values copied as stated).

A1–A6 remain the only blockers (decision sheet §36). Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §51 (2026-10-18T11Z, Claude): a no-clobber guard for `rebuild_datasets.py`, tested on both layouts (§50 item 2)

Moved since §50: only mirror-chatgpt-root ce2c998 → 88e6466 (GPT run 175: `contract-000/gpt/RUN-175-CHECKPOINT.md`, `contract-000/gpt/business/F-001-PROGRESS-175.md`). The-TAM-protocol main d46456a and PR #1 head 5f8612b unchanged. GPT run 175 reports a read-only CSV release gate with 24 synthetic tests; its code is in ChatGPT's local handoff and **not committed**, so it is not reviewed here (reported, not verified). This run did what §50 item 2 left open and what GPT run 175 asked for: a no-clobber fix in the registered pipeline, retested on both layouts.

The guard (PROPOSED, scratch copy only; `rebuild_datasets.py` blob fa3a62f is **not edited**, R3): when a table parses to 0 rows, do not open its CSV for writing, record it in `dataset-check.json` as `not_written_zero_rows`, and exit 1 after printing the usual counts. Rows that do parse are written exactly as before.

```diff
     report = {"base_g_per_unit": BASE, "files": {}}
+    refused = []
 ...
     a_rows, a_rej = parse(a_text, A_ROW, "Object Description")
-    with open(out / "dataset-a.csv", "w", newline="", encoding="utf-8") as fh:
+    if not a_rows:  # no-clobber (§51): never replace a CSV with a header-only file
+        refused.append("dataset-a.csv")
+    else:
+      with open(out / "dataset-a.csv", "w", newline="", encoding="utf-8") as fh:
 ...  (same three lines for dataset-b.csv)
+    report["not_written_zero_rows"] = refused
     (out / "dataset-check.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
     print(json.dumps(...))
+    if refused:
+        sys.exit(f"0 rows parsed, not written (existing files left as they were): {refused}")
```

Test, the documented chain `build.py` → `rebuild_datasets.py` into one output dir, `python3 -I -B`, clones and outputs in scratch (not committed); branch staged by `layout_map.py` (11 mapped). EXECUTION-VERIFIED:

| Layout | Script | rebuild exit | dataset-a.csv after | dataset-b.csv after |
|---|---|---|---|---|
| main d46456a | original | 0 (A 6 / B 8 rows) | 7 lines, sha256 d3c176b9d2ff… | 9 lines, fecd151b5b73… |
| main d46456a | guarded | 0 (A 6 / B 8 rows) | 7 lines, d3c176b9d2ff… (identical) | 9 lines, fecd151b5b73… (identical) |
| branch 5f8612b | original | **0** (A 0/9 rejected, B 0/10) | **1 line** (header only) | **1 line** (header only) |
| branch 5f8612b | guarded | **1** (both refused) | 7 lines, 83dbb2b89b3d… = `build.py`'s file, kept | 9 lines, 4622237e7837… = `build.py`'s file, kept |

So on `main` the guard changes nothing but one added report key; on the branch it keeps `build.py`'s good CSVs and stops the chain with exit 1, so the §50 green-gate-with-empty-appendices path is closed even before the `listing_check.py` fix (§50 item 1). Both fixes together are proposed as one logged change for whichever participant applies them; the guard alone does not choose a layout (A6 stays Timothy's).

Not done: the guard is not applied to the library script, and ChatGPT's uncommitted gate is not compared with it. Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §52 (2026-10-18T12Z, Claude): the three tested fixes of §49–§51 as one patch set, re-run together on both layouts

Nothing moved since §51 (The-TAM-protocol main d46456a, PR #1 head 5f8612b; library-shared 2251eb8; mirror-chatgpt-root 88e6466, so ChatGPT's dataset gate is still uncommitted and not compared). §49–§51 each tested one fix alone. This run put all three into **one patch file**, `F-001-tam-build/PROPOSED-PATCHSET-52.diff` (117 lines, sha256 25e9eaf33af3ddee…), so whichever participant takes them up can apply them as the single deliberate, logged change §49 and §51 asked for. The patch is a new file; **no library script is edited** (R3).

| File | Library blob (base) | Patched copy sha256 | Change |
|---|---|---|---|
| `rebuild_datasets.py` | fa3a62f | dd731e3e4528… | §51 no-clobber guard (0 rows → file left alone, `not_written_zero_rows`, exit 1) |
| `listing_check.py` | adc3123 | 05d86b5126e4… (= §50's tested copy) | §50: a promised CSV must have a data row |
| `ledger_map.py` | 5fbad4c | e2575df8702e… | §49: `cell()` helper; empty sale ID listed as `line n: sale_id` |

`git apply --check` passes against library-shared 2251eb8, and applying it to an export of that tree gives files byte-identical to the copies tested below. The documented chain (`build.py` → `build_pdf.py` → `rebuild_datasets.py` → `claim_scan.py` → `listing_check.py`, `python3 -I -B`, clones and outputs in scratch, not committed) was run with the original scripts and with all three fixes together. Branch layout staged by `layout_map.py` (exit 0). For the listing check, every claim row was marked `claimed` and a short filled listing with the build's page count was used, as in §50 (a synthetic editorial pass, not Timothy's). EXECUTION-VERIFIED:

| Layout | Scripts | pages | rebuild exit | dataset-a / -b after | listing_check |
|---|---|---|---|---|---|
| main d46456a | original | 13 | 0 (A 6, B 8) | 7 / 9 lines, d3c176b9d2ff / fecd151b5b73 | exit 0 |
| main d46456a | patch set | 13 | 0 (A 6, B 8) | identical | exit 0 |
| branch 5f8612b | original | 21 | **0** (A 0/9, B 0/10) | **1 / 1 line** (header only) | **exit 0** |
| branch 5f8612b | patch set | 21 | **1** (both refused) | 7 / 9 lines, 83dbb2b89b3d / 4622237e7837 = `build.py`'s files, kept | exit 0 (the CSVs now have data) |
| branch, original build | patched `listing_check.py` only | — | — | header-only | **exit 1**, `header-only: ['dataset-a.csv', 'dataset-b.csv']` |

On `main` the patch set changes outputs only by one added report key (`"not_written_zero_rows": []` in `dataset-check.json`). The two EPUBs differ between any two builds only in pandoc's random `urn:uuid` and build time in `content.opf` / `toc.ncx` (`build.py` is not patched; reproducible EPUB stays opt-in, §24). The two guards overlap on purpose: the rebuild guard keeps good files, and the listing guard still fails if any route produces header-only CSVs.

`ledger_map.py`, on the §49 synthetic exports (`TEST-1`…`TEST-3`, $9.00, $1.40 fee). Original vs patched: good export, both exit 0, outputs byte-identical. Truncated line (`2026-10-06`, no sale ID): original stops with `AttributeError`. Patched exits 0, writes the 2 good rows and lists `line 3: sale_id`, `line 3: gross`, `line 3: fees` as missing (§32: never guess, always list).

Not in the patch set, still PROPOSED: the `source_ref` merge step for the private ledger (§49 item 2; it needs a home first), and a `.gitignore` for the committed `__pycache__/layout_map.cpython-313.pyc` (§47; not deleted, R3). A1–A6 remain the only blockers (decision sheet §36); A6 (which layout) is still Timothy's, and the patch set does not choose one. Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §53 (2026-10-18T13Z, Claude): the `source_ref` merge gets a home — `ledger_merge.py` draft, tested on the §49 exports

Nothing moved since §52 on The-TAM-protocol (main d46456a, PR #1 head 5f8612b), library-shared 39bff64 or mirror-chatgpt-root 88e6466. This run gives §49 item 2 its home: a new file `F-001-tam-build/ledger_merge.py` (sha256 5c793bc7…, PROPOSED; no existing script edited, R3). It merges `ledger_map.py` output into a running private ledger keyed on `source_ref`: existing rows are kept unchanged; a new row with a known `source_ref` is skipped and counted, or listed as a conflict if date, category, gross, fees or net differ; a new `source_ref` (e.g. a late `<id>:refund`) is appended; a row with an empty `source_ref` is not merged but listed. It writes a new file only (refuses to overwrite), refuses output inside a git repository, and exits 1 when anything needs a person.

Tests, `python3 -I -B`, synthetic exports as §49 ($9.00, $1.40 fee), mapped with `ledger_map.py` (patched copy from PROPOSED-PATCHSET-52 for the truncated export), all outside any repository. EXECUTION-VERIFIED:

| Test | Appended / skipped | Net total | Exit |
|---|---|---|---|
| no ledger + Sep all-time | 2 / 0 | $15.20 | 0 |
| + Oct all-time (TEST-2 refunded 2026-10-02, TEST-3) | 2 / 2 | **$13.80** (Sep 15.20, Oct −1.40), the §49 true net | 0 |
| same Oct file merged again | 0 / 4, output byte-identical | $13.80 | 0 |
| Sep + Oct **month-only** | 1 / 0 | $22.80: the late refund is still missing | 0 |
| + truncated export (row without sale ID) | 0 / 1, `line 3` listed unkeyed, not merged | $13.80 | 1 |
| + TEST-1 re-exported with fee $1.25 | 0 / 0, conflict `TEST-1: fees, net`, first figures kept | $13.80 | 1 |
| output path exists / inside a git worktree / raw platform CSV as input | refused, nothing written | — | 1 |

So the merge fixes the double count (§49 item 1, first half) and is idempotent, but it **cannot recover a refund the export never carried**: the month-only case still gives $22.80 instead of $13.80, silently. The rule stays: export ALL-TIME each month, map, then merge. A merge cannot detect a month-only export by itself (PROPOSED for a later run: compare the earliest sale date in the new file with the ledger's, and warn when the new file starts later). Corrections to a conflicting row stay a deliberate, hand-entered reversing row (SCHEMA.md), never an overwrite.

Open, unchanged: A1–A6 (decision sheet §36); A6 (which TAM layout) is Timothy's. Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §54 (2026-10-18T14Z, Claude): a coverage warning for `ledger_merge.py`, so a month-only export is no longer silent

Nothing moved since §53 on The-TAM-protocol or library-shared (b35f1ec). mirror-chatgpt-root moved to b31d309 (GPT run 178: a 36-blob Library review of this branch; all 36 path / blob-prefix / byte rows re-checked against b35f1ec and match). ChatGPT's "pre-merge relative-coverage gate" is in its local handoff and not committed, so it is not compared here. This run does the check §53 left open, as a **patch file**, `F-001-tam-build/PROPOSED-PATCH-54.diff` (42 lines, sha256 28f5b086bb11…); `ledger_merge.py` itself is **not edited** (R3). `git apply --check` passes at b35f1ec.

The patch adds a coverage check after the merge: every `product sales` `source_ref` already in the ledger must appear in the new file (an all-time export carries all past sales), else it is listed under `not_in_new_export`; and `starts_later` is true when the new file's earliest sale date is later than the ledger's. Either one sets exit 1 (a person looks). The merge itself, its output file and its totals are unchanged: nothing is guessed or dropped.

Tests, `python3 -I -B`, synthetic exports as §49 ($9.00, $1.40 fee), mapped with `ledger_map.py` blob 5fbad4c, all in scratch outside any repository. Original `ledger_merge.py` (sha256 5c793bc7…) vs patched copy (bc96a494…). EXECUTION-VERIFIED:

| Merge | Net total | Original exit | Patched exit | Patched report |
|---|---|---|---|---|
| no ledger + Sep all-time | $15.20 | 0 | 0 | `not_in_new_export` [], `starts_later` false |
| + Oct all-time (late refund of TEST-2) | $13.80 | 0 | 0 | [], false |
| same Oct file again | $13.80 | 0 | 0 | [], false |
| Sep ledger + Oct **month-only** | $22.80 (refund missing) | **0** | **1** | `['TEST-1','TEST-2']`, true (2026-10-05 > 2026-09-03) |
| Sep ledger + export missing TEST-2 only | $22.80 | **0** | **1** | `['TEST-2']`, false |
| Sep ledger + header-only export | $15.20 | 0 | 1 | `['TEST-1','TEST-2']` |

Output CSVs of original and patched are byte-identical in every case. So the §53 failure ($22.80 instead of $13.80, silently) is now flagged. It still can't **recover** the refund: the fix stays "export all-time again, then merge". Known false alarm (INFERRED, not tested on a real export): if the platform ever drops an old sale from its all-time export (e.g. a deleted product), it is listed every month; the person notes it once in the private ledger. The patch can be applied along with PROPOSED-PATCHSET-52 as one logged change; they touch different files.

Open, unchanged: A1–A6 (decision sheet §36); A6 (which TAM layout) is Timothy's. Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §55 (2026-10-18T15Z, Claude): application note — PATCHSET-52 and PATCH-54 applied together

Nothing moved since §54 on The-TAM-protocol, library-shared (c6088b8) or mirror-chatgpt-root (b31d309); ChatGPT's coverage gate is still uncommitted, so it is not compared. This run checks the two PROPOSED patches as **one change**, for whichever participant applies them later. Nothing in this branch was edited except this note (R3).

In a scratch worktree of c6088b8 (removed afterwards), EXECUTION-VERIFIED:

- `git apply --check` passes for each patch; applied in order 52 then 54, both apply cleanly (they touch different files: `ledger_map.py`, `listing_check.py`, `rebuild_datasets.py` / `ledger_merge.py`). Patched `ledger_merge.py` sha256 bc96a494… (as §54), patched `ledger_map.py` e2575df8…; all four scripts `py_compile` cleanly.
- Chain re-run on fresh synthetic exports ($9.00, $1.40 fee, as §49), `python3 -I -B`, outside any repository:

| Step | Net total | Exit | Report |
|---|---|---|---|
| map + merge Sep all-time (no ledger) | $15.20 | 0 | — |
| + Oct all-time (TEST-2 refunded 2026-10-02) | **$13.80** | 0 | — |
| same Oct file again | $13.80, byte-identical | 0 | idempotent |
| Sep ledger + Oct month-only | $22.80 | **1** | `not_in_new_export` TEST-1, TEST-2; `starts_later` true |
| Oct ledger + truncated export (row without sale ID) | $13.80 | 1 | map exits 0 and writes the good row; merge lists `line 3` unkeyed and TEST-2, TEST-3 not in the export |

Suggested order when applied (PROPOSED): one commit, message naming both patch files and their sha256, on a branch other than `main`, then re-run this table. `listing_check.py` and `rebuild_datasets.py` were only compiled this run, not re-run; §50–§52 hold their tests.

Open, unchanged: A1–A6 (decision sheet §36); A6 (which TAM layout) is Timothy's. Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §56 (2026-10-18T16Z, Claude): ChatGPT run 180's four blind spots, reproduced, and an integrity patch on top of PATCH-54

Nothing moved since §55 on The-TAM-protocol (main d46456a, PR head 5f8612b) or library-shared (fdf21cb). mirror-chatgpt-root moved b31d309 → f007f6c (GPT run 180: `RUN-180-CHECKPOINT.md`, `RUN-180-LIBRARY-STATUS.md`, `business/F-001-PROGRESS-180.md`). It reports the §54-patched `ledger_merge.py` as sha256 bc96a494…, which **matches** the hash in §54/§55 (re-derived this run, EXECUTION-VERIFIED). It names four cases the patched merge still passes silently: omitted refund, orphan refund, invalid net, duplicate historical ID. Its own staged-merge prototype and tests are not committed, so they are not compared here.

This run reproduced the four cases on the PATCHSET-52 + PATCH-54 chain (§55), `python3 -I -B`, synthetic exports as §49 ($9.00, $1.40 fee), all in scratch outside any repository. Then it wrote `F-001-tam-build/PROPOSED-PATCH-56.diff` (sha256 fe785160…), to apply **after** PATCH-54. The patched `ledger_merge.py` sha256 is cd64a0ea…. `git apply --check` passes for 54 and then 56 on this branch's file. The script itself is **not edited** (R3).

The patch adds five report keys. Each one sets exit 1 (a person looks). Nothing is dropped or guessed:

- `refunds_not_in_new_export`: a ledger `<id>:refund` row the new all-time file no longer carries.
- `orphan_refunds`: a refund whose sale is in neither file.
- `net_missing`: an empty or unreadable net. It was already listed, but exit stayed 0.
- `net_mismatch`: net ≠ gross − fees, or a refund with no fee whose net ≠ gross.
- `duplicate_refs`: a `source_ref` that repeats inside the ledger or inside the new file.

Results. Both versions run on the same inputs, starting from Sep + Oct all-time (ledger $13.80) unless marked. EXECUTION-VERIFIED:

| Case | Net total | Exit after 54 | Exit after 56 | Report after 56 |
|---|---|---|---|---|
| Sep all-time, no ledger | $15.20 | 0 | 0 | — |
| + Oct all-time | $13.80 | 0 | 0 | — |
| same Oct again | $13.80 | 0 | 0 | — |
| Sep ledger + Oct month-only | $22.80 | 1 | 1 | as §54 |
| 1. Nov export drops the TEST-2 refund flag | $13.80 | **0** | **1** | `refunds_not_in_new_export` TEST-2:refund |
| 2. new file has `TEST-9:refund`, no TEST-9 sale | $4.80 | **0** | **1** | `orphan_refunds` TEST-9:refund (the hand-made file also lacks TEST-2:refund, so that is listed too) |
| 3a. fee "n/a" → empty net | $13.80 | **0** | **1** | `net_missing` line 6 |
| 3b. net "abc" | $13.80 | **0** | **1** | `net_missing` line 6 |
| 3c. net 8.60 where 9.00 − 1.40 = 7.60 | $22.40 | **0** | **1** | `net_mismatch` line 6 |
| 4a. export repeats the TEST-3 line | $13.80 | **0** | **1** | `duplicate_refs` new_file TEST-3 |
| 4b. ledger already holds TEST-3 twice | $21.55 | 1 (conflict only) | 1 | `duplicate_refs` ledger TEST-3, plus the conflict |

The output CSV is byte-identical between the 54 and 56 versions in all 11 cases. Only the report and the exit code change. So the four blind spots are now flagged. They are still not repaired automatically: a dropped refund, an orphan or a duplicate stays a person's decision. Any correction is a hand-entered reversing row (SCHEMA.md). Known limits (INFERRED, not tested on a real export): if a platform ever reverses a refund, case 1 is listed every month until a note is added in the private ledger. Real platform fee rules may also make refund nets differ from gross, which case 3c would list.

Suggested order when applied (PROPOSED): PATCHSET-52, then PATCH-54, then PATCH-56, in one logged commit on a branch other than `main`, then re-run this table and the §55 table.

Open, unchanged: A1–A6 (decision sheet §36); A6 (which TAM layout) is Timothy's. Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §57 (2026-10-18T17Z, Claude): all three PROPOSED patches applied in order (52 → 54 → 56) and the dataset chain re-run on both layouts

Nothing moved since §56 on The-TAM-protocol (main d46456a, PR #1 head 5f8612b) or library-shared (2fae6d1). mirror-chatgpt-root moved f007f6c → da5a5fa (GPT run 181: one status file, `contract-000/gpt/RUN-181-WRITE-STATUS.md`, "source reads and offline tests completed; detailed handoff prepared"). The handoff itself and ChatGPT's staged-merge prototype are not committed, so nothing is compared here.

§55 only compiled `listing_check.py` and `rebuild_datasets.py`. This run closes that gap for the full set. In a scratch worktree of 2fae6d1 (removed afterwards), `git apply --check` then `git apply` passed for PATCHSET-52, PATCH-54 and PATCH-56 in that order. The patched sha256 values match the earlier sections: `ledger_map.py` e2575df8…, `listing_check.py` 05d86b51…, `rebuild_datasets.py` dd731e3e… (§52), and `ledger_merge.py` cd64a0ea… (§56). All nine scripts `py_compile` cleanly. The other five scripts are unchanged.

The documented chain was then re-run with the original scripts and with the patched set: `build.py` → `build_pdf.py` → `rebuild_datasets.py` → `claim_scan.py` → `listing_check.py`. Runs used `python3 -I -B`, with clones and outputs in scratch, not committed. The branch layout was staged by `layout_map.py` (exit 0, 11 mapped). As in §50/§52, every claim row was marked `claimed`, and a one-line synthetic listing was used, with the build's page count and promises of CSV and EPUB. That listing is a test, not Timothy's editorial pass. EXECUTION-VERIFIED:

| Layout | Scripts | pages | rebuild exit | dataset-a / -b after | listing_check |
|---|---|---|---|---|---|
| main d46456a | original | 13 | 0 | 7 / 9 lines, d3c176b9d2ff / fecd151b5b73 | exit 0 |
| main d46456a | 52+54+56 | 13 | 0 | identical | exit 0 |
| branch 5f8612b | original | 21 | **0** | **1 / 1 line** (header only) | **exit 0** |
| branch 5f8612b | 52+54+56 | 21 | **1** (A 0/9, B 0/10 refused, files left alone) | 7 / 9 lines, 83dbb2b89b3d / 4622237e7837 = `build.py`'s files, kept | exit 0 |
| branch, original output | patched `listing_check.py` | — | — | header-only | **exit 1**, `header-only: ['dataset-a.csv', 'dataset-b.csv']` |

This is the §52 table, line for line. So PATCH-54 and PATCH-56 (`ledger_merge.py` only) do not disturb the dataset side. On `main`, `claims.csv` is byte-identical between the two runs. `dataset-check.json` gains only the `not_written_zero_rows` key. The ledger side was not re-run this run; §55 and §56 hold its tables.

The full set is now tested as one change. Suggested order when applied (PROPOSED): one logged commit on a branch other than `main`, naming the three patch files and their sha256 (PATCHSET-52 25e9eaf3…, PATCH-54 28f5b086…, PATCH-56 fe785160…). Then re-run this table and the §56 table. The open choice stays the same: A6 decides which layout ships. On the branch layout, the patch set is what keeps the CSVs.

Open, unchanged: A1–A6 (decision sheet §36); A6 (which TAM layout) is Timothy's. Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §58 (2026-10-18T18Z, Claude): year-end close — `year_close.py` draft, and where the 1099-K threshold stands

Nothing moved since §57 on The-TAM-protocol, library-shared (2e7fcb0) or mirror-chatgpt-root (da5a5fa). The records side (§6, §48–§56) stops at monthly rows. Nothing yet turns twelve months into the year-end figures a filing packet needs, and nothing checks those figures against a platform tax form. This run drafts that step.

**Facts for the year end** (SOURCE-OBSERVED only where marked; page titles from a search limited to irs.gov, 2026-10-18T18Z, article bodies not read):
- Form 1099-K threshold: the IRS newsroom page "[IRS issues FAQs on Form 1099-K threshold under the One, Big, Beautiful Bill; dollar limit reverts to $20,000](https://www.irs.gov/newsroom/irs-issues-faqs-on-form-1099-k-threshold-under-the-one-big-beautiful-bill-dollar-limit-reverts-to-20000)" (SOURCE-OBSERVED, title). The companion transaction-count condition, from which year it applies, and whether the platform files 1099-Ks as merchant of record are all UNVERIFIED. At F-001's scale, the INFERRED reading is that no 1099-K is likely. **Income is reportable whether or not a form is issued** (INFERRED, general rule; check [Understanding your Form 1099-K](https://www.irs.gov/businesses/understanding-your-form-1099-k)). So the ledger, not a form, is the record of truth.
- Retention: "[How long should I keep records?](https://www.irs.gov/businesses/small-businesses-self-employed/how-long-should-i-keep-records)" and [Publication 583](https://www.irs.gov/publications/p583) are the primary pages (SOURCE-OBSERVED, titles). The usual periods are 3 years from filing, with longer periods in named cases (INFERRED, not read this run). PROPOSED: keep the monthly exports, `ledger-rows.csv` and each year's close output privately for at least the longest period that page gives for Timothy's case.

**`F-001-tam-build/year_close.py`** (new, PROPOSED draft, sha256 ff980ee1…). It reads one or more `ledger-rows.csv` files from `ledger_map.py` / `ledger_merge.py`. For each calendar year it prints:
- the count and gross of product sales before refunds, which is the figure a 1099-K would be compared with;
- the count and gross of refunds, by refund date;
- fees and net;
- the number of rows missing a figure;
- the months inside the span that have no row at all, because a month with no sales and an export never merged look the same;
- repeated `source_ref` values.

`--year=YYYY --form-gross=X` prints the difference from a form figure Timothy reads himself. It writes nothing, reads no network, and exits 1 on any flag. It does not decide what goes where on a return.

Tested on synthetic exports pushed through the unmodified `ledger_map.py` at 2e7fcb0 (`python3 -I`, scratch only, nothing committed but the script). EXECUTION-VERIFIED:

| Case | Input | Output | Exit |
|---|---|---|---|
| 1 | Jan (2 sales, one refunded in Mar) + Mar (2 sales, one with an empty fee) | sales 4 / 42.00, refunds 1 / −9.00, fees 4.50, net 16.50 (hand check matches); gap 2027-02 noted; 1 row missing a figure | 1 |
| 2 | Jan only, `--form-gross=18.00` | difference 0.00 | 0 |
| 3 | Jan only, `--form-gross=27.00` | difference 9.00, flagged | 1 |
| 4 | same Jan export merged twice (the §48 case) | `source_ref repeated: S1, S2, S2:refund` | 1 |
| 5 | `--year=2026` with no rows, form figure given | "no dated rows" | 1 |
| 6 | `--form-gross` without `--year` | refused | 1 |

Case 2 also shows a limit that a reader must keep in mind. The gap note is a NOTE, not a FLAG. A Feb with no sales is normal, so only Timothy can say which kind of gap it is. Case 4 repeats what PATCH-56 already catches upstream; here it is a second net at year end.

Suggested place in the chain (PROPOSED): monthly `ledger_map.py` → `ledger_merge.py` (with 52/54/56) → once a year `year_close.py --year=YYYY`. Its output and the form, if any, then go into the private filing packet (§6).

Open, unchanged: A1–A6 (decision sheet §36); A6 (which TAM layout) is Timothy's. Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §59 (2026-10-18T19Z, Claude): the whole records chain run through a year end, and the one gap the year close could not see

Nothing moved since §58 on The-TAM-protocol, library-shared (f82164a) or mirror-chatgpt-root (da5a5fa). This run feeds the full chain into `year_close.py` for the first time, across a year boundary: thirteen monthly all-time exports (Jan 2026 to Jan 2027) → `ledger_map.py` → `ledger_merge.py` with PATCHSET-52, PATCH-54 and PATCH-56 applied in that order (scratch worktree of f82164a, all clean) → `year_close.py`. Synthetic data only: 18 sales of 9.00 with a 1.40 fee, no sales at all in May 2026, one refund in March, one Dec 2026 sale refunded on 2027-01-05. Scratch only, `python3 -I`, nothing committed but the patch below. EXECUTION-VERIFIED:

| Case | Chain | `year_close.py` result | Exit |
|---|---|---|---|
| A | all 13 exports merged | 2026: sales 17 / 153.00, refunds 1 / −9.00, fees 23.80, net 120.20 (hand check matches); gap note 2026-05 (the real no-sales month). 2027: sales 9.00, refund −9.00 (the Dec sale's refund lands in 2027 by refund date), net −1.40 | 0 / 0 |
| B | Jun and Oct merges skipped (forgotten) | identical totals to A; the merged ledgers match A on (source_ref, date, category, gross, fees, net), only `entered_by` run ids differ. All-time exports make a skipped month harmless, as §48 intended | 0 / 0 |
| C | as A, but a 2026-12-30 refund and the Dec export taken on 12-28; 2026 closed from the Dec ledger | 2026: refunds 1 / −9.00, net 120.20, `--form-gross=153.00` difference 0.00. Closed after the Jan 2027 merge: refunds 2 / −18.00, net **111.20** | **0** / 0 |

**Finding (case C).** Closing the year from a ledger whose last export was taken before Dec 31 misses late-December refunds, and nothing flags it. The sales-gross check against a form still matches, because a refund does not change sales gross. The year close cannot see the gap, because no ledger row records when its export was taken.

**`F-001-tam-build/PROPOSED-PATCH-59.diff`** (sha256 8160ee22…, applies with `git apply --check` both on f82164a and after 52/54/56; the patched script compiles). It adds `--export-date=YYYY-MM-DD`, the day the last merged all-time export was taken, given by Timothy. With `--year`, an export date on or before Dec 31 of that year is a FLAG, exit 1: "merge a later all-time export first". Dec 31 itself counts as too early, since a refund later that day could miss. Without the option, `--year` prints one NOTE and exits as before. Tests: case C with 12-28 gives exit 1; after the Jan merge with 2027-01-31, exit 0; 12-31 gives exit 1; a bad date is refused. With no option, output and exit are byte-identical to the unpatched script on all four ledgers; with `--year` only, they are identical apart from the NOTE line. EXECUTION-VERIFIED, script not edited.

PROPOSED close rule for the §6 packet: close year Y only after merging an all-time export taken in January of Y+1 or later. Run `year_close.py --year=Y --export-date=<that day>`, and add `--form-gross` if a form arrives.

Open, unchanged: A1–A6 (decision sheet §36); A6 (which TAM layout) is Timothy's. Whether the platform returns its fee on a refund is still UNVERIFIED (refund rows carry an empty fee cell by design). Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §60 (2026-10-18T20Z, Claude): application note — all four PROPOSED patches applied in order (52 → 54 → 56 → 59)

Nothing moved since §59 on The-TAM-protocol, library-shared (5d9b96e) or mirror-chatgpt-root (da5a5fa). This run checks that the four records/dataset patches drafted in §52–§59 stack as one set. Scratch worktree of 5d9b96e, `python3 -I`, synthetic data only, nothing committed but this note. EXECUTION-VERIFIED:

- `git apply --check` then `git apply`, in order: PROPOSED-PATCHSET-52 (sha256 25e9eaf3…), PROPOSED-PATCH-54 (28f5b086…), PROPOSED-PATCH-56 (fe785160…), PROPOSED-PATCH-59 (8160ee22…): all four apply cleanly. Together they touch five scripts (`ledger_map.py`, `ledger_merge.py`, `listing_check.py`, `rebuild_datasets.py`, `year_close.py`; +103 / −23 lines). All ten scripts in `F-001-tam-build/` compile.
- Patched hashes (first 16 hex): `ledger_merge.py` cd64a0ea…, `year_close.py` 795b8e31…, `rebuild_datasets.py` dd731e3e…, `listing_check.py` 05d86b51…, `ledger_map.py` e2575df8…
- Smoke run through the whole patched chain: two all-time exports (taken 2026-12-28 and 2027-01-31; 3 sales of 9.00, fee 1.40; one sale refunded 2026-12-30, which shows only in the January export) → `ledger_map.py` (exit 0, twice) → `ledger_merge.py` (exit 0: 1 row appended, 3 skipped as the same row, net 13.80) → `year_close.py --year=2026`:

| Ledger | `--export-date` | Result | Exit |
|---|---|---|---|
| December only | 2026-12-28 | refunds 0, net 22.80, FLAG "merge a later all-time export first" | 1 |
| merged | 2026-12-31 | same totals as below, FLAG (Dec 31 counts as too early) | 1 |
| merged | 2027-01-31 | sales 3 / 27.00, refunds 1 / −9.00, fees 4.20, net 13.80 (hand check matches) | 0 |

Side note, unchanged from §47: running `py_compile` rewrites the committed `__pycache__/layout_map.cpython-313.pyc` (same size, different bytes). Harmless in scratch; a run that commits from a tree where it compiled the scripts should leave that file out.

PROPOSED: the four patches be adopted as one change, in this order, by a later run that both participants have reviewed (ChatGPT's review of 56/59 has not landed yet). Until then the committed scripts stay as they are. Open, unchanged: A1–A6 (decision sheet). Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §61 (2026-10-18T21Z, Claude): the listing's price line disagrees with the decision sheet — a terms check for `listing_check.py`

Nothing moved since §60 on The-TAM-protocol (d46456a), library-shared (7c76f5d) or mirror-chatgpt-root except GPT run 185's status note (3e7131a; its "40 shared Library entries" matches the 40 blobs at 7c76f5d, EXECUTION-VERIFIED).

**Finding (SOURCE-OBSERVED, in our own drafts):** the listing text in §21.1 says **"Price: [$7] [or pay what you want, minimum $5]"**, while §13 advises $12 or more, and the decision sheet's A5 default is **$9** with a 30-day window. At the card rate used in §33/§34 (10 % + $0.50 + a hypothetical 2.9 % + $0.30), net per direct sale is $5.30 at $7 (76 %) and $3.56 at $5 (71 %), against $7.04 at $9 (78 %) (INFERRED arithmetic, python this run). Nothing in `listing_check.py` compares the page's price or refund window with what Timothy agrees, so the page could be pasted with the old $7 / $5 line.

**PROPOSED-PATCH-61** (`F-001-tam-build/PROPOSED-PATCH-61.diff`, sha256 7c045a71…): an optional `--terms=<terms.json>` (`{"price": 9, "refund_days": 30}`). Every dollar amount on the listing's `Price:` line must equal the agreed price, and the `within N days` refund line must equal `refund_days`; a missing line fails. Without `--terms` the script behaves as before. It applies cleanly both on the committed script and after PATCHSET-52 → 54 → 56 → 59 (it would be the fifth in that order). Tested in a scratch worktree with synthetic listings and a synthetic build folder (EXECUTION-VERIFIED, `python3 -I`):

| Listing | `--terms` result | Exit |
|---|---|---|
| §21.1 price line ($7 / PWYW min $5), 30 days | FAIL price line [7, 5] vs agreed $9 | 1 |
| $9, 30 days | PASS price, PASS refund window | 0 |
| $9, 14 days | FAIL refund window 14 vs 30 | 1 |
| no Price line | FAIL price line missing | 1 |
| "$9.00, or PWYW minimum $9", 30 days | PASS | 0 |

On all five listings, the output without `--terms` is byte-identical to the four-patch script's (`cmp`), so existing runs are unaffected. The committed script is not edited (R3).

PROPOSED, for the listing text (not edited): replace §21.1's price line with `**Price:** [A5 price]` so it fills from Timothy's answer rather than an older placeholder, and write `terms.json` from the same answer. Open, unchanged: A1–A6. Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §62 (2026-10-18T22Z, Claude): the listing's article count and the build's skipped sources — a second terms check for `listing_check.py`

Nothing moved since §61 on The-TAM-protocol (d46456a), library-shared (a3b452e) or mirror-chatgpt-root (3e7131a).

**Finding (SOURCE-OBSERVED, in our own drafts and scripts):** §21.1 promises "[9] articles", and §21.2 says the count becomes 10 if Article 4 turns up. `listing_check.py` (with §61) compares the page count, CSVs, EPUB, price and refund window against the build, but never the article count, and never reads `build-report.json`. So a build that skipped a source file (`report["missing"]`, e.g. on a layout where a name changed, the §39 risk) could still be listed as complete. On `main` (d46456a), `build.py` includes 6 source files and misses none: the README, Articles 1, 2, "The Color Dyed…" (3) and 5, and "Collective information" as the "6–10. Collected notes" chapter (EXECUTION-VERIFIED this run, `python3 -I`, read-only clone in scratch). Whether that is "9 articles" or "5 chapters" depends on how Timothy counts the collected notes, so the script should not guess.

**PROPOSED-PATCH-62** (`F-001-tam-build/PROPOSED-PATCH-62.diff`, sha256 88c67998…): two additions, both only when `--terms` is given.
1. An optional `"articles": N` key in `terms.json`; the page's "N articles" must equal it. Timothy sets N once he decides how the collected notes count.
2. `build-report.json` must exist in the build folder and list no missing source file.

It applies sixth, after PATCHSET-52 → 54 → 56 → 59 → 61 (it extends §61's `check_terms`, so it does not apply to the committed script alone). Patched `listing_check.py` sha256 b05036d7…. Tested in scratch (EXECUTION-VERIFIED), with a filled synthetic listing ($9, 30 days, 9 articles), the real `main` build, and a synthetic marked `claims.csv`:

| Case | New lines | Exit |
|---|---|---|
| terms 9 articles, real build | PASS article count 9; PASS 6 source files, none missing | 1 (only "CSV promised, none built", see below) |
| terms 5 articles | FAIL article count 9 vs agreed 5 | 1 |
| build-report lists Article 5 missing (synthetic edit) | FAIL build skipped source files: ['Article 5'] | 1 |
| no build-report.json | FAIL build-report.json missing | 1 |
| §61 terms file (no "articles" key) | §61 lines unchanged; adds only the build-report line | 1 (CSV) |
| real build + `rebuild_datasets.py`, terms 9 articles | all PASS | **0** |

Without `--terms`, output is byte-identical to the §61 script on all three build folders (`cmp`). The CSV line in the first rows is expected, not a defect: `build.py` alone writes no dataset CSVs on `main` ("no delimited table found"), and `rebuild_datasets.py` adds `dataset-a.csv` and `dataset-b.csv`. The last row is the first end-to-end run, from the public source to a passing listing gate, with every terms check on (EXECUTION-VERIFIED; no PDF built, so the page-count line was not exercised).

PROPOSED, for the order of steps at listing time: `build.py` → `rebuild_datasets.py` → `build_pdf.py` → `claim_scan.py` (Timothy marks every row) → `listing_check.py --terms=terms.json`. `terms.json` comes from Timothy's A5 answer, plus `articles` once he decides how to count the collected notes (a new sub-question under A1/A4, not a new blocker). The committed scripts are not edited (R3). Open, unchanged: A1–A6. Nothing was sold, listed, uploaded or published. No account, payment or contact. Not tax, legal or financial advice.

## §63 (2026-10-18T23Z, Claude): shape (b) read for structure — "Unicorn Estate" is a printed conversation with three RFC numberings, not a manuscript

Nothing moved since §62 on The-TAM-protocol (d46456a), library-shared (745fd69) or mirror-chatgpt-root (3e7131a). This run took the §62 "next" candidate: what A1(b) would actually sell. R1 lets runs draft both shapes; ChatGPT's 2026-10-11 question (`contract-000/gpt/CLAUDE-QUESTION-GDRIVE-20261011.md`) asked for exactly this check.

**What was read.** `UnicornEstate.pdf` from Timothy's Google Drive (the §14 table row; 640,786 bytes, sha256 77f0cf45…3f90a), downloaded to a scratch folder and read **for structure only**: page count, headings, RFC numbers and titles, and where conversation-turn markers fall. No prose is quoted here and the file is not committed to any branch (it is unpublished; R1 makes it Timothy's to sell, not ours to publish). All facts below are EXECUTION-VERIFIED with `pdfinfo` / `pdftotext -layout` and a heading scan, unless marked.

**Findings.**
1. 210 letter pages, ~27,700 words. Producer "Skia/PDF m131", creator "Chromium", created 2026-07-29: a browser print, not an export from a word processor.
2. It is a printed conversation. A user-turn marker appears on pages 25, 58 and 205; second-person commentary addressed to the author ("your system / framework") appears on pages 29, 57, 114, 120 and 127. INFERRED: much of the text is assistant-drafted around Timothy's prompts, so the human-authored share is unknown.
3. Only RFC-0001, -0002 and -0003 have full sections headed "(Draft 0.1)" (pages 7, 12, 19). From page 66 on, sections are headed differently ("RFC-0004 — Temporal Cognition and Collective Agency" p. 66; RFC-0009…0014 p. 144–145; RFC-0015 p. 187).
4. **At least three incompatible numberings** of the series sit inside the one file:

| RFC | Roadmap p. 5–6 | Sections p. 66–187 | Roadmap p. 202–203 |
|---|---|---|---|
| 0000 | Repository Index and Specification Roadmap | — | Vision and Design Philosophy |
| 0004 | Hebrew Symbolic Execution | Temporal Cognition and Collective Agency | Indus Icon Agents |
| 0005 | Indus Agent Architecture | — | Jurisdictions and Runtime |
| 0010 | Distributed Runtime Architecture | Hebrew Grammar and Symbolic Syntax | Collective Symbol Construction |
| 0013 | Security, Identity, and Trust | Cloudflare Runtime Reference Implementation | Hebrew Execution Calculus |
| 0014 | Future Research Directions | GitHub Repository Constitution and Versioned World Building | Symbolic Hyperlattice |
| 0015–0016 | (none) | Processional Growth and Constitutional Expansion | Constitutional Growth / Evolution |

   Mid-file lists on pp. 42 and 85 give still other orders (RFC-0004 "Temporal Model" on both; RFC-0005 "Collective Agency" on p. 42, "Causality and Symbolic Events" on p. 85), and p. 73 heads a section "RFC-0005 Hebrew Symbolic Execution". So "RFC-0000 through RFC-0014" (`genesis-documentary:docs/UPDATE_FOR_GPT.md` l. 85, §11) names a range, not a fixed table of contents.

**What this means for A1(b) (PROPOSED).**
- Shape (b) cannot be listed as-is. Before any build it needs: (i) one canonical numbering chosen by Timothy (the p. 202–203 roadmap is the latest in the file and the only one reaching 0016); (ii) an extraction pass that keeps Timothy's own text and the RFC bodies and drops conversation scaffolding; (iii) a disclosure decision, since the bodies are largely assistant-drafted (INFERRED, finding 2) — this is the same AI-disclosure question §21 left open for the platform, but sharper here.
- Effort, rough (INFERRED): (a) TAM is ~1 build step from listable (§62 gate passes end to end); (b) is an editing project of unknown length. That supports keeping the decision sheet's A1 default at (a), with (b) as a later second product (option c) once an edited RFC text exists.
- The existing `build.py` → … → `listing_check.py` chain would serve (b) unchanged once the edited text is in Markdown in a repository (R3: registered first, then edited). No script change proposed.
- `RFC Collection` (Google Doc, editable, last edited 2026-06-26 per §14) was not opened this run; it may be the cleaner source. Next F-001 step for (b), if Timothy wants it: read its headings only and compare its numbering with the three above.

New question for Timothy (under A1): if (b) goes ahead, which numbering is canonical, and is `RFC Collection` or the PDF the text to edit from? Open, unchanged: A1–A6. Nothing was sold, listed, uploaded or published; no account, payment or contact. Not legal, tax or financial advice.

## §64 (2026-10-19T00Z, Claude): `RFC Collection` read for structure — a different series (MASHET RFC 23–46), not the Unicorn Estate RFC-0000…0016 text

Nothing moved since §63 on library-shared (6e21237) or main (fea9690); mirror-chatgpt-root moved to 3777f75 (GPT run 188, status files only). This run took the §63 "next" step: `RFC Collection`'s headings, compared with the three numberings in the §63 table.

**What was read.** The Google Doc `RFC Collection` (the §14 row; created 2026-05-16, last modified 2026-06-26), fetched as plain text into a scratch folder (223,151 characters, 13,325 lines, ~19,500 words) and scanned in full **for structure only**: top-level headings, the first non-blank line under each, every RFC number it mentions, and conversation markers. No prose is quoted and nothing from it is committed. Facts below are EXECUTION-VERIFIED (heading and regex scan over 100% of the text) unless marked.

**Findings.**
1. 11 top-level sections, numbered **23, 31, 32, 33, 34, 36, 40, 41, 44, 45, 46** (titled ones: 31 "Kaballah Dependancy Graph" (spelling as in the doc), 34 "Gamma", 36 "Trigonometries", 40 "Ontological Differentiation Framework (ODF)", 44 "Taxonomic Field Classifiers (TFC)", 45 "Stratified Semantic Mountains (SSM)", 46 "Recursive Harmonic Ontology (RHO)"). Numbers 24–30, 35, 37–39 and 42–43 are mentioned or absent but have no section of their own.
2. Five sections (23, 31, 32, 33, 34) open with an IETF-style "MASHET WORKING GROUP" header block with an author byline; 31 is labelled `MASHET-RFC-0031`. The doc cites RFC 2119 (keyword conventions) three times.
3. **No RFC number from 0 to 22 appears anywhere in the doc.** The lowest is 23. So it shares no number with any of the three Unicorn Estate numberings in §63 (0000–0016).
4. Sections 36 and 45 open with second-person commentary addressed to the author, and the doc contains 2 more such markers. INFERRED: it is partly assistant-drafted, like the PDF (§63 finding 2).

**Corrections to earlier sections (append-only, the old text stays).**
- §14 row "RFC Collection — editable source of the RFC series" is wrong for the series that §11/§63 mean. It is the editable source of a **separate MASHET RFC series (23–46)**.
- §14 step 1's default proposal ("edit from `RFC Collection`") does not hold for shape (b) as §63 defines it. `RFC Collection` cannot supply the RFC-0000…0016 text.

**What this means (PROPOSED).**
- A1(b) "Unicorn Estate / RFC" now names two distinct bodies of work: (b1) the Unicorn Estate RFC-0000…0016 series, whose only source found so far is the PDF (three numberings, §63); (b2) the MASHET RFC 23–46 series in `RFC Collection` (one consistent numbering, IETF-style headers, gaps). (b2) is structurally closer to editable: one numbering and real section headers. Both still need an extraction and disclosure pass (§63 (ii)/(iii)).
- Two other §14 rows may hold the missing pieces and were **not opened**: `LHEA_TEMA_RFC_Series_v1.0-2.docx` (34 KB) and `RFC Mashet` (28 KB). Next step for (b), if Timothy wants it: headings only of those two, to see whether either carries RFC-0000…0022 or the gaps in 23–46.
- The A1 default stays (a) TAM: §62's gate passes end to end; (b1) and (b2) are both editing projects (INFERRED). No script change proposed; the existing chain serves either once an edited Markdown text is registered (R3).

New question for Timothy (under A1): does "Unicorn Estate / RFC" mean the RFC-0000…0016 series (PDF), the MASHET 23–46 series (`RFC Collection`), or both as one book? Open, unchanged: A1–A6 and §63's numbering question. Nothing was sold, listed, uploaded or published; no account, payment or contact. Not legal, tax or financial advice.

## §65 (2026-10-19T01Z, Claude): `LHEA_TEMA_RFC_Series_v1.0-2.docx` read for structure — a third, self-consistent RFC series (LHEA-001…004 + TEMA-001)

Nothing moved since §64 on library-shared (6f8e0fb), main (fea9690) or mirror-chatgpt-root (3777f75). This run took the §64 "next" step: headings only of the two unopened §14 rows.

**What was read.** `LHEA_TEMA_RFC_Series_v1.0-2.docx` (the §14 row; 34,420 bytes, created/modified 2026-06-26), fetched as text through the Drive connector into scratch (49,041 characters, 788 lines, ~7,160 words) and scanned in full **for structure only**: spec identifiers, the title/subtitle lines under each, the header-table Status and Relation fields, numbered-heading count, and second-person markers. No prose is quoted beyond titles and nothing from it is committed. Facts are EXECUTION-VERIFIED (regex scan over 100% of the text) unless marked. `RFC Mashet` was **not found** by an exact-title Drive search this run (only the docx matched `title contains 'LHEA_TEMA_RFC' or title = 'RFC Mashet'`); it stays unopened.

**Findings.**
1. Five specifications, each opening with its identifier and a header table (RFC, Status, Date, Author, Organization, Relation):
   | ID | Title / subtitle | Status | Relation (summarised) |
   |---|---|---|---|
   | RFC-LHEA-001 | Latin-Hebrew Execution Architecture / Foundational Architecture Specification | Published v1.0 | root specification |
   | RFC-LHEA-002 | Instruction Set Architecture and Kernel Memory Integration / Execution Engine Specification | Draft v1.0 | supplements 001; prerequisite for 003, 004 |
   | RFC-LHEA-003 | The LHEA Translation Pipeline / Natural Language to Executable Ontology | Draft v1.0 | supplements 001, 002 |
   | RFC-LHEA-004 | Lattice-Core Unity / LHEA and TEMA as a Unified Substrate | Draft v1.0 | supplements 001–003; read with TEMA-001 |
   | RFC-TEMA-001 | Toroidal Eigenvalue Memory Architecture / A Topological Framework for Scope-Aware AI Memory | Published v0.1 | memory spec; read with LHEA-004 |
2. The byline field names Timothy (with his handles) and "Mashet / LHEA Research — Independent". The cross-references form a closed, acyclic dependency order (001 → 002 → 003 → 004 ↔ TEMA-001); every ID referenced is present.
3. **No bare numeric RFC number appears** (no 0000–0016 and no 23–46), so it overlaps neither the Unicorn Estate numberings (§63) nor the MASHET 23–46 series (§64).
4. **Zero second-person markers** and no conversation scaffolding; 70 numbered section headings. INFERRED: this is already an edited, document-shaped text, unlike the PDF (§63) and `RFC Collection` (§64). Whether it was assistant-drafted cannot be told from structure; the AI-disclosure question (§21, §63 (iii)) still applies.

**What this means (PROPOSED).**
- A1(b) now has three candidate bodies: (b1) Unicorn Estate RFC-0000…0016 (PDF only, three numberings); (b2) MASHET RFC 23–46 (`RFC Collection`, gaps); (b3) **LHEA/TEMA five-spec series** (this docx: one naming scheme, complete cross-references, ~7,200 words, no scaffolding). (b3) is the only one that is structurally listable without an extraction pass — a short "technical monograph" product (≈ 25–30 pages) rather than a book (INFERRED from word count).
- Path for (b3) if Timothy picks it, all under R3 (register first, then edit): convert the docx to Markdown in a repository Timothy chooses → register it → run the existing `build.py` → … → `listing_check.py` chain unchanged (§62 gate). No script change proposed. Price band would sit below (a) TAM, since it is shorter; the A5 default is not changed here.
- The A1 default stays (a) TAM; (b3) is the cleanest candidate for option (c) "second product".

New question for Timothy (under A1): is the LHEA/TEMA five-spec series (b3) part of what you meant by "the RFC material", and may it be a second, short product? Open, unchanged: A1–A6, §63's numbering question, §64's series question. Nothing was sold, listed, uploaded or published; no account, payment or contact. Not legal, tax or financial advice.

## §66 (2026-10-19T02Z, Claude): (b3) delivery path — the EPUB gate is source-agnostic; build.py and claim_scan.py are TAM-wired

Nothing moved since §65 on library-shared (019c41a), main (fea9690) or mirror-chatgpt-root (3777f75). This run took half of the §65 "next" step: can the existing chain carry (b3) LHEA/TEMA without a script change?

**What was run (EXECUTION-VERIFIED, scratch only, nothing committed from it).**
1. A synthetic Markdown skeleton with the (b3) shape from §65 (five top-level specs, each opening with a header table, 70 numbered sections in total, placeholder text only; no LHEA/TEMA prose) was converted with the exact pandoc call `build.py` uses (`pandoc <md> -o <epub> --toc`, pandoc 3.1.3).
2. `epub_check.py <scratch> <scratch>/b3.epub` (unmodified, library-shared 019c41a): **0 FAIL, 2 WARN, exit 0**. Header tables, nav and the 5-chapter spine pass; the two WARNs are the known opt-in ones (no cover, §25; no schema:* accessibility metadata, §26). So the store-facing EPUB gate needs no change for (b3).
3. Not done: a real docx → Markdown conversion of `LHEA_TEMA_RFC_Series_v1.0-2.docx`. The Drive connector returned the file only as inline base64 that this run could not write to disk without re-typing it, so the conversion fidelity (tables, footnotes, comments part present in the docx) stays UNVERIFIED. The docx container does list `word/comments.xml`, `footnotes.xml` and `endnotes.xml` parts (SOURCE-OBSERVED from the zip directory, contents not read): an editing pass should check whether Word comments carry review notes before conversion.

**What is TAM-wired (SOURCE-OBSERVED, scripts not edited).**
- `build.py`: `ORDER`, `DUP_ONLY`, `DATASETS` and `TITLE` (lines 22–33) name TAM files; output names are `tam-draft.*`.
- `claim_scan.py`: `FILES` (line 21) lists the eight TAM files.
- `epub_check.py`: only the default file name `tam-draft.epub` and the placeholder pattern (which rejects a title containing "tam-draft"); an explicit epub path works, as run above.
- `listing_check.py`: TAM-shaped only in its docstring here; its `--terms` keys from §61/§62 are generic.

**PROPOSED (not applied).** If Timothy picks (b3) as a second product (A1(c)): add one optional `--source-map <json>` argument to `build.py` and `claim_scan.py` holding `{title, order:[[heading, file]...], dup_only:[], datasets:[]}`, defaulting to today's TAM constants so every existing TAM run and hash stays identical. That is a race-contract-sized change for joint review with ChatGPT, after the five pending patches (52 → 54 → 56 → 59 → 61/62), not before. Until then (b3) can be built by hand with the same pandoc call and gated with `epub_check.py <dir> <file>`.

Product shape note for (b3) (INFERRED, unchanged from §65): a short technical monograph, EPUB + PDF, priced below TAM; free-tier stack, refund window and records chain as for TAM (§21, §56–§62). Open, unchanged: A1–A6, §63's numbering question, §64's series question, §65's (b3) question. New sub-question (under A1): if (b3) goes ahead, should Word comments in the docx be kept as editorial notes or dropped in the edit? Nothing was sold, listed, uploaded or published; no account, payment or contact. Not legal, tax or financial advice.

## §67 (2026-10-19T03Z, Claude): the whole listing chain with all six PROPOSED patches and a real PDF — passes; the PDF is not byte-reproducible

Nothing moved since §66 on The-TAM-protocol (d46456a), library-shared (e953069), main (fea9690) or mirror-chatgpt-root (3777f75). §62 ran the gate end to end without a PDF, so its page-count line was not exercised with every terms check on. This run closed that gap. Scratch copy of library-shared e953069, `python3 -I -B`, nothing committed but this note.

**What was run (EXECUTION-VERIFIED).**
1. PROPOSED-PATCHSET-52 → 54 → 56 → 59 → 61 → 62 applied in order with `git apply` (diff sha256 prefixes 25e9eaf3, 28f5b086, fe785160, 8160ee22, 7c045a71, 88c67998, all as recorded); patched `listing_check.py` sha256 b05036d7… as in §62.
2. On a fresh clone of The-TAM-protocol d46456a: `build.py` (exit 0; 6 source files, none missing) → `rebuild_datasets.py` (exit 0; A 6 rows, B 8 rows, 0 rejected) → `build_pdf.py` (xelatex fails on the missing `lmodern.sty` as in §50; wkhtmltopdf: **13 pages, 121,260 bytes**, same as §50) → `epub_check.py` (0 FAIL, 2 known opt-in WARN) → `claim_scan.py` (42 rows).
3. All 42 claim rows given a synthetic `test` status (scratch only; the real marks are Timothy's). Synthetic listing: the §21.1 text with placeholders filled by test values (13 pages, 9 articles, $9, 30 days; credit line a dummy). `terms.json` = `{"price": 9, "refund_days": 30, "articles": 9}`.

| Case | Result | Exit |
|---|---|---|
| listing as above, `--terms` | 18 PASS, 0 FAIL (placeholders, wording, page count 13 = 13, claims 0/42 open, CSVs, EPUB, price, refund window, article count, build-report) | **0** |
| same, "about 40 pages" | FAIL page count: listing 40, build 13 (only FAIL) | 1 |

So the six patches stack and the full PROPOSED order (`build.py` → `rebuild_datasets.py` → `build_pdf.py` → `claim_scan.py` → [Timothy's marks] → `listing_check.py --terms`) reaches a passing gate on the public source with a real PDF.

**Finding (EXECUTION-VERIFIED).** Running `build_pdf.py` twice on the same build gives PDFs of the same size and the same extracted text (`pdftotext`, `cmp`), but different bytes: sha256 310fd2fd… then 45940cd5…; 40,208 bytes differ, including `/CreationDate` (20 s apart). The EPUB was made byte-reproducible earlier (opt-in id/epoch); the PDF is not. Consequence (INFERRED): a PDF sha256 identifies one build run, not a source commit, so a rebuild cannot later confirm "this is the file that was sold".

**PROPOSED (not applied; scripts not edited, R3).** (a) In the records chain, keep the sha256 of the PDF file actually uploaded (computed at upload time from that file), never of a rebuild; the EPUB sha256 can still be re-derived. (b) Optional, later, for joint review: try `SOURCE_DATE_EPOCH` / fixed metadata for the wkhtmltopdf path and check whether the remaining differences go away; not tested this run, so whether wkhtmltopdf can be made reproducible at all is UNVERIFIED. Side note, unchanged from §47/§60: compiling the scripts touches the committed `__pycache__/layout_map.cpython-313.pyc`; this run used `-B` and committed only this note.

Open, unchanged: A1–A6, §63–§66 questions. Nothing was sold, listed, uploaded or published; no account, payment or contact. Not legal, tax or financial advice.

## §68 (2026-10-19T04Z, Claude): the wkhtmltopdf PDF embeds the builder's local path in its table-of-contents links; a PROPOSED post-process fixes the leak, not byte-reproducibility

Nothing moved since §67 on The-TAM-protocol (d46456a), library-shared (022e602), main (fea9690) or mirror-chatgpt-root (3777f75). §67(b) asked what the PDF rebuild differences are. Scratch copy of library-shared 022e602 with PATCHSET-52 → 54 → 56 → 59 → 61 → 62 applied (all apply cleanly), fresh clone of The-TAM-protocol d46456a, `python3 -I -B`.

**What was run (EXECUTION-VERIFIED).** `build.py` (exit 0) → `build_pdf.py` twice (xelatex fails as before; wkhtmltopdf 0.12.6: 13 pages, 121,278 bytes both times; sha256 e4d93f61… vs b2865455…). Both PDFs expanded with `qpdf --qdf --object-streams=disable` and diffed.

**Finding 1 — the difference.** Besides `/CreationDate` and object numbering, the only content differences are the 9 table-of-contents link annotations: each is `/URI (file:///<absolute build directory>/toPdfViaTempFile<N>-0.html#<heading-id>)`, with `<N>` changing per run. The same happens when pandoc writes a standalone HTML first and wkhtmltopdf is called on it directly (`file:///…/d.html#introduction`). There are 0 in-document `/GoTo` or `/Dest` links.

**Finding 2 — why it matters for a sale (INFERRED).** A buyer's copy would (a) carry the seller's local folder path (user name, directory layout) in 9 places, readable with any PDF tool, and (b) have a table of contents whose entries try to open a file on the buyer's machine instead of jumping to the chapter. Neither `epub_check.py` nor `listing_check.py` looks for this; the EPUB is unaffected (its TOC is nav.xhtml).

**PROPOSED (not wired in; build_pdf.py not edited, R3).** `F-001-tam-build/PROPOSED-pdf_fix.py` (sha256 e5827b37…): reads the PDF and the standalone pandoc HTML, maps each `#id` to its heading text, turns the link into an in-document `GoTo` to the first later page whose `pdftotext` contains that heading, drops the link (keeps the text) when no page matches, sets the docinfo dates to a fixed value, and saves with a deterministic ID (pikepdf, free). On the real 13-page build: 6 links rewritten, 3 dropped (headings that wrap or differ in the PDF text: "The-TAM-protocol", "2. The Water-Weight Computer", "3. The Chemistry of the …"), 0 `file://` strings left in the expanded file, extracted text identical to the input, `qpdf --check` clean.

**Not solved (EXECUTION-VERIFIED).** Two fixed outputs still differ (3b5fbc47… vs d3ca91af…): after the fix the remaining differences are the font-subset tags (`QTDAAA+DejaVuSerif-Bold` / `QZDAAA+…` swap between runs) and object order. So §67(a) stands: records keep the sha256 of the PDF actually uploaded. Byte-reproducibility of this path stays UNVERIFIED and is low value.

**Proposed check order for joint review.** `build_pdf.py` → `PROPOSED-pdf_fix.py` → a gate line (in `listing_check.py` or `epub_check.py`'s sibling) that FAILs if the delivered PDF contains `file://`. The heading matcher is a heuristic; a more robust route (named destinations, or a LaTeX install with `lmodern`) is a later option. Questions for ChatGPT's review: is pikepdf acceptable in the free-tier stack, and should unmatched links be dropped or should the build fail?

Open, unchanged: A1–A6, §63–§67 questions. Nothing was sold, listed, uploaded or published; no account, payment or contact. Not legal, tax or financial advice.

## §69 (2026-10-19T05Z, Claude): a `file://` gate for the listing check — PROPOSED-PATCH-69, tested on the real build

Nothing moved since §68 on The-TAM-protocol (d46456a), library-shared (39b8f9f), main (fea9690) or mirror-chatgpt-root (3777f75). §68 proposed a gate line that FAILs if a delivered file contains `file://`; this section writes and tests it. Scratch copy of library-shared 39b8f9f with PATCHSET-52 → 54 → 56 → 59 → 61 → 62 applied (all clean), fresh clone of The-TAM-protocol d46456a, `python3 -I -B`.

**PROPOSED (not applied; `listing_check.py` not edited, R3).** `F-001-tam-build/PROPOSED-PATCH-69.diff` (sha256 b03faa46…, applies cleanly after PATCH-62; the full stack 52 → … → 69 was re-applied on a fresh copy, EXECUTION-VERIFIED). With `--terms` only (so the documented "without --terms the output is unchanged" holds), a new `check_local_paths()` checks every `*.pdf` and `*.epub` in the out-dir: an EPUB's members are searched directly; a PDF's raw bytes are searched **and** every stream that inflates with zlib, because a compressed object stream hides the string from a plain byte search. Standard library only (zlib, zipfile); no new dependency.

**Tests (EXECUTION-VERIFIED).** build.py → rebuild_datasets.py → build_pdf.py (wkhtmltopdf, 13 pages) → claim_scan.py (42 rows, all marked `test` — synthetic) → patched `listing_check.py --terms` on a synthetic listing (5 articles, 13 pages, EPUB, two CSVs, $9, 14-day refund; not a real listing):

| Out-dir PDF | Raw `file://` count | Gate result |
|---|---|---|
| unfixed wkhtmltopdf build | 9 | FAIL "9 file:// URI(s)", exit 1 (18 other PASS) |
| same PDF recompressed with `qpdf --object-streams=generate` (control) | **0** | FAIL "9 file:// URI(s)", exit 1 — the inflate step is what catches it |
| after `PROPOSED-pdf_fix.py` (6 GoTo, 3 dropped) | 0 | PASS, exit 0 |

The EPUB passes in every case (0 `file://`). Without `--terms`, the output on the same out-dir is byte-identical to the unpatched script.

**Limits (INFERRED).** The gate looks only for `file://`; an absolute path written some other way (e.g. a bare `/home/<user>/…` in metadata) is not caught, and streams with other filters (LZW, ASCII85 wrappers) are not decoded. wkhtmltopdf's known leak is the `file://` form, which is what §68 found. A broader "no local path" check would need the builder's own directory as an input; proposed only if ChatGPT's review wants it.

**Proposed order (unchanged from §68).** `build_pdf.py` → `PROPOSED-pdf_fix.py` → `listing_check.py --terms` with PATCH-69. Question for ChatGPT's joint review, with PATCH-56/59/61/62 and §68: should this check also run without `--terms` (it changes the no-terms output only when a leaking file exists)?

Open, unchanged: A1–A6, §63–§68 questions. Nothing was sold, listed, uploaded or published; no account, payment or contact. Not legal, tax or financial advice.

## §70 (2026-10-19T06Z, Claude): one apply-order note for the seven PROPOSED diffs

`F-001-tam-build/APPLY-ORDER.md` (new, PROPOSED) lists the seven diffs with their sha256 prefixes, the files each touches and what each needs first, checked with `git apply --check` on a scratch copy of library-shared @ 2e5098b (EXECUTION-VERIFIED): three independent chains — ledger 54 → 56, year close 59, listing gate 52 → 61 → 62 → 69 (69 fails without 62). With all seven applied every script byte-compiles and the two CLIs print usage. The scripts in the folder are not edited. Question for the joint review (ChatGPT), not for Timothy: approve the stack at once, or chain by chain?

## §71 (2026-10-19T07Z, Claude): leak probe of the delivered files, and a docinfo correction to §68

Nothing moved since §70 on The-TAM-protocol (d46456a), main (fea9690) or library-shared (b4cba46); mirror-chatgpt-root moved 3777f75 → ce1d126 (GPT run 195 status only). Scratch copy of library-shared b4cba46 (scripts as committed, no patches applied), fresh clone of The-TAM-protocol d46456a, `python3 -I -B`. §69 left open whether a local path can leak in a form other than `file://`. This section checks that directly.

**Probe (EXECUTION-VERIFIED).** build.py and build_pdf.py were run into a folder with a unique name (`ZQPROBE7_builddir`), inside the session's scratch path. Every delivered file was then searched for the folder name, the scratch path parts, `/tmp/`, `/root`, `/home/` and `file://`: the raw PDF bytes plus every zlib-inflatable stream, and every EPUB member.

| File | Hits |
|---|---|
| `tam-draft.pdf` (unfixed, wkhtmltopdf) | 9 of each path marker, all inside the 9 `file://` TOC URIs found in §68; nothing elsewhere (docinfo: empty Title, Creator, Producer, CreationDate) |
| same after `PROPOSED-pdf_fix.py` | 0 |
| `tam-draft.epub` (16 members) | 0 (the one `/root` match is the `</rootfiles>` tag in `META-INF/container.xml`, a false positive) |
| `tam-draft.md` | 0 |

So for this build the `file://` gate in PATCH-69 catches every local path the PDF carries, and the EPUB carries none. The non-delivered `pdf-report.json` does hold `/tmp/runtime-root` (wkhtmltopdf's stderr). It is a build record and must not be uploaded with the product.

**Correction to §68 (EXECUTION-VERIFIED).** §68 says `PROPOSED-pdf_fix.py` "sets the docinfo dates to a fixed value". It doesn't. Its `with pdf.open_metadata(...): pass` line (line 29) empties the whole docinfo dictionary and adds an empty XMP packet, so the date loop after it finds nothing to set. The fixed PDF ends up with no Title, Creator, Producer or dates. Removing that one line keeps the docinfo and sets CreationDate to `D:20000101000000Z` as intended. Separately, the build's PDF Title is empty even before the fix: wkhtmltopdf does not take pandoc's `pagetitle`. A reader app will then show the file name instead of the book title (INFERRED).

**PROPOSED (not applied; `PROPOSED-pdf_fix.py` not edited, R3).** `F-001-tam-build/PROPOSED-PATCH-71.diff` (sha256 0670432d…) replaces line 29 with a Title taken from the standalone HTML's `<h1 class="title">`, whitespace collapsed. With the patch, on the real build:
- Title is "The TAM Protocol: A Speculative Reconstruction (review draft)". Creator, Producer and CreationDate 2000-01-01 are kept, and there is no XMP.
- Links: 6 GoTo, 3 dropped (as before). The probe finds 0 hits, and `qpdf --check` is clean.
- Extracted text is identical to the unpatched fix output (pdftotext sha256 2b0d147f…). Two runs on the same input give the same bytes (bd343198…).
- The diff applies cleanly to the committed script. `APPLY-ORDER.md` has a one-line addendum: the diff is independent of the three chains.

Question for ChatGPT's joint review: should the Title come from the HTML, as here, or be passed in from `build.py`'s title block? Open, unchanged: A1–A6, §63–§70 questions. Nothing was sold, listed, uploaded or published; no account, payment or contact. Not legal, tax or financial advice.

## §72 (2026-10-19T08Z, Claude): a whole-line heading matcher for `PROPOSED-pdf_fix.py`: 9 of 9 TOC links resolved, 0 dropped

Nothing moved since §71 on The-TAM-protocol (d46456a), main (fea9690) or mirror-chatgpt-root (ce1d126); library-shared is at a9d6a11 (this schedule's §71 commit). §68 and §71 left 3 of the 9 table-of-contents links dropped because the heading matcher missed them. This section finds out why and proposes a fix. Scratch copy of library-shared a9d6a11, fresh clone of The-TAM-protocol d46456a, `build.py` → `build_pdf.py` (xelatex fails as before; wkhtmltopdf 0.12.6, 13 pages), standalone HTML from `pandoc tam-draft.md -s --toc`, `python3 -I -B`.

**Why links were dropped (EXECUTION-VERIFIED on this build).** This run the dropped three were "Introduction", "The-TAM-protocol" and "3. The Chemistry of the Registry". §68 listed a slightly different three, so treat its exact list as one run's result. There were two causes:
1. The matcher searches only pages after the TOC page. Here the Introduction and "The-TAM-protocol" headings are on page 1, the same page as the TOC (TOC lines 4–12, headings at lines 16 and 21). So they can never be found.
2. The HTML heading text keeps the source's line break ("3. The Chemistry of the\nRegistry"), and the PDF text has it on one line. A plain substring test fails.

A third risk was not triggered, but it is real: a substring test also matches body text. For example, "Article #3: The Chemistry of the …" on page 3, or "Metric Shock" on pages 9–10. Here it worked only because the heading happened to come first.

**Named destinations / outline (EXECUTION-VERIFIED, negative).** The wkhtmltopdf PDF has no `/Outlines`, no `/Dests` and no `/Names`. So there is nothing exact to map links to, and the matcher stays text-based.

**PROPOSED (not applied; `PROPOSED-pdf_fix.py` not edited, R3).** `F-001-tam-build/PROPOSED-PATCH-72.diff` (sha256 f7a22958…) replaces the substring test with a whole-line match:
- Both sides are normalised: NFKC, which folds the `ﬁ` ligature that pdftotext emits; curly quotes and dashes unified; whitespace collapsed; casefold.
- A heading may wrap onto two lines of the same page.
- The search starts at the TOC page itself. The first whole-line hit is the TOC entry and is skipped; the next hit is the target. When there is no second hit, the link is still dropped, as before.
- Standard library only (`unicodedata`).

**Tests (EXECUTION-VERIFIED).**

| Script | GoTo | Dropped | Targets (page) |
|---|---|---|---|
| committed + PATCH-71 | 6 | 3 | — |
| committed + PATCH-71 + PATCH-72 | **9** | **0** | 1, 1, 2, 2, 3, 4, 5, 13, 13, the same as the `pdftotext` heading lines |
| same, HTML heading "Appendix B" renamed (negative control) | 8 | 1 | the missing heading is dropped, not mis-linked |

The fixed PDF:
- has 0 `file://` strings (raw bytes plus inflated streams) and is clean under `qpdf --check`;
- has extracted text identical to the input (pdftotext sha256 2b0d147f…, as in §71);
- keeps the Title, Creator, Producer and CreationDate 2000-01-01 from PATCH-71;
- gives the same bytes on two runs (a9507f3b…).

PATCH-72 also applies alone and gives 9/0. The order 71 → 72 or 72 → 71 does not matter: both give the same file.

**Limits (INFERRED).**
- The "second whole-line hit" rule assumes each TOC entry fits on one or two lines and appears before its heading. A TOC that wraps an entry onto three lines, or a heading repeated verbatim as a whole line in the body before the real heading, would mis-target.
- The link goes to the page (`/Fit`), not to the heading's position on it.

Both are acceptable for a 13-page review draft. A LaTeX path with `lmodern` (hyperref writes real destinations) remains the exact route if one is ever installed.

Question for ChatGPT's joint review: one more for the pdf_fix stack (71 + 72). Should a dropped link fail the build instead of being dropped silently? With 72 the real build drops none. Open, unchanged: A1–A6, §63–§71 questions. Nothing was sold, listed, uploaded or published; no account, payment or contact. Not legal, tax or financial advice.

## §73 (2026-10-19T09Z, Claude): the listing gate never checks that the delivered PDF is the build's PDF; PROPOSED-PATCH-73 ties them by sha256

Nothing moved since §72 on The-TAM-protocol (d46456a), main (fea9690) or mirror-chatgpt-root (ce1d126); library-shared is at fdfb4e7 (this schedule's §72 commit). §67(a) proposed that the records keep the sha256 of the PDF actually uploaded. This section checks whether anything in the chain can say which PDF that is. Scratch copy of library-shared fdfb4e7 with PATCHSET-52 → 61 → 62 → 69 and 71 → 72 applied, fresh clone of The-TAM-protocol d46456a, `build.py` → `rebuild_datasets.py` → `build_pdf.py` (wkhtmltopdf, 13 pages, sha256 b07a91a1…) → `claim_scan.py` (42 rows, all given a synthetic `test` status in scratch), the §67 synthetic listing with `terms.json` {price 9, refund_days 30, articles 9}, `python3 -I -B`.

**Gap (EXECUTION-VERIFIED).**
- After `PROPOSED-pdf_fix.py`, the only hash in the build records (`pdf-report.json`, b07a91a1…) names the unfixed PDF, which the §69 gate rejects (9 `file://` URIs) and which must not be uploaded. The fixed file (e4d8fd44…) is recorded nowhere.
- `listing_check.py` reads only the page count from `pdf-report.json`; it never hashes the PDF in the folder. A delivery folder holding the real report, claims, CSVs and EPUB, but a **1-page PDF that is not the book**, passes the full `--terms` gate: exit 0, 20 PASS, 0 FAIL. The "about 13 pages" line passes because the count comes from the report, not from the file.
- A fixed copy written beside the unfixed one (`tam-draft-fixed.pdf`) fails, as it should, because the §69 check globs every PDF in the folder. So in practice the fixed file goes into its own delivery folder, which is exactly the layout where the gap opens.

**PROPOSED (not applied; scripts not edited, R3).** `F-001-tam-build/PROPOSED-PATCH-73.diff` (sha256 4da3cb45…, +30 lines, 2 files, standard library only):
1. `PROPOSED-pdf_fix.py` also writes `pdf-fix.json` next to its output: `src`, `src_sha256`, `dst`, `dst_sha256`, pages, goto, dropped. It is a build record, like `pdf-report.json`, not part of the product.
2. With `--terms`, `listing_check.py` hashes every delivered `*.pdf`. Each one must equal `pdf-report.json`'s `sha256`, or `pdf-fix.json`'s `dst_sha256` where that record's `src_sha256` equals the report's `sha256`. Anything else is a FAIL. Without `--terms` the output is unchanged.

**Tests (EXECUTION-VERIFIED, scratch).**

| Delivery folder | Exit | Result |
|---|---|---|
| fixed PDF + `pdf-fix.json` + report, claims, CSVs, EPUB | **0** | 21 PASS ("sha256 e4d8fd447153 is the reported build") |
| build folder as built, plus a fixed copy beside it | 1 | unfixed: 9 `file://`; fixed copy: no `pdf-fix.json` there, so no match |
| same records, 1-page stale PDF | 1 | sha256 178b52b5… matches neither (was exit 0 before the patch) |
| fixed PDF, `pdf-fix.json` missing | 1 | no match |
| `pdf-fix.json` whose `src_sha256` is from another build | 1 | no match |
| any folder, without `--terms` | — | output byte-identical to the unpatched script |

The fixed PDF is the same bytes on two runs from the same input (e4d8fd44…). It differs from §72's a9507f3b… because this run's wkhtmltopdf output differs (§67: the raw PDF is not reproducible).

**Apply order (EXECUTION-VERIFIED with `git apply --check`).** The `PROPOSED-pdf_fix.py` part applies on the clean base. The `listing_check.py` part needs the listing chain 52 → 61 → 62 → 69 first; it fails on the clean base. Checked on the full stack (52, 61, 62, 69, 71, 72). `APPLY-ORDER.md` has a one-line addendum.

**For the records chain (§67(a), PROPOSED).** At upload time, the sha256 to keep is `pdf-fix.json`'s `dst_sha256`, after checking it against the file actually uploaded. The gate now guarantees that this is the file it checked. Not tested here: hashing the upload itself, since nothing is uploaded.

Question for ChatGPT's joint review: should `pdf-fix.json` stay a separate record, or should `pdf_fix` append a `fixed` block to `pdf-report.json`? This patch keeps the build record unedited. Open, unchanged: A1–A6, §63–§72 questions. Nothing was sold, listed, uploaded or published; no account, payment or contact. Not legal, tax or financial advice.
