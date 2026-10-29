#!/usr/bin/env python3
"""Run431 source-transcribed, isolated Genesis Lobby repopulation probe.
PRE/POST: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/104
Genesis blob 63eb982; not a full Genesis import or frozen race test.
"""
import re
from types import SimpleNamespace
class WordAgent:
    def __init__(self, word, definition_words, entry_class, department, parent, raw_definition=""):
        self.word=word; self.definition_words=definition_words; self.raw_definition=raw_definition
        self.entry_class=entry_class; self.department=department; self.parent=parent
        self.ties=set(); self.neighborhood=None; self.identity_confirmed=False
        self.generality_score=0.0
        self.typical_subjects=set(); self.typical_objects=set(); self.typical_verbs=set()
    def confirm_identity(self):
        if not self.identity_confirmed: self.identity_confirmed=bool(self.word)
        return self.identity_confirmed
    def words_referenced_in_definitions(self):
        found=set()
        for token in re.findall(r"[a-z\']+", " ".join(self.definition_words).lower()):
            if token and token!=self.word.lower() and len(token)>1: found.add(token)
        return found
class Lobby:
    def __init__(self,matrix):
        self.matrix=matrix; self.agents={}; self.ties={}; self.neighborhoods={}
        self.pending_merges=[]; self.committed_count=0; self.generality_scores={}
    def populate(self):
        for word,entry_class in self.matrix.entry_classes.items():
            if entry_class=="NAME": continue
            def_words=[w for w in self.matrix.transitions.get(word,{})
                if w in self.matrix.content_units and self.matrix.entry_classes.get(w)!="NAME"]
            cats=self.matrix.word_categories.get(word,{})
            pos_tags=[k.replace("pos:","") for k in cats if k.startswith("pos:")]
            department=pos_tags[0] if pos_tags else "unclassified"
            raw_def=" ".join(sorted(self.matrix.transitions.get(word,{}).keys()))
            agent=WordAgent(word,def_words,entry_class,department,self.matrix,raw_definition=raw_def)
            agent.confirm_identity(); self.agents[word]=agent
        return len(self.agents)
    def add_tie(self,w1,w2,strength=1):
        key=tuple(sorted([w1,w2]))
        self.ties[key]=self.ties.get(key,0)+strength
        a1,a2=self.agents.get(w1),self.agents.get(w2)
        if a1: a1.ties.add(w2)
        if a2: a2.ties.add(w1)
    def run_orientation(self):
        if not all(a.identity_confirmed for a in self.agents.values()):
            unconfirmed=[w for w,a in self.agents.items() if not a.identity_confirmed]
            raise RuntimeError(f"Orientation blocked: {len(unconfirmed)} agents have not confirmed identity. First: {unconfirmed[:3]}")
        discovered={word:agent.words_referenced_in_definitions() for word,agent in self.agents.items()}
        for word,referenced_words in discovered.items():
            for other_word in referenced_words:
                if other_word in self.agents and other_word!=word: self.add_tie(word,other_word,strength=1)
        return len(self.ties)
m=SimpleNamespace(entry_classes={'resh':'ABSTRACT','aleph':'ABSTRACT'},
    transitions={'resh':{'aleph':1},'aleph':{}},
    content_units={'resh':1,'aleph':1},word_categories={})
l=Lobby(m); n=0
def check(name,cond):
    global n
    assert cond,name
    n+=1; print('PASS',n,name)
check('initial populate count',l.populate()==2)
check('initial agent sets empty',all(not a.ties for a in l.agents.values()))
check('first orientation one edge',l.run_orientation()==1)
key=('aleph','resh')
check('first edge weight one',l.ties[key]==1)
check('first local membership',l.agents['resh'].ties=={'aleph'} and l.agents['aleph'].ties=={'resh'})
old=l.agents['resh']
check('repopulate count',l.populate()==2)
check('replaced object',l.agents['resh'] is not old)
check('global edge persists',l.ties[key]==1)
check('new local sets empty',not l.agents['resh'].ties and not l.agents['aleph'].ties)
check('reorientation restores membership',l.run_orientation()==1 and l.agents['resh'].ties=={'aleph'})
check('reorientation doubles weight',l.ties[key]==2)
check('another orientation triples weight',l.run_orientation()==1 and l.ties[key]==3)
print('TOTAL',n,'PASS (isolated transcription)')
