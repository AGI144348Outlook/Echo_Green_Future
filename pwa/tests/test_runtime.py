"""Runtime tests that run in plain CPython (for GitHub Actions): python -m pytest tests"""
import json
from echo.bootstrap import boot as B


def setup_module():
    B.boot("{}")


def snap(*words):
    return json.dumps({"manifestations": [{"id": f"m{i}", "word": w, "x": 100 * i, "y": 300, "actor": "user"}
                                          for i, w in enumerate(words)], "relations": [], "selection": []})


def test_kernel_is_the_repository_skeleton():
    ident = json.loads(B.boot("{}"))["identity"]
    assert ident["kernel lines"] > 9000 and ident["letter operators"] == 22


def test_echo_reacts_with_hypernym_and_relation():
    r = json.loads(B.on_presentiate(snap("dog"), "m0"))
    ops = [(o["actor"], o["op"], o["args"].get("word")) for o in r["ops"]]
    assert ("echo", "PRESENTIATE", "canine") in ops and any(o[1] == "RELATE" for o in ops)
    assert "A dog is a canine." in r["outputs"][0]["text"]


def test_canonical_identity_cannot_be_rewritten():
    r = json.loads(B.handle("teach dog is-a cat"))
    assert r["outputs"][0]["kind"] == "error"


def test_overlay_teach_and_resolve():
    json.loads(B.handle("teach corgi is-a dog"))
    r = json.loads(B.handle("resolve corgi"))
    assert ["source", "local-overlay"] in r["outputs"][0]["rows"]


def test_common_hypernym_of_selection():
    s = json.loads(snap("dog", "cat", "horse")); s["selection"] = ["m0", "m1", "m2"]
    r = json.loads(B.handle("selection", "QUERY", json.dumps(s)))
    assert r["outputs"][0]["rows"][0][0] == "mammal"


def test_a174_reports_fixed_points_separately():
    r = json.loads(B.handle("invariant echo"))
    rows = dict((k, v) for k, v in r["outputs"][0]["rows"])
    assert rows["letter set fixed"] == "True" and rows["strict involution fixed"] == "False"


def test_governor_cycle_runs():
    r = json.loads(B.handle("cycle"))
    assert r["outputs"][0]["kind"] == "matrix"


def test_echo_cannot_move_user_presentiation():
    from echo.bootstrap.boot import _rt
    s = json.loads(snap("dog"))
    op = {"actor": "echo", "op": "MOVE", "target": "m0", "args": {}}
    assert _rt.actor.validate(op, s) is False
