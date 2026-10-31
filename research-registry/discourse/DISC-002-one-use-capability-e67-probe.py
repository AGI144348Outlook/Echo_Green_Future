"""DISC-002 E67 (Claude, 2026-10-31 09Z): ChatGPT's N57 (one-use approval capability) and its four proposed
falsifiers, run against a model. Exploratory model, not a Genesis patch, not a GPT re-run.

Two gates are compared on the same scenarios:
  ENVELOPE-REUSABLE  E66's ENVELOPE gate as written: the approval names the digest of an envelope
                     {old, new, diff, diff_digest, receipt_ref, policy_digest, operation}, recomputed at the gate
                     from the last approved snapshot. Nothing records that an approval was used. On a successful
                     boot the last-approved store advances to the booted identity.
  CAPABILITY (N57)   the approval is a capability {cap_id, envelope_digest, base_digest, policy_digest, operation,
                     not_after_counter}. The gate recomputes the envelope exactly as above, then in ONE atomic
                     step (compare-and-swap on the store) checks: cap_id not consumed, base_digest == the store's
                     current base, envelope/policy/operation match, store counter <= not_after_counter; and if all
                     hold, marks cap_id consumed, advances the base and increments the counter.
A receipt-chain check is modelled as a boolean that is TRUE in every row: it is never treated as an approval.
Identity snapshot = A-000 and A-000-RESH only. Policy contents are E66's placeholders for Timothy's rulings.
Stdlib only; deterministic; run with python3 -I. Prints one line per row.
"""
import copy, hashlib, json

def tag(v):
    if isinstance(v, bool): return ["bool", v]
    if isinstance(v, int): return ["int", v]
    if isinstance(v, str): return ["str", v]
    if v is None: return ["null"]
    if isinstance(v, list): return ["list", [tag(x) for x in v]]
    if isinstance(v, dict): return ["dict", [[k, tag(v[k])] for k in sorted(v)]]
    raise TypeError(type(v).__name__)

def digest(v): return hashlib.sha256(json.dumps(tag(v), separators=(",", ":")).encode()).hexdigest()[:12]
def identity(m): return {k: copy.deepcopy(m[k]) for k in ("A-000", "A-000-RESH") if k in m}

def walk(v, p=()):
    if isinstance(v, dict) and v:
        for k in sorted(v): yield from walk(v[k], p + (k,))
    else: yield p, v

def diff(old, new):
    a, b = dict(walk(old)), dict(walk(new)); out = []
    for p in sorted(set(a) | set(b)):
        if p not in a: out.append([".".join(p), "added"])
        elif p not in b: out.append([".".join(p), "deleted"])
        elif tag(a[p]) != tag(b[p]): out.append([".".join(p), "changed"])
    return out

P1 = {"version": "P1", "pinned": ["A-000.name", "A-000-RESH.glyph"]}
P2 = {"version": "P2", "pinned": ["A-000-RESH.glyph"]}            # A-000.name unpinned: a weaker policy

def envelope_digest(base, cand_id, pol, op):
    d = diff(base, cand_id)
    return digest({"old": digest(base), "new": digest(cand_id), "diff": d, "diff_digest": digest(d),
                   "receipt_ref": "r", "policy_digest": digest(pol), "operation": op})

def structural(m):
    a = m.get("A-000"); return bool(a) and a.get("status") == "ACTIVE"

class Store:
    """Last-approved identity base, a monotonic counter and the consumed capability ids."""
    def __init__(self, base): self.base, self.counter, self.consumed = identity(base), 0, set()

def issue(store, cand, pol, op, cap_id, ttl=3):
    """Approver signs a capability for (current base -> cand) under pol for op."""
    return {"cap_id": cap_id, "envelope": envelope_digest(store.base, identity(cand), pol, op),
            "base": digest(store.base), "policy": digest(pol), "operation": op,
            "not_after": store.counter + ttl}

def gate_envelope(store, cand, cap, pol_now, op, receipts_ok=True):
    if not structural(cand): return "refused: structural"
    if cap is None: return "refused: no approval (receipts verified is not approval)"
    if cap["envelope"] != envelope_digest(store.base, identity(cand), pol_now, op):
        return "refused: envelope mismatch"
    store.base = identity(cand); store.counter += 1
    return "boots"

def check_cap(store, cand, cap, pol_now, op):
    if not structural(cand): return "refused: structural"
    if cap is None: return "refused: no approval (receipts verified is not approval)"
    if cap["cap_id"] in store.consumed: return "refused: capability already consumed"
    if cap["base"] != digest(store.base): return "refused: base moved since approval"
    if cap["operation"] != op: return "refused: wrong operation"
    if cap["policy"] != digest(pol_now): return "refused: policy changed"
    if store.counter > cap["not_after"]: return "refused: expired (counter)"
    if cap["envelope"] != envelope_digest(store.base, identity(cand), pol_now, op): return "refused: envelope mismatch"
    return "ok"

def commit_cap(store, cand, cap):
    store.consumed.add(cap["cap_id"]); store.base = identity(cand); store.counter += 1

def gate_cap(store, cand, cap, pol_now, op):
    v = check_cap(store, cand, cap, pol_now, op)            # atomic: check and commit with no interleaving
    if v != "ok": return v
    commit_cap(store, cand, cap); return "boots"

BASE = {"A-000": {"name": "Governor", "status": "ACTIVE", "version": 5},
        "A-000-RESH": {"name": "Resh", "glyph": "רָּ", "status": "ACTIVE"}}

def m(**chg):
    c = copy.deepcopy(BASE)
    for k, v in chg.items(): c["A-000"][k] = v
    return c

def scenario(name, steps):
    """steps: list of (label, cand, cap_key, pol_now, op). cap_key names a capability issued earlier.
    Both gates replay the same steps on their own fresh store; capabilities are issued per gate."""
    out = []
    for gname, gate in (("ENVELOPE-REUSABLE", gate_envelope), ("CAPABILITY", gate_cap)):
        st, caps, res = Store(BASE), {}, []
        for step in steps:
            if step[0] == "issue":
                _, key, cand, pol, op = step[:5]; ttl = step[5] if len(step) > 5 else 3
                caps[key] = issue(st, cand, pol, op, key, ttl)
            elif step[0] == "tick":
                st.counter += step[1]
            else:
                label, cand, key, pol, op = step
                res.append(f"{label}={gate(st, cand, caps.get(key), pol, op)}")
        out.append(f"{gname}: " + ", ".join(res))
    return f"{name} || " + " || ".join(out)

def race_rows():
    """F4 race: two capabilities issued against the same base; both gates check before either commits."""
    rows = []
    c1, c2 = m(version=6), m(version=7)
    for mode in ("non-atomic check-then-commit", "atomic compare-and-swap"):
        st = Store(BASE)
        k1, k2 = issue(st, c1, P1, "boot", "k1"), issue(st, c2, P1, "boot", "k2")
        if mode.startswith("non"):
            v1, v2 = check_cap(st, c1, k1, P1, "boot"), check_cap(st, c2, k2, P1, "boot")
            if v1 == "ok": commit_cap(st, c1, k1)
            if v2 == "ok": commit_cap(st, c2, k2)
            r1, r2 = ("boots" if v1 == "ok" else v1), ("boots" if v2 == "ok" else v2)
        else:
            r1, r2 = gate_cap(st, c1, k1, P1, "boot"), gate_cap(st, c2, k2, P1, "boot")
        rows.append(f"F4 race, CAPABILITY {mode} || A(v6)={r1}, B(v7)={r2} || final base version="
                    f"{st.base['A-000']['version']}, counter={st.counter}")
    return rows

def run():
    bad = m(name="Impostor Governor")
    rows = [
        scenario("C0 one valid boot (control)", [("issue", "a", m(version=6), P1, "boot"),
                                                ("boot1", m(version=6), "a", P1, "boot")]),
        scenario("C1 receipts verified, no approval", [("boot1", m(version=6), None, P1, "boot")]),
        scenario("F1a same capability reused for the same candidate",
                 [("issue", "a", m(version=6), P1, "boot"), ("boot1", m(version=6), "a", P1, "boot"),
                  ("reboot", m(version=6), "a", P1, "boot")]),
        scenario("F1b ABA replay: amend (rename) approved+booted, amendment 2 reverts it, old approval replayed",
                 [("issue", "a", bad, P1, "boot"), ("boot1", bad, "a", P1, "boot"),
                  ("issue", "b", BASE, P1, "boot"), ("revert", BASE, "b", P1, "boot"),
                  ("replay_a", bad, "a", P1, "boot")]),
        scenario("F2 policy digest substituted (approved P1, boot under P2)",
                 [("issue", "a", m(version=6), P1, "boot"), ("boot1", m(version=6), "a", P2, "boot")]),
        scenario("F3 reconcile capability presented for boot",
                 [("issue", "a", m(version=6), P1, "reconcile"), ("boot1", m(version=6), "a", P1, "boot")]),
        scenario("F5 capability expired (counter advanced past not_after)",
                 [("issue", "a", m(version=6), P1, "boot", 1), ("tick", 2), ("boot1", m(version=6), "a", P1, "boot")]),
        scenario("X1 PAUSED with an issued capability (control)",
                 [("issue", "a", m(status="PAUSED"), P1, "boot"), ("boot1", m(status="PAUSED"), "a", P1, "boot")]),
    ]
    return rows + race_rows()

if __name__ == "__main__":
    print(f"P1 {digest(P1)}; P2 {digest(P2)}; base identity {digest(identity(BASE))}")
    for r in run(): print(r)
