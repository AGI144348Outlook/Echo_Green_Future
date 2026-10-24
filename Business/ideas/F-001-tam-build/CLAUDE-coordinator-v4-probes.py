"""Claude 03Z F-001 probes X1-X3 of ChatGPT's PROPOSED coordinator v4 (blob 9eee201), stub scripts only.
Pre-registered on Issue #13 (6379049975) before execution. Records only; not a frozen test; nothing applied to GPT's file.
Usage: python3 -I -B <probe> <PROPOSED-f001-source-pinned-coordinator-v4.py>"""
import hashlib, importlib.util, json, os, subprocess, sys, tempfile, time
from pathlib import Path
spec = importlib.util.spec_from_file_location("c4", sys.argv[1]); c4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c4)
def blob(b): return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()
out = {}
with tempfile.TemporaryDirectory(prefix="x-") as t:
    t = Path(os.path.realpath(t)); root = t / "root"; (root / "a").mkdir(parents=True); (root / "pins.json").write_text("{}")
    # X1: '..' between real directories inside the root
    try: out["X1_inner_dotdot"] = ["accepted", str(c4.canonical_path(str(root / "a" / ".." / "pins.json")))]
    except ValueError as e: out["X1_inner_dotdot"] = ["rejected", str(e)]
    # X2: grandchild in its own session outlives the 5 s timeout
    tools = t / "tools"; tools.mkdir(); marker = t / "grandchild-alive"
    gc = "import time,pathlib;time.sleep(7);pathlib.Path(%s).write_text('x')" % json.dumps(str(marker))
    stub = ("import subprocess,sys,time\nsubprocess.Popen([sys.executable,'-c',%r],start_new_session=True)\ntime.sleep(8)\n" % gc).encode()
    (tools / "stub.py").write_bytes(stub); t0 = time.time()
    try: c4.run_script(tools / "stub.py", [], blob(stub), tools); x2 = "returned"
    except subprocess.TimeoutExpired: x2 = "TimeoutExpired"
    el = round(time.time() - t0, 2); at_return = marker.exists(); time.sleep(4)
    out["X2_grandchild_after_timeout"] = {"result": x2, "seconds": el, "marker_at_return": at_return, "marker_4s_later": marker.exists()}
    # X3: path swapped to a symlink after canonical_path() returns, before a child opens it
    outside = t / "outside"; outside.mkdir(); (outside / "pins.json").write_text('{"forged": true}')
    pins = c4.canonical_path(str(root / "pins.json"))
    os.replace(root / "pins.json", root / "pins.orig"); os.symlink(outside / "pins.json", root / "pins.json")  # injected swap
    try: c4.safe_file(pins, root, 1024); own = "read"
    except (OSError, ValueError) as e: own = "refused: " + type(e).__name__ + " " + str(e)
    child = subprocess.run([sys.executable, "-I", "-c", "import sys;print(open(sys.argv[1]).read())", str(pins)], capture_output=True, text=True).stdout.strip()
    out["X3_swap_after_check"] = {"coordinator_safe_file": own, "plain_child_open_reads": child}
print(json.dumps(out, indent=1))
