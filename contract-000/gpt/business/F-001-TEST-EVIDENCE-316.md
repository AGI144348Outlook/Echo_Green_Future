# F-001 Run 316 — helper/adapter-v2 offline test evidence (2026-10-24 CT)

**Prospective plan:** [Issue #35](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/35), posted **before** any execution. **Scope:** GPT-owned helper-v2 and staged adapter-v2, synthetic fixtures from archived Run 314; actual previously reviewed receipt-v3, Dataset A parser, v5 report gate and cross-report verifier invoked by coordinator-v4 on those fixtures. Not real EPUB/PDF books. Python 3.13.5, `python -I -B test_run316.py` from a temporary scratch directory. No GitHub Actions/CI, paid inference or Cloudflare execution.

**Exact executed source blobs:** helper `21407ac59eee3ca6263a850ed50024f1249db180`; adapter `040b502c8ec02af8da0b27dd1e44c79b8b0d947d`; harness `774b165b5ab9d35cf42ea9fd5a0d861b0557d813`. These exact files were committed to `mirror-chatgpt-root` and fetched back with matching Git blob SHA. Raw local `run316-results.json` SHA-256: `486237128450e32a2b5f2404bd20924dd6cf97bc320f410b6fc9e8ed27e72c50`. Archived synthetic fixture is not independently authenticated.

| Case | Expected | Observed | Assessment |
|---|---|---|---|
| T0 valid helper copy | ACCEPTED | ACCEPTED | matched |
| T1 Claude V2 destination already exists | existing file preserved | PRESERVED | matched; original not deleted |
| T2 Claude V4 symlink swap at chmod boundary | outside file permissions unchanged | OUTSIDE_UNCHANGED | matched; held-FD fchmod |
| T3 same-size source substitution | reject | ValueError | matched |
| T4 changed staged bytes | reject | ValueError | matched |
| T5 wrong SHA pin | reject | ValueError | matched |
| T6 valid optional disposition, then duplicate-key invalid disposition | PASS then FAIL | VALID_PASS_INVALID_FAIL | matched |
| T7 duplicate-key binding JSON | FAIL | FAIL | matched |
| T8 integrated archived reviewed-script chain | PASS / HOLD / BLOCKED | PASS/HOLD/BLOCKED | matched, three stages |
| T9 same-size staged binding tamper after copy | FAIL | FAIL | matched |

**Result:** **10/10 executed preregistered test cases matched expectations**. T6 includes two internal calls and is counted as one preregistered case. The T8 `PASS` means *synthetic internal integrity consistency*, **not** publication readiness. Release remained HOLD, readiness BLOCKED, approval and source authentication false for the chain and all adapter outcomes. No unplanned tests or harness corrections; no unexpected exceptions/timeouts in this execution.

**Observed vs interpreted:** T1 preserves an existing file on O_EXCL failure, T2 leaves an outside file's 0644 mode unchanged, T9 detects the injected staged metadata modification, and the actual archived verifier chain returns three stages under synthetic fixtures. Interpretation: the new helper addresses Claude's V2/V4 counterexamples and the adapter no longer blindly re-reads unverified staged bytes. It **does not** prove safe behavior against hostile same-UID actors or authenticated source provenance.

**Limitations and next:** (1) Helper v2 still depends on a trusted, private parent path; the held parent descriptor protects its final component but not all ancestors. (2) The adapter rechecks staged hashes before handing pathnames to children, but a same-UID actor can still mutate between check and child read; descriptor passing or sandboxed isolation remains unimplemented. (3) The verifier script execution boundary and subprocess-grandchild containment remain open. (4) Caller-supplied SHA pins are not independent authentication; derived receipt is not signed. (5) The actual TAM ebook and Dataset A lines 6/7 editorial decisions, rights, pricing and approval are still outstanding. **F-001 remains HOLD/BLOCKED; no release, listing, payments, account creation or outreach.**

**Next GPT:** request Claude independent v2 review; prioritize genuine editorial/source pin provenance and descendant containment, not more overlapping verifier versions. **Next Claude:** independently probe V2/V4 regression, review v2's directory-FD assumptions and continue manuscript/claims/a11y/listing under the same F-001 ID. **Awaiting Timothy:** A1–A6/B6, Dataset A lines 6/7, publication authorization.
