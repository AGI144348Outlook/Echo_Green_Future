"""Test 008: provisional DSL Registry -> inversion -> underside -> Canvas operations.
This is a contract/fixture test, NOT the canonical DSL Registry inversion.
"""
import unittest
from copy import deepcopy

class DSLInversion:
    def __init__(self, registry):
        self.registry=deepcopy(registry)
        self.underside={}
        self.audit=[]
    def invert(self):
        # Turn declarative operation specifications into validated executable dispatch entries.
        self.underside={name:{"required":tuple(spec["required"]),"permission":spec["permission"],"handler":spec["handler"]} for name,spec in self.registry.items()}
        return self.underside
    def dispatch(self,operation,payload,canvas,permissions):
        rule=self.underside.get(operation)
        if not rule: raise ValueError("unregistered operation")
        if rule["permission"] not in permissions: raise PermissionError(operation)
        if any(k not in payload for k in rule["required"]): raise ValueError("missing required fields")
        before=deepcopy(canvas)
        try:
            if rule["handler"]=="scale":
                value=payload["value"]
                if not isinstance(value,(int,float)) or not (0<value<=1000): raise ValueError("invalid scale")
                canvas["scale"]=value
            elif rule["handler"]=="profile":
                identity=payload["identity"]
                if identity not in canvas["entities"]: raise ValueError("unknown entity")
                canvas["profiles"][identity]=payload["card"]
            elif rule["handler"]=="manifold":
                canvas["depth"]+=1
            else: raise ValueError("unknown handler")
        except Exception:
            canvas.clear();canvas.update(before);raise
        self.audit.append({"operation":operation,"payload":deepcopy(payload)})
        return canvas

class TestDSLCanvas008(unittest.TestCase):
    def setUp(self):
        self.registry={
          "SET_SCALE":{"required":["value"],"permission":"canvas:transform","handler":"scale"},
          "ASSIGN_PROFILE":{"required":["identity","card"],"permission":"registry:assign","handler":"profile"},
          "MANIFOLD_INWARD":{"required":[],"permission":"lvt:manifold","handler":"manifold"}}
        self.engine=DSLInversion(self.registry);self.engine.invert()
        self.canvas={"origin":(0,0,0),"scale":1,"depth":0,"entities":{"glyph:aleph":{"symbol":"א"}},"profiles":{}}
    def test_registry_generates_underside(self):
        self.assertEqual(set(self.engine.underside),set(self.registry))
        self.assertEqual(self.engine.underside["SET_SCALE"]["permission"],"canvas:transform")
    def test_canvas_scale_origin_identity(self):
        entity=self.canvas["entities"]["glyph:aleph"]
        self.engine.dispatch("SET_SCALE",{"value":10},self.canvas,{"canvas:transform"})
        self.assertEqual(self.canvas["origin"],(0,0,0))
        self.assertIs(self.canvas["entities"]["glyph:aleph"],entity)
    def test_profile_and_manifold(self):
        self.engine.dispatch("ASSIGN_PROFILE",{"identity":"glyph:aleph","card":"nve-ray"},self.canvas,{"registry:assign"})
        self.engine.dispatch("MANIFOLD_INWARD",{},self.canvas,{"lvt:manifold"})
        self.assertEqual(self.canvas["profiles"]["glyph:aleph"],"nve-ray")
        self.assertEqual(self.canvas["depth"],1)
    def test_unknown_operation_rejected(self):
        with self.assertRaises(ValueError): self.engine.dispatch("EXECUTE_CODE",{},self.canvas,{"canvas:transform"})
        self.assertEqual(self.engine.audit,[])
    def test_permission_gate(self):
        with self.assertRaises(PermissionError): self.engine.dispatch("SET_SCALE",{"value":10},self.canvas,set())
        self.assertEqual(self.canvas["scale"],1)
    def test_atomic_invalid_scale(self):
        before=deepcopy(self.canvas)
        with self.assertRaises(ValueError): self.engine.dispatch("SET_SCALE",{"value":0},self.canvas,{"canvas:transform"})
        self.assertEqual(self.canvas,before)
        self.assertEqual(self.engine.audit,[])
    def test_missing_payload(self):
        with self.assertRaises(ValueError): self.engine.dispatch("ASSIGN_PROFILE",{"identity":"glyph:aleph"},self.canvas,{"registry:assign"})
        self.assertEqual(self.canvas["profiles"],{})

if __name__=="__main__":unittest.main()
