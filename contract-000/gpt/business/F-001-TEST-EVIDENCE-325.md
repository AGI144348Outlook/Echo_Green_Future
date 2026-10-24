# F-001 — GPT Run 325 prospective ZIP32 v5 test evidence (2026-10-24 CT)

**Status:** DRAFT / HOLD / BLOCKED / NOT LAUNCH-READY. **Pre-test published before execution:** [Issue #44](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/44) created 2026-10-24T15:10:29Z; [post-test narrative](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/44#issuecomment-6385855069). No CI, paid inference, source mutation, public release or Cloudflare loops.

## Source pins / method

- Repository `mirror-chatgpt-root`: v4 Git blob `4e295a8e0ad66cdb45148a937a2ce43fce5b0857`, SHA-256 `3bffac5a9877cc110634dcc8d5eef9b5708a2819ae722b59d1e0f8857b2a9660`.
- Proposed v5 Git blob `cb1f7ee73b51b24d1462b335628220ec2f89c286`, SHA-256 `89c2bb512f20b5b8e7dd40a4f63fc32af52745bcac48a65ebf294d3f34fe3ab5`.
- Both local `git hash-object` values matched repository blobs before tests. Local Python 3.13.5 `-I -B`, synthetic ZIP32/EPUB fixtures; source and inputs read-only. Exact local harness SHA-256 `5cf42996400538ded19d991bfa0bcb972b09890d6541ae3ed42bb83c90b83152`; JSON results SHA-256 `49229dde5a73fc9ab95e4bc7228758748171f6a11c7ea43c58a4e6465c6ff6c7`. Harness and JSON preserved in Run 325 handoff ZIP, not claimed to have been executed by GitHub Actions.
- Local v5 source was reproduced from the pinned v4 file by the same deterministic replacement used to create v5 on GitHub, then checked against the Git blob. No live private materials.

## Observed outcomes (final corrected execution)

| Case | Expected | Observed |
|---|---|---|
| P0 | coherent synthetic ZIP PASS/HOLD | v4/v5 PASS/HOLD |
| P1 | file ancestor collision FAIL/HOLD | both FAIL, `file used as directory ancestor` |
| P2 | explicit directory and child PASS/HOLD | both PASS |
| P3 | NFC/NFD casefold ancestor FAIL/HOLD | both FAIL, ancestor issue |
| P4 | intervening `a-` name must not hide `a/b` | both FAIL, ancestor issue |
| P5 | 65,535-byte deep member PASS/HOLD, v5 faster | both PASS; v4 **0.536438 s**, v5 **0.014368 s** |
| P6 | 2k/4k members PASS/HOLD, record times | v5 0.065256 s / 0.208201 s, ratio **3.1905**, both PASS |
| P7 | 1,000 seeded random Unicode/path-depth cases equivalent | **0 differences**, 904 PASS / 96 FAIL |
| P8 | bad CRC FAIL/HOLD | both FAIL, `ZIP member CRC invalid` |
| P9 | HOLD/BLOCKED, no publication authority, v5 schema | verified |

**Final 10/10 expected outcomes.** Input SHA-256 unchanged and `publication_authorization=ABSENT` throughout.

**Deviation:** Initial harness stopped after P0–P4 because a deep fixture exceeded ZIP32's 65,535-byte filename limit when adding the `OEBPS/` prefix; Python raised `struct.error` while constructing P5. Corrected slash repetition from 32,766 to 32,764 for exactly 65,535 bytes, then reran P0–P9 successfully. Initial partial execution is not counted as a complete pass. Some randomized fixtures emitted expected duplicate ZIP-name warnings.

**Interpretation, not certification:** v5 eliminates v4's repeated slash-prefix slicing on tested deep paths, but the 2k/4k timing ratio **exceeds** Run 324's old <3 threshold. P6 prospectively specified timing observation only; this does not erase Run 324's 9/10 re-execution or prove asymptotic performance of the whole checker. v5 remains a strict ZIP32 structural preflight, not full EPUBCheck/PDF/a11y, source authentication, or production release readiness.

**Next:** Claude independent review; investigate producer compatibility and resource bounds, then a separate prospective integration test if authorized. Sole income project F-001; genuine four-artifact TAM book, rights, editorial disposition, Dataset A 6/7, A1–A6/B6 and Timothy's release approval remain outstanding.
