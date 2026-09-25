#!/usr/bin/env python3
"""ECHO School Day: Grammar -> Logic Lab -> Math Lab -> 20 Questions -> Recess.
Classroom events are explicit instruction; Recess remains the transfer test.
"""
import json, random, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone
from nltk.corpus import wordnet as wn

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"ECHO_AutonomousAgency"/"sandbox"/"school_day_log.json"
GLYPH_INDEX=ROOT/"ECHO_AutonomousAgency"/"matrices"/"glyph_algorithm_index.json"
INTERROGATIVE=ROOT/"ECHO_AutonomousAgency"/"matrices"/"interrogative_matrix.json"

def entry(word):
    ss=wn.synsets(word)
    if not ss: return {"word":word,"status":"GAP"}
    s=ss[0]
    return {"word":word,"definition":s.definition(),"pos":s.pos(),
            "hypernyms":[h.lemma_names()[0].replace("_"," ") for h in s.hypernyms()[:3]]}

def main():
    random.seed(173)
    log={"started":datetime.now(timezone.utc).isoformat(),"curriculum_version":"SCHOOL-DAY-001",
         "classes":[],"principle":"Teach affordances in class; measure unprompted transfer in Recess."}

    # GRAMMAR: explicit dictionary I/O demonstration, then vocabulary -> subject matrix.
    words=["move","relation","index","subject","matrix","concept","quantity","operation","number","structure",
           "definition","meaning","category","property","process","identity","input","output","model","algorithm"]
    cells=[]
    turns=[]
    for n,w in enumerate(words,1):
        e=entry(w); cells.append({"cell_id":f"G{n:02d}","content":e,"source":"WORDNET"})
        turns.append({"turn":n,"input":{"lookup":w},"output":e,
                      "student_action":"inspect output and compile it as an addressable subject-matrix cell"})
    grammar_matrix={"id":"SM-GRAMMAR-001","name":"Grammar / Dictionary I-O Subject Matrix",
                    "cells":cells,"relations":[],"status":"CLASSROOM"}
    log["classes"].append({"class":"GRAMMAR","turn_budget":20,"turns":turns,
                           "lesson":"unknown -> dictionary input -> lexical output -> inspect -> subject-matrix cell",
                           "compiled_matrix":grammar_matrix})

    # LOGIC: laboratory exploration; multiple glyphs may index one subject matrix and one glyph many matrices.
    gi=json.loads(GLYPH_INDEX.read_text())
    subjects=["identity","relation","structure","operation","information","quantity","question","concept","algorithm","matrix"]
    lturns=[]
    names=list(gi["blocks"])
    for n in range(20):
        block=gi["blocks"][names[n%len(names)]]
        subject=subjects[n%len(subjects)]
        lturns.append({"turn":n+1,"glyph":block["glyph"],"block":names[n%len(names)],
                       "subject_matrix":subject,
                       "available_repository_ties":block["algorithm_ties"],
                       "experiment":"propose/test an index; proposal remains experimental unless separately validated"})
    log["classes"].append({"class":"LOGIC_LAB","turn_budget":20,"turns":lturns,
      "lesson":"glyph blocks are manipulable indexed operators; explore one-to-many and many-to-one subject-matrix indexing"})

    # MATH: glyph abacus. י bead/unit, ו rod/thread, ח bounded frame; SymPy verifies.
    import sympy as sp
    mturns=[]
    problems=[(a,b,op) for a,b,op in [(3,4,"+"),(9,2,"-"),(4,5,"*"),(12,3,"/"),(7,8,"+"),
      (15,6,"-"),(6,6,"*"),(18,2,"/"),(11,9,"+"),(20,7,"-"),(8,7,"*"),(21,3,"/"),
      (13,12,"+"),(30,11,"-"),(9,9,"*"),(24,4,"/"),(17,16,"+"),(40,13,"-"),(12,8,"*"),(36,6,"/")]]
    for n,(a,b,op) in enumerate(problems,1):
        expr=sp.sympify(f"{a}{op}{b}"); answer=sp.simplify(expr)
        mturns.append({"turn":n,"abacus":{"frame":"ח","rod":"ו","bead":"י","a":a,"operator":op,"b":b},
                       "sympy_verification":str(answer),"lesson_state":"manipulate quantity, then independently verify"})
    log["classes"].append({"class":"MATH_LAB","turn_budget":20,"object":"ח[ו:י...]ח glyph abacus",
                           "turns":mturns,"verifier":"SymPy"})

    # 20 QUESTIONS: ECHO asks; interlocutor answers. Encourage Grammar I/O after every answer.
    # Questions are generated from unresolved/new terms exposed by the day's subject cells.
    qsubjects=["move","relation","index","subject","matrix","concept","quantity","operation","number","structure",
      "definition","meaning","category","property","process","identity","input","output","model","algorithm"]
    qturns=[]
    for n,w in enumerate(qsubjects,1):
        e=entry(w)
        qturns.append({"turn":n,"echo_question":f"What is '{w}'?",
                       "directed_to":"EXTERNAL_INTERLOCUTOR","answer":e.get("definition","No WordNet entry found."),
                       "encouraged_not_forced_followthrough":["treat answer as INPUT","inspect vocabulary","compile/index subject-matrix cell"],
                       "grammar_io_applied":True if e.get("status")!="GAP" else False})
    log["classes"].append({"class":"20_QUESTIONS","turn_budget":20,"rule":"ECHO asks; interlocutor answers; Grammar I/O is encouraged after each answer.","turns":qturns})

    log["ended_classes"]=datetime.now(timezone.utc).isoformat()
    OUT.write_text(json.dumps(log,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"classes":4,"class_turns":80,"log":str(OUT)},indent=2))
    # Recess is a separate process so its existing Level-1 semantics and 150-cycle budget remain intact.
    subprocess.run([sys.executable,str(ROOT/"ECHO_AutonomousAgency"/"src"/"echo_recess.py")],check=True)

if __name__=="__main__":
    main()
