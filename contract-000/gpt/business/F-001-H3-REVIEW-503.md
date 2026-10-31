# Run503 — F-001 H3 evidence gate: source review and verification plan

**Project:** F-001 TAM Protocol ebook (unchanged). **Status:** HOLD / NOT LAUNCH-READY. **Review source:** Run502 `contract-000/gpt/business/f001_h3_byte_gate_502.js`, Git blob `cc6803043703b44161e49ca5d29afbe3179e7bbb`. **Prospective tests:** Issue #183, posted before attempted execution.

## Source-observed findings (not runtime results)
- `check(root, record)` rejects missing ref, non-hex/incorrect-length SHA-256, absolute and dot-segment evidence paths, symlinks detected by sequential `lstatSync`, non-files, unreadable evidence, and digest mismatches. A digest match returns `HUMAN_REVIEW_REQUIRED` / `NOT_DETERMINED` / `HOLD`; it never grants rights.
- **Time-of-check/time-of-use risk:** `lstatSync` of each segment and `statSync(target)` precede `readFileSync(target)`. An attacker with write access to the evidence directory may replace an entry after the checks. The read is path-based rather than bound to the inspected descriptor. Thus the source does **not** establish symlink resistance under concurrent mutation.
- **Platform semantics:** `path.isAbsolute` uses host conventions. A Windows drive-letter or UNC spelling supplied on POSIX may be treated as a relative name. On POSIX this may simply fail as missing; cross-platform rejection is not demonstrated.
- **Integrity != authority:** even a correct SHA-256 binds only the bytes read to the supplied hash. Reviewer identity, provenance, scope, expiry, revocation and third-party rights remain human-gated.

## Next implementation (GPT-owned only, proposal)
1. Add explicit path grammar (portable relative POSIX segments; reject drive-letter, UNC and colon ambiguities); reject symlinks in every segment.
2. Open the final file with `O_RDONLY|O_NOFOLLOW` when supported, `fstat` the descriptor, read via that descriptor and close in `finally`. Document that parent-directory replacement remains a race absent directory-descriptor-relative opening (`openat`-style containment), which stock Node.js does not expose portably.
3. Treat mutable or adversarial evidence roots as **untrusted / HOLD** rather than claiming a secure filesystem sandbox. Require immutable evidence staging under operator control for a release process.
4. Add preregistered offline positive/negative tests in #183, record observed stdout/exit status and exact source hashes there; do not confuse a local reconstruction with an exact Git blob.
5. Retain independent human quotation-rights and reviewer-authority verification. No automatic release gate from H3 alone.

## Execution status
An attempt to fetch the GitHub raw file into the local Node runtime failed due to DNS resolution of raw.githubusercontent.com. **No H3 runtime tests were executed**, and no observations have been backfilled as tests. The source was read through the GitHub connector. The #183 pre-test remains prospective.

## Deliverables and acceptance
- [x] Identify source-pinned H3 trust boundary and concrete TOCTOU limitation.
- [x] Publish prospective test plan before testing (#183).
- [ ] Exact-byte local checkout and preregistered H3 test observations in #183.
- [ ] Harden implementation and regression suite, with independent review.
- [ ] Complete six-file replay (#161) and exact-source H2 checks (#174).
- [ ] Claude: resolve 69 rights units / 77 passages and 82 editorial decisions with evidence.
- [ ] Historical verification, final PDF/EPUB, physical Android accessibility, Timothy's A1–A6 decisions and explicit publication authority.

**Next action:** obtain exact H3 source bytes in executable runtime, execute #183 suite, publish same-thread observations, then revise gate. No new business project, publication, outreach, accounts, payment or spending.
