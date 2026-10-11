# Matrices

Populated from S1 batch 14 (2026-10-11T15Z). Each row of `REGISTER.tsv` is a provenance entry (branch, path, blob_sha, bytes, source commit, retrieval time) for a `KEPT` Library source row whose content is tabular (rows x columns of observations). Content is not copied. Nothing here is canon (Contract 000 §13).

First entry: the NVE-C reconciliation table from `library-source-transcriptions` (category x expected / observed / missing, plus glyph collisions). Its `observed_total` (93) equals the count produced by `scripts/registry_former/mashet_candidate_registry.py`, which this run executed offline in a scratch copy (EXECUTION-VERIFIED); the generator output itself was not committed.
