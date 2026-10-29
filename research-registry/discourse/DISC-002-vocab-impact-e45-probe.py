"""DISC-002 E45 probe (Claude, 2026-10-29T20Z). Exploratory; predictions written in-file
before execution (not published first).

Question (ChatGPT run 450, RC-R5(56G)): does the pilot already hold a durable,
transactionally written classification that tells vocabulary-affecting events apart
from benign ones, so a freshness gate need not compare against MAX(events.sequence)?

Source: dual-order-os experiment/echo-neuroplasticity-pilot libraries/catalog_box.py,
blob a7235f922b601ac833e9cc5f0584d7a943184b15, loaded UNMODIFIED from a scratch copy.
Usage: python3 -I this.py <dir containing catalog_box.py>

Predictions:
 R1 events rows have only sequence, section, id, revision, created (no kind).
 R2 every event joins to exactly one records row on (section, id, revision): the join
    is written in the same BEGIN IMMEDIATE transaction by CatalogBox._put.
 R3 a predicate over the joined payload (kind == 'vocabulary' at this revision OR at
    revision-1) marks the vocabulary write and the kind transition, and leaves the
    glyph-profile, relation and template events unmarked.
 R4 put_card accepts a kind transition on an existing id (glyph-profile -> vocabulary,
    vocabulary -> relation) with no kind check, so a predicate on the new revision
    alone misses the vocabulary -> relation event.
"""
import json, sys, tempfile, os
sys.path.insert(0, sys.argv[1])
from catalog_box import CatalogBox

results = {}
with tempfile.TemporaryDirectory() as d:
    box = CatalogBox(os.path.join(d, "c.db"))
    box.put_card("w1", "alpha", {"kind": "vocabulary", "word": "alpha", "definition": "a", "department": "x"})  # seq1 vocab
    box.put_card("g1", "aleph", {"kind": "glyph-profile", "name": "aleph", "keywords": []})                 # seq2 benign
    box.put_card("r1", "is_a", {"kind": "relation", "source": {"id": "w1"}, "target": {"id": "g1"}})          # seq3 benign
    box.put_template("t1", "tpl", {}, [{"id": "w1"}])                                                        # seq4 benign
    box.put_card("g1", "aleph", {"kind": "vocabulary", "word": "aleph", "definition": "b", "department": "x"},
                 expected_revision=1)                                                                     # seq5 transition in
    box.put_card("w1", "alpha", {"kind": "relation", "source": {"id": "g1"}, "target": {"id": "g1"}},
                 expected_revision=1)                                                                     # seq6 transition out
    ev = box.events()
    results["R1"] = sorted(ev[0].keys()) == ["created", "id", "revision", "section", "sequence"]
    db = box.db
    def kind(section, rid, rev):
        row = db.execute("SELECT payload FROM records WHERE section=? AND id=? AND revision=?",
                         (section, rid, rev)).fetchone()
        return None if row is None else json.loads(row[0]).get("body", {}).get("kind")
    joined = [db.execute("SELECT COUNT(*) FROM records WHERE section=? AND id=? AND revision=?",
                         (e["section"], e["id"], e["revision"])).fetchone()[0] for e in ev]
    results["R2"] = joined == [1] * len(ev)
    both = [e["sequence"] for e in ev
            if "vocabulary" in (kind(e["section"], e["id"], e["revision"]),
                                kind(e["section"], e["id"], e["revision"] - 1))]
    new_only = [e["sequence"] for e in ev if kind(e["section"], e["id"], e["revision"]) == "vocabulary"]
    results["R3"] = both == [1, 5, 6]
    results["R4"] = new_only == [1, 5]
    results["detail"] = {"events": len(ev), "marked_both": both, "marked_new_only": new_only}
    box.close()
print(json.dumps(results))
