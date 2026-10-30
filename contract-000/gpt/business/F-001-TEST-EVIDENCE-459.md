# F-001 Run459 — readable HOLD EPUB successor: prospective and actual evidence

**Pre-test published first:** [GitHub Issue #140](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/140), before local Python test execution. Source continuity: original GPT Run457 builder Git blob `8cb90e1c727995dfdc94bdadf18b4b46f8948551`, test blob `bd3f79e`; Run458 checkpoint `a4946c5`; eight production TAM Git blob pins remain unchanged in the original builder. F-001 remains HOLD.

## Method and execution

Created GPT-owned `F-001-EPUB-READABLE-BUILDER-459.py` as a successor wrapper around the **unchanged** Run457 builder. The wrapper reuses the original exact eight-source pin checking, bounded regular-file reads, deterministic ZIP metadata, and no-overwrite policy; it renders each nonblank source line in its own escaped XHTML paragraph, adds a `main` landmark, language attributes and honest textual/TOC package metadata. No unapproved editorial overlay is applied. CLI does not accept alternate pins.

Reconstructed the original Run457 builder in the local Python sandbox and independently checked its exact Git blob SHA-1 **`8cb90e1c727995dfdc94bdadf18b4b46f8948551`** against GitHub's fetched blob. Ran `python -I test_f001_readable_459.py` against eight synthetic files (not real TAM), using synthetic fixture blob pins. Executed two deterministic builds and negative tamper/missing-source/invalid-XML/overwrite/incomplete-pin cases. Read the produced archive using Python `zipfile` and `xml.etree.ElementTree`; verified content round-trip and package structure.

## Observations

**24/24 Python checks PASS** after a nonbehavioral correction to a test label. Checks cover eight inputs, deterministic SHA-256 across two builds, HOLD/no publication authority, no overlay, reader QA not claimed, 12 ZIP entries, correct uncompressed mimetype, XML parsing, four distinct paragraphs from four nonblank source lines, exact visible text preservation including ampersands, angle brackets, Hebrew and accents, main landmark, chapter language, `schema:accessMode=textual`, TOC accessibility feature, explicit draft warning, eight navigation links and spine entries, and five negative refusal/cleanup controls.

GitHub fetched **exact committed** successor builder blob `ce86e030f044bbe1d2cc75caab70e96c850c4256` and test blob `17980f650a3a6783629908fb5b1a29401ba713a7`; both match the locally tested file bytes. The original source module blob also matched. No exceptions or failures in the final 24-case run.

**Deviation:** The first test harness used the inaccurate label 'five source lines, five paragraphs' for a correct four-paragraph assertion. Corrected the label and reran; 24/24 still passed. The test suite verifies XML well-formedness, not EPUBCheck compliance.

## Interpretation, limits and next step

A structural readability improvement is demonstrated on synthetic data without modifying source text or changing release status. Accessibility metadata are present, **not** a certification of accessibility. **Not run:** real eight-source GPT EPUB, EPUBCheck, Android/e-reader QA, original Python eight-source scanner replay, PDF, historical fact-check or rights clearance. Claude's §157 real-source 26,090-byte EPUB remains Claude-executed evidence only; it used the older builder.

Next: acquire/verify all eight exact TAM source bytes in an executable local environment; build a real successor HOLD EPUB, run EPUBCheck and Android reader QA, then implement a separate approval-gated editorial overlay only after Timothy's explicit decisions. F-001 stays **HOLD / NOT LAUNCH-READY**. No publication, accounts, outreach, spending, payments, CI, paid inference or autonomous Cloudflare loops.
