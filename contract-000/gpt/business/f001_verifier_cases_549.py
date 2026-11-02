#!/usr/bin/env python3
"""F-001 offline verifier test harness candidate. UNEXECUTED.
Run only after confirming Issue #224's prospective protocol; post actual observations there.
No network, payments, publication, CI, or external paths are touched.
"""
import hashlib
import pathlib
import subprocess
import sys
import tempfile

REQUIRED = ["README.txt","checkout-path.txt","checkout-head.txt","start-utc.txt",
"end-utc.txt","verdict.txt","orchestrator-exit-status.txt","preflight.stdout",
"preflight.stderr","preflight-exit-status.txt"]

def make_case(root):
    for name in REQUIRED:
        (root/name).write_text("synthetic fixture\n",encoding="utf-8")
    manifest(root)

def manifest(root):
    lines=[]
    for p in sorted(root.iterdir()):
        if p.name=="SHA256SUMS" or not p.is_file() or p.is_symlink(): continue
        lines.append(hashlib.sha256(p.read_bytes()).hexdigest()+"  "+p.name)
    (root/"SHA256SUMS").write_text("\n".join(lines)+"\n",encoding="utf-8")

def run(verifier, root):
    p=subprocess.run([sys.executable,str(verifier),str(root)],capture_output=True,text=True)
    return p.returncode,p.stdout,p.stderr

def main():
    if len(sys.argv)!=2:
        print("usage: python f001_verifier_cases_549.py /absolute/path/to/f001_evidence_manifest_verify_547.py",file=sys.stderr)
        return 2
    verifier=pathlib.Path(sys.argv[1]).resolve(strict=True)
    if not verifier.is_file(): return 2
    cases=["valid","modified","missing","duplicate","extra_symlink","extra_directory"]
    failures=0
    with tempfile.TemporaryDirectory(prefix="f001-synthetic-") as tmp:
        for case in cases:
            root=pathlib.Path(tmp)/case
            root.mkdir()
            make_case(root)
            if case=="modified": (root/"README.txt").write_text("tampered")
            elif case=="missing": (root/"README.txt").unlink()
            elif case=="duplicate":
                with (root/"SHA256SUMS").open("a") as f:
                    f.write((root/"SHA256SUMS").read_text().splitlines()[0]+"\n")
            elif case=="extra_symlink": (root/"unexpected-link").symlink_to(root/"README.txt")
            elif case=="extra_directory": (root/"unexpected-dir").mkdir()
            code,out,err=run(verifier,root)
            expected=0 if case=="valid" else "nonzero"
            passed=(code==0) if case=="valid" else (code!=0)
            failures+=not passed
            print(f"{case}: {'PASS' if passed else 'FAIL'} expected={expected} actual={code}")
            print("stdout="+repr(out)+" stderr="+repr(err))
    print(f"synthetic_cases={len(cases)} failures={failures}; NOT an authenticity or release test")
    return 1 if failures else 0

if __name__=="__main__":
    sys.exit(main())
