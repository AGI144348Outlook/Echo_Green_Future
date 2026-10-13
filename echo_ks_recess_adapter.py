"""Kuk Sool Canvas Recess operation adapter (reference-only).

Interprets a validated subset of E12 KSRecess ops as Canvas state. It does
not import the alternate KSM kernel or infer DSL inversion semantics.
"""
SUPPORTED = {"PRESENTIATE", "MOVE", "ROTATE", "ALIGN", "CONTAIN", "SET_GROUP", "SET_SIZE"}

class RecessCanvas:
    def __init__(self):
        self.nodes = {}
        self.relations = []
        self.groups = {}
        self.audit = []

    def apply(self, operation):
        op = operation.get("op")
        if op not in SUPPORTED:
            raise ValueError("unsupported Recess operation: " + str(op))
        if op == "PRESENTIATE":
            key = operation["id"]
            if not isinstance(key, str) or not key or key in self.nodes:
                raise ValueError("duplicate or invalid presentiation identity")
            self.nodes[key] = {k: operation.get(k) for k in
                               ("id", "word", "x", "y", "r", "theta", "segments", "definition")}
        elif op in ("MOVE", "ROTATE", "SET_SIZE"):
            key = operation["id"]
            if key not in self.nodes:
                raise ValueError("unknown presented identity")
            fields = {"MOVE": ("x", "y"), "ROTATE": ("theta",), "SET_SIZE": ("r",)}[op]
            for field in fields:
                if field in operation:
                    self.nodes[key][field] = operation[field]
        elif op == "CONTAIN":
            child, parent = operation["id"], operation["parent"]
            if child not in self.nodes or parent not in self.nodes:
                raise ValueError("containment endpoints must be presented")
            self.relations.append(dict(operation))
        elif op == "ALIGN":
            a, b = operation["a"], operation["b"]
            if a not in self.nodes or b not in self.nodes:
                raise ValueError("relation endpoints must be presented")
            self.relations.append(dict(operation))
        elif op == "SET_GROUP":
            members = operation["members"]
            if any(member not in self.nodes for member in members):
                raise ValueError("unknown group member")
            self.groups[str(operation["group"])] = list(members)
        self.audit.append(dict(operation))

    def replay(self, operations):
        for operation in operations:
            self.apply(operation)
        return self.snapshot()

    def snapshot(self):
        return {"nodes": self.nodes, "relations": self.relations,
                "groups": self.groups, "operations": len(self.audit)}
