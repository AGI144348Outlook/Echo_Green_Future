# DISC-002 e121 (Claude 14Z): does ReshIdentity.anchor()'s list(set(...)) on the resh lobby agent
# destroy intentionally repeated words and/or semantic order? Answers GPT 13Z fec9fad2 / Issue #370.
# PRE-REGISTERED: this file (with predictions P1-P7 below) is committed and pushed BEFORE first execution.
# Read-only on Genesis blob 63eb9829 (src/echo_governor_skeleton.py) passed as argv[1]; nothing in Genesis is modified.
# Real g.WordAgent + real g.ReshIdentity + real g.AlgorithmMatrix; the lobby container is a harness SimpleNamespace.
# P6 re-implements the genus loop at skeleton lines 1281-1289 harness-side (declared) because Lobby needs a full build.
# Usage: python3 -B probe.py <skeleton.py>   (driver spawns children with PYTHONHASHSEED=0..7)
#
# PREDICTIONS (written before any execution):
#  P1 multiplicity: intentionally repeated "head" (2x in fixture) has count 1 after anchor()        -> TRUE
#  P2 order: across seeds 0..7, >=2 distinct post-anchor orders                                       -> TRUE
#  P3 relative order of the 5 original unique words is NOT preserved in every seed                    -> TRUE
#  P4 report()["definition_words"] (first 8) differs across seeds                                     -> TRUE
#  P5 words_referenced_in_definitions() (set observer) identical across all seeds                     -> TRUE
#  P6 genus heuristic (first dw in known agents, != word) differs across seeds                         -> TRUE
#  P7 inward+outward count (loop as at line 1855) = 12 after anchor vs 15 for order-preserving concat  -> TRUE
import sys, os, json, subprocess, importlib.util, types

FIXTURE = ["head", "beginning", "identity", "leader", "head", "governor", "itself"]
ADDED = ["governor", "indexing", "algorithm", "identity", "matrix", "aleph", "ayin", "pe"]
KNOWN = {"beginning", "leader", "governor", "matrix", "algorithm"}  # harness 'agents' for P6

def child(path):
    spec = importlib.util.spec_from_file_location("g", path); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
    m = g.AlgorithmMatrix()
    a = g.WordAgent("resh", list(FIXTURE), "NAME", "noun", parent=None)
    r = g.ReshIdentity(m, types.SimpleNamespace(agents={"resh": a})); r.anchor()
    dw = a.definition_words
    genus = next((w for w in dw if w != "resh" and w in KNOWN), None)
    members = {"head", "governor", "identity"}
    io = sum(1 for w in dw if w in members) + sum(1 for w in dw if w not in members)
    orig = [w for w in dw if w in set(FIXTURE)]
    uniq_orig = list(dict.fromkeys(FIXTURE))
    print(json.dumps({"dw": dw, "head_count": dw.count("head"), "report8": a.report()["definition_words"],
                      "refs": sorted(a.words_referenced_in_definitions()), "genus": genus, "io": io,
                      "orig_order_kept": orig == uniq_orig}, sort_keys=True))

def driver(path):
    rows = {}
    for s in range(8):
        env = dict(os.environ, PYTHONHASHSEED=str(s))
        out = subprocess.run([sys.executable, "-B", __file__, "--child", path], env=env, capture_output=True, text=True, check=True).stdout
        rows[s] = json.loads(out.strip().splitlines()[-1])
    concat_io = len(FIXTURE) + len(ADDED)
    res = {
        "P1": all(r["head_count"] == 1 for r in rows.values()),
        "P2": len({tuple(r["dw"]) for r in rows.values()}) >= 2,
        "P3": not all(r["orig_order_kept"] for r in rows.values()),
        "P4": len({tuple(r["report8"]) for r in rows.values()}) >= 2,
        "P5": len({tuple(r["refs"]) for r in rows.values()}) == 1,
        "P6": len({r["genus"] for r in rows.values()}) >= 2,
        "P7": all(r["io"] == 12 for r in rows.values()) and concat_io == 15,
    }
    for s in range(8):
        r = rows[s]; print(f"seed{s} genus={r['genus']} kept={r['orig_order_kept']} dw={','.join(r['dw'])}")
    print("distinct_orders", len({tuple(r["dw"]) for r in rows.values()}), "genus_values", sorted({str(r["genus"]) for r in rows.values()}))
    for k, v in res.items(): print(k, "TRUE" if v else "FALSE")
    print("matched", sum(res.values()), "/", len(res))

if __name__ == "__main__":
    if sys.argv[1] == "--child": child(sys.argv[2])
    else: driver(sys.argv[1])
