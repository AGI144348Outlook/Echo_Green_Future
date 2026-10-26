# F-001 TAM Protocol ebook — pinned-stage source attestation, Run 374

**Project F-001 ONLY. Status HOLD / NOT LAUNCH-READY.** This run continues [Run373](F-001-PROGRESS-373.md), [Claude's decision sheet](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-decision-sheet.md), and [Run364–365 stage/capture handoffs](F-001-REAL-STAGE-HANDOFF-364.md). No second business pipeline.

**PRE-test:** [Issue #56 #6419313309](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6419313309), posted before diagnostics. **Machine-readable artifact:** [26/26 source-pin audit](F-001-STAGE-PIN-MANIFEST-374.json).

## Executed source inspection and results

Authenticated reads of the four exact GPT-owned stage scripts and two source TAM dataset blobs. Verified their Git blob IDs, all source-commit references, cross-script builder/gate/consumer pins, both independently specified CSV SHA-256 references, and explicit HOLD/STAGED_ONLY output language. **26/26 bounded V8 string/pin assertions matched**; three were negative altered-string *absence* controls, not runtime tamper tests. This confirms cross-file pin consistency at the checked commit, **not** that the actual Python pipeline ran, not that the historical data are true, and not that a release artifact is valid.

| Input / tool | Pinned Git object | Role |
| --- | --- | --- |
| Public TAM commit | `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9` | Source HEAD required |
| Dataset A | `b62c970a660e0a6685b58db1ef121690daa4fce7` | 6 source rows expected |
| Dataset B | `12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4` | 8 source rows expected |
| Run334 builder | `e8af6e5f011ec3e827c94737c717937944924eb8` | Exact pinned builder; **not** Run332 |
| Run344 gate | `5d5bb8f85db7f21c50ca71625e82c51102fed088` | Fresh isolated stage |
| Run347 consumer | `b2a97390ba39959cd2f86a5e51ea186348f31fb2` | Read-only stage check |
| Run351 coordinator | `68eea27de6e9a961f31122a08585ee6e24fed2df` | Same-invocation capture and HOLD receipt |

Expected CSV SHA-256 from gate, consumer and coordinator: A `989d83c16568f23a97251d93919068f3a5e726c738644625af909b278f395fdb`; B `ff442e48acaf00900a3bc3d7900bf987995355a34226b749dbd5b81878e2f7c0`. These are reference digests from earlier bounded tests, **not fresh locally generated outputs**.

**Attempted read-only network precondition:** `git ls-remote https://github.com/AGI144348Outlook/The-TAM-protocol.git HEAD` in execution container returned `fatal: unable to access ... Could not resolve host: github.com`. No authenticated clean local Git clone could be established. The pinned Python builder, gate, consumer, and coordinator were **not run**. No output CSV was generated in this run. No EPUB, PDF, accessibility, listing or historical-source rights tests were run. Source connector access cannot substitute for a Git clone when the gate checks `git rev-parse HEAD` and cleanliness.

## Product acceptance checklist and complementary lanes

- [x] Source identities and all four script Git blobs cross-checked (static only).
- [x] One project F-001; no silent repinning to Run371's 9/8-column CSVs (Run334 requires 11/9).
- [ ] In trusted POSIX environment, read-only clone exact public TAM commit; prove clean `git status`, source blob pins, and builder/gate/consumer/coordinator exact Git blobs.
- [ ] Prospectively register new execution; run Run334→344→347→351 on private fresh stage using Run365 exit-capture wrapper. Preserve nonzero status, stdout/stderr, stage marker, source/report/output hashes.
- [ ] Independently run disposable altered-input negative and verify fail-closed without changing preserved positive evidence; run structural EPUB/PDF, accessibility, source-to-claim and final SHA checks.
- [ ] Claude: editorial claims, Article 4, Gerah/rounding, rights/licence, listing, price and credit; independently review this GPT source-pin audit. Do not overwrite Claude's work.
- [ ] Timothy: answer A1–A6, B6, C1 and original precision/rights decisions; explicitly authorize publication only after gates pass.

**Next GPT action:** retry the same pinned stage after GitHub DNS becomes available, not create a new project or repin to make a failure disappear. **HOLD** until actual stage evidence, editorial decisions, independent package validation and explicit Timothy approval. No account creation, outreach, payments, spending, publication, CI, paid inference or autonomous Cloudflare loops.
