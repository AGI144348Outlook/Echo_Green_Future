# F-001 sole-project source preflight — Run434

**Status:** F-001 TAM Protocol speculative research-notebook ebook; **HOLD / NOT LAUNCH-READY**. Prospective plan and actual POST: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/110.

## Identified problem
The original shared `Business/ideas/F-001-tam-build/claim_scan.py` Git blob `31f3dcff486c4c8cc96d514eb425da86834d00c3` has a fixed eight-source list but for a missing file records `source_files[name] = None`, skips it, and returns normally. Thus a syntactically successful scan can omit part of the real manuscript. This source read does not establish a real production incident.

## GPT-only separate preflight (not a patch to shared source)
- `f001_source_preflight_434.py`: exact 8 filenames, nonempty regular files, no direct file/source-dir symlinks, strict UTF-8, 8MB/file cap, source/out separation, exclusive new receipt, deterministic SHA-256 per-file manifest. **It does not run the original scanner or authenticate a source against an external pinned Git blob.**
- `test_f001_source_preflight_434.py`: 16 synthetic tests covering positive count, hashes, deterministic repeat, changed digest, missing, empty, invalid UTF-8, source/file/output symlinks, directory instead of file, write inside source, no-clobber, missing output parent, size cap and source unchanged.
- **Actual local execution:** first `python -I test_f001_source_preflight_434.py` exited 1 with `ModuleNotFoundError` because isolated Python removes script directory from import search. This was a **harness invocation failure**, not a failing control. Corrected invocation `PYTHONDONTWRITEBYTECODE=1 python -B -m unittest -v test_f001_source_preflight_434.py` ran **16/16 PASS**, 0.065s, exit 0. No test edits required.
- **Exact executed bytes independently matched committed Git blob IDs**: preflight `59720d729e0a63ec2ee2d656a4f2f4e7468fe305` (local SHA-256 `c1f3602b8d3c9b3dd7aa98df7d0dc89f3329a6abf51f3231001815448ec5a946`); tests `082c7bdfa9d72774775ac4dc80a928d9c7bdb2e2` (SHA-256 `6a56e7099ef6e9e506c50e19e576e67b682b8a01caf6931626f7038478cdc00a`).

## Limits / acceptance
This is a local **synthetic fixture** test; no eight-real-TAM-source snapshot, no original `claim_scan.py` replay, no 82-row parity, no full coordinator 334→344→347→351, EPUB/PDF/Android, rights review or publication. A malicious source can be modified after preflight (TOCTOU), and the receipt is self-reported without independently pinned hashes. An interrupted write can leave a partial manifest; a production coordinator must stage atomically, pin inputs and fail closed on errors. A receipt does not certify editorial truth or external archaeology. Preflight cannot be called release-ready.

**Next GPT action:** trusted eight-file local source snapshot from GitHub connector with exact source blob checks; bind preflight to pinned expected hashes; replay original claim scanner and compare all 82 editorial queue occurrences; then test coordinator positive/tamper-negative. Claude independently reviews historical claims, rights, chronology and proposed patch dependencies. Timothy alone decides A1–A6/B1/B4/B6/C1 and release authority. No second income project, accounts, outreach, spending, payments or publication.
