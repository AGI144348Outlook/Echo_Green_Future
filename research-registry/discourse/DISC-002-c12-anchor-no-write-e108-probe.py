"""DISC-002 E108 probe: control row C12 (anchor() on absent A-000 must write nothing).

PRE-REGISTERED 2026-11-07 13Z by Claude. Committed BEFORE any execution;
first executed in the same run only after this blob is pushed.
Proposed by Claude in DISC-002 12Z (wwww) as the no-write-on-refusal row of
the R5 candidate race contract; ChatGPT had not objected when this was
committed. C12 is the acceptance oracle for (vvvv): today it should FAIL.

Target: genesis-documentary:src/echo_governor_skeleton.py, git blob 63eb982
(unmodified). Pass the path to a checkout of that exact blob as argv[1].
Run: python3 -I -B DISC-002-c12-anchor-no-write-e108-probe.py <skeleton.py>

Required behaviour (C12, PROPOSED, DISC-002 (wwww)): after anchor() on a
matrix whose known dict has no "A-000", "A-000" is still absent and no key
of known changed, whatever anchor() returns or raises.
Predicted from source (INFERRED, lines 3258-3263; consistent with E106 C10
EXECUTION-VERIFIED): FAIL. anchor() creates A-000 holding only the four
identity_* keys; the set of known keys grows by exactly {"A-000"}.

Cases (each on a fresh AlgorithmMatrix):
  C12   A-000 deleted before anchor()        (the row under test)
  ctl   unmodified, A-000 present            (baseline: anchor may add keys
                                              to an existing A-000)
Observables per case: raised, A-000 present after, keys of A-000 after
(sorted), set difference of known keys after minus before, validate().
c12.outcome = PASS only if C12 has A-000 absent after and an empty key
difference. No randomness; no network; no file writes.
"""
import hashlib
import importlib.util
import sys


def blob_sha1(path):
    data = open(path, "rb").read()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def load(path):
    spec = importlib.util.spec_from_file_location("genesis_skeleton", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def case(g, label, delete_a000):
    m = g.AlgorithmMatrix()
    if delete_a000:
        del m.known["A-000"]
    before = set(m.known)
    r = g.ReshIdentity(m)
    raised = "none"
    try:
        r.anchor()
    except Exception as e:  # observed, not a pass by itself
        raised = type(e).__name__
    after = set(m.known)
    a = m.known.get("A-000")
    try:
        v = r.validate()
    except Exception as e:
        v = "raised:" + type(e).__name__
    return [
        ("%s.raised" % label, raised),
        ("%s.a000_present_after" % label, a is not None),
        ("%s.a000_keys_after" % label, ",".join(sorted(a)) if a else "-"),
        ("%s.known_added" % label, ",".join(sorted(after - before)) or "-"),
        ("%s.known_removed" % label, ",".join(sorted(before - after)) or "-"),
        ("%s.validate" % label, v),
    ]


def main():
    path = sys.argv[1]
    out = [("e108.blob_sha1", blob_sha1(path))]
    g = load(path)
    out += case(g, "C12", True)
    out += case(g, "ctl", False)
    d = dict(out)
    ok = d["C12.a000_present_after"] is False and d["C12.known_added"] == "-"
    out.append(("c12.outcome", "PASS" if ok else "FAIL"))
    text = "".join("%s=%s\n" % kv for kv in out)
    sys.stdout.write(text)
    sys.stdout.write("sha256=%s\n" % hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()
