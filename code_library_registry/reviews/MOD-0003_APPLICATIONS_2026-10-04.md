# MOD-0003 application review — 2026-10-04

The Structured Workspace Registry can record an archive-import plan without storing archive bytes.

A meaningful design would create one collection per import attempt; add metadata-only items for accepted and rejected entries; relate files to their parent directories; bind source/archive indexes; and persist the manifest only after MOD-0004 validates every candidate path and separate quota checks pass.

Useful fields include original entry name, canonical relative path, declared and observed sizes, rejection reason, checksum, media type and extraction status. Payload bytes should remain outside the JSON registry.

Boundary: MOD-0003 is single-process and its atomic save covers one JSON document only. It does not coordinate concurrent extractors, make file writes transactional or prove that extracted bytes are safe. This is an application note, not a change to the frozen implementation.

