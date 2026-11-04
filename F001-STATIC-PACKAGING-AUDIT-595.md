# F-001 static packaging audit — Run595 (NOT EXECUTED)
Project: **F-001 TAM Protocol ebook**. Authority: `library-shared:Business/ideas/F-001-candidate-ebook-gumroad.md` blob `d5dccce18a285688f4fcd29531e39cf34978b07a`. Build source: `library-shared:Business/ideas/F-001-tam-build/build.py` blob `ede8da6f9e33631bd7d329f0ace5a880258fac18`.

## Static observations (source-read, not experimental results)
1. `main()` refuses an output path equal to or nested within the source clone, but does **not** refuse the inverse (`out` being an ancestor of `src`); it also does not require a fresh/empty output directory. Stale `tam-draft.epub` or CSV artifacts can survive when Pandoc is absent or a dataset has no delimited table. **Release risk:** a later packaging step may mistake stale artifacts for current output. No claim that this occurred.
2. The `pandoc` command is optional; `report["epub"]` may be a string describing a skip. The script does not fail the whole build on EPUB failure. This is reasonable for review drafts but **not** a release acceptance gate.
3. `md_table_to_rows()` accepts any pipe-delimited lines without enforcing uniform column counts or header semantics. CSV presence alone does not prove table fidelity.
4. The EPUB metadata insertion uses byte replacement of the first `</metadata>` in an OPF ZIP member and does not verify a replacement actually happened, validate the resulting OPF XML, or run EPUBCheck. A truthful a11y metadata declaration is not accessibility validation.
5. The script generates a Markdown review draft and optional EPUB, not a PDF; source `TITLE` explicitly calls the work speculative and review-only. No claim of PDF/EPUB launch readiness follows from this tool.
6. Source fingerprints are recorded for ORDER items, and DUP_ONLY files only when included. A comprehensive edition manifest should also fingerprint datasets and the build script, plus the output artifacts, to bind the release to exact bytes.

## Proposed corrective development (no code or tests executed)
- Introduce a **release-only verifier**, separate from the historical draft builder, that accepts an immutable manifest of expected outputs and source inputs, rejects missing or stale artifacts, requires PDF and EPUB independently, checks all source and output SHA-256 hashes, checks EPUBCheck/PDF tooling results, and records nonzero failures.
- Require fresh isolated output directory or refuse existing outputs; record a build identifier and source commit. Never delete user files implicitly.
- Gate accessibility on observed navigation, metadata and Android-reader checks; gate editorial claims and rights independently with Claude. Preserve source privacy.
- Before any diagnostic/test/CI execution: publish a concrete PRE-TEST issue describing fixtures, expected results and falsifiers; follow up **in the same issue** with actual observations. Existing #262 is the pretest for v583 runner only, not blanket authorization for a new release verifier.

## Acceptance and handoff
Checklist: [ ] source rights/A1-A6 [ ] editorial and quotation rights (Claude) [ ] pinned source and fixture objects [ ] existing #262/#258/#256/#229 observed results [ ] PDF verified [ ] EPUB verified [ ] Android/accessibility verified [ ] checksum manifest [ ] Timothy release approval. All remain OPEN; status **HOLD / NOT LAUNCH-READY**.
Next GPT action: prepare a minimal standalone release-verifier implementation and preregister its tests before execution, while retaining the existing frozen runner experiments unchanged. Claude: check source/quote provenance and listing claims independently. No new income project.
