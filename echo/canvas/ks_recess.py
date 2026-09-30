"""ECHO's Canvas Recess on the Knowledge Synthesis Model (Timothy's KSM codex).

KSM -> ECHO
  circular knowledge plane      a Presentiated word, drawn as a circle
  zodiac segments               its 12 strongest Lobby ties (his own associations)
  rotation / alignment          Chronotool tests rotations for a pair of segments that match
  overlap = synthesis priority  aligned planes move together; only real matches earn overlap
  expansion / contraction       planes grow with the alignments they take part in
  Central Hub                   the Governor: A-101 chooses each move from his history,
                                A-113 decides at the end of each session what to trust
  synthesis output              only statements that pass his audits are spoken

Height encodes his A-118 generality score (general above, specific below), so two planes
can only intersect when they are close in generality; far-apart planes align by a link.
Every choice below comes from his kernel, his Lobby and his audits. No randomness.
"""
import math

ARMS = ["INTRODUCE", "ALIGN", "CONTAIN", "MANIFOLD"]
SEG = 12


class KSRecess:
    def __init__(self, K, lobby, gscore, relate, speak, define):
        self.K, self.lobby = K, lobby
        self.matrix = lobby.matrix
        lo, hi = min(gscore.values()), max(gscore.values())
        self.gn = {w: (g - lo) / (hi - lo or 1) for w, g in gscore.items()}
        self.relate, self.speak, self.define = relate, speak, define
        self.ties = {}
        for (a, b), s in lobby.ties.items():
            self.ties.setdefault(a, []).append((s, b)); self.ties.setdefault(b, []).append((s, a))
        for w in self.ties: self.ties[w] = [b for s, b in sorted(self.ties[w], key=lambda t: (-t[0], t[1]))]
        self.planes, self.aligned, self.groups, self.log, self.turn, self.session = {}, set(), {}, [], 0, 0
        self.next_group = 1

    # ---- geometry ------------------------------------------------------------------
    def y_of(self, w): return round(70 + (1 - self.gn.get(w, 0.5)) * 760)

    def free_x(self, x, y, r):
        for k in range(0, 60):
            for s in (1, -1):
                cx = x + s * k * 40
                if all(math.hypot(p["x"] - cx, p["y"] - y) >= p["r"] + r + 14 for p in self.planes.values() if not p["hidden"]):
                    return cx
        return x

    def segments(self, w): return [t for t in self.ties.get(w, []) if t in self.gn][:SEG]

    # ---- ops (what the page replays) ----------------------------------------------------
    def op(self, ops, name, **a): ops.append({"op": name, **a})

    def presentiate(self, ops, w, x, reason):
        r = 30; y = self.y_of(w); x = self.free_x(x, y, r)
        p = {"id": w, "word": w, "x": x, "y": y, "r": r, "theta": 0.0, "segments": self.segments(w), "parent": None,
             "folded": False, "hidden": False, "group": None, "born": self.turn, "touched": self.turn, "alignments": 0}
        self.planes[w] = p
        self.op(ops, "PRESENTIATE", id=w, word=w, x=x, y=y, r=r, theta=0.0, segments=p["segments"],
                generality=round(self.gn.get(w, 0), 3), definition=self.define(w), reason=reason)

    def move(self, ops, p, x, y):
        members = [q for q in self.planes.values() if p["group"] and q["group"] == p["group"]] or [p]
        dx, dy = x - p["x"], y - p["y"]
        moved = set()
        def carry(q):
            if q["id"] in moved: return
            moved.add(q["id"]); q["x"] += dx; q["y"] += dy
            self.op(ops, "MOVE", id=q["id"], x=round(q["x"], 1), y=round(q["y"], 1))
            for c in self.planes.values():
                if c["parent"] == q["id"]: carry(c)
        for q in members: carry(q)

    # ---- the four activities ------------------------------------------------------------
    def introduce(self, ops, say):
        vis = [p for p in self.planes.values() if not p["hidden"]]
        best = None
        for p in sorted(vis, key=lambda p: -p["born"]):
            unused = [s for s in p["segments"] if s not in self.planes]
            if unused and (best is None or len(unused) > best[1]): best = (p, len(unused), unused[0])
        if not best: return False, "every visible plane's segments are already on the Canvas"
        src, _, w = best
        self.presentiate(ops, w, src["x"] + src["r"] + 70, f"strongest unplaced segment of {src['word']}")
        src["touched"] = self.turn
        return True, f"introduced {w}, a segment of {src['word']}"

    def match(self, u, v):
        if u == v: return 3, "hinge", None
        rel = self.relate(u, v)
        if rel and rel[1] <= 2: return 2, rel[0], rel[1]
        if v in self.ties.get(u, [])[:SEG]: return 1, "tie", None
        return 0, None, None

    def align(self, ops, say):
        vis = sorted((p for p in self.planes.values() if not p["hidden"]), key=lambda p: -p["touched"])
        tested = 0
        for A in vis:
            for B in vis:
                if A is B or (A["id"], B["id"]) in self.aligned or (B["id"], A["id"]) in self.aligned: continue
                best = (0,)
                for i, u in enumerate(A["segments"]):          # Chronotool: every rotation of each plane
                    for j, v in enumerate(B["segments"]):
                        tested += 1
                        m = self.match(u, v)
                        if m[0] > best[0]: best = (m[0], i, j, u, v, m[1], m[2])
                if best[0] >= 2:
                    _, i, j, u, v, kind, depth = best
                    phi = math.atan2(B["y"] - A["y"], B["x"] - A["x"])
                    A["theta"] = (phi - i * 2 * math.pi / SEG) % (2 * math.pi)
                    B["theta"] = (phi + math.pi - j * 2 * math.pi / SEG) % (2 * math.pi)
                    self.op(ops, "ROTATE", id=A["id"], theta=round(A["theta"], 4), segment=i)
                    self.op(ops, "ROTATE", id=B["id"], theta=round(B["theta"], 4), segment=j)
                    self.aligned.add((A["id"], B["id"]))
                    self.op(ops, "ALIGN", a=A["id"], b=B["id"], sa=u, sb=v, kind=kind, score=best[0], configurations=tested)
                    for P in (A, B):
                        P["alignments"] += 1; P["touched"] = self.turn
                        P["r"] = min(95, 30 + 7 * P["alignments"]); self.op(ops, "SET_SIZE", id=P["id"], r=P["r"])
                    dy = B["y"] - A["y"]; reach = A["r"] + B["r"]
                    if abs(dy) < reach * 0.85 and not (A["parent"] or B["parent"]):
                        d = reach * (1 - 0.18 * best[0])                       # more shared ground, more overlap
                        dx = math.sqrt(max(d * d - dy * dy, 0)) * (1 if B["x"] >= A["x"] else -1)
                        self.move(ops, B, A["x"] + dx, B["y"])
                        g = A["group"] or B["group"] or f"set{self.next_group}"
                        if g == f"set{self.next_group}": self.next_group += 1
                        for q in self.planes.values():
                            if q["group"] and q["group"] in (A["group"], B["group"]): q["group"] = g
                        A["group"] = B["group"] = g
                        self.op(ops, "SET_GROUP", group=g, members=sorted(q["id"] for q in self.planes.values() if q["group"] == g))
                        how = "intersect"
                    else:
                        how = "link across generality"
                    if kind in ("is_a", "includes"):
                        s = self.speak(u, kind, v)
                        if s: say.append(s)
                    return True, f"{A['word']} and {B['word']} align on {u} / {v} ({kind}); {how}; {tested} configurations tested"
        return False, f"no pair of planes has matching segments ({tested} configurations tested)"

    def contain(self, ops, say):
        vis = [p for p in self.planes.values() if not p["hidden"]]
        for C in sorted(vis, key=lambda p: -p["touched"]):
            if C["parent"]: continue
            for P in vis:
                if P is C or P["parent"] == C["id"]: continue
                rel = self.relate(C["word"], P["word"])
                if rel and rel[0] == "is_a" and rel[1] <= 3:
                    s = self.speak(C["word"], "is_a", P["word"])
                    if not s: continue                                  # only audited claims become structure
                    kids = [k for k in self.planes.values() if k["parent"] == P["id"]]
                    spot = None
                    while spot is None:                      # a free spot inside P; grow P when it is full
                        need = C["r"] * 2.1
                        if P["r"] < need:
                            P["r"] = round(need); self.op(ops, "SET_SIZE", id=P["id"], r=P["r"])
                        for ring in (0.0, 0.42, 0.62):
                            for k in range(12 if ring else 1):
                                a = k * math.pi / 6
                                x, y = P["x"] + math.cos(a) * P["r"] * ring, P["y"] + math.sin(a) * P["r"] * ring
                                inside = math.hypot(x - P["x"], y - P["y"]) + C["r"] <= P["r"] - 4
                                if inside and all(math.hypot(x - q["x"], y - q["y"]) >= C["r"] + q["r"] + 3 for q in kids):
                                    spot = (x, y); break
                            if spot: break
                        if spot is None:
                            P["r"] = round(P["r"] * 1.18); self.op(ops, "SET_SIZE", id=P["id"], r=P["r"])
                    self.move(ops, C, *spot)
                    C["parent"] = P["id"]; C["touched"] = P["touched"] = self.turn
                    self.op(ops, "CONTAIN", id=C["id"], parent=P["id"], depth=rel[1])
                    say.append(s)
                    return True, f"{C['word']} placed inside {P['word']} (is-a at spectrum depth {rel[1]}, audited)"
        return False, "no validated is-a pair among visible planes"

    def manifold(self, ops, say):
        for P in sorted(self.planes.values(), key=lambda p: p["touched"]):
            kids = [k for k in self.planes.values() if k["parent"] == P["id"]]
            if kids and not P["folded"] and not P["hidden"] and self.turn - P["touched"] >= 8:
                P["folded"] = True
                for k in kids: k["hidden"] = True
                self.op(ops, "MANIFOLD", id=P["id"], contents=[k["id"] for k in kids])
                return True, f"folded {len(kids)} plane(s) into {P['word']}, untouched for {self.turn - P['touched']} turns"
        for P in sorted(self.planes.values(), key=lambda p: p["touched"]):
            if P["folded"]:
                P["folded"] = False; P["touched"] = self.turn
                for k in self.planes.values():
                    if k["parent"] == P["id"]: k["hidden"] = False
                self.op(ops, "UNFOLD", id=P["id"])
                return True, f"unfolded {P['word']} to revisit it"
        return False, "nothing to fold or unfold"

    # ---- the Recess loop ---------------------------------------------------------------------
    def run(self, sessions=6, turns=20, start=None):
        ops = []
        self.presentiate(ops, start, 600, "his most general canonical resident in the Lobby")
        self.log.append({"turn": 0, "session": 1, "arm": "START", "ok": True, "ops": ops, "say": [], "reason": ops[0]["reason"]})
        for s in range(1, sessions + 1):
            self.session = s
            for _ in range(turns):
                self.turn += 1
                arm = self.matrix.bandit_select("canvas", ARMS)                # A-101 chooses
                ops, say = [], []
                ok, why = getattr(self, arm.lower())(ops, say)
                self.matrix.record_outcome(arm, "canvas", ok)
                self.log.append({"turn": self.turn, "session": s, "arm": arm, "ok": ok, "ops": ops, "say": say, "reason": why})
            cp = self.matrix.checkpoint_generation()                            # A-113 judges the session
            hist = {k[0]: list(v) for k, v in self.matrix.history.items() if k[1] == "canvas"}
            self.log.append({"turn": self.turn, "session": s, "arm": "CHECKPOINT", "ok": True, "ops": [], "say": [],
                             "reason": f"A-113 {cp['decision']}: {cp.get('reason', '')}", "decision": cp["decision"], "history": hist})
        return self.log
