# F-001 — continuing TAM Protocol ebook (ChatGPT Run 361)

**SINGLE PROJECT ID: F-001. Status: HOLD / NOT LAUNCH-READY.** No new income pipeline. Reviewed [shared decision sheet](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-decision-sheet.md), shared GPT checklist, Workshop records, Run 360 progress, exact pinned Run 334/344/347/351 code and current public TAM source-commit metadata. Claude retains editorial/listing scope; GPT independently handles technical validation/packaging. No shared or Claude-owned edits.

## This run's actual increment

- Published [prospective test registration](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6406531005) **before** diagnostics; published [actual results and limitations](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6406550809) afterward in the same thread.
- Created [standalone source-pin coherence preflight](F-001-PIN-COHERENCE-361.js) with a Node CLI that recomputes the Git blob SHA-1 of supplied local script bytes before comparing the pinned source commit, source A/B Git blobs, builder/gate/consumer script pins, and expected A/B CSV SHA-256 values across the four stage components. Its static checks **cannot** establish safe runtime behavior, actual output hashes, independent provenance or publication authorization.
- Executed the shared `audit(sources)` logic in V8 on authenticated GitHub source reads, with supplied GitHub blob identities (no independent local raw-byte hash in V8): **8/8 expected outcomes**, one pinned-chain positive and seven altered/missing-source negatives. [Machine-readable evidence](F-001-PIN-COHERENCE-RESULTS-361.json). Standalone Node CLI itself **NOT RUN** this run.
- Tried `git ls-remote https://github.com/AGI144348Outlook/The-TAM-protocol.git HEAD` in the local execution container **after** prospective registration; failed with `Could not resolve host: github.com`. The authenticated GitHub connector independently located the public source commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`. No runnable clean checkout was obtained, so **pinned Run 334 Python builder / real Run 344 stage / Run 347 consumer / Run 351 coordinator NOT RUN**. No stage receipt, tamper-runtime verdict, EPUB/PDF or publication produced.

## Single-project deliverables / acceptance checklist

| Deliverable / acceptance | Verified status now | Next action / owner |
| --- | --- | --- |
| Single income project | **F-001 TAM Protocol ebook only** | Continue F-001, not another pipeline |
| Rights/source selection/licence/credit/framing (A1/A3/A4/A6) | **BLOCKED — Timothy decisions and source-rights evidence missing** | Claude prepares alternatives; Timothy authorizes exact text |
| Storefront/price/refund/payout (A2/A5/C1) | **NOT AUTHORIZED** | Draft only until Timothy approves |
| Public TAM source identity | GitHub connector resolves exact commit `d46456a`; A/B blob pins `b62c970` / `12ef0fc` in scripts | Obtain runnable **clean** checkout and independently verify source bytes |
| Run 334/344/347/351 source-pin coherence | **8/8 static controls as expected**; four script blobs pinned | Run standalone Node preflight on local bytes, then real Python chain |
| Run 358 review CSVs | Previously 6 A/8 B rows; **9/8 columns incompatible with stage 11/9** | Never self-repin/relabel Run 358 CSVs as Run 334 outputs |
| Pinned Run 334 real CSV/report | **NOT RUN**, no stage-ready output verified | Clean TAM checkout, exact builder, isolated output; verify 11/9 headers, 6/8 rows, source attestations, independent hashes |
| Fresh stage and HOLD receipt | **NOT RUN**; no `STAGED_ONLY`/consumer receipt | Execute 334→344→347 via 351 on private preexisting stage root; verify HOLD, then tamper-negative control |
| Arithmetic/claims editorial | Two Dataset A point flags potentially rounding-compatible; Dataset B ratio 1 precision question | Claude checks Gerah, rounding, claims; Timothy approves dispositions |
| EPUB/PDF/manifest/accessibility | Prior synthetic package tests only; real final files **NOT VERIFIED** | Generate reviewed book, independently inspect, hash and audit |
| Release authority | **HOLD** | Independent review and explicit Timothy signoff before any external action |

## Reproducible next-stage handoff (commands NOT EXECUTED)

1. In a network-enabled, isolated, authorized local environment, fetch **public** `AGI144348Outlook/The-TAM-protocol` at exact commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`; verify clean Git status and exact A/B Git blobs. Never substitute an arbitrary checkout or the Run 358 shared builder.
2. Fetch exact GPT-owned Run 334 builder, Run 344 gate, Run 347 consumer and Run 351 coordinator from this branch. Run `node F-001-PIN-COHERENCE-361.js <absolute-builder334.py> <absolute-gate344.py> <absolute-consumer347.py> <absolute-coordinator351.py>`; require `pass:true` and verified raw Git blob hashes. This command is a **preflight only**.
3. **Publish a fresh pre-test Issue/Discussion entry before any runtime test**, specifying the actual source checkout, root and adversarial cases. Then run `python3 -I -B F-001-STAGE-SESSION-351.py --source <absolute-clean-TAM-checkout> --builder <absolute-builder334.py> --root <absolute-preexisting-private-stage-root> --gate <absolute-gate344.py> --consumer <absolute-consumer347.py>`. Verify fresh stage, `STAGED_ONLY` gate notice, consumer `HOLD` receipt, expected SHA-256 outputs and rejection of a modified input in a separate disposable stage root. Record exact commands, hashes, observed exit statuses, failures and cleanup in the same pre-test thread.
4. Even successful staging is **NOT** publication approval: editorial, rights, final EPUB/PDF, independent release witness and Timothy signoff remain separate gates.

**Claude coordination:** challenge the static pin assumptions, review manuscript/claims/licence and the precision questions; do not overwrite GPT artifacts. **Timothy pending:** A1–A6, B6/C1, credit, source rights, identifier, final editorial decisions and authorization to publish. No account, spending, outreach, payments, publication, CI, paid API inference or autonomous Cloudflare loops this run.
