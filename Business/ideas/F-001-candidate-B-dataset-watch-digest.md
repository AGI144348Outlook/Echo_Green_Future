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

## 11. Refinement — scheduled run 2026-10-11T06Z (Claude)

New evidence from mirror-claude S1 batch 5 (75 catalog record pairs: last 9 Hugging Face, first 66 Zenodo, `code-library-registry` @ 86785a0):

- EXECUTION-VERIFIED: 75/75 raw-response checksums match `record.json` (internal consistency only).
- EXECUTION-VERIFIED: Zenodo relevance is poor, like data.gov and unlike Hugging Face. Applying rule 1 of §10 literally to the 66 Zenodo records, 13 pass. With stopwords (`of`, `and`, `the`, `a`, `in`) dropped from multi-word keywords and a slightly wider stem, 15 pass; if any single keyword word is enough, 39 pass.
- SOURCE-OBSERVED (record titles): clear off-topic hits include "Diving behaviors of juvenile northern and southern elephant seals" for `Harappan seals`, "Cotton verticillium wilt in Xinjiang" for `physics`, "Hypertension - Florida Annotated Corpus…" for `Indus sign corpus`, "Path and Row Indus River Basin" for `CISI Indus`. Plausibly on-topic records that the strict rule still rejects include "Harappan pot #1/#2", "Indus valley ceramics", "Etymologisches Wörterbuch des Deutschen: Stichwortliste". INFERRED: Zenodo's search matches single words, so a plain text filter both misses good records and passes bad ones.
- EXECUTION-VERIFIED licenses (66 Zenodo records): cc-by-4.0 56, cc-by-sa-4.0 2, cc-zero 2, cc-by-nc-sa-2.0 2, cc-by-nc-sa-4.0 1, cc-by-nc-nd-4.0 1, `notspecified` 1, none 1. So Zenodo licensing is much cleaner than Hugging Face (38/75 undeclared in batch 4).

PROPOSED changes to §10:

1. Replace the single relevance rule with three tiers: **auto** (strict all-words match after stopword removal), **review** (any-word match), **drop from digest** (no keyword word at all; record stays in the Library, only left out of the product). For this batch that would be 15 auto / 24 review / 27 dropped.
2. Treat `notspecified` like "license not declared".
3. Price per topic only after one month's review queue has been measured; if review stays above ~40% of records, the digest is not automatable yet and should not be proposed as a Fiscal Contract (INFERRED from §9 criterion 1).

Still UNVERIFIED: GitHub Sponsors fee figures and the Zenodo / Hugging Face / data.gov terms on metadata reuse (fetch of the GitHub Sponsors fees page and Zenodo terms page was not permitted in this unattended run). No account, price or listing was created.

## 12. Refinement — scheduled run 2026-10-11T07Z (Claude)

New evidence from mirror-claude S1 batch 6 (next 75 Zenodo catalog record pairs, `code-library-registry` @ 86785a0, ending at `zenodo/546302`):

- EXECUTION-VERIFIED: 75/75 raw-response checksums match `record.json` (internal consistency only); 150/150 blobs match the manifest.
- EXECUTION-VERIFIED: the §11 three-tier rule applied to these 75 records (stopwords `of/and/the/a/in` removed; a word counts as present if it appears whole or a title/description word starts with its first max(4, len−2) letters — a slightly looser stem than §11 used) gives **31 auto / 26 review / 18 drop**. Review share 35%, under the 40% line in §11.3 — but only just, and the stem rule is not yet fixed, so the two batches are not strictly comparable. INFERRED.
- SOURCE-OBSERVED (record titles): the review tier is mostly off-topic single-word hits ("Aerial survey counts of ice-associated seals in the eastern Bering Sea" for `Harappan seals`; "AI-Ready Ecuadorian Sign Language Corpus" for `Indus sign corpus`; "Egyptian blue glazed winged scarab" for `Corpus of Indus Seals and Inscriptions`). The drop tier contains at least one record that looks relevant: "The Dravidian Database: Reconstructed Lexicon of the Dravidian Subgroups…" (found for `Indus script`, but neither keyword word appears in its text).
- EXECUTION-VERIFIED licenses (75 records): cc-by-4.0 50, cc-zero 16, cc-by-sa-4.0 2, cc-by-3.0 1, cc-by-nc-sa-4.0 1, mit-license 1, none declared 4.

PROPOSED change: keep the three tiers, but add a small per-topic **allow list** of related terms that Timothy approves (e.g. for the Indus topic: Dravidian, Harappa/Harappan, Mohenjo-daro) and a **deny list** of known false friends (e.g. for `seals`: "elephant seal", "ice-associated seals", "harbor seal"). Both lists are data files beside the crawler config, versioned, and changed only by a logged commit. This should lower the review share without hiding real records. Not implemented; the crawler is not touched by this run.

Still UNVERIFIED: storefront fees other than Gumroad's, and the source terms on metadata reuse (no web fetch in unattended runs). No account, price or listing was created.

## 13. Refinement — scheduled run 2026-10-11T08Z (Claude)

New evidence from mirror-claude S1 batch 7 (last 28 Zenodo catalog record pairs, `code-library-registry` @ 86785a0; the `code-library-registry` manifest now has no INERT rows left):

- EXECUTION-VERIFIED: 28/28 raw-response checksums match `record.json` (internal consistency only); all 56 blobs match the manifest.
- EXECUTION-VERIFIED: the §12 tier rule (same stopwords and stem) gives **9 auto / 7 review / 12 drop**. Review share 25%.
- EXECUTION-VERIFIED licenses (28 records): cc-by-4.0 19, cc-zero 4, cc-by-sa-3.0 2, cc-by-3.0-at 1, cc-by-nd-4.0 1, other-open 1. INFERRED: `cc-by-nd-4.0` allows linking and describing but a digest must not ship modified copies of the data; `other-open` needs a manual look before listing.
- EXECUTION-VERIFIED test of the §12 allow/deny idea on these 28 records. Deny list (`elephant seal`, `ice-associated seal`, `harbor seal`, `harbour seal`) correctly moves "Increasing numbers of harbour seals and grey seals in the Solent" (found for `Harappan seals`) from review to drop. An allow list that also contained the bare word `indus` wrongly promoted two records to auto: "Indus River Shapefile" (for `CISI Indus`) and "Zooming in on ZooMS … Indus Valley Sites" (animal-bone protein work, for `Indus Valley script`). Without bare `indus` (only `Dravidian`, `Harappa/Harappan`, `Mohenjo-daro`, as §12 proposed) neither is promoted.
- SOURCE-OBSERVED (record titles): `lessersunda/lexirumah-data` (a lexical database, found for `linguistics`) falls in the drop tier although it looks relevant to the `my keywords` topics; "Two Multilingual Students in Tandem Language Exchange" and the German FastText embeddings (found for `Indus sign list`) are drop-tier and look correctly dropped.

PROPOSED: (1) the allow list must never contain a bare place or river name that the topic shares with geography (`Indus`); it should hold only script- or culture-specific terms. (2) A record dropped for one topic may be relevant to another topic; before dropping, test it against all topics' keywords, not only the keyword that found it (would rescue lexirumah-data under `lexicon`). Not implemented; no crawler change.

Zenodo summary across batches 5–7 (169 records): the review share went 36% (§11, looser comparison) → 35% → 25%. INFERRED: with the two proposals above the digest's Zenodo stream looks close to automatable; Hugging Face and data.gov still need their own measurement under the same rule before a Fiscal Contract proposal (§9).

Still UNVERIFIED: storefront fees other than Gumroad's and source terms on metadata reuse (no web fetch in unattended runs). No account, price or listing was created.

## 14. Refinement — scheduled run 2026-10-11T09Z (Claude)

This run's S1 batch (mirror-claude batch 8) contained no new catalog records (all 150 rows mirrored earlier decisions), so this refinement does the measurement §13 left open: the same tier rule applied to the **data.gov** and **Hugging Face** records in `code-library-registry` @ 86785a0 (72 data.gov, 89 Hugging Face `record.json` files in that tree).

Rule used (as in §12/§13): stopwords `of/and/the/a/in` removed; a keyword word counts if a title/description word equals it or starts with its first max(4, len−2) letters; tier = best over the record's `found_by_keywords`; deny list from §13; cross-topic rescue from §13 (a dropped record is tested against every other keyword for an auto match).

- EXECUTION-VERIFIED: **Hugging Face 89 auto / 0 review / 0 drop.** All 89 also pass on title alone (the title is the `owner/name` slug). 22 have an empty description, so the digest line for them would be the slug only. INFERRED: the Hugging Face stream is automatable for relevance; its problem is licensing, not relevance.
- EXECUTION-VERIFIED: Hugging Face licenses (89): none declared 44, cc-by 10, mit 9, cc-by-sa 8, cc-by-nc 7, apache-2.0 5, cc0-1.0 2, other 1. Half undeclared, matching §10.
- EXECUTION-VERIFIED: **data.gov 62 auto / 1 review / 9 drop** under the plain rule — but the rule is fooled here. 20 of the 62 auto records match only in the description, not the title. SOURCE-OBSERVED titles of those 20 include "Small Watershed Hydrology (WinTR-55)", "Airborne Magnetic Trackline Database", "National Insect and Disease Risk Maps - 2012", "NOAA Unified Access Framework (UAF)" (all for `philosophy`, INFERRED from words like "Doctor of Philosophy" or "design philosophy" in long descriptions), and "Geophysical Characteristics of the Conterminous United States", "Exxon Valdez Trustee Hydrocarbon Database" (for `lexicon`). A few description-only matches look relevant: "Native Languages Resources" (`linguistics`), "The 'four principles of bioethics' as found in 13…" (`philosophy`), "Drug Reference Vocabulary", "RadLex" (`lexicon`).
- EXECUTION-VERIFIED: data.gov licenses (72): none declared 46, cc0-1.0 18, U.S. public-domain label 3, U.S. government works 1, NIST open license 2, odbl 1, cc-by 1.
- EXECUTION-VERIFIED: the 9 dropped data.gov records are all "NEH grant data, 19x0–20x9" found for `linguistics`; no other topic's keyword rescues them. The deny list changed nothing in either source.

PROPOSED change (data.gov only): **auto requires a title match**; a description-only match goes to review. That gives data.gov **42 auto / 21 review / 9 drop** (review 29%), under the 40% line of §11.3, and puts every off-topic example above in front of a reviewer instead of in the product. For Zenodo and Hugging Face keep the §12/§13 rule unchanged (Hugging Face is unaffected: all its matches are in the title).

Status against §9 done criteria after batches 3–8: criterion 1 (relevance filter) now has a measured rule for all three sources (review share: Zenodo 25–35%, data.gov 29% with the title rule, Hugging Face 0%), still to be implemented and checked on one month of new records; criteria 2–4 unchanged (storefront fees other than Gumroad's and source terms on metadata reuse UNVERIFIED; Timothy's approval needed). The undeclared-license share (data.gov 64%, Hugging Face 49%) is now the larger obstacle: under §10 rule 2 these are listed as "license not declared — check before use", which may make the digest less useful to buyers. INFERRED. No account, price or listing was created; the crawler was not touched.

## 15. Refinement — scheduled run 2026-10-11T10Z (Claude)

This run's S1 batch (mirror-claude batch 9: 150 `library-source-transcriptions` catalog rows) again held only blobs identical to earlier-decided rows, so no new records. This refinement instead runs **one combined rule over the whole catalog** for the first time: all 339 `record.json` files in `code-library-registry` @ 86785a0 (72 data.gov, 89 Hugging Face, 178 Zenodo), rule = §12 tiers + §13 deny list and cross-topic rescue + §14 title-match for data.gov.

- EXECUTION-VERIFIED tiers: data.gov **42 auto / 21 review / 9 drop** (same as §14); Hugging Face **89 / 0 / 0**; Zenodo **69 auto / 54 review / 55 drop** (review 30%). Whole catalog: **200 auto / 75 review / 64 drop**, review share 22%.
- EXECUTION-VERIFIED license classes of the 200 auto records: open license 100, not declared (incl. `notspecified`) 83, non-commercial or no-derivatives 9, other 8 (three U.S.-government/NIST labels, one Zenodo `other-open`, four Hugging Face `other`). Not declared, by source: data.gov 36/42, Hugging Face 44/89, Zenodo 3/69.
- EXECUTION-VERIFIED by crawler topic section (auto only): "echo study topics" 111 (41 open), "my keywords" 85 (55 open), "indus valley script" 4 (4 open).
- SOURCE-OBSERVED false positive the Zenodo rule still lets through: zenodo:14941349 "Databases and scripts for Calvo, et al. Assessing the effect of glacier runoff changes on basin runoff…" is auto for `Indus script` because its description mentions the Indus basin and a code script. It is 1 of the 4 Indus-topic auto records.
- EXECUTION-VERIFIED alternative: applying the §14 title-match rule to Zenodo too gives **38 auto / 83 review / 57 drop** (review 47%), above the 40% line of §11.3. INFERRED: for Zenodo, title-only is too strict and title-or-description too loose; the deny list is the cheaper fix. PROPOSED deny entries for the Indus topic: `glacier`, `basin runoff`, `river basin` (reviewed and approved like §12's lists; not implemented).

What a digest line could look like, using one real auto record (metadata from its `record.json`, nothing invented; PROPOSED format):

> **The Indus Script: Preliminary Lexical and Functional Decipherment** — Zenodo 18421163 · license cc-by · found for `Indus script` · link and checksum of the stored API response from the Library record.

INFERRED conclusions so far: (1) relevance is close to automatable for the catalog as a whole (22% review); (2) licensing, not relevance, now decides what can be sold: only half of the auto records carry an open license, and data.gov's are mostly undeclared; (3) a first paid topic, if any, would most likely be built from Zenodo and the open-licensed Hugging Face records, where both problems are smallest. The Indus topic (4 auto records in the whole catalog so far) is too thin to sell alone.

Still open before any Fiscal Contract (§9): implement the rule and test it on one month of new records; read storefront fees and source terms from primary pages (no web fetch in unattended runs); Timothy's choices on storefront, price, refund window, and how undeclared-license records are shown. No account, price or listing was created; the crawler was not touched.

## 16. Refinement — scheduled run 2026-10-11T11Z (Claude)

This run's S1 batch (mirror-claude batch 10: 150 `library-source-transcriptions` rows, Hugging Face `Manojkl_Tulu-Dictionary` through `zenodo/10289404`) again held only blobs identical to earlier-decided `code-library-registry` rows; 75/75 raw checksums of its record pairs match (EXECUTION-VERIFIED). No new records, so this refinement checks the **license field itself**.

**Correction to §15.** The sample digest line in §15 shows Zenodo 18421163 as "license cc-by". That is what its `record.json` says (`provenance.license.value = cc-by-4.0`), but the record's own description ends: "All material is original and released for scholarly use under the CC BY-NC 4.0 license." (SOURCE-OBSERVED, `code-library-registry:Datasets/catalog/zenodo/18421163/record.json` @ 86785a0). The §15 line would have advertised a non-commercial dataset as freely reusable. The sample line is withdrawn; nothing was published.

- EXECUTION-VERIFIED scan of all 339 `record.json` files @ 86785a0 for license wording inside the description (cc-by variants, cc0, "creative commons", public domain, non-commercial, all rights reserved, MIT, Apache, GPL, ODbL, ODC-BY): 322 have no license wording; 15 are consistent with (or less specific than) the metadata; **2 are more restrictive than the metadata**: zenodo:18421163 (above) and zenodo:1291599 "Duhumbi Lexicon" (metadata `cc-by`; description mentions "CC BY-NC-SA" and "non-commercial").
- INFERRED: the metadata license field alone is not safe to print. Both conflicts sit in the lexicon/Indus records a first paid topic would be built from (§15 conclusion 3).

PROPOSED rule 4 for the digest (adds to §10): if the description names a license more restrictive than the metadata (NC, ND, "all rights reserved"), list the **more restrictive** one and flag the record "license conflict — check source page"; never resolve a conflict toward the more permissive reading. The scan is a regex, so it can miss wording; a manual look at each auto record's source page stays in the review step before any sale. Not implemented; the crawler is not touched.

Effect on §15 counts (INFERRED): open-licensed auto records drop from 100 to at most 98 (both conflicts were counted as open). The Indus topic has at most 3 auto records with a clean open license, still too thin to sell alone.

Still open before any Fiscal Contract (§9): unchanged from §15. No account, price or listing was created.
