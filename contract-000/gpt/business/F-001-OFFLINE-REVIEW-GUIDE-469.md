# F-001 TAM Protocol — offline 82-card editorial DRAFT companion
## Android-oriented review guide, Run469 (DRAFT / HOLD)

**Project:** F-001 only. **Status:** HOLD / NOT LAUNCH-READY. **Authority:** NONE. The companion is **not** the ebook and cannot approve, apply, or publish editorial changes. Every one of the 82 occurrences remains PENDING until Timothy's authenticated decision process is defined and used.

### Files and provenance

- Review page: `F-001-82-EDITORIAL-REVIEW-DRAFT-468.html` (Git blob `983ca1f6bf34d34f0dd0e442cffa388dd5ab6161`) in `contract-000/gpt/business/` on `contract-000-gpt-run468-20261030-0803` (or a descendant containing identical bytes).
- Generator: `f001_review_companion_468.js` (blob `a43e95b7bc70b48bcb3df37b156b3e4aee5d0ac3`).
- Pinned register `300dfcf0ba9e9d236326d09b2a4b6c5467d3874c`, location map `7fb5cd952127de7a0469cfb3d0139d7bdfb60b86`, intake `4cc1617d1f1bbea1661f74ba931f86660c087939`.
- Evidence: Claude §167 real Node and headless Chromium desktop/emulated-phone replay; GPT Issue #150 20/20 fake-DOM checks. **Neither constitutes a real Android device or accessibility pass.**

### Offline review workflow (proposed; Android not yet device-tested)

1. Save the **raw HTML file** to the device's local Downloads or Documents folder. A GitHub **code preview** is not the same as opening the saved HTML page; use the file itself. Do not rename it to `.txt` or paste it into a browser address bar as source text.
2. Disconnect from the network if desired, then open the saved `.html` file in a JavaScript-capable local-file browser. Confirm the prominent **HOLD / NOT LAUNCH-READY** notice and 82 editorial cards. If the browser instead shows HTML code, try a different file-opening action. Do not upload the file to a third-party HTML viewer; this may expose unpublished notes.
3. Search by occurrence ID, source or proposal. For each card, inspect the source excerpt and Claude's **PROPOSED** disposition; set a **DRAFT** status and optional note (up to 1,000 characters). Duplicate-text references are separate occurrences, not automatic approvals.
4. Tap **Export DRAFT feedback JSON (not approval)**. Confirm a local file named `F-001-82-review-DRAFT.json` was saved. Export is the only persistence mechanism; there is **no automatic save**. Before leaving the page, export again if anything changed.
5. Reopen the same pinned HTML and use **Restore previously exported DRAFT feedback JSON**. The page should say `Restored 82 DRAFT entries locally. No editorial approval or release authority.` Check at least one edited note and disposition. If a restore is refused, do not alter source pins or approval fields to bypass the refusal; retain the original JSON and report the error.
6. Keep the JSON private until Timothy chooses an authenticated editorial review channel. It is a draft worksheet, **not** an approval receipt. It cannot change the 82-row custody register, create a sale listing, authorize release, or settle rights.

### Failure and safety notes

- File download/open, Android file-picker and download behavior, virtual keyboard, TalkBack/screen-reader navigation and long-session data retention **remain unverified on a real Android device**. A mobile-sized Chromium viewport is not a phone.
- The browser's local export contains the notes you typed. Avoid putting private credentials or personal secrets into notes; export can be shared by anyone who gets the file. The page is designed to make no network requests and has no account integration; do not rely on this as a general browser security guarantee.
- If cards do not render, the HOLD notice is missing, export does not download, import changes only some fields, or an approval/release option appears, **stop and report**. Keep the source file and the exact error; do not interpret a broken page as an editorial decision.
- The companion is not a secure signing system. Authenticated editorial approval, source rights, historical claim review, EPUBCheck/PDF QA, credit, price/refund, and publication authorization are separate outstanding gates.

### Acceptance criteria before calling this Android-ready

On a **real Android device**: open local file offline; see 82 unique cards; search narrows and clears; edit/export/reopen/restore 82 draft rows; five malformed JSON inputs fail without partial mutation; no remote requests; usable scrolling, labels, focus and virtual keyboard; no unexpected errors or sideways overflow. Record device/browser version, screenshots if appropriate, exact source SHA and a prospective GitHub PRE/POST test entry. **Do not call this complete until independently executed.**
