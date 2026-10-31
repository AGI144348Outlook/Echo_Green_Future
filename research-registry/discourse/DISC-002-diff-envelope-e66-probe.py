"""DISC-002 E66 (Claude, 2026-10-31 07Z): ChatGPT's N55 falsifiers and N56 (a)-(f), run against a model.

Exploratory model, not a Genesis patch. Three gates are compared on the same cases:
  GENESIS-SHAPE  the A-000 check of real Genesis governor_validate_and_deploy (src/echo_governor_skeleton.py
                 blob 63eb982, lines 9392-9398, transcribed): name and status keys present, status == ACTIVE.
  WITNESS-ONLY   E64/E65-style: an approval names the candidate's witness id (digest of its canonical snapshot);
                 boot proceeds if the candidate's witness equals the approved one. No policy, no operation.
  ENVELOPE       N55 + N56: the boot gate recomputes, from the last approved snapshot and the candidate, a
                 canonical type-tagged path-level diff, under the CURRENT policy, for the REQUESTED operation,
                 and builds an envelope {old, new, diff, diff_digest, receipt_ref, policy_digest, operation};
                 the approval must name that whole envelope digest. The policy gate then refuses unknown fields,
                 type changes, normalization-only Unicode changes, and pinned-field moves without a semantic
                 decision. A candidate-declared diff is compared with the recomputed one and refused on mismatch.
The PINNED / KNOWN field lists and the Unicode and type rules are PLACEHOLDERS for Timothy's rulings.
Stdlib only; deterministic; run with python3 -I. Prints one line per case.
"""
import copy, hashlib, json, unicodedata

def tag(v):
    """Type-tagged canonical form, so 5 and "5" or [] and {} never collide."""
    if isinstance(v, bool): return ["bool", v]
    if isinstance(v, int): return ["int", v]
    if isinstance(v, float): return ["float", repr(v)]
    if isinstance(v, str): return ["str", v]
    if v is None: return ["null"]
    if isinstance(v, list): return ["list", [tag(x) for x in v]]
    if isinstance(v, dict): return ["dict", [[k, tag(v[k])] for k in sorted(v)]]
    raise TypeError(type(v).__name__)

def cbytes(v): return json.dumps(tag(v), ensure_ascii=True, separators=(",", ":")).encode()
def digest(v): return hashlib.sha256(cbytes(v)).hexdigest()[:12]

def identity(matrix):
    """The identity snapshot: only A-000 and A-000-RESH (A-9xx are outside it)."""
    return {k: copy.deepcopy(matrix[k]) for k in ("A-000", "A-000-RESH") if k in matrix}

def walk(v, p=()):
    if isinstance(v, dict) and v:
        for k in sorted(v): yield from walk(v[k], p + (k,))
    elif isinstance(v, list) and v:
        for i, x in enumerate(v): yield from walk(x, p + (i,))
    else:
        yield p, v

def diff(old, new):
    a, b = dict(walk(old)), dict(walk(new)); out = []
    for p in sorted(set(a) | set(b), key=lambda q: [str(x) for x in q]):
        path = ".".join(str(x) for x in p)
        if p not in a: out.append([path, "added"])
        elif p not in b: out.append([path, "deleted"])
        elif tag(a[p]) == tag(b[p]): continue
        elif type(a[p]) is not type(b[p]): out.append([path, "type"])
        elif isinstance(a[p], str) and unicodedata.normalize("NFC", a[p]) == unicodedata.normalize("NFC", b[p]):
            out.append([path, "normalization-only"])
        else: out.append([path, "changed"])
    return out

POLICY_P = {"version": "P1", "pinned": ["A-000.name", "A-000.identity_symbol", "A-000-RESH.name",
            "A-000-RESH.glyph", "A-000-RESH.status"],
            "known": ["A-000.name", "A-000.status", "A-000.identity_symbol", "A-000.aliases", "A-000.version",
                      "A-000-RESH.name", "A-000-RESH.glyph", "A-000-RESH.status"],
            "unicode": "fail-closed-on-normalization-only", "types": "fail-closed-on-type-change"}

def known(path, pol):
    return any(path == k or path.startswith(k + ".") for k in pol["known"])

def envelope(old, new, pol, op, receipt_ref):
    d = diff(old, new)
    env = {"old": digest(old), "new": digest(new), "diff": d, "diff_digest": digest(d),
           "receipt_ref": receipt_ref, "policy_digest": digest(pol), "operation": op}
    return env, digest(env)

def policy_verdict(env, pol, semantic_decision=None):
    for path, kind in env["diff"]:
        if not known(path, pol): return f"refused: unknown field {path}"
        if kind == "type": return f"refused: type change {path}"
        if kind == "normalization-only": return f"refused: normalization-only change {path}"
        if path.split(".")[0] + "." + path.split(".")[1] in pol["pinned"] and semantic_decision != env["diff_digest"]:
            return f"refused: pinned field moved {path}, no semantic decision"
    return "ok"

def genesis_shape(matrix):
    a = matrix.get("A-000")
    if not a: return "FAILED not found"
    if not {"name", "status"}.issubset(a.keys()) or a.get("status") != "ACTIVE": return "FAILED identity"
    return "boots"

def witness_only(cand_matrix, approval):
    return "boots" if approval.get("witness") == digest(identity(cand_matrix)) else "refused: witness"

def envelope_gate(approved_snap, cand_matrix, approval, pol_now, op, declared=None, semantic=None):
    if genesis_shape(cand_matrix) != "boots": return "refused: structural (Genesis shape) check"  # N55 verdict 1
    env, ed = envelope(approved_snap, identity(cand_matrix), pol_now, op, approval.get("receipt_ref"))
    if declared is not None and digest(declared) != env["diff_digest"]:
        return "refused: declared diff != recomputed diff"
    if approval.get("envelope") != ed: return "refused: approval does not name this envelope"
    v = policy_verdict(env, pol_now, semantic)
    return "boots" if v == "ok" else v

BASE = {"A-000": {"name": "Governor", "status": "ACTIVE", "identity_symbol": "resh", "version": 5,
                  "aliases": ["Resh", "Head"]},
        "A-000-RESH": {"name": "Resh", "glyph": "\u05e8\u05b8\u05bc", "status": "ACTIVE"},  # placeholder glyph: resh, qamats, dagesh (NFC order)
        "A-101": {"name": "first tool"}}

def run():
    snap0 = identity(BASE)
    lines = []
    def case(name, cand, op="boot", pol_now=POLICY_P, appr_from=None, declared=None, semantic=None,
             approve_op="boot", approve_pol=POLICY_P):
        appr_snap = identity(appr_from if appr_from is not None else cand)
        _, ed = envelope(snap0, appr_snap, approve_pol, approve_op, "r1")
        approval = {"witness": digest(appr_snap), "envelope": ed, "receipt_ref": "r1"}
        d = diff(snap0, identity(cand))
        a, b = dict(walk(snap0)), dict(walk(identity(cand)))
        display_changed = "yes" if {k: str(v) for k, v in a.items()} != {k: str(v) for k, v in b.items()} else "no"
        lines.append(f"{name} | diff={d} | display_changed={display_changed} | GENESIS-SHAPE={genesis_shape(cand)}"
                     f" | WITNESS-ONLY={witness_only(cand, approval)}"
                     f" | ENVELOPE={envelope_gate(snap0, cand, approval, pol_now, op, declared, semantic)}")
    m = copy.deepcopy

    c = m(BASE); case("C0 unchanged, approved", c)
    c = m(BASE); c["A-000"]["name"] = "Impostor Governor"; case("N55-1 rename, ACTIVE/resh kept, receipts recomputed, approved", c)
    case("N55-1b same, with a semantic decision naming this diff", c,
         semantic=digest(diff(snap0, identity(c))))
    case("N55-2 rename, candidate declares empty diff", c, declared=[])
    case("N55-3 approval of the old snapshot only", c, appr_from=BASE)
    c = m(BASE); c["A-900"] = {"name": "non-core addition"}; case("N55-4 A-900 added (outside identity)", c, appr_from=BASE)
    pol2 = m(POLICY_P); pol2["version"] = "P2"
    c = m(BASE); c["A-000"]["version"] = 6; case("N55-5 policy P1 approved, P2 at boot", c, pol_now=pol2)
    case("N55-5b same change, policy unchanged", c)
    c = m(BASE); c["A-000"]["aliases"][1] = "Impostor"; case("N56-a nested alias changed, declared no change", c, declared=[])
    c = m(BASE); c["A-000"]["version"] = "5"; case("N56-b version int 5 -> str '5'", c)
    pol3 = m(POLICY_P); pol3["pinned"] = pol3["pinned"][:-1]
    c = m(BASE); case("N56-c approve under P1, swap to P3 (RESH.status unpinned) before boot", c, pol_now=pol3)
    c = m(BASE); c["A-000-RESH"]["glyph"] = "\u05e8\u05bc\u05b8"; case("N56-d1 RESH glyph marks reordered (dagesh before qamats; NFC-equal, bytes differ)", c)
    c = m(BASE); c["A-000-RESH"]["glyph"] = "\ufb47\u05b8"; case("N56-d3 RESH glyph -> U+FB47 QOF WITH DAGESH + qamats (looks close; NFC-different letter)", c)
    c = m(BASE); c["A-000"]["name"] = "G\u043evernor"; case("N56-d2 name with Cyrillic o U+043E (looks identical, NFC-different)", c)
    c = m(BASE); c["A-000"]["shadow_authority"] = True; case("N56-e unrecognized field added to A-000", c)
    c = m(BASE); case("N56-f approval for reconcile used for boot", c, approve_op="reconcile")
    c = m(BASE); c["A-000"]["status"] = "PAUSED"; case("X1 status PAUSED (control)", c)
    return lines

if __name__ == "__main__":
    print(f"policy P1 digest {digest(POLICY_P)}; base identity digest {digest(identity(BASE))}")
    for line in run(): print(line)
