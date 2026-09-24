#!/usr/bin/env python3
"""Lobby Reset 010 — controlled language foundation.

Builds a NEW lobby artifact from:
  1) Swadesh vocabulary already recorded in sandbox/echo_sandbox_swadesh.json
  2) the recorded hypernym-chain terms for those Swadesh entries
  3) an explicit grammar curriculum and its structural relations

Historical Trial 006–009 artifacts are untouched. Grammar definitions are NOT
recursively expanded into additional dictionary vocabulary.
"""
from pathlib import Path
import json,hashlib,re
from collections import defaultdict

src=json.loads(Path("sandbox/echo_sandbox_swadesh.json").read_text())
chains=src.get("hypernym_chains",{})

def norm(x): return re.sub(r"\s+"," ",str(x).strip().lower())

lobby={}
edges=[]
def admit(word,kind,source):
    w=norm(word)
    if not w:return
    lobby.setdefault(w,{"word":w,"kinds":[],"sources":[]})
    if kind not in lobby[w]["kinds"]:lobby[w]["kinds"].append(kind)
    if source not in lobby[w]["sources"]:lobby[w]["sources"].append(source)

# Swadesh terms and only their already-recorded hypernym ancestry.
for word,chain in chains.items():
    admit(word,"swadesh","sandbox/echo_sandbox_swadesh.json")
    prev=norm(word)
    # recorded chains may run general->specific; preserve exact adjacency,
    # rather than inventing orientation.
    vals=[norm(x) for x in chain if norm(x)]
    for x in vals: admit(x,"swadesh_hypernym_chain","sandbox/echo_sandbox_swadesh.json")
    for a,b in zip(vals,vals[1:]):
        edges.append({"a":a,"relation":"recorded_hypernym_chain_next","b":b,"source":"swadesh"})
# Include explicit swadesh list fields if present.
for key in ("swadesh","swadesh_words","words"):
    if isinstance(src.get(key),list):
        for w in src[key]: admit(w,"swadesh","sandbox/echo_sandbox_swadesh.json")

grammar={
"word":"language unit","lexeme":"vocabulary unit","morpheme":"minimal meaningful unit",
"noun":"word naming entity or concept","verb":"word expressing action state or process",
"adjective":"word modifying noun","adverb":"word modifying verb adjective or adverb",
"pronoun":"word substituting for noun phrase","determiner":"word specifying noun reference",
"article":"determiner marking noun reference","preposition":"word expressing relation",
"conjunction":"word connecting words phrases or clauses","interjection":"independent expressive word",
"subject":"clause element about which predicate is asserted","predicate":"clause element asserting something about subject",
"object":"verb-related participant receiving or affected by action","direct object":"object directly governed by verb",
"indirect object":"object expressing recipient or beneficiary","complement":"element completing grammatical meaning",
"modifier":"element restricting or describing another element","head":"central element determining phrase type",
"phrase":"group of words functioning as unit","noun phrase":"phrase headed by noun",
"verb phrase":"phrase headed by verb","clause":"unit containing predicate and typically subject",
"sentence":"grammatically complete expression","declarative":"sentence or clause making statement",
"interrogative":"sentence or clause asking question","imperative":"sentence or clause expressing command",
"exclamative":"sentence or clause expressing exclamation","tense":"grammatical location in time",
"aspect":"grammatical view of temporal structure","mood":"grammatical expression of modality or attitude",
"voice":"grammatical relation between action and participants","active voice":"voice foregrounding agent-like subject",
"passive voice":"voice foregrounding affected participant","person":"grammatical participant role",
"number":"grammatical distinction such as singular and plural","singular":"grammatical number for one",
"plural":"grammatical number for more than one","gender":"grammatical noun classification",
"case":"grammatical marking of syntactic or semantic role","agreement":"matching grammatical features",
"inflection":"word-form change expressing grammatical information","conjugation":"inflection of verbs",
"declension":"inflection of nouns pronouns or adjectives","auxiliary":"verb supporting grammatical construction",
"modal":"auxiliary expressing possibility necessity permission or related modality",
"copula":"linking verb joining subject and complement","participle":"verb form with verbal and adjectival functions",
"gerund":"verb-derived form functioning nominally","infinitive":"nonfinite base-like verb form",
"antecedent":"expression to which another expression refers","relative clause":"clause modifying a noun phrase",
"independent clause":"clause capable of standing as sentence","dependent clause":"clause dependent on another construction",
"syntax":"system governing combination of linguistic units","grammar":"system of structural rules of language",
"semantics":"study or system of meaning","pragmatics":"meaning in context and use",
"phonology":"system of language sounds","morphology":"system of word structure",
"orthography":"system of written conventions","punctuation":"marks organizing written expression",
"coordination":"joining elements of equal grammatical status","subordination":"embedding dependent grammatical structure",
"transitive":"verb construction permitting or requiring object","intransitive":"verb construction without direct object",
"agent":"participant that initiates action","patient":"participant affected by action",
"recipient":"participant receiving something","theme":"participant moved located or characterized",
"deixis":"context-dependent reference","reference":"relation between expression and what it denotes",
"negation":"grammatical denial or reversal of proposition","question":"interrogative expression seeking information",
"statement":"declarative expression presenting proposition","proposition":"meaning capable of being asserted or evaluated",
}
for w,d in grammar.items(): admit(w,"grammar_seed","explicit_grammar_curriculum")

# Explicit structural grammar relations; no recursive dictionary admission.
relations=[
("article","is_a","determiner"),("noun phrase","headed_by","noun"),("verb phrase","headed_by","verb"),
("sentence","contains","clause"),("clause","contains","predicate"),("predicate","relates_to","subject"),
("direct object","is_a","object"),("indirect object","is_a","object"),
("active voice","is_a","voice"),("passive voice","is_a","voice"),
("singular","is_a","number"),("plural","is_a","number"),("conjugation","is_a","inflection"),
("declension","is_a","inflection"),("modal","is_a","auxiliary"),("relative clause","is_a","clause"),
("independent clause","is_a","clause"),("dependent clause","is_a","clause"),
("coordination","is_a","syntax"),("subordination","is_a","syntax"),
("statement","expresses","proposition"),("question","is_a","interrogative"),
("adjective","modifies","noun"),("adverb","modifies","verb"),("pronoun","substitutes_for","noun phrase"),
("conjunction","connects","clause"),("preposition","expresses","relation"),
]
for a,r,b in relations: edges.append({"a":a,"relation":r,"b":b,"source":"grammar_curriculum"})

counts=defaultdict(int)
for x in lobby.values():
    for k in x["kinds"]: counts[k]+=1
report={"state":"CONTROLLED_LANGUAGE_FOUNDATION_010","reset_semantics":"new lobby artifact; prior experimental results preserved",
"lobby_size":len(lobby),"counts":dict(counts),"entries":dict(sorted(lobby.items())),
"grammar_definitions":grammar,"relations":edges,
"constraints":["No Trial-006 recursive vocabulary carried into this lobby.","No recursive expansion from grammar definitions.","Swadesh hypernym terms come only from the existing recorded Swadesh sandbox.","Grammar vocabulary is an explicit curriculum seed."],
"next_gate":"Use this lobby as the sole vocabulary/relationship state for subsequent grammar/proposition experiments."}
raw=json.dumps(report,ensure_ascii=False,indent=2);report["sha256"]=hashlib.sha256(raw.encode()).hexdigest()
Path("sandbox/echo_lobby_language_foundation_010.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
print("STATUS: CONTROLLED_LANGUAGE_FOUNDATION_010_BUILT")
print("Lobby size:",len(lobby))
print("Counts:",dict(counts))
