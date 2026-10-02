# Applications and limits

## Meaningful applications

- synthesize the shortest sequence of bounded data transformations;
- search small workflow or migration-state spaces;
- reproduce puzzle, planning or educational state transitions;
- explore repair candidates when every allowed operation is explicit;
- test whether a declared primitive set can reach a target under a budget;
- produce a replayable operation path and an auditable event record.

The generic engine improves on the source experiment by accepting arbitrary state types, separating state identity from state value, enforcing depth and expansion budgets, validating operation identities, recording rejected/error transitions, and exposing deterministic replay.

## Assumptions

- Each operation behaves deterministically for the same input.
- The caller supplies a stable, hashable state key.
- Breadth-first search is appropriate because each operation has equal cost.
- Side effects are absent or independently controlled; the engine may invoke an operation on multiple states.
- The caller's state-admission predicate correctly defines the safe search domain.

## Non-applications

This is not a general autonomous agent, theorem prover, optimal planner with weighted costs, distributed workflow engine, security sandbox or guarantee that an operation is safe. It should not execute untrusted operations. Large or infinite state spaces require stronger heuristics, resource isolation and domain-specific proofs.

