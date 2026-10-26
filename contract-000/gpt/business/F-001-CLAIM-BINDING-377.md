# F-001 Run 377 — claim worksheet bound to source fingerprints (HOLD)

**Single income project:** F-001 TAM Protocol ebook; no second pipeline. **Pre-test:** [Issue #56 PRE](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6423541138), posted before execution. **Post-test:** [Issue #56 POST](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6423608224).

## Identified gap and evidence

Current shared `library-shared:Business/ideas/F-001-tam-build/claim_scan.py` blob `31f3dcff486c4c8cc96d514eb425da86834d00c3` writes `claims.csv` and `claims-report.json` with source SHA-256, per-file/trigger counts and candidate rows. Current `listing_check.py` blob `adc3123c303168650e03270701cd3123afe0ce28` requires marked statuses, but does not revalidate the claim ledger against the current source. A stale or edited worksheet can therefore appear complete without demonstrating that it still covers the source's trigger candidates. This is a source-observed *coverage gap*, not a demonstrated real release incident.

## New supplementary executable

- [Read-only source-binding verifier](f001_claims_binding_377.py), Git blob `b38061ed15d42525708aa8287c20e7d838bd0df2`, byte-identical to locally tested Python source.
- [14 synthetic regression tests](test_f001_claims_binding_377.py), Git blob `a699238044d02446d781590a9266b7237123e329`, byte-identical to locally executed tests.
- Usage in an offline scratch directory: `python3 -I f001_claims_binding_377.py <tam-source-dir> <claim-scan-output-dir>`. No repo edits, network calls or publication.

Verifier compares all eight required source files (refusing missing or symlinked files), SHA-256 to the scanner's report, report totals and trigger counts, exact ordered CSV candidate sentences/triggers/indices, allowed human status labels and file structure. It returns `structurally_reviewable` but **always** `status: HOLD` and `release_authorized: false`. A marked claim is not an authenticated fact; `cut` status is not proof that the final manuscript omits the sentence.

## Actual tests and limitations

**14/14 Python unittest methods passed** in local scratch. Positive: an independently constructed two-claim fixture passes structural review. Negative controls: source edit, dropped row, modified sentence, duplicate row, invalid status, open status, bad report hash, bad trigger count, missing source, source symlink, CSV symlink, reordered rows; all rejected. A `cut`-marked claim remained structurally reviewable, correctly still HOLD. The code/test Git blob hashes were fetched after commit and matched local `git hash-object` values.

**Not performed:** no real TAM source/claim-scan integration, no full pinned Run334→344→347→351 pipeline, no rights or provenance attestation of historical measurements, no manuscript inclusion check, no EPUB/PDF/a11y/listing certification. The checker mirrors current shared trigger semantics and may require review if that scanner changes. Synthetic fixtures cannot establish release readiness.

## Coordination and next

Claude: independently inspect whether `claimed`, `inferred`, `test`, `cut`, `sourced` are sufficient for editorial signoff; continue Article 4, Gerah, historical precision, author rights and claim evidence. GPT: on a future prospectively registered run, execute the real shared claim scanner and this checker against pinned TAM source, then bind approved claim dispositions to final manuscript output; do not change shared source without review. Timothy: decide A1–A6, B1/B4/B6 and C1; no default is authorization. **F-001 HOLD / NOT LAUNCH-READY.** No accounts, outreach, publication, payments, spending, paid inference, autonomous Cloudflare loops or CI.
