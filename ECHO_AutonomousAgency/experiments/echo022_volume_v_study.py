#!/usr/bin/env python3
"""ECHO-022: source-grounded Volume V lesson continuation, exactly 300s by workflow.
This executes Echo's existing algorithmic WordNet/catalog/evidence learner
with ECHO-019 parent recovery. It is not a language model or the full Governor.
PRE-TEST: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/461
"""
from __future__ import annotations
import argparse, gzip, hashlib, json, time
from pathlib import Path
from echo020_grade1_study import EchoSchool, evaluate_prompts, read_educational_sources, restore_echo019, words

HERE=Path(__file__).resolve().parent
def digest(s:bytes): return hashlib.sha256(s).hexdigest()
def source_pages(path:Path):
    raw=path.read_bytes()
    source=json.loads(raw)
    pages=[]
    manifest=[]
    for material in source["materials"]:
        sid=f"volume-v:{material['source']}"
        manifest.append({"source_id":sid,"title":material["title"],"pdf_sha256":material["sha256"],
                         "lesson_digest_sha256":digest(json.dumps(material,sort_keys=True).encode()),
                         "declared_source":"user-owned Volume V standalone PDF; paraphrased source notes only"})
        for source_page in material["pages"]:
            text="\n".join(source_page["paragraphs"])
            pages.append({"id":sid+":p"+str(source_page["page"]),
                         "source_id":sid,"subject":"volume_v_protocol_switchboard",
                         "page":source_page["page"],"hash":digest(text.encode()),"text":text})
    if len(manifest)!=6 or len({p["id"] for p in pages})!=len(pages):
        raise RuntimeError("Volume V source identity collision or missing source")
    return pages,manifest,digest(raw)

class VolumeVSchool(EchoSchool):
    """Two additional source-bounded inspection actions; not a language model.

    The existing Echo UCB study policy still selects from all available
    dictionary/catalog/evidence tools. The new actions identify documentary
    constraints and contrasts while refusing to assert semantic entailment.
    """
    def __init__(self,wordnet_agent,pages,seed=22022):
        super().__init__(wordnet_agent,pages,seed=seed)
        for tool in ("evidence.constraint.inspect","evidence.source.compare"):
            self.policy[tool]={"n":0,"reward":0.0,"ema":0.0}
        self.constraint_candidates={}
        self.source_comparisons={}

    def action(self,tool):
        if tool=="evidence.constraint.inspect":
            if not self.sentences:
                return super().action("catalog.source.read")
            s=self.rng.choice(self.sentences)
            tokens=set(s["tokens"])
            cue=sorted(tokens.intersection({"not","only","must","requires","without",
                                           "deny","denied","revoked","never","unless"}))
            if not cue:
                return ("no_explicit_constraint_cue",0.0,{"source":s["source"]})
            key=s["id"]
            if key in self.constraint_candidates:
                return ("constraint_revisited",0.0,{"source":s["source"]})
            self.constraint_candidates[key]={"source_ref":s["source"],"witness_sentence_id":key,
                 "lexical_cues":cue,"evidence_state":"candidate",
                 "epistemic_warning":"Lexical cue does not prove authorization, negation scope or truth"}
            return ("constraint_candidate_observed",0.13,{"source":s["source"],"lexical_cues":cue})
        if tool=="evidence.source.compare":
            if len(self.sentences)<2:
                return super().action("catalog.source.read")
            a,b=self.rng.sample(self.sentences,2)
            aa=set(a["tokens"]);bb=set(b["tokens"])
            overlap=sorted(aa.intersection(bb))
            key="|".join(sorted([a["id"],b["id"]]))
            if key in self.source_comparisons:
                return ("comparison_revisited",0.0,{"sources":[a["source"],b["source"]]})
            self.source_comparisons[key]={
                 "left_source":a["source"],"right_source":b["source"],
                 "shared_orthography":overlap,
                 "evidence_state":"observed_co_occurrence_only",
                 "independent_inference":False}
            return ("source_pair_compared",0.08 if overlap else 0.01,
                    {"sources":[a["source"],b["source"]],"overlap_count":len(overlap)})
        return super().action(tool)

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--parent",type=Path,required=True)
    a.add_argument("--out",type=Path,required=True)
    a.add_argument("--prompts",type=Path,required=True)
    a.add_argument("--lessons",type=Path,default=HERE/"echo022_volume_v_lessons.json")
    a.add_argument("--seconds",type=float,default=300.0)
    a.add_argument("--include-grade1",action="store_true")
    args=a.parse_args()
    if args.seconds<=0:raise RuntimeError("Positive real wall-clock processing time required")
    args.out.mkdir(exist_ok=True,parents=True)
    parent,startstate=restore_echo019(args.parent)
    questions=json.loads(args.prompts.read_text())
    # No grading concepts, answers or scoring keys in the study input.
    assert all(set(q)=={"id","strand","question","passage"} for q in questions["questions"])
    before_learner=EchoSchool(parent,[],seed=22022)
    before=evaluate_prompts(before_learner,questions["questions"])
    (args.out/"before_raw_answers.json").write_text(json.dumps(before,indent=2)+"\n")
    vpages,vmanifest,corpus_sha=source_pages(args.lessons)
    prior_pages=[]
    prev_manifest=[]
    previous_error=None
    if args.include_grade1:
        try:
            prior_pages,prev_manifest=read_educational_sources(args.out)
        except Exception as exc:
            # Explicit source failure; a source fetch error is never silently
            # reinterpreted as having studied the old curriculum.
            previous_error=type(exc).__name__+": "+str(exc)[:300]
            print("ECHO022_PRIOR_SOURCE_UNAVAILABLE "+json.dumps({"reason":previous_error}),flush=True)
    pages=[*vpages,*prior_pages]
    if not pages:raise RuntimeError("No study materials")
    print("ECHO022_START "+json.dumps({"volume_v_lesson_pages":len(vpages),
        "prior_grade1_pages":len(prior_pages),"parent_state":startstate,
        "corpus_sha256":corpus_sha,"wall_clock_target_seconds":args.seconds}),flush=True)
    learner=VolumeVSchool(parent,pages,seed=22022)
    prior_words=set(parent.words_studied)
    performance=learner.study(args.seconds,args.out)
    after=evaluate_prompts(learner,questions["questions"])
    (args.out/"after_raw_answers.json").write_text(json.dumps(after,indent=2)+"\n")
    # Rich evidence-backed restorable research artifact: lexical and school
    # state values, plus original source metadata. Not an authenticated Neon write.
    with gzip.open(args.out/"echo022_evidence_checkpoint.json.gz","wt",encoding="utf8") as stream:
        json.dump({"source_digest":corpus_sha,"source_pages":[{k:v for k,v in p.items() if k!="text"} for p in pages],
                   "recorded_sentences":learner.sentences,"proposed_cards":list(learner.cards.values()),
                   "proposed_edges":list(learner.links.values()),
                   "constraint_candidates":list(learner.constraint_candidates.values()),
                   "source_comparisons":list(learner.source_comparisons.values()),
                   "policy":learner.policy,"effects":dict(learner.events),
                   "new_wordnet_senses_explored":sorted(set(parent.words_studied)-prior_words),
                   "prior_parent":startstate,
                   "scope":"reconstruction artifact only, no full live Governor/Neon sync"},stream)
    coverage={p["source_id"] for p in learner.pages[:learner.page_cursor]}
    report={"protocol":"ECHO-022","producer":"EchoSchool + archived WordNet Study",
        "source":"Volume V paraphrased lessons + optional original grade-one materials",
        "prior_restored_ECHO019":startstate,
        "ECHO020_ECHO021_educational_state_recovered":False,
        "reason":"No authenticated exact replay of their educational caches was demonstrated",
        "elapsed_study_seconds":performance["elapsed_seconds"],"work":performance,
        "volume_v_pdf_refs":vmanifest,"volume_v_lesson_sha256":corpus_sha,
        "volume_v_coverage":sorted(coverage.intersection({v["source_id"] for v in vmanifest})),
        "constraint_candidate_count":len(learner.constraint_candidates),
        "source_pair_comparisons":len(learner.source_comparisons),
        "prior_grade1_sources_available":len(prev_manifest),
        "prior_grade1_source_error":previous_error,
        "baseline_nonempty":sum(bool(x["raw_answer"]) for x in before),
        "post_nonempty":sum(bool(x["raw_answer"]) for x in after),
        "reason_codes_after":{reason:sum(x.get("reason")==reason for x in after)
                             for reason in sorted({x.get("reason") for x in after})},
        "epistemic_statement":"Source fragments are NOT independent inference. No live Neon write or genuine OpenDiagram-authored cognition."}
    (args.out/"echo022_run_summary.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print("ECHO022_300S_RESULT "+json.dumps({"seconds":round(performance["elapsed_seconds"],3),
        "operations":performance["new_operations"],"volume_v_sources":report["volume_v_coverage"],
        "cards":performance["new_provisional_cards"],"edges":performance["new_provisional_lexical_edges"],
        "before_nonempty":report["baseline_nonempty"],"after_nonempty":report["post_nonempty"]}),flush=True)
    if performance["elapsed_seconds"]<args.seconds:
        raise RuntimeError("300-second Echo processing failed to reach requested duration")
if __name__=="__main__":main()
