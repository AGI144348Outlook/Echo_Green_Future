"""Run423 isolated SOURCE-TRANSCRIBED Genesis ReshIdentity probe.
Does not import or execute full Genesis. PRE: Echo_Green_Future issue #96.
"""
class ReshIdentity:
    def __init__(self, matrix, hebrew_lobby=None):
        self.matrix = matrix
        self.hebrew_lobby = hebrew_lobby
        self._anchored = False
        self._anchor_entry = None

    def anchor(self):
        a000 = self.matrix.known.get("A-000", {})
        a000["identity_symbol"] = "resh"
        a000["identity_glyph"] = "ר"
        a000["identity_letter"] = "resh"
        a000["identity_meaning"] = "head beginning leader identity"
        self.matrix.known["A-000"] = a000
        self.matrix.known["A-000-RESH"] = {
            "name": "Resh — Governor Identity Anchor",
            "status": "ACTIVE", "type": "IDENTITY-LETTER", "glyph": "ר",
            "aliases": ["A-000", "resh", "governor"],
            "description": "The Governor and Resh are one and the same — Resh is head, beginning, identity; the Governor reads Resh when it reads itself in the matrix. Identity validation (IDENTIFY→VALIDATE→OPEN) runs through this entry.",
            "perception_operator": "ayin", "expression_operator": "pe"
        }
        if self.hebrew_lobby:
            resh_agent = self.hebrew_lobby.agents.get("resh")
            if resh_agent:
                resh_agent.definition_words = list(set(
                    resh_agent.definition_words +
                    ["governor", "indexing", "algorithm", "identity",
                     "matrix", "aleph", "ayin", "pe"]))
        self._anchored = True
        self._anchor_entry = self.matrix.known["A-000-RESH"]
        return self._anchor_entry

    def validate(self):
        return (self._anchored
                and "A-000-RESH" in self.matrix.known
                and self.matrix.known.get("A-000", {}).get("identity_symbol") == "resh")

class StubMatrix:
    def __init__(self):
        # Exact initial A-000 shape from Genesis AlgorithmMatrix.__init__ line 350.
        self.known = {"A-000": {"name": "Governor", "status": "ACTIVE"}}
    def record(self, entry_id, entry):
        # Exact method from Genesis lines 435-436.
        self.known[entry_id] = entry

checks=[]
def check(label, condition):
    assert condition, label
    checks.append(label)

normal=StubMatrix(); r=ReshIdentity(normal)
check('normal constructor supplies A-000', normal.known['A-000']=={'name':'Governor','status':'ACTIVE'})
check('normal unanchored validation fails', not r.validate())
r.anchor()
check('normal anchor validates', r.validate())
check('normal anchor retains name/status', normal.known['A-000']['name']=='Governor' and normal.known['A-000']['status']=='ACTIVE')

missing=StubMatrix(); missing.known.pop('A-000'); m=ReshIdentity(missing)
check('deleted A-000 absent before anchor', 'A-000' not in missing.known)
check('missing pre-anchor fails', not m.validate())
m.anchor()
check('missing A-000 recreated and validates', m.validate())
check('recreated A-000 lacks name', 'name' not in missing.known['A-000'])
check('recreated A-000 lacks status', 'status' not in missing.known['A-000'])
check('recreated A-000 has only four identity fields', set(missing.known['A-000'])=={'identity_symbol','identity_glyph','identity_letter','identity_meaning'})
check('alias minted despite missing original', 'A-000-RESH' in missing.known)

replaced=StubMatrix(); replaced.record('A-000',{'status':'REPLACED'}); t=ReshIdentity(replaced)
t.anchor()
check('record replacement can be silently anchored', t.validate() and 'name' not in replaced.known['A-000'])
check('replaced non-identity status persists', replaced.known['A-000']['status']=='REPLACED')
replaced.known['A-000']['identity_symbol']='x'
check('symbol mutation noticed', not t.validate())
t.anchor()
check('re-anchor restores symbol but preserves replaced status', t.validate() and replaced.known['A-000']['status']=='REPLACED')

print(f'PASS {len(checks)}/{len(checks)} isolated source-transcribed controls')
for i,c in enumerate(checks,1): print(f'{i:02d}. {c}')
print('MISSING_A000_AFTER_ANCHOR:',missing.known['A-000'])
print('REPLACED_A000_AFTER_REANCHOR:',replaced.known['A-000'])
