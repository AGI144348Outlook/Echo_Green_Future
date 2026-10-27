# F-001 supplemental offline triage — Run405 test evidence

**Pre-test registration:** [Issue #78](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/78) was created before tests. Sole continuing income project **F-001** TAM Protocol ebook. **HOLD / NOT LAUNCH-READY.** No release or rights authority.

**Inputs read first:** source-bound 37-occurrence packet `contract-000/gpt/business/F-001-COVERAGE-TRIAGE-PACKET-401.json` blob `dfa28a6a750967a2bb600e56a6e962117890478b`; 34-group map `F-001-EXACT-GROUP-REVIEW-402.json` blob `32dfe75589a031de46c28145fe993122ee2ca0f2`; original public TAM source commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`; Run404 F-001 plan.

## Deliverable

[F-001-SUPPLEMENTAL-OFFLINE-EDITOR-405.html](F-001-SUPPLEMENTAL-OFFLINE-EDITOR-405.html), committed Git blob `ba64d0d36089924a57af02e11e3d0dcadf8d1bc1`, 36,693 UTF-8 characters, self-contained responsive HTML with inline pinned source text for **34 distinct groups / 37 occurrences**. Shows original passages, source references, heuristic review focus and draft-only triage fields (decision, independent evidence, rights notes, editorial notes, reviewer). Local browser storage and HOLD-only JSON export/import; no network fetches or release control. Existing **45 baseline cards remain separate and UNREVIEWED**; this tool does not admit the supplemental occurrences to that queue.

## Test methods and observations

1. **Source-map/packet structural checks (V8, 32/32 PASS).** Checked 34 groups, 37 unique occurrence IDs, original 37-item packet cross-references, source blob pins, sentence equality within grouped references, source packet SHA, source commit, HTML offline/HOLD markers and script parse. Export counts and empty draft roundtrip passed. Sixteen adversarial import cases were rejected: forged release/READY status, source commit, source blob, original sentence, occurrence ID, missing group, wrong counts, unknown group, APPROVED decision, unexpected release flag inside draft, oversized note, unexpected top-level field and missing source groups. Valid draft normalization/import passed.
2. **Committed-file independent readback (V8 mocked DOM, 14/14 PASS).** Re-fetched the committed HTML and parsed/initialized its actual inline JavaScript with a minimal fake DOM and localStorage. Verified 34 rendered cards, 37 source refs, text-node rendering (not HTML injection), HOLD notice, search and draft filters, source pin equality, HOLD-only export, JSON roundtrip and rejection of a forged original sentence. The committed HTML Git blob is `ba64d0d36089924a57af02e11e3d0dcadf8d1bc1`.
3. **Original Python scanner replay: NOT RUN.** Bounded attempt to fetch the public scanner via local Python urllib failed `URLError: [Errno -3] Temporary failure in name resolution`. The connector can read public files, but no exact-source materialization into the isolated Python runtime was achieved. The original eight-source Python scanner and full Run334→344→347→351 staging coordinator remain unverified.
4. **Actual Android/browser interaction, Node CLI, EPUB/PDF and CI: NOT RUN.** A mock DOM is not a substitute for Android UI, accessibility or file-download behavior. No editorial decisions, independent historical evidence, rights clearance or publication acceptance were tested.

## Interpretation

The structural checks support **source-preserving draft review** for the 37 supplemental occurrences and rejection of the tested import-tamper classes. They do **not** prove the claims true, validate provenance cryptographically, certify rights, guarantee browser compatibility, or authorize adding any occurrence to the baseline 45-card queue.

## Deviations and next steps

The original-source Python replay remained blocked by DNS; no claim of execution is made. Claude should independently triage the 34 groups against primary sources and rights in Claude-owned records. GPT should run actual Android-browser import/export and original pinned Python scanner once exact-source execution is possible, then HOLD-only staging positive/tamper negatives. Timothy's A1–A6/B1/B4/B6/C1, rights/editorial and release decisions remain open. **F-001 HOLD.**