#!/usr/bin/env python3
"""F-001 prospective #224 verifier cases; synthetic only. NOT EXECUTED.
Usage: python3 f001_verifier_cases_550.py /absolute/path/to/f001_evidence_manifest_verify_547.py
No network, CI, storefront or external data.
"""
import hashlib, os, pathlib, platform, subprocess, sys, tempfile

REQUIRED = ("README.txt", "checkout-path.txt", "checkout-head.txt",
            "start-utc.txt", "end-utc.txt", "verdict.txt",
            "orchestrator-exit-status.txt", "preflight.stdout",
            "preflight.stderr", "preflight-exit-status.txt")
CASES = ("valid", "missing_manifest", "missing_required", "extra_file",
         "omitted_entry", "duplicate_entry", "altered_digest", "symlink_artifact",
         "malformed_line", "symlink_root", "extra_symlink", "extra_directory",
         "extra_fifo", "newline_filename", "co_modified_manifest")

def manifest(root):
    lines = [hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.name
             for p in sorted(root.iterdir()) if p.is_file() and not p.is_symlink()
             and p.name != "SHA256SUMS"]
    (root / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")

def fixture(root):
    root.mkdir()
    for name in REQUIRED:
        (root / name).write_text("synthetic fixture\n", encoding="utf-8")
    manifest(root)

def mutate(case, root):
    m = root / "SHA256SUMS"
    if case == "missing_manifest": m.unlink()
    elif case == "missing_required": (root / "README.txt").unlink()
    elif case == "extra_file": (root / "extra.txt").write_text("extra")
    elif case == "omitted_entry":
        m.write_text("\n".join(x for x in m.read_text().splitlines()
                               if not x.endswith("  README.txt")) + "\n")
    elif case == "duplicate_entry":
        lines = m.read_text().splitlines()
        m.write_text("\n".join(lines + [lines[0]]) + "\n")
    elif case == "altered_digest": (root / "README.txt").write_text("tampered")
    elif case == "symlink_artifact":
        (root / "README.txt").unlink()
        (root / "README.txt").symlink_to(root / "checkout-head.txt")
    elif case == "malformed_line": m.write_text(m.read_text() + "not-a-digest\n")
    elif case == "extra_symlink": (root / "extra-link").symlink_to(root / "README.txt")
    elif case == "extra_directory": (root / "extra-dir").mkdir()
    elif case == "extra_fifo": os.mkfifo(root / "extra-fifo")
    elif case == "newline_filename": (root / "line\nbreak").write_text("extra")
    elif case == "co_modified_manifest":
        (root / "README.txt").write_text("changed artifact and manifest")
        manifest(root)

def main():
    if len(sys.argv) != 2:
        print("usage: harness /absolute/verifier.py", file=sys.stderr)
        return 2
    verifier = pathlib.Path(sys.argv[1]).resolve(strict=True)
    if not verifier.is_file():
        print("HOLD: missing verifier", file=sys.stderr)
        return 2
    print("Python:", sys.version.replace("\n", " "), "OS:", platform.platform())
    print("verifier_sha256:", hashlib.sha256(verifier.read_bytes()).hexdigest())
    failures = 0
    with tempfile.TemporaryDirectory(prefix="f001-cases-") as tmp:
        base = pathlib.Path(tmp)
        for case in CASES:
            root = base / case
            fixture(root)
            if case == "symlink_root":
                link = base / "root-link"
                link.symlink_to(root, target_is_directory=True)
                target = link
            else:
                target = root
                try:
                    mutate(case, root)
                except (OSError, NotImplementedError) as exc:
                    print(case, "SKIP platform unsupported:", repr(exc))
                    continue
            p = subprocess.run([sys.executable, str(verifier), str(target)],
                               capture_output=True, text=True)
            expected_ok = case in ("valid", "co_modified_manifest")
            observed_ok = p.returncode == 0
            pass_case = observed_ok == expected_ok
            failures += not pass_case
            print(case, "PASS" if pass_case else "FAIL",
                  "exit=", p.returncode, "expected_ok=", expected_ok,
                  "stdout=", repr(p.stdout), "stderr=", repr(p.stderr))
    print("failures=", failures, "RELEASE HOLD; internal consistency is not authenticity")
    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main())
