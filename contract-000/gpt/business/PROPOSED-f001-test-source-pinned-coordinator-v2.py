"""Synthetic characterization of proposed F-001 coordinator v2; HOLD only."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import time

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("coordinator", HERE / "PROPOSED-f001-source-pinned-coordinator-v2.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def stub(status="PASS", release="HOLD", delay=0, malformed=False, large=False):
    if delay:
        return "import time; time.sleep(8)\n"
    if large:
        return "print('x' * 1100000)\n"
    if malformed:
        return "print('{broken')\n"
    return "import json\nprint(json.dumps(" + repr({
        "integrity": status, "release": release,
        "source_pin_authenticated": False, "approval_authenticated": False,
        "publication_authorization": "ABSENT"}) + "))\n"


def run_case(name, change=None, expected=True):
    with tempfile.TemporaryDirectory(prefix="f001-coord-test-") as tmp:
        root = Path(tmp) / "artifacts"; root.mkdir()
        tools = Path(tmp) / "tools"; tools.mkdir()
        scripts = {}
        for key in mod.FIXED_BLOBS:
            path = tools / (key + ".py")
            path.write_text(stub())
            scripts[key] = path
        pins = root / "pins.json"
        receipt = root / "receipt.json"
        manifest = root / "binding.json"
        csv = root / "dataset-a.csv"; csv.write_text("test,fixture\n")
        report = root / "v5-report.json"; report.write_text("{}")
        record = root / "editorial.json"  # intentionally absent; pending editorial review
        pins.write_text(json.dumps({"artifacts": {"dataset_a_csv": {"sha256": hashlib.sha256(csv.read_bytes()).hexdigest()}}}))
        receipt.write_text(json.dumps({"artifacts": {"dataset_a_csv": {"path": "dataset-a.csv"}}}))
        manifest.write_text(json.dumps({"v5_report_sha256": hashlib.sha256(report.read_bytes()).hexdigest()}))
        args = argparse.Namespace(artifact_root=str(root), tool_root=str(tools), pins=str(pins),
                                  receipt=str(receipt), binding_manifest=str(manifest),
                                  v5_report=str(report), disposition_record=str(record),
                                  **{key: str(path) for key, path in scripts.items()})
        expected_blobs = {key: mod.git_blob(path.read_bytes()) for key, path in scripts.items()}
        cleanup = change(args, root, tools, scripts, expected_blobs) if change else None
        before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob("*") if p.is_file() and not p.is_symlink()}
        started = time.monotonic()
        try:
            result = mod.coordinate(args, expected_blobs=expected_blobs)
        finally:
            if cleanup:
                cleanup()
        elapsed = time.monotonic() - started
        after = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob("*") if p.is_file() and not p.is_symlink()}
        assert before == after, (name, "input mutation")
        assert result["integrity"] == ("PASS" if expected else "FAIL"), (name, result)
        assert result["release"] == "HOLD" and result["source_pin_authenticated"] is False
        assert result["approval_authenticated"] is False and result["publication_authorization"] == "ABSENT"
        assert elapsed < 7, (name, elapsed)
        return {"case": name, "integrity": result["integrity"], "release": result["release"],
                "elapsed_seconds": round(elapsed, 3), "issues": result["issues"]}


def ancestor_symlink(a,r,t,s,b):
    alias = r.parent / "alias"
    alias.symlink_to(r.parent, target_is_directory=True)
    a.artifact_root = str(alias / "artifacts")
    a.tool_root = str(alias / "tools")
    for key in ("pins", "receipt", "binding_manifest", "v5_report", "disposition_record"):
        a.__dict__[key] = str(alias / "artifacts" / Path(getattr(a,key)).name)
    for key in mod.FIXED_BLOBS:
        a.__dict__[key] = str(alias / "tools" / s[key].name)

def swapped_after_first_hash(a,r,t,s,b):
    original = mod.safe_file
    state = {"fired": False}
    def hook(path, root, limit, missing_ok=False):
        data = original(path, root, limit, missing_ok)
        if Path(path) == s["receipt_v3"] and not state["fired"]:
            s["receipt_v3"].write_text(stub(release="READY"))
            state["fired"] = True
        return data
    mod.safe_file = hook
    return lambda: setattr(mod, "safe_file", original)

def run_snapshot_case():
    with tempfile.TemporaryDirectory(prefix="f001-snapshot-") as tmp:
        root = Path(tmp)
        script = root / "reviewed.py"
        script.write_text(stub())
        blob = mod.git_blob(script.read_bytes())
        original = mod.safe_file
        def hook(path, toolroot, limit, missing_ok=False):
            data = original(path, toolroot, limit, missing_ok)
            script.write_text(stub(release="READY"))
            return data
        mod.safe_file = hook
        try:
            rc, report = mod.run_script(script, [], blob, root)
        finally:
            mod.safe_file = original
        assert rc == 0 and report["integrity"] == "PASS" and report["release"] == "HOLD", report
        assert "READY" in script.read_text()
        return {"case": "checked_byte_snapshot_survives_original_swap", "integrity": report["integrity"], "release": report["release"], "issues": []}

def wrong_blob(a,r,t,s,b): s["v5_gate"].write_text("# modified\n")
def symlink(a,r,t,s,b):
    (r/"pins.json").rename(r/"real-pins.json"); (r/"pins.json").symlink_to("real-pins.json")
def escape(a,r,t,s,b):
    a.pins = str(r.parent / "escape.json")
def upstream_fail(a,r,t,s,b):
    s["receipt_v3"].write_text(stub(status="FAIL")); b["receipt_v3"] = mod.git_blob(s["receipt_v3"].read_bytes())
def forged_ready(a,r,t,s,b):
    s["v4_binding"].write_text(stub(release="READY")); b["v4_binding"] = mod.git_blob(s["v4_binding"].read_bytes())
def malformed(a,r,t,s,b):
    s["v5_gate"].write_text(stub(malformed=True)); b["v5_gate"] = mod.git_blob(s["v5_gate"].read_bytes())
def timeout(a,r,t,s,b):
    s["v5_gate"].write_text(stub(delay=8)); b["v5_gate"] = mod.git_blob(s["v5_gate"].read_bytes())
def oversized(a,r,t,s,b):
    s["v5_gate"].write_text(stub(large=True)); b["v5_gate"] = mod.git_blob(s["v5_gate"].read_bytes())
def missing(a,r,t,s,b): (r/"v5-report.json").unlink()

CASES = [("consistent_synthetic", None, True), ("wrong_script_blob", wrong_blob, False),
         ("symlink_input", symlink, False), ("escaping_path", escape, False),
         ("upstream_fail", upstream_fail, False), ("forged_READY", forged_ready, False),
         ("malformed_json", malformed, False), ("subprocess_timeout", timeout, False),
         ("oversized_output", oversized, False), ("missing_input", missing, False),
         ("ancestor_symlink", ancestor_symlink, False),
         ("swapped_after_preflight", swapped_after_first_hash, False)]

if __name__ == "__main__":
    results = [run_case(*case) for case in CASES] + [run_snapshot_case()]
    (HERE / "RUN-310-TEST-RESULTS.json").write_text(json.dumps(results, indent=2))
    print(json.dumps({"expected": len(CASES) + 1, "confirmed": len(results), "cases": results}, indent=2))
