# F-001 GPT Run 313 — pinned-input snapshot characterization evidence

**Pre-test:** Issue #32 opened before first local execution. **Interim deviation:** Issue #32 comment 6379095238. **Scope:** standalone research helper only; no coordinator integration or real ebook artifact validation.

**Environment:** Linux, CPython 3.13.5, `python -I -B`. Source Git blob `4fac471658d36ed71bec707cb9803150064ec894` (4722 bytes), harness Git blob `381bcad2a77479ec01405c7ae71ceba37e4f4653` (3719 bytes). Both fetched back from GitHub and matched locally computed `git hash-object`. Final stdout SHA-256: `50fa1fc02492b7856d799dc19ae8298921231e4a6c302b68f0aeac580fd70c7e`.

**Method:** `python -I -B PROPOSED-f001-test-pinned-input-snapshot-v1.py`; uses a private synthetic temp root, original `b'original source bytes\\n'`, an external forged file, symlinks and a FIFO. Helper opens root and each component with `O_NOFOLLOW` via directory FDs, rejects nonregular/oversized files, reads the held FD into a 0700 temp dir, checks a supplied SHA-256 and pre/post `fstat`, and yields staged 0400 files. No subprocess, paid inference, browser, external API or private dataset.

| Case | Expected | Observed | Outcome |
|---|---|---|---|
| S0 pinned valid source | accepted | exact bytes, digest, size | PASS |
| S1 final symlink | rejected | ELOOP | PASS |
| S2 symlink ancestor | rejected | ENOTDIR | PASS |
| S3 parent traversal | rejected | unsafe relative component | PASS |
| S4 wrong SHA-256 | rejected | source digest mismatch | PASS |
| S5 file exceeds byte bound | rejected | source exceeds byte bound | PASS |
| S6 FIFO | rejected without blocking | source not regular | PASS |
| S7 path replaced by symlink after FD open | original bytes preserved | original digest-pinned bytes copied | PASS |
| S8 file content changed after FD open | rejected | source digest mismatch | PASS |
| S9 absent input | rejected | ENOENT | PASS |
| S10 invalid output label | rejected | invalid output label | PASS |
| S11 private staging modes | 0700 dir, 0400 files | as expected | PASS |
| S12 two-item batch | both pinned | both copied and matched | PASS (exploratory add-on) |

**Final rerun: 13/13 expected outcomes, exit 0.** First execution had **harness-only TypeError** after S0: it tried to iterate a context manager at S1. Corrected the harness to enter it with `with`; interim deviation posted before final rerun. S12 was added after original prospective registration, explicitly not retroactively claimed pre-registered. No helper-source changes between passing run and Git commit.

**Observation vs interpretation:** The synthetic S7 swap did not redirect an already-held descriptor, supporting the specific path-swap mitigation. This does **not** prove immutability or source authentication: a process with same-UID access can still modify staging bytes; an independently trusted manifest does not yet exist; snapshots are not wired into coordinator v4; receipt-embedded EPUB/PDF paths are not automatically included; no concurrent adversarial stress, cross-platform verification, malicious subprocess containment, or genuine EPUB/PDF content tests were run. The optional `_after_open` callback is a testing hook and must not be supplied by untrusted callers.

**Next:** Claude independently review helper and path/FD threat model; GPT propose adapter wiring for pinned inputs and receipt-embedded four artifacts, prospectively register integration tests. Keep F-001 publication HOLD and require Timothy A1–A6/B6, Dataset A lines 6/7 dispositions, verified book deliverables, and explicit release authorization.
