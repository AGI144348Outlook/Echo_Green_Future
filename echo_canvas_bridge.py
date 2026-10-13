"""Experimental bridge to the Genesis Documentary A-000 AlgorithmMatrix.
Not a full GraphQL implementation. Read-only subset, explicit allowlist.
"""
import json
from echo_governor_skeleton import AlgorithmMatrix
from echo_neuroplasticity_overlay import NeuroplasticityOverlay
from echo_ks_recess_adapter import RecessCanvas

class EchoCanvasBridge:
    def __init__(self):
        self.matrix = AlgorithmMatrix()
        self.plasticity = NeuroplasticityOverlay(self.matrix)
        self.recess = RecessCanvas()
        self.entities = {}
    def register(self, entity_id, kind, label, text):
        if not isinstance(entity_id,str) or not entity_id or len(text)>100000:
            raise ValueError("invalid entity")
        self.matrix.index_content(text, category=kind)
        self.entities[entity_id] = {"id":entity_id,"kind":kind,"label":label,"text":text}
        return {"id":entity_id,"indexed":True}
    def query(self, expression):
        # Deliberately bounded GraphQL-like read-only query until schema is finalized.
        import re
        match = re.fullmatch(r'\s*\{\s*entity\s*\(\s*id\s*:\s*"([^"]{1,100})"\s*\)\s*\{\s*([a-zA-Z\s]+)\s*\}\s*\}\s*',expression)
        if not match: raise ValueError("unsupported query; expected { entity(id: \"...\") { id kind label } }")
        allowed={"id","kind","label","text"}
        fields=match.group(2).split()
        if not fields or any(f not in allowed for f in fields): raise ValueError("unknown field")
        e=self.entities.get(match.group(1))
        return {"data":{"entity":({f:e[f] for f in fields} if e else None)}}
    def enable_plasticity(self, enabled=True):
        self.plasticity.enabled = bool(enabled)
        return self.plasticity.snapshot()
    def recess_operation(self, operation):
        self.recess.apply(operation)
        return self.recess.snapshot()
    def stats(self):
        return {"entities":len(self.entities),"algorithm_matrix":type(self.matrix).__name__,
                "plasticity":self.plasticity.snapshot(),"recess":self.recess.snapshot()}
bridge=EchoCanvasBridge()
