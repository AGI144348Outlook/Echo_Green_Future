# Mashet candidate registry

Run `python scripts/registry_former/mashet_candidate_registry.py` from any directory to generate `candidate_registry.json` and `audit.json` from the committed Mashet source transcript.

The first Bedrock-style legend is a **proposal**, not an authoritative 96-entry registry. The source also contains alternate legends; keep those distinct. The generator preserves concept/glyph pairs and identifies duplicate glyphs and category counts. It does not execute symbols or promote them to matrices, DSL, or codices.

The registry former is committed, but its output has **not yet been executed or committed**. The current branch is a sub-branch of `code-library-registry`.
