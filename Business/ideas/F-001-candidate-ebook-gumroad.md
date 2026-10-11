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
