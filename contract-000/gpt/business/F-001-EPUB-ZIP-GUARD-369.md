# F-001 TAM Protocol ebook — bounded EPUB ZIP preflight, Run 369

**Status: HOLD / DRAFT / NOT LAUNCH-READY.** Single income project F-001, not a new product. This is an unintegrated supplementary screen before the shared `epub_check.py`; it is not EPUBCheck, accessibility certification, malware detection, rights review or publication permission.

## Why this increment

Previous [Run 368 negative controls](F-001-LISTING-NEGATIVE-CONTROLS-368.md) executed the actual shared listing gate and showed it can accept a file with invalid EPUB bytes, because its purpose is marketing preflight. Fresh inspection of `library-shared:Business/ideas/F-001-tam-build/epub_check.py` (Git blob `176d42ee19f82580702a0bfc1941b0d28932ec31`) shows structure checks but no explicit archive entry-count, member decompression or compression-ratio budgets. A separate bounded preflight reduces exposure to malformed ZIP input without changing Claude's tool.

**Prospective test registration:** [Issue #56 comment 6413197606](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6413197606) was posted before writing or running the guard/tests.

## What was actually executed

In a disposable local directory on Linux, created [`f001_epub_zip_guard_369.py`](f001_epub_zip_guard_369.py) and [`test_f001_epub_zip_guard_369.py`](test_f001_epub_zip_guard_369.py). Ran `python3 -I -B -m unittest discover -v -p 'test_f001_epub_zip_guard_369.py'`.

**Observed: 20/20 unittest methods passed (0.020 s).** A minimal safe ZIP with the correct first uncompressed mimetype was admitted for **onward** validation, with status `HOLD_PASSED_ZIP_PREFLIGHT` (not a valid EPUB determination). Rejected synthetic cases: missing, late, compressed and wrong mimetype; duplicate member; `../` traversal; absolute, backslash and drive paths; symlink ZIP member and symlink input; extreme compression ratio; member, total and entry budgets; non-ZIP bytes; invalid limits. CLI checks confirmed exit 0 on a safe minimal ZIP and exit 2 on malformed input. No real TAM EPUB was processed.

**Verified source identities after GitHub write:** guard Git blob `d780ad1d8eb97538ebd1ad596de3f953a43ccaa3` (4243 bytes) and tests Git blob `4fdf63b8219889a9743897f96e37ec84400f51bd` (4089 bytes), each identical to the locally tested file. Local SHA-256: guard `1d18212fcd59cdef2e012580cc0c958973d93ed9752191aff42a3c57c175cc1d`, tests `fbfd852b000144290e364206b08826435fbc9af73a2b7b40c8d7762f3282be5a`.

## Limitations and next steps

The guard relies on ZIP central-directory metadata for size limits and reads only the 20-byte mimetype. It does not CRC-check every member, parse OPF/XHTML, verify accessibility, test Windows behavior, prove resistance to concurrent file replacement, or verify real EPUB/PDF/dataset bytes. Default limits (32 MiB archive, 500 entries, 16 MiB/member, 64 MiB declared expanded total, 200:1 compression) are **provisional** and may reject a legitimate future larger EPUB. Keep it unintegrated until Claude independently reviews the scope/limits and a prospective real-package run verifies `guard → epub_check.py → EPUBCheck/Ace → independent hash receipt`.

**Next GPT action:** obtain pinned real TAM build/stage via approved read path, run a preregistered actual EPUB against this guard and the existing structural checks, capture SHA-256 and failure logs; never turn guard PASS into release authority. **Next Claude action:** editorial/rights/Article 4/Gerah/claims and packaging review. **Awaiting Timothy:** F-001 A1–A6/B6/C1, final publication approval. No accounts, outreach, payments, publication, paid inference, Cloudflare loops or private Testament access.
