# F-001 candidate C — "Inert manifest + prune log" kit (small paid tool)

Draft, scheduled run 2026-10-11T14Z (Claude). Contract 000 §24–§26. Drafts only: no account, listing, payment, spend or contact was made. Needs a Fiscal Contract approved by Timothy before anything is built for sale.

Why a third candidate: candidate A (RFC ebook) is blocked on the manuscript's location and rights; candidate B (dataset digest) measured thin (§17 there: about 8–10 sellable lines a month). This one uses only a method already exercised in this project, so it has no third-party content or licensing blocker of the kind A and B have.

## 0. What exists today (evidence)

- EXECUTION-VERIFIED: the S1 pick/prune method has decided 1,866 rows across three branches in 13 hourly batches (`mirror-claude` CHECKPOINT): a status-preserving inert manifest per branch (`status, blob_sha, bytes, path`), a one-line-per-decision prune log with a restore note, provenance registers per sub-library, mirroring of decisions across identical blobs, and blob re-verification against the current branch head.
- SOURCE-OBSERVED: the scripts used are throwaway per-run scripts; nothing reusable or packaged is committed. The kit would be new code.
- Not used: the `code_library_registry/modules/MOD-*` code, whose licensing is unresolved (AGPL-3.0 part plus added terms, per its provenance.json). The kit must not include it.

## 1. Product (PROPOSED)

A small command-line tool plus templates, one-time download:
- `manifest list <ref>` → inert TSV manifest of a git ref (no blob downloads needed with `--filter=blob:none`; avoids `ls-tree -l`, which fetches every blob lazily — found the hard way this run).
- `manifest decide` → applies KEPT / PRUNED / DEFERRED with reason; appends the prune log line; refuses a decision without a reason.
- `manifest mirror` → carries a decision across identical blobs in other manifests (same path preferred), flags rows whose blob changed since listing.
- `manifest verify` → re-checks every decided row against the ref's current head.
- Templates: PRUNE-LOG.md, REGISTER.tsv, CHECKPOINT.md.
Use case: archivists, research groups and solo maintainers who must triage a messy repo or data dump reversibly, with an audit trail.

## 2. Customer (INFERRED, unverified)

Small research and digital-archive teams; maintainers inheriting large repos. Demand is unmeasured. Free tools cover parts of it (`git ls-tree`, `git-filter-repo` analysis, DVC); the sellable difference is the reversible decision log and cross-branch mirroring, not the listing itself. A free core with a paid "templates + guide" bundle may sell better than a paid core. Open question, not a claim.

## 3. Delivery (fully automatable)

1. Source in a repository Timothy chooses; tests run on GitHub Actions (free tier, non-`main` branch until approved).
2. Tagged release builds a zip + sha256 file (Actions). PROPOSED.
3. Timothy uploads the zip to the storefront once per release (same pattern as candidate A §3; no bot holds storefront credentials).
4. Buyers get updates per the listing text; free core (if chosen) stays on GitHub under a license Timothy picks.

## 4. Pricing and fees

| Item | Value | State |
|---|---|---|
| Price | placeholder $15 one-time (paid bundle) | PROPOSED, Timothy decides |
| Gumroad direct-sale fee | 10% + $0.50 | SOURCE-OBSERVED in candidate A §4 (2026-10-11); processing/payout/sales-tax handling still UNVERIFIED there |
| Net per direct sale at $15 | $15.00 − ($1.50 + $0.50) = **$13.00** | INFERRED arithmetic, same caveats |
| Alternative | GitHub Sponsors one-time tier | fees UNVERIFIED (see RUN-LOG 06Z note on web checks) |

## 5. Refunds and cancellation

One-time purchase; nothing to cancel. Refund on request within 30 days (PROPOSED, same as A §5). Ledger records a reversing row, never an edit (`ledger/SCHEMA.md`).

## 6. Records for taxes (§26)

Same as candidate A §6: monthly private export of sales/payouts into the private ledger per `ledger/SCHEMA.md`, `fiscal_contract` = `F-001`; no figures, customer names or emails in this public repository. Sales-tax treatment of software downloads differs from ebooks in some US states — UNVERIFIED, add to law-watch.

## 7. Free-tier stack

| Need | Tool | Cost |
|---|---|---|
| Code, tests, release builds | GitHub + Actions | free tier |
| Storefront, checkout, delivery | Gumroad (or Sponsors) | per-sale fees only |
| Private ledger | as open decision 13 | free tier |

## 8. Stop conditions (draft)

- Any report that the tool lost or altered a user's data → pull the release, Timothy reviews (the tool must be read-only on source branches by design).
- Refund rate above an agreed threshold, or a processor warning → pause.
- Net income measured by someone other than the builder (§25.3).

## 9. Honest assessment (INFERRED)

Lowest risk of the three (own method, no third-party content), but also the least proven demand. Copyright status of AI-written code is unsettled law; Timothy should treat "who owns the kit" as a law-watch item before sale. If A's manuscript surfaces, A is likely the better first product; C could be its free-tier companion or a second listing.

## 10. Questions for Timothy

1. Worth building at all, as paid, free-core-plus-paid-bundle, or free only?
2. If built: in which repository, under which license?

## 11. Refinement — scheduled run 2026-10-11T15Z (Claude)

S1 finished this run, so the method's full record now exists. Drafts only; nothing built, listed or sold.

**Final numbers (EXECUTION-VERIFIED, `mirror-claude` after batch 14).** 1,985 manifest rows across three branches decided in 14 hourly batches: 1,912 KEPT, 22 PRUNED, 51 DEFERRED (from the CHECKPOINT position table). Only 927 distinct blobs; 850 of them sit at more than one path or branch, so decision mirroring did most of the work.

**Real failure cases the kit must handle (each met during S1; these become its acceptance tests):**

| # | Case met | Kit behaviour (PROPOSED) |
|---|---|---|
| T1 | Manifest listed at an older commit than the branch head (two branches) | `verify` reports rows whose blob changed; such rows can only become DEFERRED until re-listed |
| T2 | `git ls-tree -r -l` on a partial clone fetched every blob and timed out | `list` reads sizes in one batched `cat-file --batch-check` call, never per-row lazy fetches |
| T3 | Same blob at several paths with different earlier decisions (license snapshots equal to root `LICENSE`) | `mirror` prefers the decision at the same path, then asks; never silently picks |
| T4 | Crawler re-fetched a record after listing (old and new blob both present) | DEFERRED with both SHAs in the log line |
| T5 | **Found this run:** 51 rows, all from batch 8 (42 `code-library-registry-ivs`, 9 `library-source-transcriptions`), are registered as a *primary* entry in two sub-libraries instead of one primary plus an `xref-from:` row | `verify` fails when one (branch, path) has two primary register rows; the per-run scripts had no such check |
| T6 | A decision with no reason | `decide` refuses it |

T5 is the useful one for the sales case: it is a defect the hand-run method produced and did not catch, which is exactly what a packaged checker would prevent. (The 51 rows are logged in `mirror-claude` RUN-LOG for a later correction pass; not fixed yet.)

**Smallest sellable version (PROPOSED).** `list`, `decide`, `mirror`, `verify` with T1–T6 as frozen tests, stdlib Python only (no dependencies to license), plus the three templates. Estimated at a few hours of bot time on a non-`main` branch once Timothy says build (INFERRED; not measured).

**Unchanged:** price placeholder, fees, refunds, tax records and stop conditions as §4–§8; the questions in §10 still decide whether any of this happens.
