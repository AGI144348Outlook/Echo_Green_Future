# F-001 export-audit evidence — Run410

**Sole continuing project:** F-001 TAM Protocol ebook. Prospective [Issue #83](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/83). No release.

## Product deliverable
[`F-001-EXPORT-AUDIT-410.js`](F-001-EXPORT-AUDIT-410.js) is a read-only offline Node 18+ verifier for exports from the existing v406 supplemental editor. It verifies the **editor's exact Git blob** `e3e2942181d5460b631e428096429c9939a6062d` (using Git's `blob <length>\0` SHA-1 framing) before reading its embedded source map. It then requires source commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`, source map blob `32dfe75589a031de46c28145fe993122ee2ca0f2`, 34 source groups / 37 occurrences / 45 baseline cards, exact source group records and pins, approved draft-field *names* and bounded values, and HOLD / release_authorized=false. Inputs must be regular files at most 2 MiB. The script performs no network calls and writes no files.

**Usage (documented, NOT RUN in Node):** `node F-001-EXPORT-AUDIT-410.js F-001-SUPPLEMENTAL-OFFLINE-EDITOR-406.html F-001-supplemental-HOLD-draft.json`. A success prints `audit:PASS` and HOLD counts; a failure prints `audit:FAIL` and exits nonzero. Use the exact pinned v406 HTML, not an arbitrary edited copy.

## Actual checks
- **14/14 V8 in-memory controls PASS** after Issue #83 PRE: one valid HOLD draft; thirteen rejection cases (release=true, changed source commit, changed source text, changed pin, unknown group, invalid decision, oversized evidence, extra top-level field, missing baseline field, invalid date, baseline mismatch, array draft collection, extra draft field).
- **2/2 committed-source re-fetch controls PASS:** extracted `auditDraft()` from newly committed `d94910df293dace93fa1904d6638ed1117a880cb` and executed it against the exact v406 map (valid empty HOLD draft accepted, release flag rejected). Verified the pinned HTML blob from GitHub connector. This is V8 execution of the function, **not Node CLI execution**.
- **A-000 independent:** 5/5 source-transcribed isolated Python controls PASS; see [A-000 report](../A-000-REGISTER-TRANSACTION-410.md).
- **Library:** 89/89 path/blob/size/rationale match; 31 KEEP, 57 DEFER, 1 PRUNE.

**Limitations:** the Node filesystem CLI and actual Android browser/import/export have **NOT RUN**; the editor SHA-1 is a Git object identity check, not a signature of editorial truth; source-group JSON equality is strict (a semantically equivalent key-reordered export can fail closed); timestamps and user-entered evidence are not independently authenticated. This does not verify historical facts, copyright, receipts, final EPUB/PDF, or dataset coordinator. An altered editor and altered export cannot pass the pinned-blob check without changing the trusted verifier itself. External verifier distribution still needs trusted provenance.

**Next:** execute CLI against a real Android-generated export in a controlled offline environment, include positive and tamper-negative files, retain exact SHA-256 of exported draft privately if it contains personal notes; perform original eight-source Python scanner and coordinator replay when exact sources are available locally. No public personal draft content.
