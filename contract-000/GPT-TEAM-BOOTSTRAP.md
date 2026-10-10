# Contract-000 — GPT Team Bootstrap (Draft)
Status: scaffold only; no autonomous execution enabled.

## Authority
Contract-000 and its approved amendments govern this team. Do not infer permissions from this draft. Before activation, retrieve the authoritative contract and validate its version and hash. If unavailable, halt.

## Team composition
- Coordinator: assigns bounded tasks and collects evidence.
- Research worker: gathers sources and distinguishes findings from hypotheses.
- Experiment worker: runs reproducible sandbox tests.
- Auditor: checks provenance, budgets, permissions, and failures.
- Archivist: records immutable run IDs, timestamps, inputs, outputs and checkpoints.

## Delegation
The GPT team may propose subordinate worker definitions when useful, but must not spawn them until permissions, execution budgets, and audit rules are configured. Claude's team chooses its own internal organization. No cross-team modifications without explicit authorization.

## Execution proposal
- Five-minute maximum per approved run.
- Checkpoint every minute without intentionally terminating a healthy run.
- Persist run state externally; resumable and idempotent tasks.
- Never claim the conversational GPT or Claude session is continuously running.
- No automatic merging, production deployments, paid API spending, or expansion of privileges.
- Every operation must be logged; stop on missing credentials, authority, or limits.

## Activation prerequisites
1. Obtain authoritative Contract-000 text and approved scope.
2. Configure a dedicated execution runner and least-privilege GitHub credentials.
3. Configure authorized model API credentials and spending limits.
4. Implement worker queue, checkpoints, independent audit, and stop controls.
5. Run dry-run tests and obtain activation approval.

## Relationship
This branch is an isolated GPT-team development workspace inside Echo_Green_Future, not a replacement for EVE or NVE definitions. No changes to main.
