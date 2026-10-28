# F-001 TAM Protocol ebook — pinned source snapshot gate (Run428)

**Project:** F-001 only, speculative research-notebook ebook. **Status: HOLD / NOT LAUNCH-READY.** **PRE-TEST:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/101. No accounts, sales, publication, outreach, spending, payment, paid inference, CI or Cloudflare loops.

## Problem and deliverable

Original shared `claim_scan.py` (Git blob `31f3dcff486c4c8cc96d514eb425da86834d00c3`) was previously executed only on synthetic inputs: a missing one of eight files still exits 0 and writes a partial worksheet. Run427's JS inventory of actual public TAM files gave **42 original-pattern / 44 enhanced** candidates, but original Python has **not** been executed on the real eight files. An input-completeness guard alone cannot tell whether a file's contents match the pinned corpus.

**New GPT-owned proposed tool:** [`f001_pinned_source_snapshot_428.py`](f001_pinned_source_snapshot_428.py), bound to public `AGI144348Outlook/The-TAM-protocol` commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`. Its eight Git blob SHA-1 pins were read from that exact tree through the GitHub connector. It checks all eight required flat filenames for nonempty, regular, non-symlink, strict UTF-8 content and the exact Git blob hash **before** creating a new scratch snapshot; writes a `PREPARED_HOLD` receipt with SHA-256s and `release_authorized=false`. It does not write to the source repository or shared Library.

**Usage once a local copy of the real public TAM sources is available:**

```bash
python3 -I -B f001_pinned_source_snapshot_428.py /trusted/tam-clone /trusted/new-snapshot
# Then, separately, using original shared scanner:
python3 -I -B claim_scan.py /trusted/new-snapshot /trusted/new-worksheet
```

Both destination folders must be outside the source; snapshot destination must not exist. The snapshot is a preparation aid, not a publication or source-rights clearance.

## Executed verification (synthetic data only)

[Committed regression harness](test_f001_pinned_source_snapshot_428.py) executed locally with Python 3 on eight synthetic UTF-8 files and synthetic pins injected into the `snapshot()` function. **14/14 assertions PASS**: complete eight-file snapshot, HOLD receipt, copied-byte Git pins, SHA-256 receipt, disk receipt parity, existing destination rejection, output-inside-source rejection, unrelated source preservation, missing file, empty file, changed bytes, invalid UTF-8, source symlink, and source-root symlink rejection. Both committed script Git blobs match the locally executed bytes:

- Gate: `b50c8341d7be4d6392d345c84e4ed12d05fdd3b8`.
- Test harness: `856e22a6c7e44288dd0c0a6e26cde44c95472f22`.

**Attempted real-source test: BLOCKED.** Local Python DNS probes for `raw.githubusercontent.com`, `api.github.com`, and `github.com` all returned `gaierror [Errno -3] Temporary failure in name resolution`. The GitHub connector can read the real public files but does not directly mount them in the Python execution container. Thus **no real-source Python scanner parity claim** and no original Python execution on real TAM bytes in Run428. The 42/44 candidate inventory from Run427 is not newly Python-verified.

## Security and correctness boundaries

- A Git blob SHA-1 identifies content, not ownership, historical accuracy, copyright, or an independently authorized pin. The source commit is hardcoded for reproducibility but its choice still requires provenance/rights review.
- `stat()` then `read_bytes()` has a TOCTOU window; `os.rename()` in a trusted scratch parent is not an adversarial multi-user atomic no-replace protocol. The receipt does not attest to external custody, durable power-loss recovery, or a second verifier.
- The tool is **unmerged** into the shared builder/coordinator and untested on the eight actual TAM texts, Android, EPUB or PDF. It does not solve the original scanner's regex coverage, missing-file exit status, or its output semantics.
- The original 82 editorial occurrences (45 baseline + 37 supplemental) are **ALL UNREVIEWED**. The 44 candidate rows are a different queue and do not replace them.

**Next action:** get the eight exact public source blobs into a trusted local read-only scratch folder, verify all eight pins with this gate, run original `claim_scan.py` on the staged snapshot, compare its per-file 42/44 selection to the JS inventory, and complete coordinator 334→344→347→351 positive/tamper-negative verification. Claude independently reviews scientific/historical claims and rights. Timothy decides A1–A6/B1/B4/B6/C1, editorial dispositions, attribution and publication. **F-001 remains HOLD.**
