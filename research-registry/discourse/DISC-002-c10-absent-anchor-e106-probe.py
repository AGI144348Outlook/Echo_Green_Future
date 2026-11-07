"""DISC-002 E106 probe: control row C10 (anchor() on a matrix without A-000).

PRE-REGISTERED 2026-11-07 08Z by Claude. Committed BEFORE any execution.
Not run in the run that committed it; the first execution is the next run's,
against this exact blob.

Target: genesis-documentary:src/echo_governor_skeleton.py, git blob 63eb982
(unmodified). Pass the path to a checkout of that exact blob as argv[1].
Run: python3 -I -B DISC-002-c10-absent-anchor-e106-probe.py <skeleton.py>

Required behaviour (C10, PROPOSED, DISC-002 (nnnn)): anchor() must refuse
when A-000 is absent, not mint an entry. Predicted from source (INFERRED,
lines 3258-3263 and 3296-3302): FAIL, i.e. anchor() mints an A-000 holding
only the four identity_* keys, with no name and no status, and validate()
returns True.

Observables printed (one per line, key=value), then the sha256 of them:
  c10.blob_sha1          git blob sha1 of argv[1] (must be 63eb982...)
  c10.pre_has_a000       A-000 in known before anchor (expected False)
  c10.post_has_a000      A-000 in known after anchor
  c10.post_a000_keys     sorted keys of the post-anchor A-000
  c10.post_has_name      'name' in post-anchor A-000
  c10.post_has_status    'status' in post-anchor A-000
  c10.validate           ReshIdentity.validate() after anchor
  c10.raised             exception class name raised by anchor(), or none
  c10.outcome            PASS if anchor raised or left A-000 absent and
                         validate() False; else FAIL
  ctl.present_validate   control: unmodified matrix, A-000 present,
                         validate() after anchor (expected True)
  ctl.present_kept_name  control: 'name' still in A-000 (expected True)
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


def main():
    path = sys.argv[1]
    out = [("c10.blob_sha1", blob_sha1(path))]
    g = load(path)

    m = g.AlgorithmMatrix()
    del m.known["A-000"]
    out.append(("c10.pre_has_a000", "A-000" in m.known))
    r = g.ReshIdentity(m)
    raised = "none"
    try:
        r.anchor()
    except Exception as e:  # observed, not a pass by itself
        raised = type(e).__name__
    a = m.known.get("A-000")
    out.append(("c10.post_has_a000", a is not None))
    out.append(("c10.post_a000_keys", ",".join(sorted(a)) if a else "-"))
    out.append(("c10.post_has_name", bool(a) and "name" in a))
    out.append(("c10.post_has_status", bool(a) and "status" in a))
    v = r.validate()
    out.append(("c10.validate", v))
    out.append(("c10.raised", raised))
    refused = raised != "none" or a is None
    out.append(("c10.outcome", "PASS" if (refused and not v) else "FAIL"))

    m2 = g.AlgorithmMatrix()
    r2 = g.ReshIdentity(m2)
    r2.anchor()
    out.append(("ctl.present_validate", r2.validate()))
    out.append(("ctl.present_kept_name", "name" in m2.known["A-000"]))

    text = "".join("%s=%s\n" % kv for kv in out)
    sys.stdout.write(text)
    sys.stdout.write("sha256=%s\n" % hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()
