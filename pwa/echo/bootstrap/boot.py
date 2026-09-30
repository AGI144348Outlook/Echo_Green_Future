"""Boot and JSON entry points for the JavaScript bridge.

The bridge only ever calls the functions at the bottom of this file, passing
and receiving JSON strings, so the JS/Python boundary stays one narrow seam.
"""
import json
import random
import time

from .. import __version__
from ..kernel import (AlgorithmMatrix, State, Request, Context, run_cycle,
                      HEBREW_LETTER_INDEX, kernel_lines)
from ..matrix.registry import Registry
from ..canvas.actor import EchoActor
from ..mcw.client import Outbox


class Runtime:
    def __init__(self, instance_id=None, overlay=None):
        self.instance_id = instance_id or f"nve-{random.getrandbits(32):08x}"
        self.booted_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.matrix = AlgorithmMatrix()
        self.registry = Registry(kernel_matrix=self.matrix)
        self.registry.load_overlay(overlay or {})
        self.outbox = Outbox(self.instance_id)
        self.actor = EchoActor(self.registry, self)
        self.theta = {}
        self.state = State(content="", quality=0.0)
        self.cycles = 0

    def identify(self):
        return {
            "identity": "\u05e8 ECHO \u00b7 A-000 Governor",
            "runtime": f"echo {__version__} (Pyodide)",
            "instance": self.instance_id,
            "kernel lines": kernel_lines(),
            "kernel tool belt": ", ".join(sorted(getattr(self.matrix, "known", {}).keys())) or "\u2014",
            "letter operators": len([k for k in HEBREW_LETTER_INDEX if "sofit" not in k]),
            "canonical residents": len(self.registry.canonical),
            "overlay residents": len(self.registry.overlay),
            "indexed into kernel": self.registry.kernel_indexed,
            "governor cycles run": self.cycles,
            "booted": self.booted_at,
        }

    def cycle(self, text):
        """One real Governor cycle through the kernel's run_cycle."""
        r = Request(text=text, value=1.0)
        c = Context(value=0.5)
        invariants = [{"id": "I-001", "check": lambda st: st.quality < 100}]
        thresholds = {"epsilon_max": 0.1, "delta_max": 5.0, "C_max": 50, "content_sim_min": 0.9}
        budgets = {"B_G": 20, "B_E": 10, "C_max": 50, "F_max": 20}
        before = self.state.quality
        self.state = run_cycle(self.theta, self.state, r, c, self.matrix, invariants, budgets, thresholds)
        self.cycles += 1
        return {"cycle": self.cycles, "input": text, "quality before": round(before, 3),
                "quality after": round(self.state.quality, 3),
                "content": (self.state.content or "")[:120],
                "note": "Propose is still a single no-op candidate in the kernel (M-000-NOOP)."}


_rt = None


def _snap(s):
    try:
        return json.loads(s) if s else {}
    except ValueError:
        return {}


def boot(config_json="{}"):
    global _rt
    cfg = _snap(config_json)
    _rt = Runtime(instance_id=cfg.get("instance_id"), overlay=cfg.get("overlay"))
    return json.dumps({"ok": True, "identity": _rt.identify(), "instance_id": _rt.instance_id})


def handle(text, mode="TEXT", snapshot_json="{}"):
    try:
        return json.dumps(_rt.actor.handle(text, mode, _snap(snapshot_json)))
    except Exception as e:  # report, never crash the host
        return json.dumps({"outputs": [{"actor": "echo", "kind": "error", "text": f"{type(e).__name__}: {e}", "refs": []}], "ops": []})


def on_presentiate(snapshot_json, manifestation_id):
    try:
        return json.dumps(_rt.actor.on_presentiate(_snap(snapshot_json), manifestation_id))
    except Exception as e:
        return json.dumps({"outputs": [{"actor": "echo", "kind": "error", "text": f"{type(e).__name__}: {e}", "refs": []}], "ops": []})


def resolve(word):
    return json.dumps(_rt.registry.resolve(word))


def words():
    return json.dumps([_rt.registry.resolve(w) | {"hyponyms": [], "chain": []} for w in _rt.registry.all_words()])


def set_overlay(overlay_json="{}"):
    _rt.registry.load_overlay(_snap(overlay_json))
    return json.dumps({"ok": True, "overlay": len(_rt.registry.overlay)})
