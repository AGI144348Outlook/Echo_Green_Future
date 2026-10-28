#!/usr/bin/env python3
"""Isolated source-transcribed Genesis fixture; NOT full Genesis execution.
Pinned sources: genesis-documentary src/echo_governor_skeleton.py
63eb982989b4f3478d649430b555c8f4ba755c27, src/alphabet_data.py
3ec8330646880e69dd9dd74b35f79fd58409af0e.
Reproduces method statements for WordAgent references, Lobby orientation,
make_letter_lobby ordering and ReshIdentity.anchor() semantic-list update.
"""
import json
import re

class Agent:
    def __init__(self, word, properties):
        self.word=word
        self.definition_words=list(properties)
        self.raw_definition=" ".join(properties)
        self.identity_confirmed=True
        self.ties=set()
        self.generality_score=0.9
    def words_referenced_in_definitions(self):
        found=set()
        for token in re.findall(r"[a-z']+", " ".join(self.definition_words).lower()):
            if token and token != self.word.lower() and len(token)>1:
                found.add(token)
        return found

class Lobby:
    def __init__(self, agents):
        self.agents=agents
        self.ties={}
    def add_tie(self,w1,w2,strength=1):
        key=tuple(sorted([w1,w2]))
        self.ties[key]=self.ties.get(key,0)+strength
        a1,a2=self.agents.get(w1),self.agents.get(w2)
        if a1:a1.ties.add(w2)
        if a2:a2.ties.add(w1)
    def run_orientation(self):
        if not all(a.identity_confirmed for a in self.agents.values()):
            raise RuntimeError("unconfirmed")
        discovered={word:agent.words_referenced_in_definitions() for word,agent in self.agents.items()}
        for word, referenced_words in discovered.items():
            for other_word in referenced_words:
                if other_word in self.agents and other_word != word:
                    self.add_tie(word,other_word,strength=1)
        return len(self.ties)

# Four entries transcribed from actual HEBREW_ALPHABET; original has 22.
props={
 "aleph":["silent","breath","primal","potential","unity","ox","beginning","one","spirit","air","mother","operator","oneness","divine","aleph_gematria_1"],
 "ayin":["eye","seeing","spring","source","seventy","ayin_gematria_70","elemental","perception","insight","depth"],
 "pe":["mouth","speech","expression","face","eighty","pe_gematria_80","double","peh","language","command","prayer"],
 "resh":["head","beginning","leader","identity","two_hundred","resh_gematria_200","double","rosh","chief","poverty","wickedness"],
}

# make_letter_lobby calls run_orientation BEFORE ReshIdentity.anchor().
lobby=Lobby({name:Agent(name,p) for name,p in props.items()})
initial_edges=lobby.run_orientation()
resh=lobby.agents["resh"]
initial_defs=set(resh.definition_words)
initial_raw=resh.raw_definition
initial_score=resh.generality_score
initial_ties=set(resh.ties)

# Exact mutation expression from ReshIdentity.anchor() (without full matrix).
resh.definition_words=list(set(resh.definition_words +
    ["governor","indexing","algorithm","identity","matrix","aleph","ayin","pe"]))
post_defs=set(resh.definition_words)
post_ties=set(resh.ties)
post_edges=dict(lobby.ties)

checks=[]
def check(name,value):
    checks.append((name,bool(value)))
    assert value,name

check("initial 4-letter orientation no ties", initial_edges==0)
check("initial resh no aleph/ayin/pe definition", not ({"aleph","ayin","pe"}&initial_defs))
check("anchor adds three letter references", {"aleph","ayin","pe"}.issubset(post_defs))
check("anchor retains original definition membership", initial_defs.issubset(post_defs))
check("anchor leaves existing tie set unchanged", post_ties==initial_ties==set())
check("anchor leaves Lobby tie map unchanged", post_edges=={})
check("anchor leaves raw_definition stale", resh.raw_definition==initial_raw and "aleph" not in resh.raw_definition)
check("anchor leaves generality score unchanged", resh.generality_score==initial_score==0.9)
check("definition reference scan sees new links", {"aleph","ayin","pe"}.issubset(resh.words_referenced_in_definitions()))

# This is a deliberate later re-orientation, NOT called by anchor() or demo.
reorient=lobby.run_orientation()
check("explicit re-orientation yields three links", reorient==3)
check("resh ties then include three letters", {"aleph","ayin","pe"}.issubset(resh.ties))
check("tie map symmetric through bidirectional agent sets", all("resh" in lobby.agents[w].ties for w in ("aleph","ayin","pe")))
print(json.dumps({"passed":len(checks),"total":len(checks),"initial_edges":initial_edges,
                  "post_anchor_edges":len(post_edges),"after_explicit_reorientation":reorient,
                  "checks":checks},indent=2))
