#!/usr/bin/env python3
"""Run 355 synthetic closure-only tests, pre-registered Issue #53 comment 6402533147.

The Run 354 digest verifier is intentionally STUBBED here: these cases test
only the new closure boundary and delegation, NOT real digest integration.
"""
import importlib.util
import json
import os
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("closure355", HERE / "F-001-BUNDLE-CLOSURE-355.py")
closure = importlib.util.module_from_spec(spec)
spec.loader.exec_module(closure)

class Stub:
    def __init__(self, fn):
        self.fn = fn
    def verify(self, root, pin):
        return self.fn(root, pin)

def good(root, pin):
    return {"result":"BYTE_CONSISTENT_ONLY", "release":"HOLD",
            "publication_authorized":False,"files_hashed":11,
            "manifest_sha256":pin}

def ready(root, pin):
    r = good(root, pin)
    r["release"] = "READY"
    return r

def error(root, pin):
    raise ValueError("stub simulated wrong manifest pin")

def change(root, pin):
    (Path(root)/"ebook.epub").write_bytes(b"changed")
    return good(root, pin)

cases = ("valid_stub", "extra_hidden", "extra_regular", "extra_directory",
         "symlink_expected", "hardlink_expected", "missing_expected",
         "symlink_root", "fifo_expected", "ready_stub", "pin_error_stub",
         "changed_during_stub")
results = []
for name in cases:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)/"bundle"
        root.mkdir()
        for filename in closure.EXPECTED:
            (root/filename).write_bytes(b"synthetic")
        target = root
        fn = good
        if name == "extra_hidden": (root/".unlisted").write_bytes(b"x")
        if name == "extra_regular": (root/"other.txt").write_bytes(b"x")
        if name == "extra_directory": (root/"extras").mkdir()
        if name == "symlink_expected":
            (root/"ebook.epub").unlink()
            (root/"ebook.epub").symlink_to(root/"ebook.pdf")
        if name == "hardlink_expected":
            (root/"ebook.epub").unlink()
            os.link(root/"ebook.pdf",root/"ebook.epub")
        if name == "missing_expected": (root/"rights.json").unlink()
        if name == "symlink_root":
            target = Path(td)/"link"
            target.symlink_to(root, target_is_directory=True)
        if name == "fifo_expected":
            (root/"ebook.epub").unlink()
            os.mkfifo(root/"ebook.epub")
        if name == "ready_stub": fn = ready
        if name == "pin_error_stub": fn = error
        if name == "changed_during_stub": fn = change
        closure.load_base = lambda fn=fn: Stub(fn)
        try:
            result = closure.verify(str(target),"a"*64)
            accepted = result["result"] == "CLOSED_BYTE_CONSISTENT_ONLY" and result["release"] == "HOLD" and result["publication_authorized"] is False
        except (OSError,ValueError,TypeError,UnicodeError,AttributeError):
            accepted = False
        passed = accepted == (name == "valid_stub")
        results.append({"case":name,"passed":passed,"accepted":accepted})
print(json.dumps({"project":"F-001","scope":"CLOSURE_ONLY_BASE_VERIFIER_STUBBED",
                  "passed":sum(x["passed"] for x in results),"total":len(results),
                  "results":results},sort_keys=True))
raise SystemExit(0 if all(x["passed"] for x in results) else 1)
