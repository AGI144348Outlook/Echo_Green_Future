# F-001 GPT packaging: EPUB archive/OPF validation contract — T71 (draft, untested)

Status: **PROPOSED / UNTESTED / HOLD**. Sole income project **F-001 TAM Protocol ebook**. Claude owns editorial, manuscript rights and listing; GPT owns independent packaging verification. This is not a release certificate.

## Input trust boundaries
A verifier MUST open the EPUB itself, not trust a caller-provided manifest. Require ZIP archive integrity, unique normalized entry names, bounded uncompressed sizes and compression ratios, no absolute paths, traversal, backslashes or ambiguous percent encoding. Reject duplicate ZIP members and case/Unicode normalization collisions where applicable. Never extract to a filesystem during validation.

Parse `META-INF/container.xml` with an XML parser configured to reject DTD/external entities, and require exactly one resolvable rootfile pointing to an existing OPF package document. Parse OPF manifest and spine directly from archive bytes; reject duplicate IDs, missing IDs, remote resources unless explicitly permitted by a documented policy, and path/fragment/query confusion. Resolve each manifest href relative to the OPF directory using POSIX archive semantics, after controlled percent decoding; require its target to exist and remain inside archive. Every spine idref must resolve to a manifest item; verify at least one linear reading item. Check the EPUB mimetype member is stored, first, and exactly `application/epub+zip`.

Do not infer publication rights, semantic accessibility, visual layout quality, EPUBCheck conformance or PDF validity from structural checks. Produce machine-readable refusal codes and a deterministic JSON report with source SHA-256, tool/runtime version, fixture IDs and observed outcomes; redact private manuscript content.

## Next preregistered fixture families (NOT EXECUTED)
1. Valid minimal EPUB with one OPF, one XHTML spine item.
2. Missing container.xml.
3. Rootfile escapes archive.
4. Duplicate rootfile ambiguity.
5. Duplicate OPF manifest ID.
6. Manifest href absent from ZIP.
7. Manifest href percent-encoded traversal.
8. Spine idref missing.
9. Duplicate normalized ZIP member.
10. ZIP bomb size/ratio policy violation.

Acceptance: all negative fixtures refused for the intended reason, valid fixture accepted; deterministic repeat, source-pinned exact-byte replay; no external network, extraction or CI. Publish prospective issue entry before execution and same-thread actual results afterward. Keep F-001 HOLD until manuscript, rights A1-A6, editorial, accessibility, Android QA, independent PDF validation and Timothy's explicit release authorization.

## Evidence and limitations
Governing Contract-000 blob `fc4b675a`; F-001 shared plan blob `1e5f8d33`; GPT T70 checkpoint `b65839cf`. Prior GPT href gate and manually transcribed 11-fixture smoke run: Issue #463; **not** full OPF parsing or exact-source execution. Claude's separate path-containment probe was not a GPT test. No private manuscript material included.
