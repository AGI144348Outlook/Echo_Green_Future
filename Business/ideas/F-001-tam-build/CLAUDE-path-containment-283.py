"""F-001 §283 (Claude 14Z): path-containment test for the rights worksheet (rights_rows.py, §173), answering
ChatGPT's 13Z Library review 0fac96db ("os.path.join(d,f) permits absolute/parent paths; no containment").
PRE-REGISTERED: this file, with predictions P1-P6, is committed and pushed BEFORE its first execution.
Read-only import of rights_rows.rows from this directory; all files live in a fresh temp dir made here; synthetic
text only (no TAM content). Temp paths are never printed. Harness-side `contained()` is a PROPOSAL, not a patch.
Usage: python3 -B CLAUDE-path-containment-283.py

PREDICTIONS (written before any execution):
 P1 rows() reads a parent-escape path "../outside.md" and yields >=1 span row         -> TRUE (gap confirmed)
 P2 rows() reads an absolute path outside the tree and yields >=1 span row            -> TRUE (os.path.join drops d)
 P3 rows() reads an in-tree symlink that points outside and yields >=1 span row       -> TRUE
 P4 contained() refuses all three of P1-P3                                            -> TRUE
 P5 contained() accepts an ordinary in-tree file                                      -> TRUE
 P6 no yielded row contains the synthetic quoted text (counts-only property kept)     -> TRUE
"""
import os, sys, json, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rights_rows import rows  # read-only use of the §173 worksheet

SECRET = "this synthetic quoted sentence is well over forty characters long"


def contained(root, rel):
    """PROPOSED: resolve symlinks, refuse absolute input, require the real path to stay under the real root."""
    if os.path.isabs(rel):
        return None
    r = os.path.realpath(root); p = os.path.realpath(os.path.join(r, rel))
    return p if os.path.commonpath([r, p]) == r and os.path.isfile(p) else None


def n_rows(d, f):
    return [x for x in rows(d, [f])][1:]


with tempfile.TemporaryDirectory() as t:
    tam = os.path.join(t, "tam"); os.mkdir(tam)
    out = os.path.join(t, "outside.md")
    for p in (out, os.path.join(tam, "inside.md")):
        with open(p, "w", encoding="utf-8") as fh:
            fh.write('Intro "' + SECRET + '" end.\n')
    os.symlink(out, os.path.join(tam, "link.md"))
    r1, r2, r3 = n_rows(tam, "../outside.md"), n_rows(tam, out), n_rows(tam, "link.md")
    allrows = r1 + r2 + r3 + n_rows(tam, "inside.md")
    res = {
        "P1": len(r1) >= 1,
        "P2": len(r2) >= 1,
        "P3": len(r3) >= 1,
        "P4": all(contained(tam, f) is None for f in ("../outside.md", out, "link.md")),
        "P5": contained(tam, "inside.md") is not None,
        "P6": not any(SECRET in "\t".join(r) for r in allrows),
    }
    print(json.dumps({"rows": {"parent": len(r1), "absolute": len(r2), "symlink": len(r3)},
                      "predictions": {k: ("TRUE" if v else "FALSE") for k, v in res.items()},
                      "matched": sum(res.values()), "of": len(res)}, sort_keys=True))
