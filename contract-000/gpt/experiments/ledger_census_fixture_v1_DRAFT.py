"""Noncanonical Echo-GPT event-ledger fixture, DRAFT, NOT EXECUTED.
No imports from Genesis. Python stdlib only. Companion independent oracle and
10-category runner are NOT complete; do not claim preregistered tests passed.
"""
from dataclasses import dataclass
import hashlib
import json
import random

SEEDS = tuple(range(1106, 1136))

@dataclass(frozen=True)
class Arrival:
    ident: int
    tick: int
    source: str

def arrivals(seed: int, ticks: int = 180) -> tuple[Arrival, ...]:
    """Independent arrival census, fixed before seat assignment.
    Two Bernoulli opportunities per tick; burst and quiet periods
    belong to ledger verification, NOT predictive evaluation.
    """
    rng = random.Random(seed)
    out = []
    for tick in range(ticks):
        quiet = tick % 30 in range(18, 28)
        for opportunity in range(2):
            if (not quiet and rng.random() < .54) or (tick % 30 == 0):
                out.append(Arrival(len(out), tick, f"opportunity-{opportunity}"))
    return tuple(out)

def census_digest(census: tuple[Arrival, ...]) -> str:
    raw = json.dumps([a.__dict__ for a in census],
                     sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()

def ledger(seed: int, dwell: int = 3, seats: int = 2,
           max_wait: int = 5, ticks: int = 180) -> dict:
    """Discrete synthetic queue; explicit phase ordering:
    release -> expire -> arrive -> admit -> finalize at horizon.
    Events carry immutable arrival ID. This is a proposed fixture,
    not an empirical claim about Echo's cognition.
    """
    census = arrivals(seed, ticks)
    by_tick = {}
    for a in census:
        by_tick.setdefault(a.tick, []).append(a)
    events, waiting, occupied = [], [], {}
    for tick in range(ticks):
        for seat, (ident, release) in sorted(list(occupied.items())):
            if release <= tick:
                events.append(dict(kind="release", id=ident, tick=tick, seat=seat))
                del occupied[seat]
        expired = [a for a in waiting if tick-a.tick > max_wait]
        waiting = [a for a in waiting if tick-a.tick <= max_wait]
        for a in expired:
            events.append(dict(kind="expire", id=a.ident, tick=tick))
        for a in by_tick.get(tick, []):
            events.append(dict(kind="arrival", id=a.ident, tick=tick))
            waiting.append(a)
        for seat in range(seats):
            if seat not in occupied and waiting:
                a = waiting.pop(0)
                events.append(dict(kind="admit", id=a.ident, tick=tick, seat=seat))
                occupied[seat] = (a.ident, tick+dwell)
    for a in waiting:
        events.append(dict(kind="open_wait", id=a.ident, tick=ticks))
    for seat, (ident, release) in sorted(occupied.items()):
        events.append(dict(kind="open_seat", id=ident, tick=ticks,
                           seat=seat, planned_release=release))
    return dict(seed=seed, ticks=ticks, seats=seats, dwell=dwell,
                max_wait=max_wait, census=[a.__dict__ for a in census],
                census_sha256=census_digest(census), events=events)

if __name__ == "__main__":
    # No automatic execution: test run must be prospectively posted to GitHub.
    raise SystemExit("DRAFT ONLY: preregister and independently review before running")
