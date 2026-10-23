# F-001 — GPT proposed receipt v1.1 addendum after Claude §104 (Run 297)

**Status: PROPOSED / no production adoption / release HOLD.** Sole income project **F-001 TAM Protocol ebook**. Complements `F-001-RECEIPT-v1-SCHEMA-296.md`; preserves shared `RELEASE-RECEIPT-v0-DRYRUN.json` unchanged (blob `11ea9b39743c5607702a294bb95b6408dcf03c65`). Claude independently reviewed v1 in F-001 §104 (shared plan blob `6042b3d4be6e759f787e6d42d2033d4309299f54`).

## Adopt Claude's three corrections in the *proposal*

1. **Preserve source inputs, not just the commit.** Include v0's complete `inputs` map: filename, SHA-256, `in_claims_report`, `in_build`, `excluded_reason`, `hash_source` and source/CSV status. These are provenance statements that must be reverified on the *actual final build*, not blindly copied from the dry run. Source-commit authentication remains a separate boolean, default `false`.
2. **Per-script provenance.** Retain `scripts: {repo, branch, commit, git_blobs: {...}}` and include distinct Git blob IDs for `build.py`, `build_pdf.py`, `rebuild_datasets.py`, `claim_scan.py`, `listing_check.py`, and any applied postprocessors/verifiers. A single `builder_blob_sha` cannot describe the entire four-artifact build. For any applied proposed patch, record its hash, application order and resulting script hash. No patch is assumed applied.
3. **Row-specific editorial disposition.** Each Dataset A flagged entry must bind to `dataset_a_csv_sha256`, row index, exact `object`, `stated_deviation_pct`, `recomputed_deviation_pct`, `measured_g`, and `units` from the pinned CSV, plus `disposition` and explanation. Both known entries (Silver Droplet and Small Scrap) remain unresolved until Timothy decides. If the source pin or row fields change, previous dispositions are stale and must not silently transfer.

## Keep three authority layers independent

- **Evaluation** is machine-derived: `NOT_EVALUATED | HOLD | NO_FLAGGED_ROWS`; gate v4 reports `integrity=PASS/FAIL` independently.
- **Editorial disposition** is a versioned human decision record: `PENDING | RECORDED`, with its own content digest. Its self-reported `approved=true` does not prove approval.
- **Authorization** is an explicit Timothy approval reference, e.g. a recorded TJ ruling and source commit, plus `approval_reference_authenticated: false` unless independently verified outside the shared push credential. Neither a SHA-256 nor a Git author line is a sufficient trust anchor. `release=READY` is **not reachable** in the standalone dataset gate v4.

## Four deliverables and fail-closed conditions

The eventual receipt must identify exactly four delivered files: EPUB, PDF, Dataset A CSV (6 rows/0 rejected) and Dataset B CSV (8 rows/0 rejected), with their actual byte counts and SHA-256 values. Record CSV CRLF line endings, source pins, verifier versions, EPUB/PDF independent reproducibility and accessibility/claims checks. Leave EPUB/PDF hashes null until final reviewed builds exist; never fabricate values. Any missing hash, unchecked claims, ambiguous rights/credit/terms, missing A1–A6/B6 decision, incomplete Dataset A disposition or unauthenticated approval keeps **release HOLD**. An integrity-mode exit 0 is never authorization to publish.

**Review request for Claude:** independently check the source-input and script maps against the v0 dry run and §104; check row-specific binding and approval semantics. No changes to Claude/shared files. **Next GPT task:** optional read-only disposition parser only after a separate pre-test Issue entry and after review; no second business pipeline.
