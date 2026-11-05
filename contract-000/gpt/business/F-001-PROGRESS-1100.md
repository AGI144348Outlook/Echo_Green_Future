# F-001 — Run1100 packaging acceptance handoff
**Single project:** F-001 TAM Protocol ebook. Status HOLD / NOT LAUNCH READY. This advances existing packaging verification, not a new pipeline.

## Source evidence read
- Shared Business decision sheet blob `2975edcc4cae8a17499e873b68ba75f5c39ea527` — A1–A5 and B1–B6 undecided, defaults are placeholders.
- Shared GPT checklist blob `69449fceac9d4b7b5ac516318c685ec610fdd6df` — GPT owns PDF/EPUB integrity; Claude owns editorial/listing.
- Existing Run509 progress blob `4e01182a80c2042faadc19eae794b3d26e059425` — H3b ten-case harness incomplete, close-error and parent-swap issues unresolved.
- Source candidate A blob `e5a0e655c6cd68330dbe117c7a346d1acef31540` — manuscript and rights not automatically established by the draft.

## New concrete deliverable: fail-closed package acceptance matrix
| Gate | Required evidence | Failure behavior |
|---|---|---|
| F001-G1 Source custody | exact source commit/blob and independent receipt for input bytes | HOLD if absent or mutable |
| F001-G2 Editorial | dispositions for 82 editorial items, authored/approved provenance | HOLD if unresolved |
| F001-G3 Rights | 69 quotation-rights decisions covering 77 passages, per-source license/permission evidence | HOLD if unresolved |
| F001-G4 Build | source-pinned deterministic EPUB/PDF build, verified tool versions, stable identifier and metadata | HOLD if non-reproducible |
| F001-G5 Integrity/accessibility | SHA-256 file manifest and verified independent receipt; EPUB structural checks, PDF tagging/fonts, Android manual read/navigation | HOLD if missing or failed |
| F001-G6 Publication | explicit Timothy decisions A1–A5 and B1–B6 as applicable, plus separate affirmative release approval | HOLD if no approval |

**Acceptance rule:** launch_ready = G1 AND G2 AND G3 AND G4 AND G5 AND G6. A passing synthetic verifier alone cannot satisfy G2/G3/G5 manual checks or G6.

## H3c design increment (draft only)
Close failures must not turn a structured HOLD/REJECT into an unhandled exception. Preserve first failure and append close failure to audit; never return PASS if close failed. Path resolution should require a trusted immutable root or directory-relative traversal with explicit platform guarantees. Source-hash checks must bind the exact opened file bytes, not a separate preflight pathname. No claim of race safety until adversarial parent replacement tests run. The existing H3b source is unchanged.

## Next action and collaboration
GPT: implement standalone H3c candidate and preregister missing close-error, symlink-parent, UNC, over-16MiB, replacement-race and concurrent-swap cases before any execution; then complete source-pinned package acceptance.
Claude: continue editorial, quotation-rights and historical verification; do not duplicate packaging code.
Timothy: A1–A5, B decisions, signing/witness custody where relevant, and explicit release approval remain outstanding.
No publication, outreach, account creation, spending or paid inference.