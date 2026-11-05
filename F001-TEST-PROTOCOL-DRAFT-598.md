# Run598 — F-001 release-gate test preregistration draft (NOT EXECUTED)

Project: F-001 TAM Protocol ebook. Source: F001-RELEASE-GATE-597.py blob 11c54d6daaacd0fe90a53c396645f299406bcf17. This document is a draft for a GitHub Issue, NOT evidence that preregistration was published and NOT permission to run tests.

## Problem and hypothesis
The gate correctly stays HOLD by construction, so testing only its exit status cannot reveal false negatives. Hypothesis: malformed CSV and JSON reports are represented by explicit findings rather than crashes or falsely clean evidence; matching artifact digests are necessary but not sufficient for acceptance.

## Proposed controlled method (future, after Issue preregistration)
Pin exact source SHA and isolated scratch fixtures; do not use private manuscripts or quotations. Create a minimal fixture set with all eight required artifact filenames and controlled synthetic data. Run python3 -I F001-RELEASE-GATE-597.py <fixture-dir> per case, capture stdout/stderr/exit, SHA256 of inputs, and compare finding codes. Include: absent directory; symlink artifact; zero-byte artifact; non-object JSON; EPUB results list containing null/string; EPUB digest mismatch; CSV unequal row widths; CSV duplicate headers; CSV with blank headers; CSV reported row-count disagreement; CSV quoted newlines; PDF report present but no approved schema. Assert all cases remain HOLD, no uncaught exception, no real release authorization. Record any current omissions as failures, not retroactive test changes.

## Falsifiers and limitations
Any uncaught exception, missing expected finding, ignored structural defect, artifact mutation, or falsely claimed approval challenges the hypothesis. Current code does not check duplicate/blank CSV headers, reported-vs-actual row-count parity, full source fingerprint parity, or PDF semantics; these are predicted weaknesses, not execution observations. A successful structural test would not establish manuscript rights, PDF accessibility, Android reader usability, or permission to sell.

## Acceptance checklist and next action
[ ] Publish this protocol in an Issue before any execution. [ ] Freeze fixture hashes and expected observations. [ ] Execute without network/paid inference. [ ] Comment actual evidence on same Issue. [ ] Fix confirmed defects on GPT-owned branch. [ ] Obtain Claude rights/editorial disposition. [ ] Verify EPUB/PDF and Android. [ ] Obtain Timothy A1–A6 and explicit release approval. Status HOLD / NOT LAUNCH-READY.
