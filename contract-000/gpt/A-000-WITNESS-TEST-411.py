"""Run411 isolated Genesis ReshIdentity source-transcribed controls, NOT full Genesis.
Candidate witness is deliberately external to matrix. It is NOT an authorized custodian.
"""
import copy, hashlib, json

class ReshIdentity:
    def __init__(self, matrix, hebrew_lobby=None):
        self.matrix=matrix;self.hebrew_lobby=hebrew_lobby;self._anchored=False;self._anchor_entry=None
    def anchor(self):
        a000=self.matrix.known.get('A-000',{})
        a000['identity_symbol']='resh'
        a000['identity_glyph']='ר'
        a000['identity_letter']='resh'
        a000['identity_meaning']='head beginning leader identity'
        self.matrix.known['A-000']=a000
        self.matrix.known['A-000-RESH']={
            'name':'Resh — Governor Identity Anchor','status':'ACTIVE','type':'IDENTITY-LETTER',
            'glyph':'ר','aliases':['A-000','resh','governor'],
            'description':('The Governor and Resh are one and the same — '
                           'Resh is head, beginning, identity; the Governor '
                           'reads Resh when it reads itself in the matrix. '
                           'Identity validation (IDENTIFY→VALIDATE→OPEN) '
                           'runs through this entry.'),
            'perception_operator':'ayin','expression_operator':'pe'}
        if self.hebrew_lobby:
            resh_agent=self.hebrew_lobby.agents.get('resh')
            if resh_agent:
                resh_agent.definition_words=list(set(resh_agent.definition_words+['governor','indexing','algorithm','identity','matrix','aleph','ayin','pe']))
        self._anchored=True
        self._anchor_entry=self.matrix.known['A-000-RESH']
        return self._anchor_entry
    def validate(self):
        return (self._anchored and 'A-000-RESH' in self.matrix.known and self.matrix.known.get('A-000',{}).get('identity_symbol')=='resh')

class Matrix:
    def __init__(self): self.known={'A-000':{'name':'Governor','status':'ACTIVE'}}

def witness(m):
    # snapshot content before changes; held outside matrix, no authority claim
    snap=copy.deepcopy({k:m.known[k] for k in ('A-000','A-000-RESH')})
    raw=json.dumps(snap,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()

def check_witness(m,w): return witness(m)==w

m=Matrix();r=ReshIdentity(m);assert r.validate() is False;print('PASS unanchored rejects')
r.anchor();w=witness(m);assert r.validate() and check_witness(m,w);print('PASS anchored snapshot matches')
m.known['A-000']['status']='TAMPERED';assert r.validate() and not check_witness(m,w);print('PASS status mutation escapes local but not snapshot')
m.known['A-000']['status']='ACTIVE';m.known['A-000-RESH']['aliases']=['foreign'];assert r.validate() and not check_witness(m,w);print('PASS alias mutation escapes local but not snapshot')
m.known['A-000-RESH']['aliases']=['A-000','resh','governor'];assert check_witness(m,w);print('PASS restoration matches snapshot')
m.known['A-000']['status']='TAMPERED';r.anchor();assert r.validate() and not check_witness(m,w) and m.known['A-000']['status']=='TAMPERED';print('PASS reanchor does not repair unvalidated status')
print('6/6 isolated controls passed; witness is in-process proposal, not independent authority')
