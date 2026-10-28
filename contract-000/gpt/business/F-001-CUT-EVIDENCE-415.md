# F-001 TAM Protocol ebook — listing/cut disposition verification, Run415

**Project remains F-001 only, HOLD / NOT LAUNCH-READY.** [Prospective PRE and fallback addendum, Issue #88](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/88). No real customer, sale, publication or claim approval.

## Exact source and observation

Read `library-shared:Business/ideas/F-001-tam-build/listing_check.py` blob `adc3123c303168650e03270701cd3123afe0ce28`. Its `DONE` includes `cut`, and the source checks whether every CSV status belongs to `DONE` but does not read the manuscript to confirm the sentence was actually removed. [Pinned verbatim copy](F-001-LISTING-CHECK-PINNED-415.py) has the **same Git blob** as the shared original. This copy is isolated evidence, not a proposed edit of shared source.

## Synthetic execution and controls

Using Python 3.13 in temporary local fixtures, generated a one-row `claims.csv` with `status=cut`, a `tam-draft.md` **still containing the supposedly cut sentence**, and an otherwise benign listing. Executed the byte-identical original listing checker as a subprocess: **exit 0, PASS**. This demonstrates a narrow false-positive listing gate under this synthetic condition; it does **not** demonstrate that Timothy's actual TAM draft contains an unremoved cut.

Created independent [F-001-CUT-DISPOSITION-GATE-415.py](F-001-CUT-DISPOSITION-GATE-415.py) (Git blob `6ae96fee668e714eff5d4c8d4082736e529ed9bc`) and [reproducible synthetic test suite](test_f001_cut_415.py) (blob `c816ecfb6403d1cab180133db156c6475b18762c`). **16/16 final checks passed**: original false PASS, new rejection of present cut, positive cut-absent and sourced-present cases, and rejection of blank/unknown status, duplicate ID, empty ledger/sentence, malformed sentence number, normalized whitespace/zero-width present cut, expected-row mismatch, missing ledger and missing manuscript. Exact committed script/test blobs were independently fetched and matched the locally executed bytes.

The new guard reads only local CSV and Markdown; refuses unresolved statuses, duplicate source IDs and missing inputs; normalizes Unicode/whitespace; rejects a `cut` sentence still present. Every successful receipt says `HOLD / NOT LAUNCH-READY`, `editorial_approved=false`, `release_authorized=false`. **It is a supplemental draft consistency gate, not a replacement for the original listing checker, source pins, human review or final package checks.**

## Failures / deviations / limits

- Local DNS resolution for `api.github.com`, `raw.githubusercontent.com` and `github.com` returned `socket.gaierror [Errno -3]`. Therefore **the original eight-source Python scanner against real TAM files was NOT RUN**; Run412's independent JavaScript 42-occurrence estimate remains provisional. Run414's exact-pinned offline ZIP replay adapter remains the pending real-source route.
- This test uses **synthetic** one-row editorial inputs; the real **45 baseline + 37 supplemental occurrences remain UNREVIEWED**. A CSV row can be forged, and this guard alone does not prove source identity, provenance, historical/scientific accuracy or final EPUB/PDF parity.
- The text match is conservative but not complete: significant Markdown rewriting, paraphrases, image/EPUB text or HTML rendering could evade direct normalized sentence comparison; conversely, a quoted cut sentence retained as an editorial note could cause a false refusal. A true release gate needs source-pinned, build-bound disposition tracking and human signoff.
- No tests were run on actual source documents, Android, full coordinator, final EPUB/PDF, paid API, CI or Cloudflare.

## Next acceptance action

1. Obtain the exact eight public source files through an authorized read-only ZIP and run the pinned original Python scanner with the Run414 adapter; record a source-bound HOLD receipt, or explicitly report count disagreement.
2. Once Timothy and Claude complete editorial dispositions, bind each source occurrence to a **specific final manuscript/build version** and run the cut gate plus original listing checker and independent export/EPUB checks.
3. Preserve F-001 HOLD until all rights, price, credit, identifier, storefront, refund and publication approvals are explicitly decided by Timothy. Claude owns independent evidence/rights review; GPT owns reproducible packaging and verification.
