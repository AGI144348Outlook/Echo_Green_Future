#!/usr/bin/env python3
"""DISC-002 E48 (Claude, 2026-10-30 00Z) -- ChatGPT run 454's N12: two writers insert the same
normalized vocabulary word under different card ids; both pass put_word's duplicate scan.

Exploratory, NOT pre-registered (predictions written here before the first run, not published first).
Usage: python3 -I E48.py <pilot_root>   where <pilot_root> holds libraries/ and vendor/echo-genesis/src/
exported UNMODIFIED from dual-order-os experiment/echo-neuroplasticity-pilot (echo_workspace.py blob
b8be7c2, catalog_box.py blob a7235f9, Genesis blob 63eb982 checked by echo_workspace.genesis()).
No network. Scratch SQLite file in a temp dir; two EchoWorkspace objects = two connections.

Interleaving: A.put_word runs its duplicate scan (echo_workspace.py lines 112-114), then calls
box.put_card. A probe hook on A's box runs B.put_word to completion at that point (after A's scan,
before A's BEGIN IMMEDIATE), then lets A's put_card continue. This is a deterministic stand-in for
two processes; it does not exercise real thread timing.

SOURCE-OBSERVED: the scan reads self.box.list('cards') outside any transaction; CatalogBox._put's
check covers (section, id, revision) only; the schema has no unique constraint on the word.

Predictions:
 P1 same word, different ids, interleaved: BOTH put_word calls return; the store then holds two
    vocabulary cards with word 'lumen' (N12 hazard is real).                               -> True
 P2 a fresh EchoWorkspace opened on that file rebuilds without error, i.e. nothing downstream
    rejects the duplicate.                                                                 -> True
 P3 control, sequential: same word, different id, second put_word raises Conflict.        -> True
 P4 control, same id, interleaved, both expected_revision=0: A's put raises Conflict (record CAS),
    one card stored.                                                                       -> True
 P5 control, distinct words interleaved: both commit, two cards.                          -> True
 P6 candidate shape: A's box swapped to a probe-local GuardedBox whose _put re-runs the word check
    AFTER BEGIN IMMEDIATE (under the writer lock); in the P1 interleaving A is refused, one card,
    no extra event.                                                                        -> True
"""
import importlib, json, os, sys, tempfile

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
ew = importlib.import_module("libraries.echo_workspace")
cb = importlib.import_module("libraries.catalog_box")

CAPS = ("read", "cards:write")


def vocab_words(path):
    with ew.EchoWorkspace(path, capabilities=("read",)) as c:
        return sorted((x["id"], x["body"]["word"]) for x in c.box.list("cards")
                      if x["body"].get("kind") == "vocabulary")


def events(ws):
    return ws.box.db.execute("SELECT COUNT(*) FROM events").fetchone()[0]


class GuardedBox(cb.CatalogBox):
    """Probe-local: a7235f9 _put with one added word-uniqueness check under the writer lock.
    Conflict path kept; title validation kept, glyph validation omitted (docstring corrected after
    the first run, code unchanged). A shape, not a patch."""

    def _put(self, section, record_id, title, payload, expected_revision, glyph=None):
        self._id(record_id)
        self._revision(expected_revision, allow_zero=True)
        if not isinstance(title, str) or not title.strip():
            raise ValueError("A nonblank title is required")
        result = dict(payload, id=record_id, revision=expected_revision + 1,
                      section=section, title=title, glyph=glyph)
        encoded = self._json(result)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            current = self.db.execute(
                "SELECT MAX(revision) FROM records WHERE section=? AND id=?",
                (section, record_id)).fetchone()[0] or 0
            if current != expected_revision:
                raise cb.Conflict("revision")
            body = payload.get("body", {})
            if section == "cards" and body.get("kind") == "vocabulary":
                clash = self.db.execute(
                    """SELECT 1 FROM records r WHERE r.section='cards' AND r.id<>?
                       AND r.revision=(SELECT MAX(revision) FROM records q WHERE q.section=r.section AND q.id=r.id)
                       AND json_extract(r.payload,'$.body.kind')='vocabulary'
                       AND json_extract(r.payload,'$.body.word')=?""",
                    (record_id, body.get("word"))).fetchone()
                if clash:
                    raise cb.Conflict("word already has a catalog identity (checked under lock)")
            self.db.execute("INSERT INTO records VALUES(?,?,?,?,?,?)",
                            (section, record_id, current + 1, glyph, title, encoded))
            self.db.execute("INSERT INTO events(section,id,revision) VALUES(?,?,?)",
                            (section, record_id, current + 1))
            self.db.execute("COMMIT")
        except BaseException:
            self.db.execute("ROLLBACK")
            raise
        return json.loads(encoded)


def interleave(path, a_args, b_args, guarded=False):
    """A scans, then B runs to completion, then A's put_card proceeds."""
    a = ew.EchoWorkspace(path, capabilities=CAPS)
    b = ew.EchoWorkspace(path, capabilities=CAPS)
    if guarded:
        a.box.__class__ = GuardedBox
    real = a.box.put_card
    out = {}

    def hooked(*args, **kw):
        out["b"] = b.put_word(*b_args)
        return real(*args, **kw)

    a.box.put_card = hooked
    try:
        out["a"] = a.put_word(*a_args)
    except cb.Conflict as e:
        out["a_conflict"] = str(e)
    out["events"] = events(a)
    a.close(); b.close()
    return out


def fresh(tmp, name):
    return os.path.join(tmp, name + ".sqlite")


res, detail = {}, {}
with tempfile.TemporaryDirectory() as tmp:
    p = fresh(tmp, "p1")
    o = interleave(p, ("vocab:a", "Lumen", "light (A)"), ("vocab:b", "lumen", "light (B)"))
    w = vocab_words(p)
    res["P1"] = "a" in o and "b" in o and [x[1] for x in w] == ["lumen", "lumen"]
    detail["P1"] = {"stored": w, "a_conflict": o.get("a_conflict")}

    try:
        with ew.EchoWorkspace(p, capabilities=("read",)) as c:
            res["P2"] = True
            detail["P2"] = {"rebuild": "ok", "lobby_agents": len(c.lobby.agents or [])}
    except Exception as e:  # noqa
        res["P2"] = False; detail["P2"] = repr(e)

    p = fresh(tmp, "p3")
    with ew.EchoWorkspace(p, capabilities=CAPS) as s:
        s.put_word("vocab:a", "lumen", "light (A)")
        try:
            s.put_word("vocab:b", "lumen", "light (B)"); res["P3"] = False
        except cb.Conflict:
            res["P3"] = True
    detail["P3"] = vocab_words(p)

    p = fresh(tmp, "p4")
    o = interleave(p, ("vocab:a", "lumen", "light (A)"), ("vocab:a", "lumen", "light (B)"))
    w = vocab_words(p)
    res["P4"] = "a_conflict" in o and len(w) == 1
    detail["P4"] = {"stored": w, "a_conflict": o.get("a_conflict")}

    p = fresh(tmp, "p5")
    o = interleave(p, ("vocab:a", "lumen", "light"), ("vocab:b", "umbra", "shade"))
    w = vocab_words(p)
    res["P5"] = "a" in o and "b" in o and len(w) == 2
    detail["P5"] = w

    p = fresh(tmp, "p6")
    o = interleave(p, ("vocab:a", "lumen", "light (A)"), ("vocab:b", "lumen", "light (B)"), guarded=True)
    w = vocab_words(p)
    res["P6"] = "a_conflict" in o and w == [("vocab:b", "lumen")] and o["events"] == 1
    detail["P6"] = {"stored": w, "a_conflict": o.get("a_conflict"), "events": o["events"]}

import sqlite3
print(json.dumps({"result": res, "detail": detail, "sqlite": sqlite3.sqlite_version}, indent=1))
sys.exit(0 if all(res.values()) else 1)
