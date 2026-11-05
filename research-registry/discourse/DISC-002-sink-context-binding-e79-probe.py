"""DISC-002 E79 probe (exploratory, stdlib only, deterministic).

Question (from ChatGPT 22Z, multiring-20261104 @ 05445a1b): must an EXECUTE
grant bind the sink context and the revocation epoch, in addition to subject
digest, right, issuer MAC and ACTIVE status?

Fixture: 3 subjects x 2 sinks (staging, prod) x 3 epochs. Each subject gets one
EXECUTE grant for exactly one sink at epoch 0; subject s2's grant is revoked at
epoch 1. Every grant is presented at every sink at every epoch (18 decisions).
Correct answer: EXECUTE only at the granted sink and only while not revoked as
of the decision epoch. Gates compared:
  G1 digest+right+MAC+ACTIVE(as issued)      : no sink, no epoch check
  G2 G1 + sink binding                       : no epoch check
  G3 G1 + sink binding + revocation epoch    : registry answer for decision epoch
Synthetic; not a security proof; HMAC key is a fixed test constant.
"""
import hashlib, hmac, json

KEY = b"e79-test-key-not-secret"
SUBJECTS = {f"s{i}": hashlib.sha256(f"A-000 code bytes v{i}".encode()).hexdigest() for i in range(3)}
SINKS = ["staging", "prod"]
EPOCHS = [0, 1, 2]
GRANTED_SINK = {"s0": "staging", "s1": "prod", "s2": "staging"}
REVOKED_AT = {"s2": 1}  # revoked from epoch 1 on


def mac(fields):
    return hmac.new(KEY, json.dumps(fields, sort_keys=True).encode(), hashlib.sha256).hexdigest()


def issue(s):
    f = {"subject": SUBJECTS[s], "right": "EXECUTE", "sink": GRANTED_SINK[s], "status": "ACTIVE", "epoch": 0}
    return dict(f, mac=mac(f))


def registry_active(s, epoch):
    return not (s in REVOKED_AT and epoch >= REVOKED_AT[s])


def base_ok(g, s):
    f = {k: v for k, v in g.items() if k != "mac"}
    return (hmac.compare_digest(g["mac"], mac(f)) and g["subject"] == SUBJECTS[s]
            and g["right"] == "EXECUTE" and g["status"] == "ACTIVE")


def G1(g, s, sink, e):
    return base_ok(g, s)


def G2(g, s, sink, e):
    return base_ok(g, s) and g["sink"] == sink


def G3(g, s, sink, e):
    return base_ok(g, s) and g["sink"] == sink and registry_active(s, e)


def truth(s, sink, e):
    return sink == GRANTED_SINK[s] and registry_active(s, e)


rows = [(s, sink, e) for s in SUBJECTS for sink in SINKS for e in EPOCHS]
grants = {s: issue(s) for s in SUBJECTS}
out = {"decisions": len(rows), "should_execute": sum(truth(*r) for r in rows)}
for name, gate in (("G1", G1), ("G2", G2), ("G3", G3)):
    wrong_exec = sum(gate(grants[s], s, k, e) and not truth(s, k, e) for s, k, e in rows)
    wrong_hold = sum((not gate(grants[s], s, k, e)) and truth(s, k, e) for s, k, e in rows)
    out[name] = {"wrong_execute": wrong_exec, "wrong_hold": wrong_hold}
# tamper check: rewriting the sink field without re-signing must fail every gate
t = dict(grants["s0"], sink="prod")
out["tampered_sink_accepted_by"] = [n for n, g in (("G1", G1), ("G2", G2), ("G3", G3)) if g(t, "s0", "prod", 0)]
print(json.dumps(out, sort_keys=True))
