# Executable-code inventory delta — 2026-10-02

## Branch refresh

The repository now has **18 current branches**, compared with 16 in the 2026-10-01 snapshot. Two branches were added and one source branch advanced:

- `chat-archive-pyodide-workbench@2d129db69d48f66effd7d47732c03cd394f44755`
- `chatgpt-conversation-archive@1b029f5cb2fa02ce80f1aec41ac31c3f1de7f9f2`
- `autonomous-agency` advanced from `abdf12a60cba8ea4baf420e16aaf9116289f6dc7` to `583caad066fe68b7595fa2bea1d083a0f9e6acd9`

The autonomous-agency comparison is five commits ahead but changes only `recess_session_log.json` and `school_day_log.json`; no executable source blob changed.

## Deduplication findings

The conversation-archive branch contains four large conversation JSON segments plus `shared_conversations.json`. These are data archives, not executable modules. Its workflows, root license, README, CLA, ZIP, Cloudflare migrator, Worker source and Wrangler configuration reuse exact Git blobs already present in repository history.

The workbench branch reuses those same foundation blobs and adds a small browser PWA surface. Its distinct functional files include `app.js`, `index.html`, `styles.css`, `sw.js`, `manifest.webmanifest`, `ARCHIVE_WORKBENCH.md` and an archive-workbench deployment workflow.

Classification of the workbench ZIP path:

- `app.js` initializes Pyodide, renders a high-DPI grid, accepts file/drop input and can request a browser directory handle.
- `ensurePath` and `writeEntry` are executable file-writing helpers.
- `unzip` does **not** parse or extract ZIP entries. It explicitly logs that the ZIP directory parser and Pyodide fallback are future work and advances progress to 10%.
- No workbench test suite is present.

Therefore the branch is classified as **partly executable PWA scaffold with an explicit ZIP-extraction stub**, not as a validated large-archive extractor.

## New module selection

`sandbox/test_autonomous_agency_a1.py` was selected from the existing autonomous-agency inventory because it contains a self-contained, deterministic breadth-first composition mechanism with an executable assertion and a control case. Its exact source blob is `a5d4ece3ad283e576ac0761039332a70c818ba35` at current branch commit `583caad066fe68b7595fa2bea1d083a0f9e6acd9`.

It was dissected into `MOD-0002-bounded-composition-search`; Echo/homework/agency language and fixed integer bindings were excluded from the generalized mechanism.

## Remaining inventory gaps

- The full repository-wide executable blob registry is not complete; this review covered all current heads for changes and performed exact blob deduplication on the branch delta.
- Large ZIP files remain archived evidence until their internal manifests are separately extracted and hashed.
- Generated experiment logs and conversation exports must remain distinguished from executable source.

