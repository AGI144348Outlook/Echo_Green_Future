"""Claude 19Z F-001 probes R1-R4 against GPT receipt verifier v1 (blob 696e66f). Synthetic fixture only."""
import importlib.util, json, subprocess, sys, tempfile, hashlib
from pathlib import Path
D = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("h", D / "PROPOSED-f001-test-receipt-v1.py")
h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
V = D / "PROPOSED-f001-receipt-verify-v1.py"

def run(name, edit):
    with tempfile.TemporaryDirectory() as t:
        root = Path(t) / "out"; root.mkdir()
        pin, rec = h.fixture(root)
        edit(root, pin, rec)
        (Path(t) / "pins.json").write_text(json.dumps(pin)); (Path(t) / "rec.json").write_text(json.dumps(rec))
        p = subprocess.run([sys.executable, "-I", "-B", str(V), "--pins", str(Path(t)/"pins.json"),
                            "--receipt", str(Path(t)/"rec.json"), "--artifact-root", str(root)],
                           capture_output=True, text=True, timeout=10)
        o = json.loads(p.stdout)
        print(json.dumps({"case": name, "exit": p.returncode, "integrity": o["integrity"], "release": o["release"],
                          "authenticated": o["source_pin_authenticated"] or o["approval_authenticated"], "issues": o["issues"]}))

def r1(root, pin, rec): rec["editorial"]["status"] = "NO_FLAGGED_ROWS"
def r2(root, pin, rec): rec["editorial"]["flagged_csv_lines"] = [6.0, 7.0]
def r3(root, pin, rec):
    lines = (root / "dataset_a_csv.bin").read_bytes().splitlines()
    print("# R3 dataset_a lines:", len(lines))
def r4(root, pin, rec):
    b = b"x"; (root / "epub.bin").write_bytes(b)
    pin["artifacts"]["epub"] = {"sha256": hashlib.sha256(b).hexdigest(), "size": 1}
    rec["artifacts"]["epub"] = {"path": "epub.bin", "sha256": hashlib.sha256(b).hexdigest(), "size": True}
for n, f in (("R1", r1), ("R2", r2), ("R3", r3), ("R4", r4)): run(n, f)
