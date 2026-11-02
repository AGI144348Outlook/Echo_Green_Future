# F-001 — Run543 evidence-custody remediation specification (DRAFT; NOT TESTED)

Project identifier: F-001 TAM Protocol ebook. This is a revision plan for the Run541 orchestration, **not** a new product or release approval.

## Static source observations
- `f001_preflight_custody_541.sh` captures preflight stdout/stderr in a shell variable. On a nonzero preflight exit it prints that output to stderr and exits 10 **before creating durable evidence**. This contradicts the intended ability to audit negative cases without relying on terminal capture.
- It checks `out` nonexistence and resolves its path before preflight, but ancestor symlinks can change between validation and custody; `realpath/commonpath` is a check, not an atomic containment guarantee.
- It runs `sha256sum` over six named files if `out` exists. If custody leaves a partial directory, the manifest command fails closed, but the caller must preserve the incomplete directory and stdout/stderr to explain the failure.
- `f001_preflight_536.sh` checks clean checkout including untracked files and three pinned source identities; these are prerequisites, **not proof** of a nine-case test or ebook rights clearance.

## Proposed fix for a later independently preregistered implementation
1. Require an external, newly created evidence directory, with strict permissions and no checkout writes; reject existing destinations and unexpected symlinks.
2. Create a uniquely named run record **before** preflight, recording command, source refs, UTC time, environment and a redacted invocation ID. Persist preflight stdout/stderr and its exact exit status whether it passes or fails.
3. On preflight failure, write a HOLD verdict and manifest, do not invoke custody/regression, and exit nonzero. A missing artifact must also produce HOLD and be recorded.
4. On successful preflight, execute the existing custody script without changing pinned source. Preserve custody stdout/stderr, exit status, artifact list and SHA-256 manifest. Require explicit success checks for every expected artifact.
5. Distinguish an execution result (observed) from the release gate (always HOLD until editorial, rights, accessible PDF/EPUB, Android QA and Timothy's authorization).
6. Use a disposable, pinned checkout and capture source hashes before any execution. Do not promise resistance to concurrent ancestor-symlink replacement without a separate threat model and atomic filesystem design.

## Acceptance criteria and test registration
Existing prospective Issue #220 covers destination, dirty-checkout, missing-dependency and custody-failure cases for the Run541 implementation. **Do not silently apply its preregistration to a changed wrapper.** Before executing any revised implementation, append a clearly prospective amendment in #220 specifying the new blob and new failure-evidence assertions. After testing, post observed results in that same issue. Issue #197 remains the distinct nine-case regression preregistration.

## Product gates
G1 nine-case exact-source regression #197 OPEN; orchestration #220 OPEN; G2 H2 #174 OPEN; G3 six-file replay #161 OPEN; G4 82 editorial decisions OPEN (Claude); G5 69 rights units/77 passages, history, A1–A6 OPEN; G6 accessible PDF/EPUB and Android QA OPEN; G7 explicit Timothy publication authorization NOT GIVEN.

Next GPT action: implement a fail-closed evidence-preserving successor, prospectively amend #220, and execute only in a clean disposable checkout. Claude retains editorial/history/rights; no publication, accounts, outreach or payments.
