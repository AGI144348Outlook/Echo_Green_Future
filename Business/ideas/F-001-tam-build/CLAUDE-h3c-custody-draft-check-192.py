#!/usr/bin/env python3
"""F-001 §192 (Claude 16Z, 2026-11-05): Claude-side observation run of
ChatGPT's UNTESTED draft f001_h3c_custody_draft_1500.py (blob db81321 on
contract-000-gpt-run1500-20261105 @ 912de08). Not ChatGPT's preregistered
test and not a replacement for it; it only records what the draft prints
for each fixture class. Builds fixtures in a fresh temporary directory,
never touches the repository or the network.

Usage: python3 -I CLAUDE-h3c-custody-draft-check-192.py path/to/f001_h3c_custody_draft_1500.py
"""
import hashlib, json, os, shutil, subprocess, sys, tempfile

draft = os.path.abspath(sys.argv[1])
with open(draft, "rb") as f:
    DRAFT_BYTES = f.read()
if not DRAFT_BYTES:  # an empty file "passes" with rc 0 and no output; refuse it
    sys.exit("refusing: draft file is empty")
DRAFT_SHA256 = hashlib.sha256(DRAFT_BYTES).hexdigest()
DATA = b"TAM source fixture bytes\n"
H = hashlib.sha256(DATA).hexdigest()
COMMIT = "d46456a" + "0" * 33  # fixture value, 40 lowercase hex; not a real pin
OK = {"editorial_approved": True, "rights_approved": True, "owner_release_authorized": True}

def case(name, files, approvals=OK, setup=None, commit=COMMIT, root_name="src"):
    t = tempfile.mkdtemp(prefix="h3c192-")
    try:
        src = os.path.join(t, "src"); os.makedirs(os.path.join(src, "ch"))
        with open(os.path.join(src, "ch", "a.md"), "wb") as f: f.write(DATA)
        if setup: setup(t, src)
        man = dict(source_commit=commit, files=files, **approvals)
        mp = os.path.join(t, "m.json")
        with open(mp, "w") as f: json.dump(man, f)
        p = subprocess.run([sys.executable, "-I", draft, mp, os.path.join(t, root_name)],
                           capture_output=True, text=True, timeout=30)
        return {"case": name, "rc": p.returncode, "out": p.stdout.strip(), "err": p.stderr.strip()[-120:]}
    finally:
        shutil.rmtree(t)

good = [{"path": "ch/a.md", "sha256": H, "size": len(DATA)}]
def sym_last(t, s): os.symlink("a.md", os.path.join(s, "ch", "b.md"))
def sym_dir(t, s): os.symlink("ch", os.path.join(s, "cl"))
def sym_root(t, s): os.symlink("src", os.path.join(t, "srclink"))
def fifo(t, s): os.mkfifo(os.path.join(s, "ch", "p"))

rows = [
    case("C01 valid, all approvals", good),
    case("C02 valid, approvals missing", good, approvals={}),
    case("C03 mutated bytes (wrong sha256)", [{"path": "ch/a.md", "sha256": "0" * 64, "size": len(DATA)}]),
    case("C04 wrong size", [{"path": "ch/a.md", "sha256": H, "size": len(DATA) + 1}]),
    case("C05 traversal ..", [{"path": "../src/ch/a.md", "sha256": H, "size": len(DATA)}]),
    case("C06 absolute path", [{"path": "/etc/hostname", "sha256": H, "size": len(DATA)}]),
    case("C07 duplicate path", good + good),
    case("C08 symlink last component", [{"path": "ch/b.md", "sha256": H, "size": len(DATA)}], setup=sym_last),
    case("C09 symlink directory component", [{"path": "cl/a.md", "sha256": H, "size": len(DATA)}], setup=sym_dir),
    case("C10 root is a symlink", good, setup=sym_root, root_name="srclink"),
    case("C11 fifo (non-regular)", [{"path": "ch/p", "sha256": H, "size": 0}], setup=fifo),
    case("C12 missing file", [{"path": "ch/zz.md", "sha256": H, "size": 1}]),
    case("C13 bad source commit", good, commit="HEAD"),
    case("C14 empty file list", []),
]
for r in rows:
    print(json.dumps(r, sort_keys=True))
print(json.dumps({"draft_sha256": DRAFT_SHA256, "rc_values": sorted({r["rc"] for r in rows}),
                  "rows_sha256": hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()}, sort_keys=True))
