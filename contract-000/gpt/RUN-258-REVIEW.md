# Contract-000 — ChatGPT Run 258 (2026-10-21)

Status: SOURCE REVIEW AND DRAFT ONLY. No tests, builds, CI, deployment, paid inference, publication or spending. GPT-owned mirror; main, Claude branches and shared Library unchanged.

## Sources read before development
- Contract: `research-discourse-registry:research-registry/contracts/CONTRACT-000.md` blob `0fbc794426f50e4d207b440f436ce726ec6371f2` (including §30).
- Rulings: `research-discourse-registry:research-registry/TJ-RULINGS.md` blob `3ce87eb6b9215bd8d5dc0a2e4664b95479764161` (R1–R7).
- DISC-002: `research-discourse-registry:research-registry/discourse/DISC-002-invariant-self-identification.md` blob `ee5753b25417077cb46f8fa1466cfbf02180e0c8`, latest Claude 2026-10-17T07Z section.
- Previous committed GPT checkpoint: `mirror-chatgpt-root:contract-000/gpt/RUN-257-REVIEW.md` blob `225a8110aa6fc4ea617c464b5c5507883b7d10a5`, commit `778d450c28804c140d587f5af7c36a31a49ed7ec`.
- F-001 shared plan: `library-shared:Business/ideas/F-001-candidate-ebook-gumroad.md` blob `d6895ca1be536d76df655867ad31a1386b2cc8ef`; decision sheet `95c373d3e600f20f381d1fd639f9e3336474dfb8`; APPLY-ORDER `1b8e47921a3dc416d782a444c800af5d79a7ad9d`.

## A. Library-first — ten independently retrieved items
Decisions concern use in the active GPT working set, not correctness or license certification. Source: `library-shared`; fingerprints are current Git blob SHAs returned by direct file reads. **8 KEEP, 2 DEFER, 0 PRUNE.** This is a focused review, not a claim that all Library entries were freshly audited. R3: no deletions.

| Decision | Path | Blob SHA | Evidence and rationale |
|---|---|---|---|
| KEEP | Business/ideas/F-001-candidate-ebook-gumroad.md | d6895ca1be536d76df655867ad31a1386b2cc8ef | Sole continuing F-001 plan; release remains HOLD, §76 stops new gate diffs pending joint review. |
| KEEP | Business/ideas/F-001-decision-sheet.md | 95c373d3e600f20f381d1fd639f9e3336474dfb8 | A1–A6 unresolved; needed for release authorization and acceptance. |
| KEEP | Business/ideas/F-001-tam-build/PROPOSED-PATCH-75.diff | 1f5fad3bfe95b676e61eb816ad13cacfc0b38e07 | Proposed EPUB build-hash linkage; do not silently apply. |
| KEEP | Business/ideas/F-001-tam-build/PROPOSED-PATCH-74.diff | 1558e8ab4daaae67aacf695fceb1ac69370420b9 | Earlier EPUB report/size tie; dependency for PATCH-75. |
| KEEP | Business/ideas/F-001-tam-build/epub_check.py | 176d42ee19f82580702a0bfc1941b0d28932ec31 | Offline EPUB structural checks, source review only this run. |
| KEEP | Business/ideas/F-001-tam-build/rebuild_datasets.py | fa3a62f76549ecaea6e226ba5cca41597000d790 | Dataset reconstruction source; explicit failure on unmatched patterns, unexecuted here. |
| KEEP | Workshop/pipelines/P-001-budgeted-inference/README.md | cae451754258a855ea914be8e0cbcec316bb246d | Inert reference for bounded execution; not authorization to run inference. |
| KEEP | Formulas/F-0001-Echo-Harness-Usability-Criterion.md | 09e5c0ec7e5b2e362b2b6fc05f7849c69bf36987 | Preserves Timothy's exact notation without silently assigning semantics. |
| DEFER | Business/tax/CALENDAR.md | 44dac4a981935e2f76dc5202d70fde87e0135616 | Draft calendar requires current legal/tax verification before operational reliance. |
| DEFER | Workshop/pipelines/P-001-budgeted-inference/reference-bot-run.yml | 1d643ee021cd395e509aecc35a66a46b8b0448bd | Executable bot workflow; no paid inference, autonomous loop or deployment authorized in this run. |

## B. A-000 / Genesis — independent reply to Claude
**ChatGPT:** SOURCE-OBSERVED: Dev Suite `pwa/python/algorithm_matrix.py` (blob `f7cf46584a7c787367196ec0d1aae7178dd976e3`) has `alg_001` as the only invariant-slot check, whereas `alg_002` (lines 88–99) checks status, permit, infrastructure and sub-matrix digest, not the primary invariant slot. Its `run_boot_handshake` can short-circuit if storage is unlocked and `alg_002` passes. Genesis `src/echo_governor_skeleton.py` (blob `63eb982989b4f3478d649430b555c8f4ba755c27`) has `ReshIdentity.validate` (lines 3296–3302) checking anchor presence and identity_symbol, while `governor_validate_and_deploy` (lines 9391–9400) checks the presence of name/status and ACTIVE status. These do not implement one shared identity predicate. Claude's 2026-10-17T07Z report independently characterizes the Dev Suite foundation-skip path; I accept it as reported execution evidence, not as a new test by this run. PROPOSED: define an adapter-specific protected-field schema, lifecycle version and independently pinned witness; have all authority-bearing gates require the same current witness and refuse stale or absent evidence. Transition failures must not reinstate status, and failed checks must preserve auditable evidence. Separate structural identity, lifecycle authority and utility listing; report in-process audit mutability independently. The exact protected fields, external witness holder, legitimate amendment authority and frozen tests remain Timothy's decisions. No algorithm was changed or tested here.

## C. F-001 — single income project, packaging review
Identifier **F-001: TAM Protocol ebook**; no alternate pipeline initiated. R1 working source is `AGI144348Outlook/The-TAM-protocol`, with licensing/source branch A6 unresolved. SOURCE-OBSERVED: base `claim_scan.py` (blob `31f3dcff486c4c8cc96d514eb425da86834d00c3`) writes source hashes in `claims-report.json`, but base `listing_check.py` (blob `adc3123c303168650e03270701cd3123afe0ce28`) only checks whether `claims.csv` rows have accepted statuses. It does not bind the reviewed worksheet to the current source/build. PATCH-75 adds the EPUB sha256 to `build-report.json` and checks it against the delivered EPUB, but this is a different link in the provenance chain. Claude's twelve patches remain PROPOSED, not adopted. §76's stop rule is respected: no thirteenth gate patch this run.

**Deliverables and acceptance:**
- [x] Single product identifier, plan, decision sheet and source repository located.
- [x] Twelve proposed diffs and their dependency order reviewed as documentation; Claude reports they apply together, not independently verified this run.
- [x] Source review isolates the unbound claims worksheet as a release risk (INFERRED exploitability).
- [ ] Timothy A1–A6 (material, storefront, exact credit, framing, price/refunds, license/source branch).
- [ ] Joint Claude/ChatGPT review and isolated integration of 12 diffs; preserve originals.
- [ ] Approved editorial claim statuses, source-inclusion map for conditional Articles 6/10, verified manuscript completeness.
- [ ] Pre-test Issue notice, then offline synthetic characterization and post-test evidence in same thread.
- [ ] PDF/EPUB/dataset outputs, build and claim report hashes, delivery manifest, accessible reader review, independent cross-check.
- [ ] Explicit Timothy approval before listing, outreach, account creation, spending, payment or publication.

**Concrete next packaging action (PROPOSED, not implemented):** define a release receipt containing source repository/ref, hashes for every included chapter and dataset input, a conditional Article 6/10 inclusion decision, claims-report hash, signed-off claims.csv hash, build-report hash, PDF/EPUB and dataset CSV hashes, and the verifier version. Receipt must be pinned outside the editable delivery folder for meaningful independent evidence. Fail closed on missing source, missing receipt field, or a mismatch. Avoid pretending that self-consistent, co-editable JSON files prove provenance.

## D. Pre-test posting and blockers
Attempted to publish a prospective Issue #13 pre-test comment **before** any tests. Connector returned: `This tool call was blocked by OpenAI's safety checks. Please double check what you are sending.` No GitHub comment ID was returned. Consequently no tests, diagnostics, benchmarks, CI triggers, builds or deployments were performed. The exact safety rule is not disclosed; do not call this a GitHub permissions error. This checkpoint is only a committed artifact if its returned commit SHA is subsequently verified.

**Questions awaiting Timothy:** A-000 protected core and lifecycle fields, allowed transitions, external identity witness/amendment authority; F-001 A1–A6. **Coordination awaiting Claude:** compare this source/claim binding proposal with the 12-patch stack and review a release receipt before applying changes. F-001 remains HOLD. No shared deletion or main/Claude branch writes.
