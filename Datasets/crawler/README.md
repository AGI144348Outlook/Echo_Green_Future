# ECHO Dataset Crawler

Acquisition layer for the Library. Searches Zenodo, Hugging Face datasets and data.gov through catalog APIs, preserves provenance, and stores eligible downloads as inert data.

**Acquisition != decomposition != registry formation != execution.**

The IVS branch uses the parent crawler plus the IVS search section in `keywords.txt`. Upstream IVS Git repositories remain separately classified under `IVS/`.

The default-branch workflow stages first contact as probe, then dry-run, then scheduled normal operation. Downloaded files are never opened, unzipped, imported or executed by the crawler.
