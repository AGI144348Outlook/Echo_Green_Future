"""Isolated source-transcribed ReshIdentity restart fixture (no Genesis import)."""
from copy import deepcopy
class Matrix:
    def __init__(self):self.known={'A-000':{'name':'Governor','status':'ACTIVE'}}
class ReshIdentity:
    def __init__(self,matrix,hebrew_lobby=None):
        self.matrix=matrix;self.hebrew_lobby=hebrew_lobby
        self._anchored=False;self._anchor_entry=None
    def anchor(self):
        a000=self.matrix.known.get('A-000',{})
        a000['identity_symbol']='resh';a000['identity_glyph']='ר'
        a000['identity_letter']='resh';a000['identity_meaning']='head beginning leader identity'
        self.matrix.known['A-000']=a000
        self.matrix.known['A-000-RESH']={
            'name':'Resh — Governor Identity Anchor','status':'ACTIVE','type':'IDENTITY-LETTER',
            'glyph':'ר','aliases':['A-000','resh','governor'],
            'description':'The Governor and Resh are one and the same — Resh is head, beginning, identity; the Governor reads Resh when it reads itself in the matrix. Identity validation (IDENTIFY→VALIDATE→OPEN) runs through this entry.',
            'perception_operator':'ayin','expression_operator':'pe'}
        self._anchored=True;self._anchor_entry=self.matrix.known['A-000-RESH']
        return self._anchor_entry
    def validate(self):
        return (self._anchored and 'A-000-RESH' in self.matrix.known and
                self.matrix.known.get('A-000',{}).get('identity_symbol')=='resh')

def check(name,value):
    assert value,name
    print('PASS',name)

m=Matrix();a=ReshIdentity(m)
check('fresh unanchored',a.validate() is False)
a.anchor();check('anchor validates',a.validate() is True)
saved=deepcopy(m.known)
old_alias=m.known['A-000-RESH']
b=ReshIdentity(m)
check('same matrix new Resh instance fails',b.validate() is False and m.known==saved)
# This is exactly the two-line branch in PeCommunicator.open_exchanges().
if not b.validate():b.anchor()
check('open_exchanges branch reanchors on restart',b.validate() is True)
check('reanchor replaces alias dict',m.known['A-000-RESH']==saved['A-000-RESH'] and m.known['A-000-RESH'] is not old_alias)
m.known['A-000']['status']='REVIEW-PENDING'
c=ReshIdentity(m)
if not c.validate():c.anchor()
check('reanchor leaves other status unchanged',m.known['A-000']['status']=='REVIEW-PENDING' and c.validate())
print('6/6 isolated fixture controls; not full Genesis execution')
