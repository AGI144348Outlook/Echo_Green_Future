#!/usr/bin/env python3
"""DISC-002 E47 (Claude, 2026-10-29 23Z) -- ChatGPT run 453's N9: a writer commits between the
freshness gate and the gated mutation.

Exploratory, NOT pre-registered (predictions written here before the first run, not published first).
Loads dual-order-os pilot libraries/catalog_box.py blob a7235f9 UNMODIFIED from a path given on the
command line; no Genesis, no EchoWorkspace, no network. Scratch SQLite files in a temp dir.

SOURCE-OBSERVED (catalog_box.py a7235f9): CatalogBox._put already does a per-RECORD compare-and-set
(expected_revision vs MAX(revision) for that id) inside its own BEGIN IMMEDIATE. The question is
whether that is enough for a VIEW-level freshness contract (56G-a stamp), and whether a caller can
add a view check from outside without changing _put.

GuardedBox below is a PROBE-LOCAL candidate shape, not a pilot change: it copies _put's body and adds
one line, a precondition evaluated after BEGIN IMMEDIATE (so under the writer lock).

Predictions:
 P1 gate reads stamp S (fresh); B adds vocabulary word w2; A put_card(w3, expected_revision=0) on the
    unmodified box COMMITS: record CAS cannot see view staleness (N9 hazard is real).       -> True
 P2 a caller cannot wrap put_card in its own BEGIN IMMEDIATE to add the view check: SQLite raises
    'cannot start a transaction within a transaction' (_put opens its own).                 -> True
 P3 GuardedBox with precondition stamp()==S inside the lock REFUSES after B's vocabulary write, and
    the refused write leaves no record and no event.                                       -> True
 P4 control: B writes a TEMPLATE instead; GuardedBox's guarded put COMMITS (benign write does not
    invalidate the vocabulary view).                                                        -> True
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
def has(box, i):
    # harness fix after first run: CatalogBox.get raises KeyError for a missing id (it never returns None)
    try:
        box.get("cards", i); return True
    except KeyError:
        return False
def vocab(w): return {"kind": "vocabulary", "word": w, "definition": "d", "department": "x"}


class StaleView(Exception):
    pass


class GuardedBox(cb.CatalogBox):
    """Probe-local: _put copied from a7235f9 with one added precondition check under the lock."""
    precondition = None

    def _put(self, section, record_id, title, payload, expected_revision, glyph=None):
        self._id(record_id)
        self._revision(expected_revision, allow_zero=True)
        result = dict(payload, id=record_id, revision=expected_revision + 1,
                      section=section, title=title, glyph=glyph)
        encoded = self._json(result)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            if self.precondition is not None and not self.precondition(self):   # added line
                raise StaleView("view stamp moved")
            current = self.db.execute(
                "SELECT MAX(revision) FROM records WHERE section=? AND id=?",
                (section, record_id)).fetchone()[0] or 0
            if current != expected_revision:
                raise cb.Conflict(f"Expected revision {expected_revision}; current revision is {current}")
            self.db.execute("INSERT INTO records VALUES(?,?,?,?,?,?)",
                            (section, record_id, current + 1, glyph, title, encoded))
            self.db.execute("INSERT INTO events(section,id,revision) VALUES(?,?,?)",
                            (section, record_id, current + 1))
            self.db.execute("COMMIT")
        except BaseException:
            self.db.execute("ROLLBACK")
            raise
        return json.loads(encoded)


def pair(tmp, name, cls_a=cb.CatalogBox):
    path = os.path.join(tmp, name)
    a, b = cls_a(path), cb.CatalogBox(path)
    a.put_card("w1", "alpha", vocab("alpha"))
    return a, b

out, detail = {}, {}
with tempfile.TemporaryDirectory() as tmp:
    # P1
    a, b = pair(tmp, "p1.db")
    s = stamp(a)                                   # gate: fresh
    b.put_card("w2", "beta", vocab("beta"))        # writer between gate and mutation
    a.put_card("w3", "gamma", vocab("gamma"))      # gated mutation, record CAS only
    out["P1"] = stamp(a) > s and has(a, "w3")
    # P2
    a, b = pair(tmp, "p2.db")
    a.db.execute("BEGIN IMMEDIATE")
    try:
        a.put_card("w3", "gamma", vocab("gamma")); nested = "no error"
    except sqlite3.OperationalError as e:
        nested = str(e)
    a.db.execute("ROLLBACK")
    detail["p2_error"] = nested
    out["P2"] = "within a transaction" in nested
    # P3
    a, b = pair(tmp, "p3.db", GuardedBox)
    s = stamp(a); a.precondition = lambda box, s=s: stamp(box) == s
    b.put_card("w2", "beta", vocab("beta"))
    try:
        a.put_card("w3", "gamma", vocab("gamma")); refused = False
    except StaleView:
        refused = True
    n_events = len(a.events())
    out["P3"] = refused and not has(a, "w3") and n_events == 2
    detail["p3_events"] = n_events
    # P4
    a, b = pair(tmp, "p4.db", GuardedBox)
    s = stamp(a); a.precondition = lambda box, s=s: stamp(box) == s
    b.put_template("t1", "T", {"k": 1}, [])
    a.put_card("w3", "gamma", vocab("gamma"))
    out["P4"] = has(a, "w3")
    detail["sqlite"] = sqlite3.sqlite_version
print(json.dumps({**out, "detail": detail}))
sys.exit(0 if all(out.values()) else 1)
