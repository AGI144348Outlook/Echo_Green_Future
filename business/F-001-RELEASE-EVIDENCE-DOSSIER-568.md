# F-001 release-evidence dossier — Run568 (DRAFT, HOLD)
Project ID: **F-001 TAM Protocol ebook**. This is an evidence index and acceptance contract, **not** a release certificate. A blank or absent observation is `UNKNOWN`, never PASS.

## Immutable evidence slots
| ID | Gate | Source of truth | Observed status | Promotion condition |
| --- | --- | --- | --- | --- |
| CUST-8 | Custody synthetic static suite | Issue #234, Run565 post-test | 8/8 PASS (synthetic only) | Preserve exact pinned code, Python version, exit and outputs; cannot imply concurrency or independent custody |
| VER-15 | Evidence-manifest verifier | Issue #229 (prospective) | NOT RUN | 15/15 named cases PASS, zero SKIP, guard exit 0, pinned blob identities, verifier HOLD disclaimer captured |
| REG-9 | Nine-case regression | Issue #197 | NOT VERIFIED HERE | Same-thread observed execution against preregistered pinned code |
| H2 | Independent origin/provenance | Issue #174 | NOT VERIFIED HERE | Independently signed or externally attested origin and immutable artifact-to-source linkage; checksum alone insufficient |
| REPLAY-6 | Six-file custody replay | Issue #161 | NOT VERIFIED HERE | Exact six artifacts and reproducible comparison with independently verified input provenance |
| EDIT | Editorial/history/quotation rights | Claude-owned F-001 review | PENDING | Trace every substantive claim and quoted passage to reviewed source and rights decision |
| PACK | EPUB/PDF/a11y/Android | GPT packaging remit | PENDING | Deliver both formats, validation reports, hashes, Android open/read and accessibility observations |
| AUTH | Product decisions | Shared Business/ideas/F-001-decision-sheet.md | A1–A6 OPEN | Explicit Timothy decisions, source/licence and publication authorization |

## Required observation record for VER-15
Do not run until Issue #229 prospective entry has been checked against exact pinned cases. Record:
- verifier blob `ecb88e250e05d0d4c1378b04b1864cc9af776b44`
- harness blob `325628adb168f5d012f115445a68bb4bd83fbc3d`
- guard blob `38312aa0d91d85fb4dc55fbebddb460b4d2dbf54`
- full source SHA-256, interpreter and OS, command, exit status, stdout, stderr, per-case names, skipped cases, run timestamp, and same-thread Issue #229 observation link.
- Verify the source is byte-faithful before execution. Never replace frozen tests with a modified harness.

## Explicit limits
A co-modified artifact and manifest may be internally consistent yet unauthentic; that fixture is deliberately positive in the synthetic verifier. Receiver acknowledgments, file hashes and source labels do not independently establish source custody. All release gates remain HOLD until their separate evidence exists. This dossier does not authorize publishing, account creation, payment, spending, outreach or paid inference.

## Complementary ownership
GPT: verified code execution, reproducibility, packaging, checksums, a11y/Android evidence. Claude: editorial/historical assertions, quotation rights, manuscript provenance. Timothy: A1–A6, release and commercial authorization. Next GPT action: **execute pinned VER-15**, not create another verifier, and report in Issue #229.
