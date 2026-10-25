# F-001 — release-receipt integration map (GPT Run 342; DRAFT / HOLD)

**One project only:** F-001 TAM Protocol ebook. This is a **read-only design map**, not a release receipt, accepted manuscript, verified package or permission to publish. Shared source: `library-shared@470d3c827fd1cdd5e96b4f4ca91281e02d676bad`, `Business/ideas/F-001-tam-build/RELEASE-RECEIPT-v0-DRYRUN.json` blob `11ea9b39743c5607702a294bb95b6408dcf03c65`. Do not replace that Claude-owned artifact without review.

## What the existing dry run actually records

| Receipt field | Current source-observed state | Required for a *future* independently verified package |
| --- | --- | --- |
| `source.commit` | `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9` | Explicit Timothy A1/A6 choice and clean source/blob checks. |
| `claims_worksheet.sha256_after_signoff` | `null`; editorial statuses unapproved | A named signoff on every flagged claim, source evidence or clearly marked inference, then SHA-256 of the signed worksheet. `claimed` alone is a classification, not factual verification. |
| `pdf.sha256` | `null` | Independently opened/inspected final PDF, accessibility and TOC checks, source/build/tool pins, exact SHA-256 and byte count. |
| `epub.sha256` | `null` | Stable B6 identifier and date, independent EPUBCheck/Ace or documented equivalent, exact SHA-256 and byte count. |
| `dataset_csvs.sha256` | `null`, historical note says CSV not generated | New **independently tested** pinned A/B CSVs, exact hashes and counts; preserve A rows 6/7 and *Gerah* as editorial disputes until Timothy rules. |
| `verifier_versions` | `missing` | Exact script Git blobs, test source pins, verification commands, CI/scratch environment and evidence links. |
| Release decision | `DRY RUN` | Never infer release from a successful stage. Timothy must separately authorize rights, listing, pricing and publication. |

**Important temporal distinction:** The shared dry-run receipt predates GPT's Run 332–341 candidate CSV/staging artifacts. A newer draft gate's `STAGED_ONLY` marker **must not be spliced into the historical receipt as though it verified a final EPUB/PDF**. The GPT Run 342 stage session, even if it later passes tests, proves at most that *one current dataset-stage invocation* is internally consistent. Its `release=HOLD` must remain unchanged. Editorial signoff and final receipt are separate steps.

## Single-receipt proposal (for Claude review, not adopted)

1. Timothy selects A1–A6 and B6; source branch, rights and exact credit are recorded. No silent draft defaults become approvals.
2. Claude performs independent editorial and rights/claims review; publish only public-safe summaries, not private manuscript/financial records.
3. GPT runs an **authorized, prospectively registered** pinned dataset-stage verification in a disposable location, records exact inputs, outputs, hashes, process exit, and same-Issue post-test report. Until then, `dataset_csvs` remains unqualified.
4. Claude builds review-edition EPUB/PDF under the approved book identifier and source epoch; GPT independently verifies actual final bytes, accessibility and checksum evidence. No simulated hashes.
5. One reconciled `REVIEW-RECEIPT.json` or renamed `RELEASE-RECEIPT` (not competing parallel receipts) binds **all** required SHA-256 values, source/script blobs, editorial approvals and unresolved limitations. Reject null/missing fields and mismatched source editions. A signed review receipt is still **not** publication authority.
6. Timothy explicitly authorizes storefront/account/payment/publication actions separately. Default status: **HOLD / NOT LAUNCH-READY**.

**Acceptance criteria:** One named F-001 project; no unapproved secondary income pipeline; independent source and output verification; claims adjudicated; stable EPUB/PDF and CSV bytes; final receipt consistent with approved source; zero open release-blocking fields; Timothy's explicit release authorization. A dry run, staging marker, or a green synthetic CI job cannot satisfy these by itself.

**Next action:** Claude independently challenge the single-receipt mapping and the source/editorial boundary. GPT must first regain current Contract-000/protected DISC-002 access and test the proposed Run 342 process-control draft against Issue #53 P40–P47 before any promotion. No new test executed here. No accounts, outreach, publication, spending, payments, paid inference or Cloudflare loops.
