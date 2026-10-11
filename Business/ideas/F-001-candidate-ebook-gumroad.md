# F-001 candidate A — Timothy's RFC ebook series on Gumroad

**Status:** DRAFT idea by Claude (scheduled run 2026-10-11). Not a Fiscal Contract. Nothing has been created, priced live, sold or announced. Timothy approves any Fiscal Contract before it takes money from anyone (Contract 000 §25.2).
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

## 9. Questions for Timothy

1. Where is the RFC ebook series, and do you hold full rights to sell it?
2. Gumroad, or another storefront you prefer?
3. Price, bundle, and refund window.
