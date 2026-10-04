# Executable-code inventory delta — 2026-10-04

## Branch refresh

All **18** current branch heads were pinned. No branch was added or removed since the October 3 snapshot.

`autonomous-agency` advanced from `3ea19eda97f8ca0003050c5565b1b1f93ed03da2` to `442e0971069a3318adb6b08cc04855e5d4f6b655`. The five-commit comparison changes only:

- `ECHO_AutonomousAgency/sandbox/recess_session_log.json`
- `ECHO_AutonomousAgency/sandbox/school_day_log.json`

Those are generated/session data. No executable source blob changed in the branch delta.

## New module selection

The existing `chat-archive-pyodide-workbench@app.js` source was selected from the prior inventory because it contains executable nested file-handle helpers despite the surrounding archive extractor being unfinished.

Pinned source identity:

- branch/commit: `chat-archive-pyodide-workbench@2d129db69d48f66effd7d47732c03cd394f44755`
- path: `app.js`
- Git blob: `e0e476bc9c44436dc35e9894e8ca8bb8511bee6a`
- branch license blob: `02b1b4026ec7479d892ef951148798567444e07d`

The preserved source blobs were reused exactly in the registry tree. The generalized module isolates relative entry writing and adds a fail-before-mutation path policy. Canvas drawing, Pyodide startup, DOM wiring, service-worker registration and the non-operational `unzip()` stub were excluded.

## Source and validation classification

- Source: partly executable browser PWA scaffold.
- ZIP parser/decompressor: explicit stub, not functional extraction code.
- Upstream tests: absent.
- Independent source characterization: **2 passed, 0 failed**.
- Generalized validation: **6 passed, 0 failed**.

One characterization test records that the source writer passes a `..` segment to its directory adapter. The generalized module rejects traversal, absolute/drive-prefixed paths, backslashes, NUL bytes, empty/dot segments, directory-only paths and configured length/depth excesses before source or destination mutation.

## Remaining inventory gaps

- The full historical executable-blob registry across every commit and branch is not complete.
- The workbench still lacks ZIP central-directory parsing, decompression, entry/byte/ratio quotas, symlink policy and end-to-end extraction tests.
- Large ZIP archives remain evidence until their internal manifests are separately extracted and hashed.

