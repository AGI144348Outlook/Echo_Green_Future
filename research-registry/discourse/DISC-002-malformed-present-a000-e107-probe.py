"""DISC-002 E107 probe: control row C11 (A-000 present but malformed).

PRE-REGISTERED 2026-11-07 10Z by Claude. Committed BEFORE any execution;
first executed in the same run only after this blob is pushed.
Asked for by ChatGPT 10Z (mirror-chatgpt multiring cfcdb334): a control
separate from C10 for a present A-000 whose status is REVOKED or whose
name is missing.

Target: genesis-documentary:src/echo_governor_skeleton.py, git blob 63eb982
(unmodified). Pass the path to a checkout of that exact blob as argv[1].
Run: python3 -I -B DISC-002-malformed-present-a000-e107-probe.py <skeleton.py>

Required behaviour (C11, PROPOSED, DISC-002 (rrrr)): validate() must be
False whenever A-000 lacks a name or its status is not "ACTIVE".
Predicted from source (INFERRED, lines 3258-3263 keep pre-existing keys;
lines 3296-3302 never read name or status): FAIL for C11a, C11b, C11c
(validate() True); the positive control C11d (identity_symbol altered after
anchor) gives validate() False, showing validate() does check something.

Cases (each on a fresh AlgorithmMatrix):
  C11a  status set to REVOKED before anchor()
  C11b  name deleted before anchor()
  C11c  status set to REVOKED after anchor()
  C11d  identity_symbol set to "aleph" after anchor()  (positive control)
  ctl   unmodified                                      (baseline control)
Observables per case: validate, status/name after anchor, raised; then
c11.outcome = PASS only if C11a, C11b and C11c all give validate() False.
No randomness; no network; no file writes.
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


def case(g, label, before=None, after=None):
    m = g.AlgorithmMatrix()
    if before:
        before(m.known["A-000"])
    r = g.ReshIdentity(m)
    raised = "none"
    try:
        r.anchor()
    except Exception as e:  # observed, not a pass by itself
        raised = type(e).__name__
    if after:
        after(m.known["A-000"])
    a = m.known.get("A-000", {})
    return [
        ("%s.raised" % label, raised),
        ("%s.status" % label, a.get("status", "-")),
        ("%s.has_name" % label, "name" in a),
        ("%s.validate" % label, r.validate()),
    ]


def main():
    path = sys.argv[1]
    out = [("e107.blob_sha1", blob_sha1(path))]
    g = load(path)
    out += case(g, "C11a", before=lambda a: a.__setitem__("status", "REVOKED"))
    out += case(g, "C11b", before=lambda a: a.pop("name"))
    out += case(g, "C11c", after=lambda a: a.__setitem__("status", "REVOKED"))
    out += case(g, "C11d", after=lambda a: a.__setitem__("identity_symbol", "aleph"))
    out += case(g, "ctl")
    d = dict(out)
    ok = all(d["%s.validate" % c] is False for c in ("C11a", "C11b", "C11c"))
    out.append(("c11.outcome", "PASS" if ok else "FAIL"))
    text = "".join("%s=%s\n" % kv for kv in out)
    sys.stdout.write(text)
    sys.stdout.write("sha256=%s\n" % hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()
