# F-001 TAM ebook — post-snapshot consumer verification, Run429

**PRE:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/102. **Only active income project:** F-001 speculative research-notebook ebook. **HOLD / NOT LAUNCH-READY**. No publication, storefront, account, payment, customer data, or release approval.

## What was inspected

- Previous Run428 [source snapshot gate](f001_pinned_source_snapshot_428.py), exact blob `b50c8341d7be4d6392d345c84e4ed12d05fdd3b8`, and its [synthetic tests](test_f001_pinned_source_snapshot_428.py). It validates eight pinned TAM files and writes a `PREPARED_HOLD` receipt, but the subsequent consumer was not independently verifying staged bytes and receipt.
- Original shared `library-shared:Business/ideas/F-001-tam-build/claim_scan.py`, Git blob `31f3dcff486c4c8cc96d514eb425da86834d00c3`. It reads file paths, and is not itself a pin/receipt verifier. Its missing-file success was previously reproduced in Run427.
- The eight **real** public TAM files at `AGI144348Outlook/The-TAM-protocol` commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9` were fetched separately through authenticated GitHub read tools; **8/8 returned blob SHAs exactly matched the Run428 PINS**. This is source-identity verification via GitHub, **not** local materialization, original Python scanner execution or a release claim.
- Local scratch DNS attempts for `github.com`, `api.github.com`, and `raw.githubusercontent.com` each failed with `gaierror [Errno -3]`; original Python claim scanner against all eight real files **NOT RUN**.

## New HOLD-only deliverable

[Consumer-side verifier](f001_snapshot_consumer_verify_429.py), **exact executed source blob `050d885362e1828ffb3e56f896cb006396c3a362`**, checks a staged snapshot *again*, using **independent hard-coded Git pins**, before a downstream scanner is allowed to consume it. It rejects missing/extra files, symlink paths, changed bytes, malformed/altered receipts, incorrect `source_commit`, status/release flag changes, and wrong inventory or hashes. It does not modify the source or change the release state. The CLI uses fixed PINS; an override exists only for synthetic tests.

**Execution:** Python 3, `python3 -I -B test_f001_snapshot_consumer_verify_429.py` on synthetic placeholder texts. **18/18 checks passed**: three positive assertions and fifteen negative controls (altered source, missing, extra, bad UTF-8, empty, wrong independent pin, missing/malformed receipt, flipped release flag, wrong commit, status flip, extra receipt field, empty inventory, source symlink, root symlink). [Reproduction harness](test_f001_snapshot_consumer_verify_429.py) committed; local execution used the exact verifier bytes, confirmed by Git blob comparison. This is not a production adversarial security audit or actual TAM end-to-end test.

**Limits:** The verifier operates in a trusted single-user scratch directory; `stat`/read and verify/consume remain vulnerable to concurrent hostile filesystem mutation. It does not use openat directory-fd custody or atomically hand verified open handles to `claim_scan.py`. It does not authenticate the choice of the source commit, scientific claims, rights, or human editorial statuses. The **committed verifier** Git blob `050d885362e1828ffb3e56f896cb006396c3a362` and **committed synthetic harness** Git blob `14eac79c57f1ab7205f6d5ad67503a639156a070` both matched their locally executed bytes exactly. The apparent three-character difference in one preliminary length printout came from UTF-8 multibyte characters, not a source mismatch. No full coordinator 334→344→347→351, real-source scanner, EPUB/PDF/Android, Node CLI, or CI executed.

## Acceptance / next

1. In a trusted scratch environment, materialize all eight exact public Git-pinned source files and stage through Run428 snapshot gate.
2. Invoke the new Run429 consumer verifier on the completed snapshot, then original `claim_scan.py` immediately, with output elsewhere. Capture per-file and per-trigger rows; compare with the existing **42 original-pattern / 44 enhanced JS candidate** inventory. The new verifier is a **proposal**, not an integrated guarantee.
3. Review source/snapshot race assumptions; for hostile multi-user environments use directory-fd custody and immutable/read-once handoff, not check-then-use path trust.
4. Preserve **all 82 editorial occurrences (45 baseline + 37 supplemental) as UNREVIEWED** pending Claude/Timothy independent evidence and rights review. No claim is promoted by a passing integrity check.
5. Keep **F-001 HOLD / NOT LAUNCH-READY** pending complete coordinator, editorial rights, deterministic EPUB/PDF/Android QA, listing/credit/price decisions, and Timothy's explicit release authorization.
