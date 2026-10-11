# F-001 candidate B — "Open Dataset Watch": a provenance-stamped monthly digest

**Status:** DRAFT idea by Claude (scheduled run 2026-10-11T04Z). Not a Fiscal Contract. Nothing has been created, priced live, sold or announced. No accounts, no payments, no outreach. Timothy approves any Fiscal Contract before it takes money from anyone (Contract 000 §25.2).
**Evidence states:** SOURCE-OBSERVED (seen in a primary source, cited), EXECUTION-VERIFIED (run by Claude this run), INFERRED, PROPOSED, UNVERIFIED (must be checked before use).
**Why a second candidate:** candidate A (RFC ebook) is blocked until Timothy locates the manuscript and confirms rights. This one is built only from machinery already in the repository.

## 0. What already exists

- SOURCE-OBSERVED: `code-library-registry:Datasets/crawler/` searches Zenodo, Hugging Face and data.gov through their official APIs, stdlib only, and writes one `record.json` per dataset with source, version, date, license, method and checksum (all marked `unverified`), plus the raw API response (`record.raw.json.gz`). Schedule: daily at 04:00 America/Chicago.
- EXECUTION-VERIFIED (mirror-claude S1 batch 3, 2026-10-11T04Z): for the first 69 data.gov records, the sha256 of each decompressed `record.raw.json.gz` equals the checksum stored in its `record.json` (69/69). This proves internal consistency only, not that the upstream source is correct.
- SOURCE-OBSERVED: the crawler only downloads files under an allow-list of open licenses (`config.json`: cc0-1.0, public-domain, pddl, cc-by, cc-by-sa, odc-by, odbl, mit, apache-2.0, bsd).

## 1. Product

A monthly digest, per topic, of newly found open datasets: title, link, license, size, first-seen date, one-line plain description, and the checksum line. Metadata and links only; the digest does not resell the datasets. PROPOSED.

Topics start from the crawler's own keyword sections (etymology/lexicons, philosophy and science, Indus script). A buyer pays for curation and provenance, not for public data.

**Known quality gap (SOURCE-OBSERVED in the records this run):** keyword matching is loose. Examples from batch 3: "Small Watershed Hydrology (WinTR-55)" was found by `philosophy`; a grapevine nematode study by `word roots`; "Science And Technology Exports" by `science`. A paid digest needs a relevance filter (title/description must contain the phrase, or a human/agent review step) before anything is sold. PROPOSED fix: add a `relevance` field and only publish records that pass it.

## 2. Customer

Researchers, librarians, hobby linguists and educators who track open data in a niche. INFERRED; no customer has been asked. No cold outreach, no purchased lists, no fake testimonials (§18.3, §25.3).

## 3. Delivery (fully automatable after one-time setup by Timothy)

1. Crawler runs daily (exists).
2. New monthly job (GitHub Actions, non-`main` branch): select records first seen in the month, apply relevance filter, render Markdown + PDF. PROPOSED.
3. Publish: a free public sample (one topic, previous month) in the repository; the full digest delivered through the storefront's own email or file delivery. PROPOSED.
4. No bot holds storefront credentials. Timothy uploads, or approves an API token kept in secrets (his decision; §25.2).

## 4. Storefront options, pricing and fees

| Option | Fees | State |
|---|---|---|
| Gumroad membership | 10% + $0.50 per charge direct; 30% via Discover | SOURCE-OBSERVED in candidate A ([Gumroad pricing](https://gumroad.com/pricing), 2026-10-11) |
| GitHub Sponsors tiers (sponsor-only repo or file) | stated by GitHub in its [fees and taxes page](https://docs.github.com/en/enterprise-cloud@latest/sponsors/sponsoring-open-source-contributors/about-sponsorships-fees-and-taxes) | UNVERIFIED this run (page found, figures not read); check before choosing |
| Price | placeholder $3/month or $25/year per topic | PROPOSED, Timothy decides |

INFERRED arithmetic on Gumroad direct: $3.00 − ($0.30 + $0.50) = $2.20 net (73%); annual $25.00 − ($2.50 + $0.50) = $22.00 (88%). The fixed $0.50 makes annual billing clearly better.

## 5. Refunds and cancellation

- Monthly: cancel anytime from the storefront; access runs to the end of the paid period. PROPOSED.
- Refund on request within 14 days of a charge if no digest has been delivered for that period. PROPOSED.
- Ledger: refunds are reversing rows, never edits (`ledger/SCHEMA.md`).

## 6. Records for taxes

Each charge, fee and refund goes into the private ledger with `fiscal_contract = F-001`, `source_ref` = processor transaction ID, `evidence = SOURCE-OBSERVED` only from a processor export. Monthly export kept per `records/RETENTION.md`. Sales tax / VAT handling depends on whether the storefront acts as merchant of record: UNVERIFIED.

## 7. Free-tier stack

GitHub Actions (crawler + digest build) · repository storage for the public sample · Pandoc for PDF · storefront hosting and email delivery. No paid resource is required. INFERRED.

## 8. Legal and attribution checks before any sale (UNVERIFIED)

- Each source's API terms must allow redistributing metadata in a paid product (Zenodo, Hugging Face, data.gov). data.gov metadata is generally U.S. government work, but each record's own license line must be honored and shown.
- CC-BY / ODbL records need attribution lines in the digest.
- Repository licensing is still unresolved (AGPL-3.0 part plus added terms, see mirror-claude RUN-LOG). The crawler code itself is not sold; only its output is. Timothy rules.

## 9. Done criteria for a Fiscal Contract proposal

1. Relevance filter implemented and a sample digest produced with zero off-topic records on manual review.
2. Storefront chosen and its fees read from the primary page on the day of proposal.
3. API terms for all three sources checked and cited.
4. Timothy approves price, refund window and storefront.

## 10. Refinement — scheduled run 2026-10-11T05Z (Claude)

New evidence from mirror-claude S1 batch 4 (75 catalog record pairs: last 3 data.gov, first 72 Hugging Face, `code-library-registry` @ 86785a0):

- EXECUTION-VERIFIED: 75/75 raw-response checksums match `record.json` (internal consistency only).
- EXECUTION-VERIFIED: relevance is source-specific. For the 72 Hugging Face records, 71 contain the search keyword (or all its words) in title or description; the one miss is `chendelong/linguistic-similarity` for `linguistics`, a stem match. The off-topic hits seen in batch 3 came from data.gov. So the relevance filter in §1 matters mostly for data.gov.
- EXECUTION-VERIFIED: 38 of the 75 records declare no license; 4 are `cc-by-nc` (non-commercial); 5 Hugging Face datasets are gated ("files need an account").

PROPOSED rules for the digest, to implement before any sample is published:

1. Relevance: publish a record only if a keyword (stemmed) or all its words appear in title or description; otherwise hold it for review. Data.gov records go to review by default until the filter is measured on them.
2. License line: show the declared license verbatim. Records with no declared license are listed as "license not declared — check before use" and never described as open.
3. Non-commercial (`*-nc`) records: list metadata only, flagged; never bundle their files. Whether listing NC-licensed metadata inside a paid digest is acceptable is UNVERIFIED and goes to Timothy with the source-terms check (§8).
4. Gated datasets: list with a "gated" flag; no access workaround.

Still UNVERIFIED after this run: GitHub Sponsors fee figures and the Hugging Face / Zenodo / data.gov API terms (primary pages could not be fetched from this run). No account, price or listing was created.
