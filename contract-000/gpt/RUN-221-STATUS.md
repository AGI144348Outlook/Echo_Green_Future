# ChatGPT Contract-000 Run 221 — 2026-10-20

Status: independent scheduled development; F-001 TAM Protocol ebook only; RELEASE HOLD.

Read authoritative Contract-000 blob 0fbc794426f50e4d207b440f436ce726ec6371f2 (§§3, 12–15, 25–26, 30), TJ R1–R7 blob 3ce87eb6b9215bd8d5dc0a2e4664b95479764161, DISC-002 blob ee5753b25417077cb46f8fa1466cfbf02180e0c8, library-shared@77889b2f025c64b0a79f5b11cccfc4efdefc6232, F-001 decision sheet 95c373d3e600f20f381d1fd639f9e3336474dfb8, previous Run-220 handoff.

Library-first: 50/50 unchanged entries verified by unchanged shared tree SHA; 43 KEEP, 7 DEFER, 0 PRUNE. Detailed source-specific rationale retained in Run-220 handoff; no deletions or shared edits. No new full-body reread claimed.

A-000: characterization on unchanged Dev Suite blob f7cf46584a7c787367196ec0d1aae7178dd976e3: the digest intentionally excludes each submatrix's storage contents but also omits storage *schema*. Replacing storage with list/string, or deleting the storage key, leaves alg_002 True; storage() can return wrong types or raise KeyError. Propose shape validation distinct from mutable contents. Genesis blob 63eb982989b4f3478d649430b555c8f4ba755c27 inspected; no source changes, no frozen tests.

F-001: new read-only section-local Markdown/EPUB/PDF coverage gate. Run-220 global six-gram parity can accept a complete paragraph moved from Article 1 to Article 2; the new gate rejects it, validates EPUB TOC href targets, ordered chapter/PDF body headings, section-local paragraph coverage, and release-hold markers in delivered files. On the unchanged five-article/two-dataset editorial preview: 9 sections, 59 EPUB and 59 PDF section-local paragraphs, PASS. 19 new + 29 inherited offline tests = 48/48 PASS. The original preview is unchanged and not publication-ready. 13 tracked claims OPEN, A1–A6 unresolved, 12 production patches unmerged, rights and accessibility pending.

Next: Claude independent editorial review and technical gate review; stage production builder in disposable checkout and test final-format parity; obtain Timothy's explicit decisions and publication authorization. No main/Claude/shared edits, outreach, paid inference, spending, Cloudflare loops or publication.
