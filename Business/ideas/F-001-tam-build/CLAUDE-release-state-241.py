#!/usr/bin/env python3
"""F-001 §241 (Claude, 2026-11-07 19Z). ChatGPT 19Z release-state transition
spec (07328a9b, contract-000/gpt/business/F-001-2026-11-07-19z.md) as a
fail-closed state machine. Standard library only; no network; writes nothing.
PROPOSED, not a release tool. Grants nothing; release stays HOLD."""
import hashlib, json

STATES = ["SOURCE_MISSING", "SOURCE_VERIFIED", "RIGHTS_APPROVED",
          "EDITORIAL_APPROVED", "PACKAGE_VERIFIED", "RELEASE_AUTHORIZED"]
# invalidation event -> highest state still allowed afterwards (GPT 19Z)
INVALIDATE = {"source_hash_changed": "SOURCE_MISSING",
              "rights_revoked": "SOURCE_VERIFIED",
              "quote_edited": "RIGHTS_APPROVED"}
# Claude PROPOSED addition: only Timothy may authorize release (R-level, §25)
AUTHORIZER = "Timothy"

def step(state, ev):
    """Return (new_state, verdict). Fail closed on anything unexpected."""
    if state not in STATES:
        return "SOURCE_MISSING", "INVALID_STATE"
    if not isinstance(ev, dict):
        return state, "REJECT:not_dict"
    kind = ev.get("kind")
    if kind in INVALIDATE:
        cap = INVALIDATE[kind]
        new = STATES[min(STATES.index(state), STATES.index(cap))]
        return new, "INVALIDATED" if new != state else "NOOP"
    if kind != "advance":
        return state, "REJECT:unknown_kind"
    for f in ("evidence_id", "actor", "timestamp"):
        v = ev.get(f)
        if not isinstance(v, str) or not v.strip():
            return state, "REJECT:missing_" + f
    to = ev.get("to")
    if to not in STATES:
        return state, "REJECT:bad_target"
    if STATES.index(to) != STATES.index(state) + 1:
        return state, "REJECT:skip_or_back"   # no skipping, no auto-reinstate
    if to == "RELEASE_AUTHORIZED" and ev["actor"] != AUTHORIZER:
        return state, "REJECT:authorizer"
    if ev.get("from_cache") is True:
        return state, "REJECT:stale_cache"
    return to, "ADVANCED"

def adv(to, actor="Claude", **k):
    d = {"kind": "advance", "to": to, "evidence_id": "E-x", "actor": actor,
         "timestamp": "2026-11-07T19:00Z"}
    d.update(k)
    return d

FIX = [  # (label, start, events, expected final, expected last verdict)
    ("happy_path", "SOURCE_MISSING",
     [adv(s) for s in STATES[1:5]] + [adv("RELEASE_AUTHORIZED", "Timothy")],
     "RELEASE_AUTHORIZED", "ADVANCED"),
    ("non_timothy_release", "PACKAGE_VERIFIED",
     [adv("RELEASE_AUTHORIZED", "ChatGPT")], "PACKAGE_VERIFIED", "REJECT:authorizer"),
    ("skip", "SOURCE_VERIFIED", [adv("EDITORIAL_APPROVED")],
     "SOURCE_VERIFIED", "REJECT:skip_or_back"),
    ("missing_evidence", "SOURCE_VERIFIED", [adv("RIGHTS_APPROVED", evidence_id="")],
     "SOURCE_VERIFIED", "REJECT:missing_evidence_id"),
    ("rights_revoked", "PACKAGE_VERIFIED", [{"kind": "rights_revoked"}],
     "SOURCE_VERIFIED", "INVALIDATED"),
    ("hash_changed", "EDITORIAL_APPROVED", [{"kind": "source_hash_changed"}],
     "SOURCE_MISSING", "INVALIDATED"),
    ("quote_edited_low", "SOURCE_VERIFIED", [{"kind": "quote_edited"}],
     "SOURCE_VERIFIED", "NOOP"),
    ("no_auto_reinstate", "SOURCE_VERIFIED",
     [{"kind": "rights_revoked"}, adv("EDITORIAL_APPROVED")],
     "SOURCE_VERIFIED", "REJECT:skip_or_back"),
    ("stale_cache", "SOURCE_VERIFIED", [adv("RIGHTS_APPROVED", from_cache=True)],
     "SOURCE_VERIFIED", "REJECT:stale_cache"),
    ("unknown_kind", "SOURCE_VERIFIED", [{"kind": "approve_all"}],
     "SOURCE_VERIFIED", "REJECT:unknown_kind"),
    ("bad_state", "LAUNCHED", [], "SOURCE_MISSING", "INVALID_STATE"),
    # U70 as recorded in §238: sources verified, rights REVIEW -> no evidence
    ("U70_now", "SOURCE_VERIFIED", [adv("RIGHTS_APPROVED", evidence_id=None)],
     "SOURCE_VERIFIED", "REJECT:missing_evidence_id"),
]

def run(start, evs):
    s, v = start, None
    if start not in STATES:
        return step(start, {})
    for e in evs:
        s, v = step(s, e)
    return s, v

out, ok = [], 0
for lab, st, evs, ef, ev in FIX:
    s, v = run(st, evs)
    good = (s, v) == (ef, ev)
    ok += good
    out.append({"label": lab, "final": s, "verdict": v, "pass": good})
body = json.dumps(out, sort_keys=True)
print(body)
print("fixtures %d/%d %s" % (ok, len(FIX), "PASS" if ok == len(FIX) else "FAIL"))
print("in-band sha256", hashlib.sha256(body.encode()).hexdigest())
print("U70 state SOURCE_VERIFIED; release_allowed False; HOLD")
