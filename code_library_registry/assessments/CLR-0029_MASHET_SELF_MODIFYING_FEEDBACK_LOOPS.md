# CLR-0029 — Mashet Self-Modifying Architecture with Feedback Loops

## Classification
Historical governance/self-modification prototype; very high architectural relevance.

## Core lifecycle
Proposal -> substrate validation -> runtime execution/observation -> post-execution analysis -> adaptation proposal -> hash-linked audit.

This is an important bridge between CLR-0022 capability/admission governance, CLR-0027 substrate contracts, CLR-0028 generation, and Echo's Governor/audit architecture.

## Five loops
1. Pre-execution substrate rule validation.
2. Runtime activation/assertion/property checks.
3. Post-execution fidelity analysis.
4. Historical success-rate based adaptation proposal.
5. Hash-linked event history.

## Strong architectural contribution
The artifact separates generation from validation and creates explicit intervention points before, during, and after execution. This is substantially stronger than allowing a generated glyph sequence to imply executable authority.

## Critical findings

### 1. Active is not verified
execute_with_feedback activates every dominant substrate before operation execution, then constructs:
substrates_verified = runtime_loop.active_substrates.copy()

Therefore fidelity can be 1.0 merely because the controller inserted labels into active_substrates. Runtime assertions mostly verify bookkeeping membership, not behavioral substrate satisfaction.

Required split:
declared_substrates
authorized_substrates
active_substrates
observed_properties
verified_substrates

A substrate should become verified only from an independent predicate over execution evidence.

### 2. Runtime state leaks between executions
active_substrates and violation_log are instance-global and are not cleared per execution. A later operation can inherit active labels and old violations. Introduce ExecutionContext with execution_id and per-run activation/violation/evidence state, then close/deactivate it in finally.

### 3. Pre-validation does not gate execution
generate_and_verify_word returns invalid words, and execute_with_feedback has no mandatory validation token/result parameter. Invalid generation can still be executed by a caller.

Governor rule:
Execute(req) only if validation.valid AND authorization.valid AND contract.valid.

### 4. all_substrates vs dominant_substrates mismatch
Pre-validation checks word.all_substrates, while runtime activates only word.dominant_substrates. The object being validated is therefore not necessarily the object being executed. Define required, optional, contextual and incidental substrate sets explicitly.

### 5. Runtime property checks are placeholders
Iterable data is not evidence of flow continuity, and recursion boundedness always returns True. These should be recorded as stub predicates, not substrate verification.

### 6. Success is too weak
execution_successful means operation_fn did not throw. It does not establish task success, contract satisfaction, output correctness, or substrate fidelity.

Use separate fields:
completed_without_exception
task_success
contract_satisfied
substrate_evidence
safety_violations

### 7. Self-improvement does not yet modify the generator
generate_improved_operation prints prefer/avoid proposals, then calls the unchanged generator. This is a proposal loop, not executable self-modification.

This is actually a safer architecture. Preserve proposal/commit separation:
Evidence -> Proposal -> Governor review -> bounded patch -> tests -> commit or rollback.

### 8. Substrate success attribution is confounded
Every claimed substrate receives the whole operation's success/failure. This cannot identify which substrate association helped or harmed performance. Use controlled ablations, counterfactual runs, or attribution evidence.

### 9. Confidence is sample volume, not epistemic confidence
min(1,total_executions/100) measures exposure only. It ignores failure variance, task diversity, dependence, distribution shift and evidence quality. Rename sample_coverage or replace with calibrated uncertainty.

### 10. Audit chain verification is incomplete
verify_chain_integrity checks only previous_hash links. It never recomputes each event hash from its contents. An event can be altered while retaining stored hash/links and still pass.

Verification must recompute every event hash and validate its predecessor relation.

### 11. The audit trail is tamper-evident only under stronger storage assumptions
An in-memory mutable Python list is not immutable. Hash chaining provides tamper evidence only when hashes are correctly recomputed/verified and an external trusted anchor/checkpoint prevents wholesale chain rewriting.

### 12. 64-bit truncated SHA-256 is unnecessary
Sixteen hex characters gives 64 bits. Keep full SHA-256 for audit identifiers unless compact display is separately derived.

### 13. Mutual exclusion loop can duplicate violations
Nested ordered iteration can report the same contradiction twice. Iterate unordered pairs/combinations.

### 14. Context is accepted but not semantically used
Validation accepts context but rules are global. Future substrate contracts should support environment/domain-specific prerequisites and exclusions.

## Recommended governed model

ExecutionRequest
-> GenerationRecord
-> SemanticContract
-> CapabilityAuthorization
-> ValidationEvidence
-> ExecutionContext
-> RuntimeEvidence
-> OutcomeEvaluation
-> ImprovementProposal
-> GovernorDecision
-> VersionedPatch
-> Regression/Ablation Tests
-> Commit or Rollback
-> AuditCheckpoint

Verification relation:
Verified(s,e) iff declared(s,e) AND authorized(s,e) AND predicate_s(trace_e, input_e, output_e, context_e) = true.

Self-modification relation:
PatchAccepted(p) iff authorized(p) AND tests(p) pass AND invariants(p) hold AND rollback(p) exists.

## Connection to Echo
This is a direct historical ancestor of the five-loop architecture already used in the Mashet/Echo design:
L1 Validation
L2 Runtime
L3 Analysis
L4 Self-Expansion
L5 Audit Chain.

For the modern system, L4 should remain proposal-driven rather than allowing unreviewed mutation.

## Status
Assessed / Historical Governor-feedback ancestor / High-priority reconstruction candidate.
