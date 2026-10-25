# F-001 — Run 344 bounded nested output: preregistered synthetic results

**Project:** F-001 TAM Protocol ebook (same product). **Status:** DRAFT / HOLD / NOT LAUNCH-READY.

**Pre-test:** [Issue #53 comment 6395680400](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6395680400) was posted **before** execution. Current authority read first: Contract-000 `0fbc794`, DISC-002 `ee443fb` at `research-discourse-registry@0b6a968`.

**Code reviewed and committed:** [F-001-DATASET-STAGE-GATE-344.py](F-001-DATASET-STAGE-GATE-344.py), blob `5d5bb8f85db7f21c50ca71625e82c51102fed088`. It copies Run 339 gate blob `25f0130b9dd92bcc175ed6191a467fd75cc45856` and changes the nested builder invocation from `capture_output=True, text=True` to `stdin/stdout/stderr=subprocess.DEVNULL`; updates comments and filename in docstring. Git `verify_inputs()` still captures small git-command output; this change is scoped to the **nested builder**. The gate's expected source pins, CSV digests, timeout, marker names and failure behavior were not intentionally altered.

## EXECUTION-VERIFIED — synthetic subprocess boundary, NOT full gate

Environment: Python **3.13.5**, isolated `python3 -I -B`, offline. Local throwaway test file `/tmp/f001_run344_synthetic.py` created outside all repositories. It calls the same Python `subprocess.run(..., stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL, timeout=..., check=False)` pattern, but **does not import or execute the complete gate**. Command: `python3 -I -B /tmp/f001_run344_synthetic.py`.

| Preregistered case | Observation | Result |
| --- | --- | --- |
| T1: synthetic child writes 2,200,000 bytes to stdout and 2,200,000 to stderr | exit 0; returned stdout/stderr both `None`; elapsed ~0.92s | PASS (no Python capture buffer) |
| T2: synthetic child emits text then exits 7 | exit 7; stdout/stderr both `None` | PASS (exit preserved) |
| T3: child sleeps 2s with 0.2s synthetic timeout | `TimeoutExpired` after ~0.202s | PASS (timeout observed) |
| T4: read the actual GitHub-committed new gate blob | Nested `child = subprocess.run(...)` has all three DEVNULL streams, no `capture_output`/`text`, preserves `timeout=TIMEOUT_SECONDS`, `check=False`, five pin/CSV constant lines and both marker names | PASS (6 static checks) |

**Observation vs interpretation:** The synthetic subprocess does not accumulate stdout/stderr into Python's returned object and retains exit/timeout signals. The static check confirms that the committed draft uses that invocation pattern. **INFERRED:** this closes the identified *nested capture* memory growth mechanism. We did not measure the gate's peak RSS, run the actual pinned TAM builder, execute Run 342's pinned caller, or verify generated CSVs in this run. We did not exercise hostile descendants, OS quotas, disk exhaustion, or tampered files.

**Known integration blocker:** Run 342 caller pins Run 339 gate blob `25f0130`, so it will **reject** this new gate blob `5d5bb8f` until a separately reviewed, preregistered caller update. Do not silently swap scripts or label any stage RELEASED. No CI or remote Actions triggered.

**Next action:** Claude independently reviews the scoped DEVNULL change and the loss of builder diagnostics. Then preregister real pinned-source end-to-end gate+consumer+caller tests, pin the reviewed gate blob in a new GPT-only caller draft, and compare all three output hashes against prior independent references. F-001 editorial/rights A1–A6/B6, *Gerah*, Dataset A, EPUB/PDF, final receipt and publication remain blocked by Timothy's decisions.

No main/shared/Claude edits, no deletion, spending, accounts, outreach, publication, payments, paid inference or autonomous Cloudflare loops.
