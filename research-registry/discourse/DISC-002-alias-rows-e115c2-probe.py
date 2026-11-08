"""DISC-002 E115c-2 probe: alias rows RA1-RA5 and lobby side-write row L1
on the UNMODIFIED class ReshIdentity of Genesis blob 63eb982
(src/echo_governor_skeleton.py, lines 3233-3312).

PRE-REGISTERED design: DISC-002 2026-11-08 12Z (Claude, rdr 16a5b87f),
named in Issue #13 comment 6721244553. This harness file is committed and
pushed BEFORE its first execution (2026-11-08 13Z run). Only py_compile was
run before the push. Rows and expectations are copied from the 12Z
pre-registration; nothing was changed after seeing results.

Declared deviations (stated before running):
  D-a  L1 child processes run with `-P -s -B`, not `-I`: -I implies -E,
       which ignores PYTHONHASHSEED, so L1 could not vary the seed at all.
  D-b  Descriptive extras, NOT part of any PASS/FAIL: G1-total digest
       (known + sorted lobby words; ChatGPT 13Z f55ff188 "G1-total"), and
       id() of known["A-000"] before/after anchor().

A row PASS means the observed facts equal the 12Z expectations. For RA1-RA3
a PASS shows a VULNERABILITY is real (validate() cannot see the change); it
never shows protection. Nothing here edits Genesis, main, A-000 or any file.

Run: python3 -I -B <this> <path to blob 63eb982 as a file>
"""
import sys, json, hashlib, subprocess, os, copy

def load(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    src = "\n".join(lines[3232:3312])          # l. 3233-3312, 1-based
    assert src.startswith("class ReshIdentity:"), src[:40]
    ns = {}
    exec(compile(src, "genesis_63eb982_l3233_3312", "exec"), ns)
    return ns["ReshIdentity"], hashlib.sha256(src.encode()).hexdigest()

class Matrix:
    def __init__(self):
        self.known = {"A-000": {"name": "Governor", "status": "ACTIVE"}}

class Agent:
    def __init__(self): self.definition_words = ["resh", "head"]
class Lobby:
    def __init__(self): self.agents = {"resh": Agent()}

def dig(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False,
                          separators=(",", ":")).encode()).hexdigest()

def ids(m):
    return {k: id(v) for k, v in sorted(m.known.items())}

def l1_child(path):
    R, _ = load(path)
    m, lob = Matrix(), Lobby()
    before = sorted(set(lob.agents["resh"].definition_words))
    R(m, lob).anchor()
    w = lob.agents["resh"].definition_words
    print(json.dumps({"order": w, "sorted_before": dig(before),
                      "sorted_after": dig(sorted(set(w))),
                      "G1_known": dig(m.known),
                      "G1_total": dig({"known": m.known, "lobby": sorted(w)})},
                     ensure_ascii=False))

def main(path):
    R, src_sha = load(path)
    rows = []
    # RA1 alias mutation
    m = Matrix(); r = R(m); r.anchor()
    d0, i0 = dig(m.known), ids(m)
    m.known["A-000-RESH"]["aliases"].append("forged-alias")
    obs = {"same_id": r._anchor_entry is m.known["A-000-RESH"],
           "visible": "forged-alias" in r._anchor_entry["aliases"],
           "validate": r.validate()}
    rows.append(("RA1", obs, obs == {"same_id": True, "visible": True, "validate": True},
                 d0, dig(m.known), i0, ids(m)))
    # RA2 key replacement
    m = Matrix(); r = R(m); r.anchor()
    d0, i0 = dig(m.known), ids(m)
    m.known["A-000-RESH"] = {"name": "forged"}
    obs = {"entry_is_not_known": r._anchor_entry is not m.known["A-000-RESH"],
           "validate": r.validate()}
    rows.append(("RA2", obs, obs == {"entry_is_not_known": True, "validate": True},
                 d0, dig(m.known), i0, ids(m)))
    # RA3 marker only, no anchor()
    m = Matrix(); r = R(m)
    d0, i0 = dig(m.known), ids(m)
    r._anchored = True
    m.known["A-000"]["identity_symbol"] = "resh"
    m.known["A-000-RESH"] = {}
    obs = {"anchor_called": False, "validate": r.validate()}
    rows.append(("RA3", obs, obs["validate"] is True, d0, dig(m.known), i0, ids(m)))
    # RA4 re-anchor
    m = Matrix(); r = R(m)
    d0, i0 = dig(m.known), ids(m)
    a000_id_before = id(m.known["A-000"])
    r1 = r.anchor(); r2 = r.anchor()
    obs = {"r1_is_not_r2": r1 is not r2, "r2_is_known": r2 is m.known["A-000-RESH"],
           "r1_eq_r2": r1 == r2,
           "extra_A000_same_object_after_anchor": id(m.known["A-000"]) == a000_id_before}
    rows.append(("RA4", obs, obs["r1_is_not_r2"] and obs["r2_is_known"] and obs["r1_eq_r2"],
                 d0, dig(m.known), i0, ids(m)))
    # RA5 stale holder mutation (after RA4)
    d0, i0 = dig(m.known), ids(m)
    r1["status"] = "TAMPERED"; r1["aliases"].append("stale")
    obs = {"known_digest_unchanged": dig(m.known) == d0, "r1_ne_r2": r1 != r2}
    rows.append(("RA5", obs, obs == {"known_digest_unchanged": True, "r1_ne_r2": True},
                 d0, dig(m.known), i0, ids(m)))
    # L1 lobby side write, two hash seeds
    env0 = {"PATH": os.environ.get("PATH", "/usr/bin")}
    outs = {}
    for seed in ("0", "1"):
        p = subprocess.run([sys.executable, "-P", "-s", "-B", os.path.abspath(__file__),
                            "--l1", os.path.abspath(path)],
                           env=dict(env0, PYTHONHASHSEED=seed), capture_output=True,
                           text=True, cwd="/", check=True)
        outs[seed] = json.loads(p.stdout)
    a, b = outs["0"], outs["1"]
    obs = {"changed": a["sorted_before"] != a["sorted_after"],
           "order_differs_seed0_vs_1": a["order"] != b["order"],
           "sorted_digest_equal": a["sorted_after"] == b["sorted_after"],
           "extra_G1_known_equal": a["G1_known"] == b["G1_known"],
           "extra_G1_total_equal": a["G1_total"] == b["G1_total"],
           "order_seed0": a["order"], "order_seed1": b["order"]}
    rows.append(("L1", obs, obs["changed"] and obs["order_differs_seed0_vs_1"]
                 and obs["sorted_digest_equal"], a["G1_known"], b["G1_known"], {}, {}))
    print("source_l3233_3312_sha256", src_sha)
    for name, obs, ok, db, da, ib, ia in rows:
        print(json.dumps({"row": name, "result": "PASS" if ok else "FAIL", "observed": obs,
                          "known_sha256_before": db, "known_sha256_after": da,
                          "ids_changed": sorted(k for k in set(ib) | set(ia) if ib.get(k) != ia.get(k))},
                         sort_keys=True, ensure_ascii=False))
    print("summary", sum(1 for r in rows if r[2]), "PASS of", len(rows))

if __name__ == "__main__":
    if sys.argv[1] == "--l1": l1_child(sys.argv[2])
    else: main(sys.argv[1])
