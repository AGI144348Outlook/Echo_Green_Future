# GPT T67 — F-001 exact-source verification and integration gate (draft)
Status: NOT EXECUTED; not release approval. Project F-001 TAM Protocol ebook only.

## Verified baseline
- Shared plan: library-shared:Business/ideas/F-001-candidate-ebook-gumroad.md (rights/manuscript not cleared).
- Gate source: contract-000/gpt/business/F-001-EPUB-HREF-GATE-20261113-17Z.py, commit 3734f3980776b248b826167ccd6c9885ad2b903f.
- Fixture runner: contract-000/gpt/business/test_f001_epub_href_20261113.py, commit 85c799e414230e3c8732d3f0342464d426c2be8e.
- Prospective test family: Issue #463. Earlier 11/11 results used a manual transcription, not exact-source.
- No exact-source run claimed here.

## Implementation gap: nested EPUB resource validation
The standalone gate accepts caller-supplied manifest dictionaries and archive member names. It does not itself parse OPF XML, prove that manifest dictionaries were extracted from the actual ZIP, enforce the EPUB mimetype/container/spine, or validate content. A caller could supply an incomplete manifest and receive a narrow pass. This is an interface-level limitation, not a demonstrated exploit.

## Next bounded verification
1. Obtain exact source bytes from GPT-owned branch and pin blob SHAs.
2. Run committed runner with Python stdlib, record interpreter, command, SHA-256 of both scripts, exit code and JSON outputs.
3. Before any materially new tests, amend Issue #463 prospectively to include: duplicate href targets under different IDs; missing OPF; empty manifest; unsafe ZIP member; missing OPF manifest item; malformed OPF XML; missing container.xml; invalid spine IDREF. The last three require a new parser, so must not be counted as existing gate coverage.
4. Post actual observations and deviations in Issue #463, including negatives. Do not infer EPUB validity or release authority from a narrow gate.
5. Integrate read-only validation only after independent review. Keep a fail-closed PDF verifier and explicit rights/Timothy approval gate.

## Deliverables / acceptance
[x] Source draft [x] Fixture runner [x] Prospective Issue #463 [ ] Exact-source results [ ] OPF parser [ ] EPUBCheck or equivalent independent EPUB validation [ ] PDF parser [ ] accessible EPUB/PDF QA [ ] rights and editorial signoff [ ] Android review [ ] Timothy publication approval.
F-001 HOLD / NOT LAUNCH-READY. Claude editorial/rights; GPT packaging. No storefront actions.
