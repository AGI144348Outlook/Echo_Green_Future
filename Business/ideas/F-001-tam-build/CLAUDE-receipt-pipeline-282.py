# F-001 §282 (Claude 13Z): one pipeline over bytes, §281 parse_inert -> §280 shape -> FILE-BACKED nonce ledger with a REAL process restart.
# PRE-REGISTERED (predictions below, pushed before first run). Answers ChatGPT 12Z v18 (927ee268) phase 4 COMMITTED: "atomically insert
# unique nonce and record digest/decision; on duplicate identical digest return prior receipt without granting new authority; on
# conflicting reuse fail closed", incl. "crash after commit/before acknowledgement". Same commit pattern as DISC-002 e120 (rdr 9a8779a0).
# parse_inert/canon (§281, f52cef10) and shape (§280, e8f581e9) are copied verbatim below. The ledger digest binds the exact receipt bytes.
# Best status stays SHAPE_VALID_CHANNEL_CLAIMED: no signature, no issuer key, no authentication (v18 phase 3 needs a protected host root).
# Synthetic fixtures only; reads RIGHTS-CLASSES-277.tsv for class names; reads no TAM text; no network; writes only in a temp dir it creates.
# Usage: python3 -I -B CLAUDE-receipt-pipeline-282.py RIGHTS-CLASSES-277.tsv   (children run with -I -B; temp paths never printed)
import sys, os, json, csv, hashlib, subprocess, tempfile
from datetime import datetime
MAX = 4096
class Dup(Exception): pass
class Const(Exception): pass
def pairs(ps):
    d = {}
    for k, v in ps:
        if k in d: raise Dup(k)
        d[k] = v
    return d
def const(x): raise Const(x)
def canon(o): return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
def parse_inert(b):
    if not isinstance(b, bytes): return "NOT_BYTES", None
    if len(b) > MAX: return "TOO_LARGE", None
    try: s = b.decode("utf-8", errors="strict")
    except UnicodeDecodeError: return "NOT_UTF8", None
    try: o = json.loads(s, object_pairs_hook=pairs, parse_constant=const)
    except Dup as e: return "DUPLICATE_KEY:" + str(e), None
    except Const as e: return "BAD_CONSTANT:" + str(e), None
    except json.JSONDecodeError: return "NOT_JSON", None
    if not isinstance(o, dict): return "NOT_OBJECT", None
    if canon(o) != b: return "NONCANONICAL", None
    return "PARSED", o
HOST = {"schema_version": "rights-receipt-v2", "now": "2026-11-09T11:00:00+00:00"}   # protected side (stand-in)
KEYS = {"schema_version", "scope", "target", "source_file_blob", "decision", "decided_by", "channel",
        "mixed_content_checked", "issued_at", "expires_at", "nonce"}
def ts(s):
    try: d = datetime.fromisoformat(s)
    except (TypeError, ValueError): return None
    return d if d.tzinfo else None
def shape(rc, host):
    if not isinstance(rc, dict): return "INVALID_RECEIPT:type"
    if KEYS - set(rc): return "INVALID_RECEIPT:missing=" + ",".join(sorted(KEYS - set(rc)))
    if set(rc) - KEYS: return "INVALID_RECEIPT:extra=" + ",".join(sorted(set(rc) - KEYS))
    if rc["schema_version"] != host["schema_version"]: return "INVALID_RECEIPT:schema_version"
    if rc["scope"] not in ("class", "unit"): return "INVALID_RECEIPT:scope"
    if rc["scope"] == "class" and rc["target"] not in CLASSES: return "INVALID_RECEIPT:unknown_class"
    if rc["decision"] not in ("CLEAR", "REJECT"): return "INVALID_RECEIPT:decision"
    if not (isinstance(rc["nonce"], str) and len(rc["nonce"]) >= 16): return "INVALID_RECEIPT:nonce"
    i, e, now = ts(rc["issued_at"]), ts(rc["expires_at"]), ts(host["now"])
    if i is None or e is None or not i < e: return "INVALID_RECEIPT:time"
    if not i <= now < e: return "EXPIRED_OR_FUTURE"
    if rc["decision"] == "REJECT": return "RIGHTS_REJECTED"   # rejection accepted from any well-formed receipt (fail-closed side)
    if rc["decided_by"] != "Timothy": return "RIGHTS_UNVERIFIED:not_timothy"
    if rc["scope"] == "class" and rc["mixed_content_checked"] is not True: return "RIGHTS_UNVERIFIED:mixed_content_unchecked"
    return "SHAPE_VALID_CHANNEL_CLAIMED"   # channel is a claimed string until Timothy names the trust root (EB-TJ, §270)
def load(d):
    p = os.path.join(d, "ledger.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {"nonces": {}}
def child(classes_path, d, crash, b):
    global CLASSES
    CLASSES = {r["class"] for r in csv.DictReader((l for l in open(classes_path) if not l.startswith("#")), delimiter="\t")}
    st, rc = parse_inert(b)
    if st != "PARSED": print(st + "|NOT_RECORDED"); return
    st = shape(rc, HOST)
    if st.startswith("INVALID") or st == "EXPIRED_OR_FUTURE": print(st + "|NOT_RECORDED"); return
    led, dg = load(d), hashlib.sha256(b).hexdigest()
    if rc["nonce"] in led["nonces"]:
        print("PRIOR_RECEIPT|" + led["nonces"][rc["nonce"]]["outcome"] if led["nonces"][rc["nonce"]]["digest"] == dg else "NONCE_CONFLICT|NOT_RECORDED"); return
    new = {"nonces": dict(led["nonces"])}; new["nonces"][rc["nonce"]] = {"digest": dg, "outcome": st}
    tmp = os.path.join(d, "ledger.json.tmp")
    with open(tmp, "w", encoding="utf-8") as f: json.dump(new, f, sort_keys=True); f.flush(); os.fsync(f.fileno())
    if crash == "C1": os._exit(9)                                   # before commit
    os.replace(tmp, os.path.join(d, "ledger.json"))                 # commit
    if crash == "C2": os._exit(9)                                   # after commit, before acknowledgement
    print(st + "|RECORDED")
def run(cp, d, crash, b):
    r = subprocess.run([sys.executable, "-I", "-B", os.path.abspath(__file__), "--child", cp, d, crash], input=b, capture_output=True)
    return r.returncode, r.stdout.decode("utf-8").strip()
def lsha(d):
    p = os.path.join(d, "ledger.json")
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.exists(p) else None
def main(cp):
    base = {"schema_version": "rights-receipt-v2", "scope": "class", "target": "Article 5", "source_file_blob": "0" * 40,
            "decision": "CLEAR", "decided_by": "Timothy", "channel": "issue-comment", "mixed_content_checked": True,
            "issued_at": "2026-11-09T10:00:00+00:00", "expires_at": "2026-11-10T10:00:00+00:00", "nonce": "synthetic-nonce-0001"}
    def rc(**kw): return canon({**base, **kw})
    r1, r2, r6 = rc(), rc(nonce="synthetic-nonce-0002"), rc(nonce="synthetic-nonce-0006", decision="REJECT")
    out = {}
    with tempfile.TemporaryDirectory() as d:
        c = run(cp, d, "C2", r1); out["P1"] = [c[0], c[1], sorted(load(d)["nonces"]), run(cp, d, "-", r1)[1]]
        before = lsha(d); c = run(cp, d, "C1", r2)
        out["P2"] = [c[0], lsha(d) == before, os.path.exists(os.path.join(d, "ledger.json.tmp")), run(cp, d, "-", r2)[1]]
        before = lsha(d)
        out["P3"] = run(cp, d, "-", rc(decision="REJECT"))[1]                      # same nonce 0001, different bytes
        out["P4"] = run(cp, d, "-", r6.replace(b'"decision":"REJECT"', b'"decision":"REJECT","decision":"CLEAR"'))[1]
        out["P5"] = run(cp, d, "-", json.dumps({**base, "nonce": "synthetic-nonce-0005"}, sort_keys=True, indent=1, ensure_ascii=False).encode("utf-8"))[1]
        out["P8"] = [lsha(d) == before]
        out["P6"] = run(cp, d, "-", r6)[1]
        out["P7"] = sorted(load(d)["nonces"])
    PRED = {"P1": [9, "", ["synthetic-nonce-0001"], "PRIOR_RECEIPT|SHAPE_VALID_CHANNEL_CLAIMED"],
            "P2": [9, True, True, "SHAPE_VALID_CHANNEL_CLAIMED|RECORDED"],
            "P3": "NONCE_CONFLICT|NOT_RECORDED", "P4": "DUPLICATE_KEY:decision|NOT_RECORDED", "P5": "NONCANONICAL|NOT_RECORDED",
            "P8": [True], "P6": "RIGHTS_REJECTED|RECORDED",
            "P7": ["synthetic-nonce-0001", "synthetic-nonce-0002", "synthetic-nonce-0006"]}
    res = {k: {"observed": out[k], "predicted": PRED[k], "match": out[k] == PRED[k]} for k in PRED}
    res["summary"] = f"{sum(v['match'] for v in res.values())}/{len(PRED)} matched; best status SHAPE_VALID_CHANNEL_CLAIMED; not authentication; HOLD"
    print(json.dumps(res, sort_keys=True, ensure_ascii=False))
if __name__ == "__main__":
    if sys.argv[1] == "--child": child(sys.argv[2], sys.argv[3], sys.argv[4], sys.stdin.buffer.read())
    else: main(os.path.abspath(sys.argv[1]))
