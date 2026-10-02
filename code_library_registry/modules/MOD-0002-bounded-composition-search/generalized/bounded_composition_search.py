"""Deterministic breadth-first search over bounded operation compositions.

The search is intentionally domain-neutral. Callers supply the initial state,
goal predicate and ordered operations. No operation is executed outside the
declared depth, expansion and state-admission limits.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Hashable, Iterable, Sequence


State = Any
Operation = tuple[str, Callable[[State], State]]


@dataclass(frozen=True)
class SearchEvent:
    depth: int
    operation: str
    source_key: Hashable
    outcome_key: Hashable | None
    status: str
    detail: str = ""


@dataclass(frozen=True)
class SearchResult:
    found: bool
    path: tuple[str, ...]
    final_state: State | None
    visited_count: int
    expansions: int
    reason: str
    events: tuple[SearchEvent, ...]


class BoundedCompositionSearch:
    """Find the shortest admitted operation sequence with deterministic BFS.

    Operations are tried in caller-supplied order. States are deduplicated by
    ``state_key``. An operation exception is recorded and skipped; it never
    counts as a candidate state. ``admit_state`` can reject unsafe or
    out-of-domain outcomes before they enter the frontier.
    """

    def __init__(
        self,
        operations: Iterable[Operation],
        *,
        state_key: Callable[[State], Hashable] | None = None,
        admit_state: Callable[[State], bool] | None = None,
    ) -> None:
        self.operations: tuple[Operation, ...] = tuple(operations)
        if not self.operations:
            raise ValueError("at least one operation is required")

        names = [name for name, _ in self.operations]
        if any(not isinstance(name, str) or not name for name in names):
            raise ValueError("operation names must be non-empty strings")
        if len(set(names)) != len(names):
            raise ValueError("operation names must be unique")
        if any(not callable(fn) for _, fn in self.operations):
            raise TypeError("every operation must be callable")

        self.state_key = state_key or (lambda state: state)
        self.admit_state = admit_state or (lambda _state: True)

    def find(
        self,
        initial_state: State,
        is_goal: Callable[[State], bool],
        *,
        max_depth: int,
        max_expansions: int = 10_000,
    ) -> SearchResult:
        if max_depth < 0:
            raise ValueError("max_depth must be non-negative")
        if max_expansions < 0:
            raise ValueError("max_expansions must be non-negative")
        if not callable(is_goal):
            raise TypeError("is_goal must be callable")

        initial_key = self._key(initial_state)
        if is_goal(initial_state):
            return SearchResult(True, (), initial_state, 1, 0, "initial-state-is-goal", ())

        frontier: list[tuple[State, tuple[str, ...]]] = [(initial_state, ())]
        visited = {initial_key}
        events: list[SearchEvent] = []
        expansions = 0

        for depth in range(1, max_depth + 1):
            next_frontier: list[tuple[State, tuple[str, ...]]] = []
            for state, path in frontier:
                source_key = self._key(state)
                for name, operation in self.operations:
                    if expansions >= max_expansions:
                        return SearchResult(
                            False, (), None, len(visited), expansions,
                            "expansion-limit", tuple(events)
                        )
                    expansions += 1
                    try:
                        outcome = operation(state)
                        outcome_key = self._key(outcome)
                    except Exception as exc:  # operation boundary is recorded, not hidden
                        events.append(SearchEvent(
                            depth, name, source_key, None, "operation-error",
                            f"{type(exc).__name__}: {exc}",
                        ))
                        continue

                    candidate = path + (name,)
                    if not self.admit_state(outcome):
                        events.append(SearchEvent(
                            depth, name, source_key, outcome_key, "rejected-state"
                        ))
                        continue

                    events.append(SearchEvent(
                        depth, name, source_key, outcome_key, "tested"
                    ))
                    if is_goal(outcome):
                        return SearchResult(
                            True, candidate, outcome, len(visited) + (outcome_key not in visited),
                            expansions, "goal-found", tuple(events)
                        )

                    if outcome_key not in visited:
                        visited.add(outcome_key)
                        next_frontier.append((outcome, candidate))
            frontier = next_frontier
            if not frontier:
                return SearchResult(
                    False, (), None, len(visited), expansions,
                    "frontier-exhausted", tuple(events)
                )

        return SearchResult(
            False, (), None, len(visited), expansions,
            "depth-limit", tuple(events)
        )

    def _key(self, state: State) -> Hashable:
        key = self.state_key(state)
        try:
            hash(key)
        except TypeError as exc:
            raise TypeError("state_key must return a hashable value") from exc
        return key


def replay(
    initial_state: State,
    path: Sequence[str],
    operations: Iterable[Operation],
) -> State:
    """Reapply a named path, rejecting missing or duplicate operation names."""
    operation_list = tuple(operations)
    table = {name: fn for name, fn in operation_list}
    if len(table) != len(operation_list):
        raise ValueError("operation names must be unique")
    state = initial_state
    for name in path:
        try:
            operation = table[name]
        except KeyError as exc:
            raise KeyError(f"unknown operation in path: {name}") from exc
        state = operation(state)
    return state

