# IVS Intake Library

This branch is the Indus Valley Script intake workspace derived from `code-library-registry`.

## Evidence boundary

Keep these layers separate:

1. `external/corpus/` — digitized inscription/corpus sources.
2. `external/structural-analysis/` — statistical/structural work that does not need a decipherment.
3. `external/visual-signs/` — sign-image datasets.
4. `external/hypotheses/` — language/decipherment hypotheses; never treated as corpus truth.
5. `internal-history/` — Echo/Mashet's earlier Indus interpretations; architectural provenance, not archaeological evidence.

**Corpus evidence != structural inference != decipherment hypothesis != Echo/Mashet interpretation.**

Run `sh IVS/bootstrap.sh` from the repository root to clone the external sources into the ignored `IVS/vendor/` working area.

See `IVS/SOURCES.tsv` for source classification and upstream URLs.
