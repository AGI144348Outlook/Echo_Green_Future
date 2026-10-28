# F-001 — Android offline reviewer acceptance protocol (Run410; NOT RUN)

This is a prospective manual QA procedure for the **existing** v406 HTML reviewer and new read-only export verifier. It is not a report of Android execution or editorial approval.

1. Obtain the exact pinned `F-001-SUPPLEMENTAL-OFFLINE-EDITOR-406.html` from the GPT branch (Git blob `e3e2942181d5460b631e428096429c9939a6062d`). Open as a local file in an Android browser; confirm HOLD banner and **34 groups / 37 source occurrences**. Record Android/browser version and whether local-file storage is available.
2. Add a *synthetic* draft to G001, choose `DEFER_MORE_EVIDENCE`, type a nonsensitive placeholder in evidence. Export JSON; confirm file is created and no publication or network request is triggered. Preserve original backup.
3. Clear local notes (confirm prompt), then import the export. Confirm the synthetic note is restored and count is one; baseline 45 and supplemental 37 remain UNREVIEWED. Test canceling an import when notes exist; verify no overwrite.
4. Create separate disposable tamper copies (never modify original): flip `release_authorized` to true; change a `source_groups[0].full_sentence` character; change `source_commit`; add an unknown draft group. Import each and expect rejection with previous valid notes retained. Test malformed JSON and oversized draft field. Do not import actual private notes into public tools.
5. In Termux or another offline Node 18+ environment, run `node F-001-EXPORT-AUDIT-410.js <pinned-editor.html> <valid-export.json>` (expect PASS) and each tamper copy (expect FAIL/nonzero). Record stdout/stderr, file hashes and actual exit codes. **Neither Node CLI nor Android browser was executed during Run410.**
6. Check that reloading with valid storage restores notes, and corrupted storage is quarantined rather than silently overwritten. Check screen-reader labels and keyboard focus if available. Verify airplane-mode use does not require external services.

**Pass criteria:** exact source pin and counts, local-only draft persistence, export/import parity, fail-closed tamper behavior, no release state, no data loss on refused import, reproducible Node verifier result, documented environment. **Hold if any fails.** This protocol does not clear editorial/rights/EPUB/PDF gates.
