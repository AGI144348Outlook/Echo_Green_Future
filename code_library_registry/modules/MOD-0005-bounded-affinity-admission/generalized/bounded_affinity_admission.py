"""Deterministic bounded admission and weighted undirected tie accounting."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Callable, Generic, Hashable, Iterable, TypeVar

Item = TypeVar("Item", bound=Hashable)
ScoreFunction = Callable[[Item, Item], float]
KeyFunction = Callable[[Item], str]


def _positive_int(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _score(value: float, name: str = "score") -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")
    result = float(value)
    if not isfinite(result) or not 0.0 <= result <= 1.0:
        raise ValueError(f"{name} must be finite and between 0 and 1")
    return result


@dataclass(frozen=True)
class AdmissionDecision(Generic[Item]):
    item: Item
    accepted: bool
    score: float | None
    reason: str
    neighbors: tuple[tuple[Item, float], ...] = ()


@dataclass(frozen=True)
class CycleResult(Generic[Item]):
    cycle: int
    considered: int
    accepted: tuple[AdmissionDecision[Item], ...]
    rejected: tuple[AdmissionDecision[Item], ...]
    queue_remaining: int
    population_size: int


class WeightedTieLedger(Generic[Item]):
    def __init__(self, *, key: KeyFunction[Item] = str) -> None:
        self._key = key
        self._weights: dict[tuple[Item, Item], float] = {}
        self._activations: dict[Item, int] = {}
        self._events = 0

    def _pair(self, left: Item, right: Item) -> tuple[Item, Item]:
        if left == right:
            raise ValueError("a tie requires two distinct items")
        left_key, right_key = self._key(left), self._key(right)
        if left_key == right_key:
            raise ValueError("key function must distinguish tied items")
        return (left, right) if left_key < right_key else (right, left)

    def record(self, left: Item, right: Item, weight: float) -> None:
        pair = self._pair(left, right)
        amount = _score(weight, "weight")
        self._weights[pair] = self._weights.get(pair, 0.0) + amount
        self._activations[left] = self._activations.get(left, 0) + 1
        self._activations[right] = self._activations.get(right, 0) + 1
        self._events += 1

    @property
    def event_count(self) -> int:
        return self._events

    def activation_count(self, item: Item) -> int:
        return self._activations.get(item, 0)

    def strongest(self, limit: int = 10) -> tuple[tuple[tuple[Item, Item], float], ...]:
        _positive_int(limit, "limit")
        ordered = sorted(
            self._weights.items(),
            key=lambda row: (-row[1], self._key(row[0][0]), self._key(row[0][1])),
        )
        return tuple(ordered[:limit])

    def snapshot(self) -> dict[str, object]:
        ties = [
            {"left": self._key(pair[0]), "right": self._key(pair[1]), "weight": weight}
            for pair, weight in self.strongest(max(1, len(self._weights)))
        ] if self._weights else []
        activations = {
            self._key(item): count
            for item, count in sorted(self._activations.items(), key=lambda row: self._key(row[0]))
        }
        return {
            "ties": ties,
            "activations": activations,
            "event_count": self._events,
            "unique_ties": len(self._weights),
        }


class BoundedAffinityAdmission(Generic[Item]):
    def __init__(
        self,
        existing: Iterable[Item],
        *,
        per_cycle: int = 6,
        scan_multiplier: int = 3,
        min_score: float = 0.05,
        max_score: float = 0.90,
        admission_sample_limit: int = 80,
        neighbor_sample_limit: int = 120,
        neighbor_min_score: float = 0.15,
        max_neighbors: int = 4,
        key: KeyFunction[Item] = str,
    ) -> None:
        self._per_cycle = _positive_int(per_cycle, "per_cycle")
        self._scan_multiplier = _positive_int(scan_multiplier, "scan_multiplier")
        self._min_score = _score(min_score, "min_score")
        self._max_score = _score(max_score, "max_score")
        if self._min_score > self._max_score:
            raise ValueError("min_score must not exceed max_score")
        self._admission_sample_limit = _positive_int(
            admission_sample_limit, "admission_sample_limit"
        )
        self._neighbor_sample_limit = _positive_int(
            neighbor_sample_limit, "neighbor_sample_limit"
        )
        self._neighbor_min_score = _score(neighbor_min_score, "neighbor_min_score")
        self._max_neighbors = _positive_int(max_neighbors, "max_neighbors")
        self._key = key

        self._population: list[Item] = []
        self._population_set: set[Item] = set()
        for item in existing:
            if item not in self._population_set:
                self._population.append(item)
                self._population_set.add(item)
        self._queue: list[Item] = []
        self._cycles = 0

    @property
    def population(self) -> tuple[Item, ...]:
        return tuple(self._population)

    @property
    def queue(self) -> tuple[Item, ...]:
        return tuple(self._queue)

    def enqueue(self, candidates: Iterable[Item]) -> None:
        self._queue.extend(candidates)

    def _ordered_sample(self, population: tuple[Item, ...], limit: int) -> tuple[Item, ...]:
        return tuple(sorted(population, key=self._key)[:limit])

    def run_cycle(
        self,
        ledger: WeightedTieLedger[Item],
        affinity: ScoreFunction[Item],
        *,
        tie_score: ScoreFunction[Item] | None = None,
    ) -> CycleResult[Item]:
        snapshot = tuple(self._population)
        scan_count = self._per_cycle * self._scan_multiplier
        considered = tuple(self._queue[:scan_count])
        admission_refs = self._ordered_sample(snapshot, self._admission_sample_limit)
        neighbor_refs = self._ordered_sample(snapshot, self._neighbor_sample_limit)
        tie_fn = tie_score or affinity

        accepted: list[AdmissionDecision[Item]] = []
        rejected: list[AdmissionDecision[Item]] = []

        for candidate in considered:
            if candidate in self._population_set:
                rejected.append(AdmissionDecision(candidate, False, None, "duplicate"))
                continue
            if not admission_refs:
                rejected.append(
                    AdmissionDecision(candidate, False, None, "no_reference_population")
                )
                continue

            score = max(_score(affinity(candidate, item), "affinity") for item in admission_refs)
            if score < self._min_score:
                rejected.append(AdmissionDecision(candidate, False, score, "below_minimum"))
                continue
            if score > self._max_score:
                rejected.append(AdmissionDecision(candidate, False, score, "above_maximum"))
                continue
            if len(accepted) >= self._per_cycle:
                rejected.append(AdmissionDecision(candidate, False, score, "cycle_capacity"))
                continue

            neighbors = []
            for item in neighbor_refs:
                strength = _score(tie_fn(candidate, item), "tie score")
                if strength >= self._neighbor_min_score:
                    neighbors.append((item, strength))
            neighbors.sort(key=lambda row: (-row[1], self._key(row[0])))
            accepted.append(
                AdmissionDecision(
                    candidate,
                    True,
                    score,
                    "accepted",
                    tuple(neighbors[: self._max_neighbors]),
                )
            )

        # Commit only after all scoring succeeds.
        self._queue = self._queue[len(considered) :]
        for decision in accepted:
            self._population.append(decision.item)
            self._population_set.add(decision.item)
            for neighbor, strength in decision.neighbors:
                ledger.record(decision.item, neighbor, strength)
        self._cycles += 1

        return CycleResult(
            cycle=self._cycles,
            considered=len(considered),
            accepted=tuple(accepted),
            rejected=tuple(rejected),
            queue_remaining=len(self._queue),
            population_size=len(self._population),
        )
