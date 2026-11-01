# F-001 TAM ebook — Run510 acceptance gap and actionable next test

Project identifier: **F-001** (same TAM Protocol ebook, no alternative pipeline). Source-read H3b `f001_h3b_descriptor_gate_505.js` and ten-case harness `test_f001_h3b_synthetic_508.js` on Run509 branch. Prospective protocol is already published in issue #186. No tests executed this run; no retrospective preregistration claim.

## Static observations

1. `finally { if(fd!==undefined)fs.closeSync(fd); }` is outside the catch boundary: a close failure can throw instead of returning the structured HOLD/REJECT envelope. A narrowly scoped candidate is to catch close errors, preserve HOLD, and mark integrity verification indeterminate, while explicitly acknowledging that close failure after a successful read does not necessarily invalidate the bytes read.
2. `lstatSync` on parent directories is not atomic with `openSync(target)`. Parent symlink or directory replacement between checks remains possible. Do **not** claim hostile-filesystem safety; require trusted immutable evidence root until a verified directory-descriptor traversal implementation exists.
3. Existing harness covers ten deterministic fixtures but omits preregistered >16MiB, symlink parent, UNC/backslash and controlled race cases. These are coverage gaps, not observed failures.

## Deliverables and acceptance

- [x] H3 baseline 10/10 in prior Run504, Linux synthetic only (#183).
- [x] H3b draft and prospective protocol (#186).
- [x] Ten-case H3b harness committed, **not executed**.
- [ ] Pin H3b and harness exact Git blobs; run offline under #186, then post actual results in #186 (OS, Node, command, pass/fail, deviations, limitations).
- [ ] Extend preregistered missing cases, rerun and report in same issue.
- [ ] H2 exact-source verification (#174), six-file replay (#161).
- [ ] Resolve 82 editorial decisions and 69 quotation-rights decisions (77 passages), historical checks, final PDF/EPUB and Android accessibility.
- [ ] Explicit Timothy publication authorization; **HOLD / NOT LAUNCH-READY** until all gates pass.

Claude: please continue editorial/rights provenance; GPT: validator hardening, offline test evidence and packaging. No private source, publication, outreach, payments or paid inference.
