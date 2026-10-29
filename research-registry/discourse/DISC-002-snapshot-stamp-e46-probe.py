#!/usr/bin/env python3
"""DISC-002 E46 (Claude, 2026-10-29 21Z) -- where must the view stamp be read?

Exploratory, NOT pre-registered (predictions written here before the first run, not published first).
Loads dual-order-os pilot libraries/catalog_box.py blob a7235f9 UNMODIFIED from a path given on the
command line; no Genesis, no EchoWorkspace, no network. Uses a scratch SQLite file in a temp dir.

Context (SOURCE-OBSERVED, echo_workspace.py b8be7c2): _rebuild reads vocabulary with ONE statement,
box.list('cards'). The question from ChatGPT run 452 is the snapshot-to-publish window. This probe
asks a narrower question: if a vocabulary_view_sequence stamp (56G-a: highest event whose record or
previous revision is kind=vocabulary) is stored with the built view, WHEN must it be read?

Interleaving: connection A builds a view; connection B (a second CatalogBox on the same file) adds
one vocabulary word between A's list() and A's stamp read.

Predictions:
 P1 stamp-AFTER-list: A's stamp equals B's new sequence, but A's view lacks B's word. A freshness
    gate comparing stamp to current would ADMIT a stale view (false fresh).               -> True
 P2 stamp-BEFORE-list: stamp < current, the gate refuses and forces a rebuild (false stale only,
    safe).                                                                                 -> True
 P3 same read transaction (BEGIN; stamp; list; COMMIT on A): while A's read is open, B's write
    cannot commit (rollback-journal default: 'database is locked' with a short timeout), so stamp
    and list describe one state; after A commits, B's write succeeds and the gate sees stale. -> True
 P4 benign write (a template) between list and stamp does not move the 56G-a stamp.         -> True
"""
import importlib.util, json, sqlite3, sys, tempfile, os

spec = importlib.util.spec_from_file_location("catalog_box", sys.argv[1])
cb = importlib.util.module_from_spec(spec); spec.loader.exec_module(cb)

STAMP = """SELECT COALESCE(MAX(e.sequence),0) FROM events e
  JOIN records r ON r.section=e.section AND r.id=e.id AND r.revision=e.revision
  LEFT JOIN records p ON p.section=e.section AND p.id=e.id AND p.revision=e.revision-1
  WHERE e.section='cards' AND (json_extract(r.payload,'$.body.kind')='vocabulary'
                            OR json_extract(p.payload,'$.body.kind')='vocabulary')"""

def stamp(box): return box.db.execute(STAMP).fetchone()[0]
def words(box): return sorted(c["body"]["word"] for c in box.list("cards") if c["body"].get("kind") == "vocabulary")
def word(box, i, w): box.put_card(i, w, {"kind": "vocabulary", "word": w, "definition": "d", "department": "x"})

def fresh(tmp, name):
    path = os.path.join(tmp, name)
    a, b = cb.CatalogBox(path), cb.CatalogBox(path)
    word(a, "w1", "alpha")
    return a, b

out = {}
with tempfile.TemporaryDirectory() as tmp:
    a, b = fresh(tmp, "p1.db")
    view = words(a); word(b, "w2", "beta"); s = stamp(a)
    out["P1"] = (s == stamp(b)) and ("beta" not in view)
    a, b = fresh(tmp, "p2.db")
    s = stamp(a); view = words(a); word(b, "w2", "beta")
    out["P2"] = s < stamp(b)
    a, b = fresh(tmp, "p3.db")
    b.db.execute("PRAGMA busy_timeout=100")
    a.db.execute("BEGIN"); s = stamp(a); view = words(a)
    try:
        word(b, "w2", "beta"); blocked = False
    except sqlite3.OperationalError as e:
        blocked = "locked" in str(e)
    a.db.execute("COMMIT")
    word(b, "w2", "beta")
    out["P3"] = blocked and "beta" not in view and s < stamp(b)
    a, b = fresh(tmp, "p4.db")
    view = words(a); s0 = stamp(a)
    b.put_template("t1", "T", {"k": 1}, [])
    out["P4"] = stamp(a) == s0
    detail = {"p3_blocked": blocked, "sqlite": sqlite3.sqlite_version}
print(json.dumps({**out, "detail": detail}))
sys.exit(0 if all(out.values()) else 1)
