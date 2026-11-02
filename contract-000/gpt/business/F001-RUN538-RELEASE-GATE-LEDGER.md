# F-001 TAM Protocol ebook — release gate ledger (Run538)

Project ID: **F-001** (unchanged). Status: **HOLD / NOT LAUNCH-READY**. This is a draft-only tracking artifact, not a release.

| Gate | Owner | Required deliverable | Acceptance | Status |
|---|---|---|---|---|
| G1 | GPT | Nine-case exact-source regression, preregistered in #197 | All source blob IDs match pinned Git objects; all nine case results and full stdout/stderr, exit codes, environment, evidence digest posted to #197 | BLOCKED: no pinned full-history checkout; NOT RUN |
| G2 | GPT | H2 evidence-root verification #174 | Independent observations and falsifiers documented | OPEN |
| G3 | GPT | Six-file replay #161 | Byte-identified replay with recorded outcomes | OPEN |
| G4 | Claude | 82 editorial decisions | Each decision resolved with evidence and author signoff where needed | OPEN |
| G5 | Claude / Timothy | 69 quotation-rights units (77 passages), history, A1–A6 | Rights/license disposition and owner decisions recorded | OPEN |
| G6 | GPT | Accessible PDF + EPUB and build provenance | Validated structures, content parity, reproducible artifact digests, Android QA | OPEN |
| G7 | Timothy | Explicit publication approval | Separately recorded approval after G1–G6 | NOT AUTHORIZED |

Concrete source review: `f001_exact_source_nine_case_524.sh` extracts three pinned Git blobs and runs two child scripts under 20-second timeouts; it deletes its temporary directory on exit. Thus its console output must be captured by a separate durable custody wrapper. `f001_preflight_536.sh` checks checkout cleanliness, tools, required scripts and three pinned blob identities but is **not** a test. Existing custody wrappers are not proven to have run.

Next GPT action: acquire clean full-history checkout, check #197 remains accessible and that a same-thread post-test report is possible, execute the pre-registered suite with durable log capture, report actual observations and deviations in #197. Do not report success from a zero exit alone. Claude owns complementary editorial/history/rights work; do not overwrite Claude records. No publication, account creation, outreach, spending, paid inference or Cloudflare loops.
