# F-001 TAM Protocol ebook — release-candidate evidence manifest (Run593, DRAFT)

Project ID: **F-001**. Status: **HOLD / NOT LAUNCH-READY**. This is a release packaging control document, **not** a claim that any test passed or that a product was published. No new income pipeline.

## Artifact manifest (fill only from produced, verified files)
| Deliverable | Required evidence | State |
| --- | --- | --- |
| Source manuscript | canonical source path, immutable blob SHA, edition/version, author/rights review | MISSING |
| Claims-to-sources ledger | claim ID -> source locator -> license/quotation disposition -> editor signoff | MISSING |
| Six-case verifier (#258) | frozen source/fixture SHAs, six named cases, assertions, exit code, outputs, same-thread result | UNEXECUTED |
| Runner verification (#262) | pinned runner SHA, pre-registered six checks, observed outcomes and failures, same-thread result | UNEXECUTED |
| Regression evidence (#256, #229) | original preregistration and independent result per declared case | UNEXECUTED |
| Accessible PDF | artifact SHA-256, metadata, selectable text, logical reading order, links, alt text or decorative tagging, navigation | NOT BUILT |
| Accessible EPUB | artifact SHA-256, EPUBCheck result, navigation, language, semantics, image text alternatives | NOT BUILT |
| Android acceptance | device/app/version, open/navigation/search/reflow, links, screen reader where available, screenshots without private data | UNTESTED |
| Release decision | Timothy A1–A6 recorded; explicit approval for publication and sales | AWAITING TIMOTHY |

## Acceptance rule
A row is complete only with a verifiable evidence locator and a named reviewer/decision; blank or unexecuted is not PASS. Technical PASS cannot override unresolved rights, accessibility or authorization. Any change to the frozen test plan requires a new prospective preregistration, not retroactive editing. No public listing, outreach, account creation, payment, spend, or upload to a sales platform without Timothy's explicit authorization.

## Work partition and next action
ChatGPT: locate pinned Git objects for #262, execute only its already-preregistered checks after verifying bytes, post actual results **in #262**. If executable transfer remains blocked, keep UNEXECUTED. Claude: independent editorial claim/quotation/source review; preserve independent findings. Timothy: A1–A6 and eventual publication decision. Original F-001 project plan path is still unresolved and must be located before treating this manifest as an authoritative replacement.
