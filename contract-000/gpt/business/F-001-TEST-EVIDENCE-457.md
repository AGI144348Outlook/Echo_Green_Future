# F-001 Run457 — independent local synthetic EPUB builder evidence

**Prospective entry (published before tests):** [Issue #138](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/138). **Actual results posted afterward in same issue.** No CI, production TAM source fetch, paid inference, Cloudflare loops, publication or real EPUB/PDF claims.

## Executed procedure
Created eight *synthetic* UTF-8 source files in a temporary directory under the exact expected TAM filenames; calculated fixture Git blob pins using the same `git_blob` function. Imported the builder's `build()` directly with fixture pins (CLI does **not** accept overrides). Invoked `python /mnt/data/test_f001_epub_builder_457.py` locally. Committed exact tested sources to GPT branch and checked their returned Git blob SHA against local `git hash-object`.

**Final exact source hashes:** builder Git blob `8cb90e1c727995dfdc94bdadf18b4b46f8948551`, local SHA-256 `76d8d0382be4221451dfce5712fac305919ce7b033c44a78374f688bf8bbaec8`; harness Git blob `bd3f79e1a2bba640a8cd12432948e6668b0acd9b`, local SHA-256 `ce2ae251f900d145d15fe5a18af838acedaf2a8d21b40aec2e32cf31739d15ef`.

## Observations
Initial synthetic harness: **14/14 passed**. Additional review identified that the XML-parse phase occurred outside the cleanup block. Moved it inside and added an invalid-XML NUL-byte negative control. Final harness: **15/15 passed**:
1. eight sources;
2. identical SHA-256 for repeated synthetic builds;
3. HOLD status and publication=false;
4. `mimetype` first and stored;
5. exact EPUB MIME bytes;
6. twelve expected ZIP entries;
7. all included XML/XHTML/OPF parse with Python ElementTree;
8. `&` and `<` escaped in chapter;
9. eight navigation links;
10. overwrite refused;
11. tampered source refused;
12. missing source refused;
13. output inside source tree refused;
14. invalid XML refused and output removed;
15. incomplete fixture pin map refused.

**Interpretation:** deterministic ZIP packaging and local fail-closed controls work for the tested synthetic inputs. A source file containing invalid XML 1.0 characters fails rather than silently producing a broken draft. The cleanup fix was made **before** final source commit; no claim of first-pass perfection.

## Limits / next
No real TAM article bytes, no full original Python scanner replay, no real ebook, no PDF, no EPUBCheck/EPUB reader validation, no accessibility review, no historical or rights clearance, no Timothy publication approval. The builder emits escaped plain text, not Markdown styling. Future real-source failure on invalid XML must be reported, not silently stripped. F-001 remains HOLD.
