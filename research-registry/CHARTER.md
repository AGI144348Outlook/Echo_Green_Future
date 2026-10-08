# -0 Discourse & Workshop Charter (v0.1)

Status: proposed governance for research-discourse-registry (-0); does not modify main. Human owner has final approval authority.

## Layout
- `research-registry/matrices/`: topic indexes linking to primary records.
- `research-registry/discourse/`: audience-readable chapters (question, positions, counterarguments, experiments, limits).
- `research-registry/races/RACE-XXXX/`: immutable race manifest, test specification, run evidence, adjudication and links to contenders.
- `research-registry/locker/R2/`: temporary candidate queue and retention ledger; not a source of truth.
- `research-registry/proposals/`: human-reviewed proposals to main.
- Workshop implementations live on separate contender branches, not in the discourse branch.

## Opening a debate
Create a numbered question and a claim ledger. Record independent positions, sources, falsifiable predictions and known unknowns. Open a race only for claims that can be tested. Publish a readable chapter with links to evidence.

## Race contract — finish line first
Before contenders code, freeze: task, input fixtures, expected output/schema, pass/fail assertions, evaluation runner version/hash, time/memory/compute budgets, allowed dependencies, reproducibility requirements, tie handling, and safety boundaries. Both models acknowledge the same manifest. After freeze, no contender may alter tests; changes require a new race revision and equal notice. Prefer hidden holdout cases plus public fixtures, with test integrity verified by a neutral runner.

## Execution and adjudication
Separate contender branches and isolated execution environments; prohibit access to opponent branch or hidden tests until closure. Capture commit SHA, environment, logs, test results, resource usage and artifacts. The independent tests decide objective outcomes, not either model's opinion. If both pass, use preregistered tie-breakers; otherwise declare tie/no winner. Human owner can approve, reject, or flag an invalid race, with reasons recorded. No self-awarded wins.

## R2 locker clearance
R2 holds temporary submissions pending validation, review, and disposition. At race closure: inventory all items; verify each has a canonical permanent reference and SHA; promote accepted evidence to immutable race records; quarantine disputed or unsafe items; delete only disposable copies after human-approved retention checks; log each clearance with timestamp, item hash, destination and authorizer. Never erase audit history or unresolved evidence.

## Promotion toward main
A race win is evidence, not merge authorization. A proposal needs: user-visible value, tests and reproduction instructions, threat/license review, dependency and regression checks, source links, rollback plan, and owner approval. Submit PR toward main only after explicit human approval and existing branch protections. No automatic merge.

## First proposed finish line: Echo online from a phone
A public HTTPS page on a test deployment shows `Echo: online` only after a live health endpoint returns a JSON response with `service: echo`, `status: ready`, `version`, and `timestamp`. Acceptance tests, fixed before race: (1) Android browser can open URL without login; (2) endpoint returns HTTP 200 and valid JSON matching schema; (3) timestamp fresh within 60 seconds at request time; (4) a user-triggered `ping` yields a server-generated request ID visible in UI and corresponding server log; (5) disconnected backend cannot falsely show online; (6) repeat 10 requests with at least 9 successful under 5 seconds each. Passing means transport/service reachability, NOT intelligence, autonomy, or reasoning. Exact endpoint and fixture URLs must be fixed in the race manifest before execution.

## Discourse ↔ workshop loop
Each public chapter references race IDs and results; each race links back to the originating philosophical claim. Preserve disagreements and failed tests rather than rewriting history. Model-to-model scheduled exchanges require separately deployed authenticated API orchestration; this charter does not activate them.
