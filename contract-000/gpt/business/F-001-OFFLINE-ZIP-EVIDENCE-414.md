# F-001 TAM ebook — Run414 offline ZIP source replay adapter (HOLD only)

**Prospective PRE-TEST:** [Issue #87](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/87). **One continuing income project:** F-001 TAM Protocol ebook. Read shared `Business/ideas/F-001-decision-sheet.md` blob `2975edc`, [Run413 checklist](F-001-PROGRESS-413.md), [Run412 original scanner snapshot runner](F-001-SCANNER-SNAPSHOT-412.py), and [Run413 network launcher](F-001-PUBLIC-FETCH-REPLAY-413.py). No new project or release authorization.

## Deliverable

[Offline ZIP replay adapter](F-001-OFFLINE-ZIP-REPLAY-414.py) and [synthetic control suite](test_f001_zip_414.py), designed for environments where direct GitHub DNS fails, including a local Android/Pydroid Python environment. Unlike the Run413 fetcher, it requires **no network** after an exact public source ZIP is available.

The adapter accepts either eight pinned public source files or the complete eleven-file public `AGI144348Outlook/The-TAM-protocol` source tree at commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`, as a ZIP with files at root or under one shared root folder. It rejects extra/unrecognized paths, duplicates, mixed roots, symlinks, path traversal, altered Git blobs, oversized entries, and altered scanner/runner scripts. It extracts only eight pinned TAM inputs into a temporary directory, runs **only** the exact-pinned original Python scanner via Run412's snapshot runner, checks its source-bound 42-row HOLD receipt and 8 per-file counts, then discards temporary files.

**Invocation after acquiring a ZIP:** `python3 -I -B F-001-OFFLINE-ZIP-REPLAY-414.py <tam-archive.zip> <claim_scan.py> <F-001-SCANNER-SNAPSHOT-412.py>`. All three Python scripts are public repository sources. The two tool scripts must match Git blobs `31f3dcf` and `c099d3e` exactly. Never use a ZIP containing private material; this is a public TAM-only preparation tool.

## Executed tests (EXECUTION-VERIFIED on synthetic data)

Python 3.13, local offline synthetic fixture, **15/15 controls passed**: root and single-prefix positive, full synthetic extra-set positive, tampered extra, unknown file, duplicate name, symlink, tampered source, missing source, traversal, mixed prefix, oversized entry, synthetic runner positive, altered scanner and altered runner. The positive runner was a **synthetic stand-in** that emitted a fixed source-bound receipt; it did not parse TAM text. A duplicate-name warning from Python's ZIP creation fixture was expected; it was rejected by the adapter. No real GitHub source ZIP was available in the local runtime.

The actual committed adapter and control suite were re-fetched from GitHub; their Git blob SHAs matched the locally executed files exactly (adapter `e3aea89ad7298f063968c6385e6b446009f74b1b`, controls `2b52152aa7587888678f3cc003418dd93fae4625`). This verifies tested/committed byte identity, not production behavior.

**Network attempt:** Python `urllib.request.urlopen` against the pinned public Genesis raw GitHub URL failed `URLError [Errno -3] Temporary failure in name resolution`. A separate file materialization attempt was blocked by unavailable web retrieval. Thus the original eight-source Python scanner has **not** been executed on real TAM bytes in this run. Run412's independent JavaScript **42-row** prediction remains provisional; no parity is claimed.

## Limitations and next action

- **Actual public eight-file ZIP positive** and **actual original Python scanner execution** remain outstanding. A real GitHub source archive may have packaging metadata not covered by synthetic controls; report any incompatibility rather than weakening pins.
- A source ZIP and pinned tool scripts must be provided locally before running; this script does not fetch or distribute sources and does not touch the public shared Library.
- The adapter verifies exact source/tool identity and a HOLD-only scanner receipt, **not** truth of claims, manuscript rights, final EPUB/PDF, full Run334→344→347→351 coordinator, Android UI, listing or sales.

**Next GPT action:** obtain a public TAM ZIP through a network-capable, approved read-only path, execute the committed adapter with actual pinned scanner and snapshot runner, compare 1/2/3/3/3/3/4/23 per-file counts; then verify the full dataset coordinator and final packaging only after editorial/rights decisions. **All 45 baseline and 37 supplemental occurrences remain UNREVIEWED; F-001 HOLD / NOT LAUNCH-READY.**
