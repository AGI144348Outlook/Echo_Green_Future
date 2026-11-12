#!/usr/bin/env python3
"""ECHO-020 independent educational study, before held-out year-end exam.

This is Echo's experimental algorithmic WordNet+card/evidence learner, NOT an
LLM surrogate, and NOT a live Neon-connected full 3^3 Governor. Human-facing
contact UI is not involved. Study duration is 300 real seconds, no action quota.

Pre-test plan: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/448
"""
from __future__ import annotations
import collections
import gzip
import hashlib
import json
import math
import os
import random
import re
import sys
import time
from pathlib import Path

import fitz
import requests
from bs4 import BeautifulSoup
from echo019_resume_wordnet import recover
from nltk.corpus import wordnet as wn

HERE=Path(__file__).resolve().parent
MANIFEST=HERE/"echo020_grade1_source_manifest.json"
STOP=set("the and for with into this that have they them which what when where from were there their it its you your our has are was how why did who his her she him had does can could all would through been not more most some many of in on is be a an to by or as at do will about each after before than while then".split())
TOKEN_RE=re.compile(r"[a-z][a-z'-]{2,}",re.I)

def words(x):
    return [t.lower() for t in TOKEN_RE.findall(str(x)) if t.lower() not in STOP]
def phrase_split(text):
    # Preserve all extractable text, but sentence-tokenize for contextual cards.
    chunks=re.split(r"(?<=[.!?])\s+(?=[A-Z0-9“\"'])|[\r\n]{2,}",text)
    return [s.strip() for s in chunks if len(s.strip())>=12]
def stable_hash(obj):
    return hashlib.sha256(obj).hexdigest()
def read_educational_sources(outdir):
    """Get actual Core Knowledge grade-one books at the original cited URLs.
    PDF text extraction happens locally; no copyrighted full texts in artifacts.
    """
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    source_log=[]
    pages=[]
    s=requests.Session()
    s.headers.update({"User-Agent":"Mozilla/5.0 (compatible; EchoEducationalStudy/0.2; educational research)"})
    for row in manifest["sources"]:
        r=s.get(row["url"],timeout=110)
        r.raise_for_status()
        data=r.content
        if row["type"]=="pdf":
            if not data.startswith(b"%PDF"):raise RuntimeError("Not a PDF "+row["id"])
            doc=fitz.open(stream=data,filetype="pdf")
            original_page_count=len(doc)
            texts=[p.get_text(sort=True) for p in doc]
            doc.close()
        else:
            soup=BeautifulSoup(data,"html.parser")
            for elem in soup.select("script,style,nav,footer,header,form"):
                elem.decompose()
            article=soup.select_one("main") or soup.select_one("article") or soup.body or soup
            texts=[article.get_text(" ",strip=True)]
            original_page_count=1
        if sum(len(x.strip()) for x in texts)<200:raise RuntimeError("Source text extraction insufficient "+row["id"])
        for i,p in enumerate(texts):
            if p.strip(): pages.append({"id":f"{row['id']}:p{i+1}","source_id":row["id"],"subject":row["strand"],
              "page":i+1,"hash":stable_hash(p.encode("utf-8")),"text":p})
        source_log.append({
            "id":row["id"],"title":row["title"],"strand":row["strand"],"source_url":row["url"],
            "sha256":stable_hash(data),"license_note":row["license"],"bytes":len(data),
            "pages":original_page_count,"pages_text_extracted":sum(bool(p.strip()) for p in texts),
            "total_extracted_chars":sum(len(p) for p in texts)
        })
    # The corpus is broad; do not artificially cap source pages or original
    # WordNet vocabulary. All pages are available to the study policy.
    (outdir/"source_manifest_checksums.json").write_text(json.dumps(source_log,indent=2)+"\n")
    print("ECHO020_SOURCES "+json.dumps({
        "materials":len(source_log),"available_pages":len(pages),
        "total_source_bytes":sum(x["bytes"] for x in source_log),
        "subjects":dict(collections.Counter(x["strand"] for x in source_log))
    }),flush=True)
    return pages,source_log

def restore_echo019(archive_dir):
    """Rebuild previous study state exactly from parent + ECHO019 event records."""
    old_dir=archive_dir/"echo017_parent_checkpoint"
    old_dir.mkdir(exist_ok=True,parents=True)
    aliases={
        "parent_echo017_summary.json":"echo017_full_wordnet_summary.json",
        "parent_echo017_episodes.jsonl.gz":"echo017_full_wordnet_episodes.jsonl.gz",
        "parent_echo017_edges.jsonl.gz":"echo017_full_wordnet_proposed_edges.jsonl.gz",
    }
    for name,alias in aliases.items():
        if not (archive_dir/name).is_file():raise RuntimeError("Missing archived parent "+name)
        # Symlink to original bytes; no copying large files.
        target=old_dir/alias
        if not target.exists():target.symlink_to((archive_dir/name).resolve())
    agent,parent,meta=recover(old_dir)
    prior=json.loads((archive_dir/"echo019_resumed_summary.json").read_text())
    if prior.get("id")!="ECHO-019-FULL-WORDNET-RESUMED-300S":
        raise RuntimeError("Unexpected ECHO-019 checkpoint")
    new_log=archive_dir/"echo017_full_wordnet_episodes.jsonl.gz"
    if not new_log.is_file():raise RuntimeError("Missing ECHO-019 new-session episodes")
    n=0
    with gzip.open(new_log,"rt",encoding="utf8") as file:
        for line in file:
            e=json.loads(line)
            if int(e["step"])!=agent.current_step+1:raise RuntimeError("Noncontiguous ECHO-019 episode")
            out=agent._perform(e["tool"],e["input"])
            if out.get("outcome")!=e["result"]:
                raise RuntimeError("Historical semantic event divergence at "+str(e["step"]))
            agent.current_step+=1
            agent.effects[e["result"]]+=1
            agent.families[e["tool"]]+=1
            n+=1
    old_policy=prior["policy_state"]
    if sum(x["n"] for x in old_policy.values())!=prior["action_count"]:
        raise RuntimeError("ECHO-019 saved policy count mismatch")
    agent.arm={k:dict(v) for k,v in old_policy.items()}
    expected=(prior["action_count"],prior["words_with_senses_explored"],
              prior["new_source_lexical_edges"],prior["new_study_cards"],
              prior["remaining_proposal_queue"])
    actual=(agent.current_step,len(agent.words_studied),len(agent.edges),len(agent.cards),len(agent.edge_pending))
    if actual!=expected:raise RuntimeError("ECHO-019 recovery mismatch: "+str(actual)+" != "+str(expected))
    report={"prior_actions":agent.current_step,"prior_words":len(agent.words_studied),
       "prior_edges":len(agent.edges),"prior_cards":len(agent.cards),
       "prior_pending":len(agent.edge_pending),"replayed_episodes":n,
       "parent_recovery_errors":meta["restoration_mismatches"],
       "random_state":"deterministically_reseeded; full prior RNG state not stored"}
    print("ECHO020_RECOVERY "+json.dumps(report),flush=True)
    return agent,report

class EchoSchool:
    """Source-driven acquisition using dictionary/catalog/evidence capabilities.

    UCB reward depends on source novelty and review, not on held-out answer keys.
    The curriculum is indexed as source-labeled observations rather than passed
    into a language model. Tools are internal Echo study actions only.
    """
    def __init__(self, wordnet_agent,pages,seed=2020):
        self.wn=wordnet_agent
        self.pages=pages
        self.index={}
        self.sentences=[]
        self.page_cursor=0
        self.cards={}
        self.links={}
        self.context_terms=collections.deque()
        self.reviewed=set()
        self.patterns=collections.Counter()
        self.events=collections.Counter()
        self.rng=random.Random(seed)
        self.policy={x:{"n":0,"reward":0.0,"ema":0.0} for x in [
            "catalog.source.read","dictionary.senses.explore",
            "catalog.source.card","evidence.content.link",
            "evidence.context.review","evidence.pattern.inspect"
        ]}
        self.study_steps=0
        self.post_source=[]

    def pick(self):
        actions=[]
        total=sum(a["n"] for a in self.policy.values())
        for name,a in self.policy.items():
            if name=="catalog.source.card" and not self.sentences:continue
            if name=="evidence.content.link" and not self.sentences:continue
            if name=="evidence.context.review" and not self.sentences:continue
            if name=="evidence.pattern.inspect" and not self.sentences:continue
            if name=="dictionary.senses.explore" and not self.context_terms:continue
            mean=a["reward"]/a["n"] if a["n"] else 0
            ucb=0.75*math.sqrt(2*math.log(total+2)/a["n"]) if a["n"] else 100
            actions.append((mean+ucb,self.rng.random(),name))
        return max(actions)[2]

    def action(self, tool):
        if tool=="catalog.source.read":
            if self.page_cursor>=len(self.pages):
                source=self.rng.choice(self.pages)
                fresh=False
            else:
                source=self.pages[self.page_cursor]
                self.page_cursor+=1
                fresh=True
            token_list=words(source["text"])
            self.context_terms.extend(x for x in token_list if x not in self.wn.words_studied)
            # Index source text by page/paragraph without guessing contents.
            added=0
            for sent in phrase_split(source["text"]):
                sid=stable_hash((source["id"]+"|"+sent).encode())[:20]
                if sid in self.index:continue
                item={"id":sid,"source":source["id"],"strand":source["subject"],
                      "text":sent,"tokens":list(set(words(sent)))}
                self.index[sid]=item
                self.sentences.append(item)
                added+=1
            return ("page_read" if fresh else "page_revisited",min(0.45,0.08+added*0.008) if fresh else 0.0,
                    {"source":source["id"],"new_sentence_records":added})

        if tool=="dictionary.senses.explore":
            term=self.context_terms.popleft()
            if term not in self.wn.lemma_set:return ("not_in_wordnet",0.02,{"word":term})
            response=self.wn._study_senses(term)
            good=response.get("outcome")=="senses_loaded"
            return ("sense_linked" if good else "absent_sense",0.16 if good and response.get("novel") else 0,
                    {"word":term,"synsets":response.get("synsets",0)})

        if tool=="catalog.source.card":
            s=self.rng.choice(self.sentences)
            cid="g1:source:"+s["id"]
            if cid in self.cards:return ("revisited_card",0,{"card":cid})
            self.cards[cid]={"card_id":cid,"source_ref":s["source"],"source_hash":s["id"],
               "review_state":"proposed","tokens":s["tokens"],"strand":s["strand"]}
            return ("proposed_source_card",0.18,{"card":cid,"source":s["source"]})

        if tool=="evidence.content.link":
            s=self.rng.choice(self.sentences)
            terms=[x for x in s["tokens"] if x in self.wn.lemma_set]
            if len(terms)<2:return ("insufficient_wordnet_relation",0.01,{"source":s["source"]})
            a,b=self.rng.sample(terms,2)
            edge=tuple(sorted((a,b)))+(s["id"],)
            k=stable_hash("|".join(edge).encode())[:24]
            if k in self.links:return ("link_revisited",0,{"edge_id":k})
            self.links[k]={"edge_id":k,"source_words":list(edge[:2]),"source_ref":s["source"],
                "witness_sentence_id":s["id"],"relation_type":"co_occurs_in_source",
                "evidence_state":"proposed","independently_verified":False}
            return ("proposed_context_edge",0.17,{"edge_id":k,"source":s["source"]})

        if tool=="evidence.context.review":
            s=self.rng.choice(self.sentences)
            key=s["id"]
            if key in self.reviewed:return ("revisited_source",0,{"source":s["source"]})
            self.reviewed.add(key)
            for t in s["tokens"]:
                if t in self.wn.lemma_set and t not in self.wn.words_studied:
                    self.context_terms.append(t)
            return ("reviewed_source",0.11,{"source":s["source"],"related_terms":len(s["tokens"])})

        if tool=="evidence.pattern.inspect":
            s=self.rng.choice(self.sentences)
            txt=s["text"].lower()
            for cue in ("addition","subtraction","sum","difference","add","subtract","total",
                        "plus","minus","tens","ones","sentence","noun","verb",
                        "punctuation","question mark","vowel","consonant"):
                if cue in txt:self.patterns[cue]+=1
            for sign in ("+","−","-","="):
                if sign in txt:self.patterns[sign]+=1
            return ("inspected_patterns",0.08 if any(cue in txt for cue in ("add","sum","subtract","tens","vowel","noun")) else 0.005,
                {"source":s["source"]})
        raise RuntimeError("Non-authorized education tool "+tool)

    def study(self, seconds,folder):
        if not (0<seconds<=300):raise ValueError("Only authorized maximum 300 seconds")
        folder.mkdir(exist_ok=True,parents=True)
        path=folder/"echo020_study_actions.jsonl.gz"
        t0=time.monotonic()
        with gzip.open(path,"wt",encoding="utf8",compresslevel=3) as f:
            until=t0+seconds
            last=t0
            while time.monotonic()<until:
                tool=self.pick()
                outcome,reward,details=self.action(tool)
                self.study_steps+=1
                self.events[outcome]+=1
                arm=self.policy[tool];arm["n"]+=1;arm["reward"]+=reward
                arm["ema"]=0.20*reward+0.80*arm["ema"]
                f.write(json.dumps({"step":self.study_steps,"tool":tool,"outcome":outcome,
                                    "reward":reward,"details":details},separators=(",",":"))+"\n")
                now=time.monotonic()
                if now-last>=30:
                    print("ECHO020_STUDY_PROGRESS "+json.dumps({
                        "elapsed_seconds":round(now-t0,3),"operations":self.study_steps,
                        "pages_read":self.page_cursor,"cards":len(self.cards),
                        "proposed_edges":len(self.links),"sentence_witnesses":len(self.sentences)
                    }),flush=True)
                    last=now
        elapsed=time.monotonic()-t0
        return {"elapsed_seconds":elapsed,"new_operations":self.study_steps,
                "source_pages_total":len(self.pages),"source_pages_read":self.page_cursor,
                "source_sentence_witnesses":len(self.sentences),"new_provisional_cards":len(self.cards),
                "new_provisional_lexical_edges":len(self.links),
                "wordnet_words_total":len(self.wn.words_studied),
                "original_wordnet_policy_preserved":True,
                "curriculum_policy":self.policy,"outcomes":dict(self.events),
                "study_stage":"experiment-only; not live Neon, not a speaking interface"}

    def answer(self,prompt,passage=""):
        """Generic text-search + source-supported arithmetic expression model.

        The respondent cannot read the question bank or rubric. It gets only
        a question string and optional unseen reading passage; it may abstain.
        """
        query=words(prompt)
        if not query:return {"text":None,"reason":"no_query_terms","source_refs":[]}

        # Simple algorithmic numeric operators become eligible from observed
        # real grade-one mathematical pages only; never a test-item lookup.
        import re
        num=[int(x) for x in re.findall(r"\d+",prompt)]
        explicit_plus=bool(re.search(r"\d+\s*\+\s*\d+",prompt))
        explicit_minus=bool(re.search(r"\d+\s*[-−]\s*\d+",prompt))
        enabled_add=(self.patterns["addition"]+self.patterns["sum"]+self.patterns["add"]+
                     self.patterns["+"]+self.patterns["plus"])>0
        enabled_sub=(self.patterns["subtraction"]+self.patterns["difference"]+
                     self.patterns["subtract"]+self.patterns["minus"])>0
        if len(num)>=2 and (explicit_plus or explicit_minus):
            if explicit_plus and enabled_add:
                return {"text":str(num[0]+num[1]),"reason":"observed_math_operator",
                    "source_refs":["curriculum:math:observed_addition"]}
            if explicit_minus and enabled_sub:
                return {"text":str(num[0]-num[1]),"reason":"observed_math_operator",
                    "source_refs":["curriculum:math:observed_subtraction"]}
        if len(num)>=2 and enabled_add and any(x in prompt.lower() for x in ("more","altogether","total","finds","now")):
            return {"text":str(sum(num[:2])),"reason":"observed_math_structure",
                    "source_refs":["curriculum:math:observed_addition"]}
        if len(num)>=2 and enabled_sub and any(x in prompt.lower() for x in ("left","gave","remaining")):
            return {"text":str(num[0]-num[1]),"reason":"observed_math_structure",
                    "source_refs":["curriculum:math:observed_subtraction"]}

        # Evidence retrieval rather than independently authored sentences:
        # For reading, the paragraph is supplied in the assessment itself.
        pool=[]
        for p in phrase_split(passage):
            pool.append({"text":p,"source":"assessment:unseen_passage","tokens":list(set(words(p)))})
        # The agent can recall material only if it was actually indexed.
        pool.extend(self.sentences)
        qs=set(query)
        ranked=[]
        for doc in pool:
            ts=set(doc["tokens"])
            overlap=qs&ts
            if not overlap:continue
            value=len(overlap)/(len(qs)+2)+len(overlap)/(len(ts)+5)
            if doc["source"]=="assessment:unseen_passage":value+=0.65
            ranked.append((value,doc))
        if not ranked:return {"text":None,"reason":"no_evidence_path","source_refs":[]}
        ranked.sort(key=lambda t:(-t[0],t[1]["source"],t[1]["text"]))
        best=ranked[0]
        if best[0]<0.21:return {"text":None,"reason":"insufficient_evidence","source_refs":[]}
        # A source-derived fragment is not a fluent generated answer.
        return {"text":best[1]["text"][:300],"reason":"source_retrieval_fragment",
                "source_refs":[best[1]["source"]],"score":round(best[0],4)}

def evaluate_prompts(agent,prompts):
    answers=[]
    for p in prompts:
        x=agent.answer(p["question"],p.get("passage",""))
        answers.append({"id":p["id"],"strand":p["strand"],
                        "question":p["question"],"raw_answer":x["text"],
                        "reason":x["reason"],"source_refs":x["source_refs"]})
    return answers

def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--parent",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--prompts",type=Path,required=True)
    parser.add_argument("--seconds",type=float,default=300)
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    echo,restored=restore_echo019(args.parent)
    # Exam prompts contain NO keys. The evaluator/answer key is a separate
    # executable and is only launched after this study process exits.
    raw=json.loads(args.prompts.read_text())
    if any("acceptable" in x for x in raw["questions"]):
        raise RuntimeError("Exam answer keys leaked to study process")
    baseline=EchoSchool(echo,[])
    before=evaluate_prompts(baseline,raw["questions"])
    (args.out/"before_raw_answers.json").write_text(json.dumps(before,indent=2)+"\n")
    pages,srcmeta=read_educational_sources(args.out)
    learner=EchoSchool(echo,pages)
    performance=learner.study(args.seconds,args.out)
    after=evaluate_prompts(learner,raw["questions"])
    (args.out/"after_raw_answers.json").write_text(json.dumps(after,indent=2)+"\n")
    # Preserve only source references, source hashes and provisional research
    # graph summaries, not wholesale copies of copyrighted textbook pages.
    (args.out/"curriculum_evidence_summary.json").write_text(json.dumps({
        "sources":srcmeta,"source_cards":list(learner.cards.values())[:250],
        "total_cards":len(learner.cards),
        "link_examples":list(learner.links.values())[:250],
        "total_links":len(learner.links),
        "patterns_observed":dict(learner.patterns)
    },indent=2)+"\n")
    summary={"study":"ECHO-020 Grade 1","prior_wordnet_state":restored,
        "source_count":len(srcmeta),"curriculum":performance,
        "baseline_response_count":sum(bool(a["raw_answer"]) for a in before),
        "post_response_count":sum(bool(a["raw_answer"]) for a in after),
        "pre_and_post_answer_source":"EchoSchool.answer() algorithmic evidence retrieval; no LLM or canned reply",
        "test_key_exposed_during_study":False,"communication_interface_used":False,
        "evidence_state":"proposed / not independently verified",
        "limitation":"No active Neon write-through in GitHub CI; curriculum cards and relations are experimental artifacts"}
    (args.out/"echo020_study_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print("ECHO020_STUDY_RESULT "+json.dumps({
        "seconds":performance["elapsed_seconds"],"actions":performance["new_operations"],
        "sources":len(srcmeta),"pages_studied":performance["source_pages_read"],
        "cards":performance["new_provisional_cards"],"edges":performance["new_provisional_lexical_edges"],
        "baseline_responses":summary["baseline_response_count"],
        "post_responses":summary["post_response_count"]
    }),flush=True)
    if performance["elapsed_seconds"]<args.seconds:raise RuntimeError("Study stopped before requested duration")

if __name__=="__main__":
    main()
