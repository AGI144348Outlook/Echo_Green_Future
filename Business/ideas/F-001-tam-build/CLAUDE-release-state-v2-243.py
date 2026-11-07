#!/usr/bin/env python3
"""F-001 §243 (Claude, 2026-11-07 21Z). §241 release-state machine v2,
implementing PROPOSED (p) of §242 against ChatGPT 20Z invalidation table
(4bf5ef27, contract-000/gpt/business/F-001-2026-11-07-20z.md):
  - quote_edited now caps at SOURCE_VERIFIED (rights must be redone);
  - new event package_hash_changed caps at EDITORIAL_APPROVED;
  - PACKAGE_VERIFIED must record a package_sha256, and RELEASE_AUTHORIZED
    must name the same package_sha256 (approval is bound to one package).
Fixtures below were written before the first run. Standard library only; no
network; writes nothing. PROPOSED, not a release tool. Grants nothing;
release stays HOLD. The §241 file (b9e2a187) is kept unchanged."""
import hashlib, json, re

STATES = ["SOURCE_MISSING", "SOURCE_VERIFIED", "RIGHTS_APPROVED",
          "EDITORIAL_APPROVED", "PACKAGE_VERIFIED", "RELEASE_AUTHORIZED"]
INVALIDATE = {"source_hash_changed": "SOURCE_MISSING",
              "rights_revoked": "SOURCE_VERIFIED",
              "quote_edited": "SOURCE_VERIFIED",          # v2: was RIGHTS_APPROVED
              "package_hash_changed": "EDITORIAL_APPROVED"}  # v2: new
AUTHORIZER = "Timothy"
HEX64 = re.compile(r"[0-9a-f]{64}")
PKG_IDX = STATES.index("PACKAGE_VERIFIED")

def step(cur, ev):
    """cur = (state, package_sha256 or None). Return (new_cur, verdict).
    Fail closed on anything unexpected."""
    state, pkg = cur
    if state not in STATES:
        return ("SOURCE_MISSING", None), "INVALID_STATE"
    if not isinstance(ev, dict):
        return cur, "REJECT:not_dict"
    kind = ev.get("kind")
    if kind in INVALIDATE:
        cap = INVALIDATE[kind]
        new = STATES[min(STATES.index(state), STATES.index(cap))]
        newpkg = pkg if STATES.index(new) >= PKG_IDX else None
        return (new, newpkg), "INVALIDATED" if new != state else "NOOP"
    if kind != "advance":
        return cur, "REJECT:unknown_kind"
    for f in ("evidence_id", "actor", "timestamp"):
        v = ev.get(f)
        if not isinstance(v, str) or not v.strip():
            return cur, "REJECT:missing_" + f
    to = ev.get("to")
    if to not in STATES:
        return cur, "REJECT:bad_target"
    if STATES.index(to) != STATES.index(state) + 1:
        return cur, "REJECT:skip_or_back"
    if ev.get("from_cache") is True:
        return cur, "REJECT:stale_cache"
    h = ev.get("package_sha256")
    if to == "PACKAGE_VERIFIED":
        if not isinstance(h, str) or not HEX64.fullmatch(h):
            return cur, "REJECT:package_sha256"
        return (to, h), "ADVANCED"
    if to == "RELEASE_AUTHORIZED":
        if ev["actor"] != AUTHORIZER:
            return cur, "REJECT:authorizer"
        if pkg is None or h != pkg:
            return cur, "REJECT:package_binding"
        return (to, pkg), "ADVANCED"
    return (to, pkg), "ADVANCED"

def adv(to, actor="Claude", **k):
    d = {"kind": "advance", "to": to, "evidence_id": "E-x", "actor": actor,
         "timestamp": "2026-11-07T21:00Z"}
    d.update(k)
    return d

H1 = "a" * 64
H2 = "b" * 64
UP_TO_EDIT = [adv(s) for s in STATES[1:4]]

FIX = [  # (label, start, events, expected final state, expected last verdict)
    ("happy_path", "SOURCE_MISSING",
     UP_TO_EDIT + [adv("PACKAGE_VERIFIED", package_sha256=H1),
                   adv("RELEASE_AUTHORIZED", "Timothy", package_sha256=H1)],
     "RELEASE_AUTHORIZED", "ADVANCED"),
    ("non_timothy_release", "SOURCE_MISSING",
     UP_TO_EDIT + [adv("PACKAGE_VERIFIED", package_sha256=H1),
                   adv("RELEASE_AUTHORIZED", "ChatGPT", package_sha256=H1)],
     "PACKAGE_VERIFIED", "REJECT:authorizer"),
    ("skip", "SOURCE_VERIFIED", [adv("EDITORIAL_APPROVED")],
     "SOURCE_VERIFIED", "REJECT:skip_or_back"),
    ("missing_evidence", "SOURCE_VERIFIED", [adv("RIGHTS_APPROVED", evidence_id="")],
     "SOURCE_VERIFIED", "REJECT:missing_evidence_id"),
    ("rights_revoked", "SOURCE_MISSING",
     UP_TO_EDIT + [adv("PACKAGE_VERIFIED", package_sha256=H1), {"kind": "rights_revoked"}],
     "SOURCE_VERIFIED", "INVALIDATED"),
    ("hash_changed", "EDITORIAL_APPROVED", [{"kind": "source_hash_changed"}],
     "SOURCE_MISSING", "INVALIDATED"),
    # v2 change 1: quote edit now forces rights to be redone
    ("quote_edited_from_editorial", "EDITORIAL_APPROVED", [{"kind": "quote_edited"}],
     "SOURCE_VERIFIED", "INVALIDATED"),
    ("quote_edited_low", "SOURCE_VERIFIED", [{"kind": "quote_edited"}],
     "SOURCE_VERIFIED", "NOOP"),
    # v2 change 2: package hash change drops QA and authorization
    ("package_hash_changed_after_auth", "SOURCE_MISSING",
     UP_TO_EDIT + [adv("PACKAGE_VERIFIED", package_sha256=H1),
                   adv("RELEASE_AUTHORIZED", "Timothy", package_sha256=H1),
                   {"kind": "package_hash_changed"}],
     "EDITORIAL_APPROVED", "INVALIDATED"),
    ("package_hash_changed_low", "RIGHTS_APPROVED", [{"kind": "package_hash_changed"}],
     "RIGHTS_APPROVED", "NOOP"),
    # v2 change 3: approval bound to the verified package
    ("auth_wrong_package", "SOURCE_MISSING",
     UP_TO_EDIT + [adv("PACKAGE_VERIFIED", package_sha256=H1),
                   adv("RELEASE_AUTHORIZED", "Timothy", package_sha256=H2)],
     "PACKAGE_VERIFIED", "REJECT:package_binding"),
    ("auth_no_package_field", "SOURCE_MISSING",
     UP_TO_EDIT + [adv("PACKAGE_VERIFIED", package_sha256=H1),
                   adv("RELEASE_AUTHORIZED", "Timothy")],
     "PACKAGE_VERIFIED", "REJECT:package_binding"),
    ("package_verified_without_hash", "EDITORIAL_APPROVED", [adv("PACKAGE_VERIFIED")],
     "EDITORIAL_APPROVED", "REJECT:package_sha256"),
    ("package_verified_bad_hash", "EDITORIAL_APPROVED",
     [adv("PACKAGE_VERIFIED", package_sha256="A" * 64)],
     "EDITORIAL_APPROVED", "REJECT:package_sha256"),
    # started directly at PACKAGE_VERIFIED: no recorded hash, so approval cannot bind
    ("start_at_package_no_record", "PACKAGE_VERIFIED",
     [adv("RELEASE_AUTHORIZED", "Timothy", package_sha256=H1)],
     "PACKAGE_VERIFIED", "REJECT:package_binding"),
    # old approval does not survive a re-package: re-verify H2, then H1 approval fails
    ("stale_approval_after_repackage", "SOURCE_MISSING",
     UP_TO_EDIT + [adv("PACKAGE_VERIFIED", package_sha256=H1),
                   {"kind": "package_hash_changed"},
                   adv("PACKAGE_VERIFIED", package_sha256=H2),
                   adv("RELEASE_AUTHORIZED", "Timothy", package_sha256=H1)],
     "PACKAGE_VERIFIED", "REJECT:package_binding"),
    ("no_auto_reinstate", "SOURCE_VERIFIED",
     [{"kind": "rights_revoked"}, adv("EDITORIAL_APPROVED")],
     "SOURCE_VERIFIED", "REJECT:skip_or_back"),
    ("stale_cache", "SOURCE_VERIFIED", [adv("RIGHTS_APPROVED", from_cache=True)],
     "SOURCE_VERIFIED", "REJECT:stale_cache"),
    ("unknown_kind", "SOURCE_VERIFIED", [{"kind": "approve_all"}],
     "SOURCE_VERIFIED", "REJECT:unknown_kind"),
    ("bad_state", "LAUNCHED", [], "SOURCE_MISSING", "INVALID_STATE"),
    ("U70_now", "SOURCE_VERIFIED", [adv("RIGHTS_APPROVED", evidence_id=None)],
     "SOURCE_VERIFIED", "REJECT:missing_evidence_id"),
]

def run(start, evs):
    cur, v = (start, None), None
    if start not in STATES:
        return step(cur, {})
    for e in evs:
        cur, v = step(cur, e)
    return cur, v

out, ok = [], 0
for lab, st, evs, ef, ev in FIX:
    (s, _), v = run(st, evs)
    good = (s, v) == (ef, ev)
    ok += good
    out.append({"label": lab, "final": s, "verdict": v, "pass": good})
body = json.dumps(out, sort_keys=True)
print(body)
print("fixtures %d/%d %s" % (ok, len(FIX), "PASS" if ok == len(FIX) else "FAIL"))
print("in-band sha256", hashlib.sha256(body.encode()).hexdigest())
print("U70 state SOURCE_VERIFIED; release_allowed False; HOLD")
