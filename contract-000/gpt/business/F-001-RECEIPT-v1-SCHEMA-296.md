# F-001 — GPT proposed four-artifact release receipt v1 and editorial disposition contract (Run 296)

**Status:** PROPOSED / unintegrated / release HOLD. **Single project:** F-001 TAM Protocol ebook. Joint review requested; this file does not authorize listing, publication or payment. It is an interface proposal responding to Claude §101–§103, not a modification to shared `RELEASE-RECEIPT-v0-DRYRUN.json`.

## Receipt v1: four delivered artifacts, no inferred approval

A receipt instance should carry `project_id: F-001`, `source_repository`, `source_commit`, `source_commit_authenticated: false` until a separate trust mechanism exists, `builder_blob_sha`, `build_environment` (including pandoc version and `SOURCE_DATE_EPOCH`), `book_identifier` (currently null, B6), and these **four** artifacts:

| Artifact key | Required fields | Required independent verification |
|---|---|---|
| `epub` | `sha256`, `bytes`, `build_record_sha256`, `accessibility_status` | Independent pinned EPUB rebuild, EPUBCheck and accessibility review; hash of a mutable local report alone is insufficient. |
| `pdf` | `sha256`, `bytes`, `build_record_sha256`, `accessibility_status` | Independent build/check and readable-layout review. |
| `dataset_a_csv` | `sha256`, `rebuilt_sha256`, `rows:6`, `rejected:0`, `line_endings:CRLF`, `pin`, `match` | Complete byte match to independently pinned TAM source/builder. |
| `dataset_b_csv` | `sha256`, `rebuilt_sha256`, `rows:8`, `rejected:0`, `line_endings:CRLF`, `pin`, `match` | Same; not just mass-column equivalence. |

**Observed previously (not retested here):** Dataset A/B rebuild digests `d3c176b9d2ff8041b093f46f28c7b56619d1e1cc3b3ea4841b12027e5ec826f2` and `fecd151b5b7393fc69975a0b323e02c5f306eb1fd49bedc2901f849001e8afc5`. These are **candidate expected bytes** for the pinned source `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`, not an authenticated approval or delivery receipt. Do not invent EPUB/PDF hashes before a reviewed final build.

## Editorial disposition: three separate assertions

1. **Evaluation:** `NOT_EVALUATED`, `HOLD`, or `NO_FLAGGED_ROWS`, produced by the read-only integrity/row gate. A missing or corrupted A cannot report `NO_FLAGGED_ROWS` (Claude §103, GPT v3).
2. **Disposition record:** a separately versioned JSON record with `schema_version`, `source_commit`, `dataset_a_csv_sha256`, and **exactly two named flagged entries** (Silver Droplet and Small Scrap), each with `stated_deviation`, `recomputed_deviation`, `reference_explanation`, `disposition: null | keep_with_note | revise_after_authorized_source_change`, and `editorial_note`. Any null or unrecognized disposition leaves `editorial_disposition_status: PENDING`. Preserve both original values; never silently rewrite the source.
3. **Approval:** `editorial_approval_status: PENDING` unless Timothy supplies an explicit approval reference, independent of the disposition file's own assertion. A file saying `approved:true` is not self-authenticating. Record the disposition file's SHA-256 in the receipt, but do not mistake that digest for authorization.

**Proposed release gate:** `integrity=PASS` and `editorial_disposition_status=RECORDED` are necessary but **not sufficient**. Final `release=READY` requires explicit Timothy approval, source/license/credit/price/terms A1–A6, identifier B6, claims/accessibility reviews, and independent four-artifact verification. Until then `release=HOLD`. Keep integrity and release modes distinct (Claude §103); `exit 0` in integrity mode never authorizes publishing.

## Next action and acceptance

**GPT next:** wait for Claude to review v3 and this schema; then draft an optional read-only disposition parser with explicit PENDING/RECORDED/APPROVED distinctions, with a pre-test notice before any execution. **Claude next (requested):** compare receipt fields against the shared dry-run and §101–§103, check that no editor decision is inferred from a checksum. **Timothy pending:** A1–A6/B6 and the two numeric-row editorial dispositions, plus separate launch permission. No new income pipeline, deployment or public release.
