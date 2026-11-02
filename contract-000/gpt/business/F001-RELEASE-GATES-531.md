# F-001 TAM Protocol ebook — evidence-driven release gates (Run531)
**Single continuing product identifier:** F-001. **Status:** HOLD / NOT LAUNCH-READY. This is a draft acceptance matrix, not publication authorization. Source: shared Business decision sheet (blob 2975edcc), GPT checklist (69449fce), current pinned nine-case runner (4df5aaed), audited runner (e44975e7), custody wrapper (eb00fc26), preregistered Issue #197.
| Gate | Owner | Required acceptance evidence | Current state |
|---|---|---|---|
| H3b evidence validator | GPT | Exact Git source identities; all nine case names and two expected summaries; raw stdout/stderr, exit statuses, environment and SHA256 manifest; same-thread post-test narrative in #197 | BLOCKED: pinned replay not executed; earlier six-case transcription not equivalent |
| H2 | GPT | Preregistered #174, executed observations and evidence posted to same thread | OPEN |
| Six-file replay | GPT | Preregistered #161, source-pinned six-file observations and same-thread report | OPEN |
| Editorial | Claude | Each of 82 decision cards resolved with provenance, final manuscript changes reviewed | OPEN (82) |
| Quotation rights | Claude / Timothy | 69 rights units / 77 passages each cleared, replaced, removed or explicitly held with documented permission basis | OPEN |
| Historical/claim accuracy | Claude | Claim-by-claim source support or clear speculative labeling; no historical certainty inferred from arithmetic | OPEN |
| Packaging | GPT | Accessible PDF/EPUB, independently verified hashes, accessibility checks, actual Android review | OPEN |
| Product decisions | Timothy | A1–A6, credit, license/source, pricing, refund terms, release authority | OPEN |
**Immediate next action:** run already-preregistered #197 nine-case replay against pinned Git objects in an isolated offline checkout, post actual observations to #197. Do not interpret a passing harness as rights clearance. No tests/CI executed this run. Do not create a new product or storefront.
**Static inspection finding:** custody wrapper records dirty status but does not reject dirty checkout; evidence must therefore explicitly distinguish source-pinned test files from mutable runner/wrapper files. A clean checkout or captured diff is required for stronger reproducibility. This is a source-review concern, not a demonstrated exploit.
**Coordination:** Claude owns editorial, quotation provenance and historical review; GPT owns technical replay, packaging and evidence. Shared files unchanged. No outreach, account creation, spending, publication, payments, paid inference or Cloudflare loops.
