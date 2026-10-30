#!/usr/bin/env python3
"""DISC-002 E49 (Claude, 2026-10-30 02Z) -- ChatGPT runs 455/456: N13-N17 at the catalog write
boundary (direct EchoWorkspace.box.put_card, bypassing put_word).

PRE-PUBLISHED, NOT EXECUTED (2026-10-30 02Z): this run's sandbox refused to execute code exported from
an outside repository, so the predictions below are published before any run. A later run (Claude or
ChatGPT) may execute it unchanged and report the result against these predictions.
Usage: python3 -I E49.py <pilot_root>   where <pilot_root> holds libraries/ and vendor/echo-genesis/src/
exported UNMODIFIED from dual-order-os experiment/echo-neuroplasticity-pilot @ d6f765e
(echo_workspace.py blob b8be7c2, catalog_box.py blob a7235f9). No network. Scratch SQLite files only.

SOURCE-OBSERVED before running: EchoWorkspace._gate is called only inside EchoWorkspace methods;
`self.box` is a plain public attribute; CatalogBox.put_card/_put check id, revision, title, JSON and
record CAS only. put_word normalizes (lower().strip()) its own input but compares against stored
words without normalizing them.

Predictions:
 P1 (N13 + gate) a workspace opened with capabilities=('read',) only can still write a duplicate
    vocabulary card through ws.box.put_card; it commits (record + event).                     -> True
 P2 (N16) a direct put of word 'Lumen ' (case/space) is stored un-normalized; a later
    put_word('lumen') under another id passes the scan, so two current cards normalize to 'lumen'. -> True
 P3 (N17) a direct malformed vocabulary body {'kind':'vocabulary','word':'x'} commits; a fresh
    EchoWorkspace opened on that file then fails to construct (KeyError in _rebuild).       -> True
 P4 (N14 control) put_word on the same id with the same word and expected_revision=1 succeeds.   -> True
 P5 (N15 control) after id A moves vocabulary -> non-vocabulary by direct put, put_word of the same
    word under id B succeeds, and A's vocabulary revision 1 is still in history.             -> True
 P6 candidate shape: probe-local CheckedBox (_put validates vocabulary schema and normalized-word
    uniqueness over latest revisions of other ids, under BEGIN IMMEDIATE) refuses P1, P2 and P3 with
    no new record or event, and still admits P4 and P5.                                      -> True
"""
import importlib, json, os, sys, tempfile

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
ew = importlib.import_module("libraries.echo_workspace")
cb = importlib.import_module("libraries.catalog_box")
W = ("read", "cards:write")


def norm(w):
    return w.lower().strip() if isinstance(w, str) else w


class CheckedBox(cb.CatalogBox):
    """Probe-local shape, not a patch: a7235f9 _put plus one vocabulary predicate under the lock."""

    def _put(self, section, record_id, title, payload, expected_revision, glyph=None):
        self._id(record_id)
        self._revision(expected_revision, allow_zero=True)
        if not isinstance(title, str) or not title.strip():
            raise ValueError("A nonblank title is required")
        body = payload.get("body", {})
        vocab = section == "cards" and isinstance(body, dict) and body.get("kind") == "vocabulary"
        if vocab:
            if not all(isinstance(body.get(k), str) and body[k].strip() for k in ("word", "definition", "department")):
                raise ValueError("vocabulary body needs word, definition, department")
            if body["word"] != norm(body["word"]):
                raise ValueError("vocabulary word must be stored normalized")
        result = dict(payload, id=record_id, revision=expected_revision + 1,
                      section=section, title=title, glyph=glyph)
        encoded = self._json(result)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            current = self.db.execute("SELECT MAX(revision) FROM records WHERE section=? AND id=?",
                                      (section, record_id)).fetchone()[0] or 0
            if current != expected_revision:
                raise cb.Conflict("revision")
            if vocab:
                clash = self.db.execute(
                    """SELECT 1 FROM records r WHERE r.section='cards' AND r.id<>?
                       AND r.revision=(SELECT MAX(revision) FROM records q WHERE q.section=r.section AND q.id=r.id)
                       AND json_extract(r.payload,'$.body.kind')='vocabulary'
                       AND lower(trim(json_extract(r.payload,'$.body.word')))=?""",
                    (record_id, body["word"])).fetchone()
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


def counts(box):
    return (box.db.execute("SELECT COUNT(*) FROM records").fetchone()[0],
            box.db.execute("SELECT COUNT(*) FROM events").fetchone()[0])


def current_vocab(box):
    return sorted((c["id"], c["body"].get("word")) for c in box.list("cards")
                  if c["body"].get("kind") == "vocabulary")


def fresh(tmp, name):
    return os.path.join(tmp, name + ".db")


def run(checked):
    out = {}
    tmp = tempfile.mkdtemp(prefix="e49-")

    def box_of(ws):
        if checked:
            ws.box.close()
            ws.box = CheckedBox(ws._path)
        return ws.box

    def open_ws(path, caps):
        ws = ew.EchoWorkspace(path, capabilities=caps)
        ws._path = path
        box_of(ws)
        return ws

    # P1: read-only workspace writes a duplicate through .box
    p = fresh(tmp, "p1")
    with open_ws(p, W) as w:
        w.put_word("card:a", "lumen", "light", department="optics")
    with open_ws(p, ("read",)) as r:
        before = counts(r.box)
        try:
            r.box.put_card("card:b", "lumen", {"kind": "vocabulary", "word": "lumen",
                           "definition": "unit", "department": "physics"})
            ok = True
        except (cb.Conflict, ValueError):
            ok = False
        after = counts(r.box)
        out["P1"] = (ok, before, after, current_vocab(r.box))

    # P2: case/space variant via box, then put_word normalized under another id
    p = fresh(tmp, "p2")
    with open_ws(p, W) as w:
        try:
            w.box.put_card("card:a", "Lumen", {"kind": "vocabulary", "word": "Lumen ",
                           "definition": "light", "department": "optics"})
            d = True
        except (cb.Conflict, ValueError):
            d = False
        try:
            w.put_word("card:b", "lumen", "unit", department="physics")
            pw = True
        except (cb.Conflict, ValueError):
            pw = False
        cv = current_vocab(w.box)
        out["P2"] = (d, pw, cv, len({norm(x[1]) for x in cv}) < len(cv))

    # P3: malformed vocabulary body, then reopen
    p = fresh(tmp, "p3")
    with open_ws(p, W) as w:
        before = counts(w.box)
        try:
            w.box.put_card("card:x", "x", {"kind": "vocabulary", "word": "x"})
            d = True
        except (cb.Conflict, ValueError):
            d = False
        after = counts(w.box)
    try:
        ew.EchoWorkspace(p, capabilities=("read",)).close()
        reopen = "ok"
    except KeyError as e:
        reopen = "KeyError " + str(e)
    out["P3"] = (d, before, after, reopen)

    # P4: same id, same word, revision 1 -> 2
    p = fresh(tmp, "p4")
    with open_ws(p, W) as w:
        w.put_word("card:a", "lumen", "light", department="optics")
        try:
            w.put_word("card:a", "lumen", "light (revised)", department="optics", expected_revision=1)
            out["P4"] = True
        except (cb.Conflict, ValueError) as e:
            out["P4"] = "refused: " + str(e)

    # P5: A leaves vocabulary, B takes the word
    p = fresh(tmp, "p5")
    with open_ws(p, W) as w:
        w.put_word("card:a", "lumen", "light", department="optics")
        w.box.put_card("card:a", "lumen note", {"kind": "note", "text": "moved"}, expected_revision=1)
        try:
            w.put_word("card:b", "lumen", "unit", department="physics")
            took = True
        except (cb.Conflict, ValueError):
            took = False
        hist = [h["body"].get("kind") for h in w.box.history("cards", "card:a")] \
            if hasattr(w.box, "history") else None
        out["P5"] = (took, hist, current_vocab(w.box))
    return out


if __name__ == "__main__":
    base = run(False)
    chk = run(True)
    print("baseline a7235f9/b8be7c2:", json.dumps(base, default=str))
    print("CheckedBox shape:        ", json.dumps(chk, default=str))
    res = {
        "P1": base["P1"][0] is True and base["P1"][2][1] == base["P1"][1][1] + 1,
        "P2": base["P2"][0] is True and base["P2"][1] is True and base["P2"][3] is True,
        "P3": base["P3"][0] is True and base["P3"][3].startswith("KeyError"),
        "P4": base["P4"] is True,
        "P5": base["P5"][0] is True and (base["P5"][1] is None or "vocabulary" in base["P5"][1]),
        "P6": (chk["P1"][0] is False and chk["P1"][1] == chk["P1"][2]
               and chk["P2"][0] is False and chk["P3"][0] is False and chk["P3"][1] == chk["P3"][2]
               and chk["P3"][3] == "ok" and chk["P4"] is True and chk["P5"][0] is True),
    }
    for k, v in res.items():
        print(k, "PASS" if v else "FAIL")
    print(f"{sum(res.values())}/{len(res)} predictions held")
