# F-001 Run 351 — prospective tests, source checks and limitations (2026-10-25 ~11 CT)

**Sole project:** F-001 TAM Protocol ebook. **Status:** HOLD / NOT LAUNCH-READY. No second project or release authorization.

## Pre-test registration
- [Issue #53 PRE](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6399854099) preceded all Run 351 F-001 checks; [builder-snapshot PRE amendment](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6399861421) preceded the source-level assertions.
- Problem: Run 350 stages gate/consumer as pinned private scripts, but passes the caller's original builder path to gate. Gate 344 hashes that builder before and after and executes it by pathname between checks. A swap-and-restore during execution is therefore not excluded by those two hashes alone.
- Hypothesis: a private builder snapshot with independently pinned Git blob removes the original builder pathname from the check/execute interval, without weakening gate/consumer pins or changing HOLD status.
- Expected source check: builder pin matches gate and consumer, all three scripts pinned before execution, all three copied into private directory, gate invoked with `str(builder)` and not `args.builder`. Unexpected script bytes, source drift, or runtime failures would challenge the proposal.

## Source observations and implemented draft
- **Source-read:** Gate 344 `verify_inputs(source,builder)` hashes actual builder bytes with `git_blob(builder)`, compares to `e8af6e5f011ec3e827c94737c717937944924eb8`, and launches `str(builder)`. It does not require the original path. Gate blob `5d5bb8f`; consumer blob `b2a9739`.
- **GPT-only draft:** [F-001-STAGE-SESSION-351.py](F-001-STAGE-SESSION-351.py), Git blob `68eea27de6e9a961f31122a08585ee6e24fed2df`. New `PIN_BUILDER_BLOB`; `pin_script_bytes(args.builder, PIN_BUILDER_BLOB, "builder")`; `write_private_script(private_root, "builder.py", builder_bytes)`; pass `str(builder)` to gate; add `pinned_builder_git_blob` to STAGING_ONLY/HOLD receipt. All existing gate/consumer pins and timeouts unchanged.
- **Limit:** this reduces a pathname-swap window only if the private temporary directory and same-user process environment are trustworthy. It does not sandbox malicious builder code, defend against a compromised parent process, pin a mutable TAM source clone throughout execution, guarantee descendant cleanup, or approve book content.

## Actual Run 351 checks
1. **Local source retrieval attempt:** `urllib.request.urlopen` for the exact Run 350 caller at `raw.githubusercontent.com` failed with `URLError: [Errno -3] Temporary failure in name resolution`. No local file created, no Python caller compile/import/harness execution. This is an environment blockage, not a failed caller assertion.
2. **GitHub connector reads:** exact Run 351 caller, gate 344, consumer 347 fetched by branch path, with blobs `68eea27`, `5d5bb8f`, `b2a9739`.
3. **JavaScript V8 *source-string* assertions on committed file text:** **20/20 PASS**. Checked pin matches in gate/consumer; gate's blob validation and invocation; caller's three pin reads and private writes; private builder invocation instead of original path; receipt builder pin and HOLD status; unchanged gate/consumer pins. No Python behavior was exercised by these checks.
4. **Run 350 prospective Python harness:** **NOT RUN**; it is pinned to the Run 350 caller, and source retrieval failed. The Run 350 16/16 helper result is previous-run evidence, not a Run 351 rerun.
5. **Full caller, real TAM dataset, PDF/EPUB, CI:** **NOT RUN**. No paid inference or Cloudflare action.

**Interpretation:** source structure supports the proposed private-builder transition. The 20 checks cannot establish race resistance or end-to-end stage correctness. No claim of production readiness.

**Next reproducible test (after a fresh PRE entry if execution is resumed):** materialize exact committed caller `68eea27`, gate `5d5bb8f`, consumer `b2a9739`, builder `e8af6e5`, pinned public TAM clone `d46456a`; verify all blob IDs; compile/import; run synthetic positive/negative stage invocation and deliberate original builder pathname swap, confirm private snapshot remains used and nonzero/timeout/stale/symlink cases fail closed; then independent Claude review. Record actual results in Issue #53.

**Release remains HOLD** pending Timothy's A1–A6/B6/C1, rights/credit/licence, Dataset A 6/7, Gerah, editorial claims, final EPUB/PDF and explicit publication permission.
