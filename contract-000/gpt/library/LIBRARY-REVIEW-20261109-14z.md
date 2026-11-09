# GPT Library-first recursive review — 2026-11-09 14Z
Read authoritative Contract-000 (research-discourse-registry), TJ rulings R3 (no deletions), previous GPT checkpoint, shared Library source. Three source-backed re-reviews (not new inventory rows):
- **DEFER** `Business/ideas/F-001-tam-build/rights_rows.py` blob `976a726c1db595809ab35777731c1a1c2dd38074`: `os.path.join(d,f)` accepts absolute/parent paths; `isfile` follows symlinks; `open(...).read()` unbounded; replacement decode hides errors. Claude's §283 confirms parent/absolute/outward-symlink reads. Retain unchanged as dataset; not safe release evidence.
- **KEEP (fixture only)** `Business/ideas/F-001-tam-build/RECEIPT-BYTES-281.json`: Claude's canonical-byte examples inform strict parsing but are not authenticated rights proof. No issuer trust root.
- **KEEP (source only)** `Business/ideas/F-001-tam-build/epub_check.py` blob `176d42ee19f82580702a0bfc1941b0d28932ec31`: useful offline EPUB preflight; not EPUBCheck or complete accessibility attestation.
Decisions are version-scoped. Historical 158-entry 145 KEEP/12 DEFER/1 PRUNE is inherited, not recounted. No shared mutation, no deletions, no test of Library source.
