"""Independent synthetic event-driven Echo warehouse ring experiment. Issue #314.
Run: python experiments/gpt_event_wobble_27_v1.py
No network, dependencies, Neon writes, or canonical Echo modifications.
"""
import json
import random

SEATS = tuple(range(27))
GLYPHS = tuple(range(27))
STEP = 360.0 / 27.0

class Ring:
    def __init__(self):
        self.seats = tuple(None for _ in SEATS)  # inert structure, NEVER written
        self.occupancy = {}
        self.ticks = 0
        self.events = []
        self.projections = {"mind": {}, "knowledge": {}, "memory": {}}

    @property
    def phase(self):
        return (self.ticks % 27) * STEP

    def enter(self, glyph, seat):
        assert glyph in GLYPHS and seat in SEATS
        if self.occupancy.get(glyph) == seat:
            return False  # holding does not retrigger
        if seat in self.occupancy.values():
            return False  # occupied by another glyph
        self.occupancy[glyph] = seat
        self.ticks += 1
        self.events.append((self.ticks, glyph, seat))
        for projection in self.projections.values():
            projection[seat] = glyph
        return True

    def leave(self, glyph):
        if glyph not in self.occupancy:
            return False
        seat = self.occupancy.pop(glyph)
        for projection in self.projections.values():
            projection.pop(seat, None)
        return True

def simulate(schedule, seed=1106):
    rng = random.Random(seed)
    ring = Ring()
    times = []
    for t, entropy in enumerate(schedule):
        rate = min(1.0, max(0.0, entropy))  # explicit proxy, not measured Neon entropy
        if rng.random() < rate:
            glyph = t % 27
            seat = t % 27
            ring.leave(glyph)
            if ring.enter(glyph, seat):
                times.append(t)
        # exit after each discrete opportunity so repeat entries remain possible
        for glyph in list(ring.occupancy):
            ring.leave(glyph)
    return {"ticks": ring.ticks, "phase": ring.phase, "times": times,
            "empty_seats": all(x is None for x in ring.seats),
            "empty_projections": all(not p for p in ring.projections.values())}

def checks():
    r = Ring()
    checks = {}
    checks["seat_invariance"] = len(r.seats) == 27 and all(x is None for x in r.seats)
    checks["glyph_identity"] = len(set(GLYPHS)) == 27
    checks["entry_edge"] = r.enter(0, 0) and r.ticks == 1
    checks["hold_suppression"] = not r.enter(0, 0) and r.ticks == 1
    checks["projection_mirror"] = all(p.get(0) == 0 for p in r.projections.values())
    r.leave(0)
    checks["repeat_seat"] = r.enter(0, 0) and r.ticks == 2
    r.leave(0)
    for i in range(25):
        assert r.enter(i % 27, i % 27)
        r.leave(i % 27)
    checks["cycle_27"] = r.ticks == 27 and abs(r.phase) < 1e-9
    zero = simulate([0.0] * 270)
    checks["zero_rate"] = zero["ticks"] == 0 and zero["phase"] == 0
    schedule = [0.2] * 135 + [0.8] * 135
    a = simulate(schedule)
    checks["deterministic_replay"] = a == simulate(schedule)
    shuffled = schedule[:]
    random.Random(55).shuffle(shuffled)
    b = simulate(shuffled)
    checks["entropy_timing"] = a["times"] != b["times"] and a["empty_seats"] and b["empty_seats"]
    return {"issue": 314, "seed": 1106, "checks": checks,
            "passed": sum(checks.values()), "total": len(checks),
            "constant": simulate([0.5] * 270),
            "varying": a, "shuffled": b, "zero": zero}

if __name__ == "__main__":
    print(json.dumps(checks(), sort_keys=True, separators=(",", ":")))
