# F-001 TAM Protocol ebook — Run 337 single-project continuity and acceptance (2026-10-24 CT)

**Project identifier:** F-001, unchanged. **Selection:** TAM Protocol ebook/research notebook; no competing income pipeline. **Status:** HOLD / NOT LAUNCH-READY.

**Read before work:** `library-shared@470d3c8` [existing F-001 project plan](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-candidate-ebook-gumroad.md) through §140 and [decision sheet](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-decision-sheet.md); Run 336 checklist and stage gate; Run 334 actual builder (Git blob `e8af6e5`); Run 332 source-pinned test evidence and Run 334 parity evidence; Claude's shared `PROPOSED-csv_pin_check.py` and stage-copy probes. Current Contract/DISC still inaccessible; no execution.

**Bounded new deliverable:** [Run 337 independent CSV digest gate](F-001-DATASET-STAGE-GATE-337.py), an **UNTESTED GPT-only candidate** derived from Run 336. Previously the gate recorded hashes after checking builder/source pins, but did not compare CSV bytes against independent fixed expected hashes. Run 337 checks Dataset A `989d83c...` and Dataset B `ff442e48...` against reference digests from the independently registered Run 332/334 test records, rejecting a mismatch before writing `VERIFIED-STAGE.json`. This adds a fail-closed acceptance predicate, not publication authority. [Prospective Issue #53 amendment](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6392212037) specifies P14–P17; **no tests have run**.

| Deliverable | State | Acceptance criteria / complementary owner |
| --- | --- | --- |
| Authored source, rights, license, credit and claims | BLOCKED | Timothy A1/A3/A4/A6 and rights/credit confirmation; Claude editorial/source audit. |
| Edited manuscript and precision appendix | DRAFT | Review ~35 claim markers, resolve Dataset A rows 6/7 and *Gerah* conflicting definitions; preserve stated versus computed values. |
| EPUB | REVIEW DRAFT | Approved manuscript, fixed ID/date, reproducible build, EPUBCheck/Ace and independent checksum/receipt. |
| PDF | REVIEW DRAFT | Approved manuscript, links/fonts/accessibility and independent checksum/receipt. |
| Dataset A/B CSV + JSON | GPT candidate, **Run 337 UNTESTED** | Reproduce actual source+builder pins and both fixed digests; reject stale, symlinked, altered or failed stage; independent Claude review and prospectively registered execution. |
| Release manifest/receipt | DRAFT ONLY | Bind exact approved EPUB/PDF/CSV, source commits, verified independent digests, editorial authorization and no stale stage. A self-issued stage marker is insufficient. |
| Storefront/customer terms | BLOCKED | Timothy A2/A5/B6 and payout C1 as applicable, followed by explicit account/upload/publication authorization. |

**Division of labor:** GPT maintains source-pinned dataset-stage draft and eventual independent package verification. Claude reviews stage/exit/source trust boundaries and continues manuscript/editorial/rights work, without editing GPT branch. Both keep separate evidence and avoid shared-branch overwrites.

**Single next action:** restore authoritative Contract-000/DISC-002 read access and obtain Claude's static challenge of the Run 337 digest fixture. Then run only prospectively published #53 cases, with same-thread results. If blocked, continue source review and preserve unexecuted status.

**Awaiting Timothy:** A-000 identity custodian/recovery/DEC-0007; F-001 A1–A6, B6, Dataset A rows 6/7, *Gerah*, rights, exact credit, price/refund, final release approval. No accounts, outreach, spending, payments, paid inference, autonomous Cloudflare loops or publication.
