# F-001 — TAM Protocol ebook: continuing product checkpoint (GPT Run 363)

**Single project identifier: F-001. Status: HOLD / NOT LAUNCH-READY.** No alternate income project. Read shared `Business/ideas/F-001-decision-sheet.md`, GPT checklist, Workshop README, Run 362 progress, and exact pinned Run 334 builder / Run 347 consumer before development. Claude owns complementary editorial, rights, claims, accessibility and listing review; GPT independently develops validation/packaging. The protected Contract/DISC repository remains 404 and was not bypassed.

## New development increment (evidence vs interpretation)

- [Prospective F-001 Issue #56](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6407889327) and [pre-execution Python amendment](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6407900829); [actual results in same thread](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6407918080).
- **Observed source compatibility:** pinned Run 334 builder emits report top-level keys `base_g_per_unit,source_commit,files`; A/B each `sha256,git_blob,rows,rejected`. These match the intended Run 362 supplementary checker shape. Run 358 historical report is from a different builder and intentionally incompatible.
- **Improvement:** [F-001-REPORT-PIN-363.py](F-001-REPORT-PIN-363.py), an independent read-only Python 3 strict JSON checker: duplicate keys/nonfinite values rejected, POSIX no-follow bounded file read, exact record keys/pinned source values, boolean row-count rejected, explicit HOLD regardless of consistency. Not integrated into shared or production gate.
- **Executed:** `python3 -I -B TEST-F-001-REPORT-PIN-363.py` in disposable local directory: **7/7 unittest methods passed**, including 13 corrupt-field subcases, nested/top duplicate keys, NaN, symlink, oversized, directory, absent file and positive/negative CLI exits. [Exact tested harness](TEST-F-001-REPORT-PIN-363.py). First GitHub upload transcribed the B SHA incorrectly; detected by comparing Git blob hash with locally tested source; corrected [commit dc443a9](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/dc443a915684a499a8ac4b41602f632836124877). Final file blob `53635fd721784de818612f0b808e24dfda48f9da` **equals** local tested Git blob. The test harness blob `73a3aeb417ade44ea4a1ab38fca0812f0f9fe85c` also matches.
- **Limitations:** fixtures synthetic, historical Run 358 shape synthetically reproduced. Local `git ls-remote` failed DNS resolution (`Could not resolve host: github.com`); exact TAM checkout, Run 334→344→347→351 Python stage and real HOLD receipt **NOT RUN**. The new checker does not authenticate a source signature, verify real bytes independently, solve ancestor symlink races, certify rights or approve publication.

## Same-product deliverables / acceptance criteria

| Deliverable | Current evidence / status | Next action and owner |
| --- | --- | --- |
| Single project F-001 TAM Protocol ebook | **KEEP**; no competing project | Continue until genuinely ready |
| Source rights, licence, material, credit and framing | **OPEN** A1/A3/A4/A6 | Claude: prepare evidence/options; Timothy: explicit decisions |
| Storefront, price, refund and payout | **OPEN** A2/A5/C1; no authorization | Draft only; Timothy approves |
| Article/terminology/rounding editorial | Article gap, Gerah ambiguity, precision observations | Claude independent editorial claims review; Timothy decides |
| Stable book identifier | **OPEN** B6 | Timothy selects fixed identifier before final reproducible build |
| Source pin | TAM commit `d46456a`, source A/B Git blobs and raw SHA-256 references documented | Obtain clean read-only exact source checkout |
| Stage-compatible Dataset A/B CSVs | Run 358 shared-builder outputs 9/8 columns, NOT Run 334 11/9; actual Run 334 NOT RUN | Execute pinned Run 334 on verified clean source |
| HOLD staging/receipt and tamper tests | Four-source static pin check Run 361; no real integration | Execute Run 344→347→351 stage and altered-file negative |
| Report shape and strict parsing | Run 363 7/7 Python methods, 13 corrupt-field cases; source field mapping confirmed | Independently run on actual Run 334 output; integrate only after review |
| EPUB/PDF accessibility, claims, rights and packaging | Shared historical checks; final artifact NOT independently verified | Claude editorial; GPT independent final hashes and format |
| Two-party signoff and launch | **HOLD / NOT LAUNCH-READY** | Timothy explicitly authorizes publication after acceptance |

**Acceptance criteria:** exact pinned clean source and independently verified file bytes; approved rights/credit/framing and resolved claim worksheet; reproducible EPUB/PDF and accessible packaging; real dataset builder and HOLD stage receipts with negative controls; consistent listing/terms and stable identifier; Claude/GPT cross-review; explicit Timothy publication authorization. A synthetic PASS is not a release.

**Immediate next action:** obtain authorized clean pinned TAM checkout, execute Run 334→344→347→351 under prospective Issue #56 pretest with real HOLD receipt and tamper control; independently inspect the editorial worksheet with Claude. **Outstanding Timothy decisions:** A1–A6, B6, C1, A-000 identity issuer/witness/recovery. No paid inference, autonomous Cloudflare loops, accounts, outreach, spending, payment or publication.
