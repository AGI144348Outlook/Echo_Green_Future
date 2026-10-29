#!/usr/bin/env python3
"""Run432 isolated source-transcribed Ayin SELF branch (Genesis blob 63eb982).

Only the class's __init__ and classify() early-return path are represented.
Not the complete Genesis module, not a live security bypass demonstration.
"""
from types import SimpleNamespace

class AyinSelfBranch:
    def __init__(self, lobby, governor_word='resh'):
        self.lobby = lobby
        self.governor_word = governor_word.lower()

    def classify(self, word):
        w = word.lower()
        agent = self.lobby.agents.get(w)
        if not agent:
            return {'word': w, 'category': 'UNKNOWN', 'signals': []}
        if w == self.governor_word:
            return {'word': w, 'category': 'SELF', 'signals': ['governor_identity']}
        return {'word': w, 'category': 'NON_AGENTIVE', 'signals': []} # fallback outside the scoped source branch

class ReshStub:
    def __init__(self, anchored=False, intact=True):
        self.anchored = anchored
        self.intact = intact
    def validate(self):
        return self.anchored and self.intact

def authorized_self(ayin, resh, word):
    return ayin.classify(word)['category'] == 'SELF' and resh.validate()

checks=[]
def check(name, got, want):
    assert got==want,(name,got,want)
    checks.append(name)

lobby=SimpleNamespace(agents={'resh': SimpleNamespace(word='resh'), 'cat': SimpleNamespace(word='cat')})
ayin=AyinSelfBranch(lobby)
check('unanchored_still_self',ayin.classify('resh')['category'],'SELF')
check('casefold_still_self',ayin.classify('RESH')['category'],'SELF')
check('no_agent_unknown',AyinSelfBranch(SimpleNamespace(agents={})).classify('resh')['category'],'UNKNOWN')
check('nonself_not_self',ayin.classify('cat')['category'],'NON_AGENTIVE')
check('unanchored_gate_rejects',authorized_self(ayin,ReshStub(), 'resh'),False)
check('anchored_gate_accepts',authorized_self(ayin,ReshStub(True), 'resh'),True)
check('tampered_gate_rejects',authorized_self(ayin,ReshStub(True,False), 'resh'),False)
check('tampered_classifier_still_self',ayin.classify('resh')['category'],'SELF')
check('arbitrary_governor_word_self',AyinSelfBranch(lobby,'cat').classify('cat')['category'],'SELF')
check('arbitrary_governor_word_resh_not_self',AyinSelfBranch(lobby,'cat').classify('resh')['category'],'NON_AGENTIVE')
lobby.agents['resh'].word='not-resh'
check('mismatched_agent_word_still_self',ayin.classify('resh')['category'],'SELF')
check('mismatched_agent_gate_rejects',authorized_self(ayin,ReshStub(False), 'resh'),False)
print(f'PASS {len(checks)}/{len(checks)} source-transcribed Ayin SELF controls')
