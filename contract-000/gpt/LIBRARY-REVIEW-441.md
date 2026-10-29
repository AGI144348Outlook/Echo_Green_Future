# Contract-000 GPT Library-first review — Run441 (2026-10-29 ~05 CT)

**Pre-test:** Issue #121. **Authority read:** Contract-000 blob `0fbc794`, TJ rulings `3ce87eb`, Claude DISC-002 `ee443fb`, shared Library README `59be277`, Run440 checkpoint `219397a`, inherited full ledger Run436, and sole F-001 decision `2975edc`.

**Complete metadata reconciliation:** compared all 89 source-bound paths, Git blob IDs, byte sizes and nonblank rationales from Run436 against current nontruncated `library-shared` tree `470d3c827fd1cdd5e96b4f4ca91281e02d676bad`. **89/89 match, zero discrepancies**. The accompanying [89-row TSV](LIBRARY-DECISIONS-441.tsv) carries every KEEP/PRUNE/DEFER decision and its inherited evidence/reason without deleting anything: **31 KEEP / 57 DEFER / 1 PRUNE**. These are inherited judgments rechecked against Git metadata, **not** 89 independent source-body rereads. PRUNE means reversible inactive selection only (TJ R3).

**Four fresh, exact public source-body reads:**

| Shared path | Git blob | Decision | Reason / limits |
| --- | --- | --- | --- |
| `Business/ideas/F-001-tam-build/claim_scan.py` | `31f3dcff486c4c8cc96d514eb425da86834d00c3` | KEEP | Original Python scanner needed for source-grounded F-001 editorial worksheet. It silently skips absent files; this run executed only a pinned Article10 pilot, not full eight-file parity. |
| `Business/ideas/F-001-tam-build/CLAUDE-zip-layout-audit-v5-probes.py` | `929c0d6eb17551070ace6bb1ae5ad4de46a5af56` | DEFER | Claude's synthetic EPUB ZIP-layout adversarial probes. Retain independently authored evidence; not executed or adopted by GPT this run. |
| `Business/ideas/F-001-tam-build/CLAUDE-verified-stage-copy-v2-probes.py` | `1bbb14f8f1e27acd80ca79cdbcad5aa62ae01c74` | DEFER | Claude's W1–W6 stage-copy synthetic probes. Source-read only, no GPT reproduction or production adoption. |
| `Workshop/solutions/S-001-cloudflare-deploy-without-github-app/README.md` | `54c7280741d9b18954cfc92dedb591ad4394584b` | KEEP | Historical manually authorized deployment workaround; no Worker, CI or Cloudflare action initiated. |

All four fetched Git blob IDs match the inherited ledger. No shared Library mutation, deletion, main write, private Testament access or second income project. The new GPT-only pilot is a **candidate** for later Library registration, not an automatically promoted shared tool.
