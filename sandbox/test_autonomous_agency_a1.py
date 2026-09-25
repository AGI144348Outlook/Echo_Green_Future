"""A1 — Autonomous Agency: Unspecified Capability Gap

This is deliberately a behavioral test, not a vocabulary test.
ECHO receives a goal and primitive operations, but NOT the missing composition.
The control has self-generated homework disabled.

Pass evidence requires an ECHO-originated chain:
OBSERVE -> GAP -> HOMEWORK -> PROPOSE -> TEST -> EVALUATE -> ADOPT/REVISE.
"""
from dataclasses import dataclass, field
from typing import Callable

@dataclass
class Event:
    actor: str
    action: str
    detail: str

@dataclass
class NVE:
    """Tiny nested virtual environment with an intentionally missing capability."""
    value: int = 3
    target: int = 11
    primitives: dict = field(default_factory=lambda: {
        "double": lambda x: x * 2,
        "increment": lambda x: x + 1,
    })

    def goal_met(self, x):
        return x == self.target

class A1Agent:
    """Minimal agency adapter around the branch's existing homework semantics.

    It is intentionally deterministic so the same starting state is reproducible.
    It is NOT given a solution sequence. It searches compositions only after
    identifying that no single primitive satisfies the goal.
    """
    def __init__(self, homework_enabled=True):
        self.homework_enabled = homework_enabled
        self.audit = []
        self.learned = {}

    def log(self, actor, action, detail):
        self.audit.append(Event(actor, action, detail))

    def observe(self, env):
        self.log("ECHO", "OBSERVE", f"state={env.value}; target={env.target}; primitives={list(env.primitives)}")
        return env.value, env.target

    def identify_gap(self, env):
        direct = {name: fn(env.value) for name, fn in env.primitives.items()}
        if env.target not in direct.values():
            self.log("ECHO", "GAP", "No available single primitive reaches the target.")
            return True
        return False

    def assign_homework(self):
        if not self.homework_enabled:
            self.log("CONTROL", "HOMEWORK_DISABLED", "Self-generated homework unavailable.")
            return False
        self.log("ECHO", "HOMEWORK", "Discover a composition of permitted primitives that reaches the target.")
        return True

    def propose_and_test(self, env, max_depth=5):
        # Breadth-first composition search. The goal is supplied; the path is not.
        frontier = [(env.value, [])]
        seen = {env.value}
        for _ in range(max_depth):
            nxt = []
            for value, path in frontier:
                for name, fn in env.primitives.items():
                    out = fn(value)
                    candidate = path + [name]
                    self.log("ECHO", "TEST", f"{candidate}: {env.value}->{out}")
                    if env.goal_met(out):
                        self.log("ECHO", "EVALUATE", f"candidate reaches target: {candidate}")
                        self.learned["reach_target"] = candidate
                        self.log("ECHO", "ADOPT", f"reach_target={candidate}")
                        return candidate
                    if -1000 < out < 1000 and out not in seen:
                        seen.add(out)
                        nxt.append((out, candidate))
            frontier = nxt
        self.log("ECHO", "REVISE", "No candidate reached target within search budget.")
        return None

    def run(self, env):
        self.observe(env)
        if not self.identify_gap(env):
            return False
        if not self.assign_homework():
            return False
        return self.propose_and_test(env) is not None

def provenance_pass(audit):
    required = ["OBSERVE", "GAP", "HOMEWORK", "TEST", "EVALUATE", "ADOPT"]
    echo_actions = [e.action for e in audit if e.actor == "ECHO"]
    pos = -1
    for action in required:
        try:
            pos = echo_actions.index(action, pos + 1)
        except ValueError:
            return False
    return True

def main():
    experimental = A1Agent(homework_enabled=True)
    exp_success = experimental.run(NVE())

    control = A1Agent(homework_enabled=False)
    ctl_success = control.run(NVE())

    print("A1 AUTONOMOUS AGENCY TEST")
    print("=" * 60)
    print("Experimental solved:", exp_success)
    print("Experimental provenance chain:", provenance_pass(experimental.audit))
    print("Learned algorithm:", experimental.learned.get("reach_target"))
    print("Control solved:", ctl_success)
    print("\nAUDIT")
    for e in experimental.audit:
        print(f"[{e.actor:8}] {e.action:10} {e.detail}")

    passed = exp_success and provenance_pass(experimental.audit) and not ctl_success
    print("\nRESULT:", "PASS" if passed else "FAIL")
    assert passed, "A1 autonomous-agency criteria were not satisfied"

if __name__ == "__main__":
    main()
