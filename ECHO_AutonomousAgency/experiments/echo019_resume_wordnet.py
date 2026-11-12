#!/usr/bin/env python3
"""ECHO-019: resume full WordNet study from prior ECHO-017 archival evidence.

Pre-test: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/438
Replays historical action inputs to reconstruct in-memory meaning, cards,
evidence nodes, pending edge candidates and UCB/EMA policy. Replay is NOT
counted as new learning. Then gives Echo another unpaced 300-second study.
Only Dictionary, Catalog, Evidence operations are discoverable.

This runner uses complete NLTK WordNet, not a 22-word fixture. It does
NOT claim the GitHub-runner session writes live Neon; actual research output
and a new restorable checkpoint artifact are preserved with provenance.
"""
from __future__ import annotations
import argparse
import collections
import gzip
import json
import random
import shutil
import time
from pathlib import Path

from echo017_full_wordnet_study import Study

EXPECTED_PARENT = "ECHO-017-FULL-WORDNET-300S"
SOURCE = "Princeton WordNet via NLTK"
REQUIRED_TOOLS = {
    "dictionary.lexical_senses",
    "dictionary.semantic_neighbors",
    "dictionary.definition_terms",
    "catalog.card.propose",
    "catalog.card.read",
    "evidence.node.get",
    "evidence.edge.trace",
    "evidence.edge.propose",
}

def recover(parent: Path) -> tuple[Study, dict, dict]:
    summary_path = parent / "echo017_full_wordnet_summary.json"
    episode_path = parent / "echo017_full_wordnet_episodes.jsonl.gz"
    edge_path = parent / "echo017_full_wordnet_proposed_edges.jsonl.gz"
    if not all(path.is_file() for path in (summary_path, episode_path, edge_path)):
        raise RuntimeError("Parent checkpoint is missing its summary, episodes or edge log")
    old = json.loads(summary_path.read_text())
    if old.get("id") != EXPECTED_PARENT:
        raise RuntimeError("Wrong parent experiment; refusing to reset state")
    if set(old.get("allowed_tool_names", [])) != REQUIRED_TOOLS:
        raise RuntimeError("Parent tool scope mismatch")
    if old.get("source") != SOURCE or not old.get("dictionary_source_complete"):
        raise RuntimeError("Parent corpus mismatch")

    st = Study(seed=17017 + int(old["action_count"]))
    if st.full_synsets != old["wordnet_total_synsets_available"]:
        raise RuntimeError("WordNet synset count changed; cannot reconstruct safely")
    if len(st.full_lemmas) != old["wordnet_lemma_names_available"]:
        raise RuntimeError("WordNet lemma inventory changed; cannot reconstruct safely")

    expected_episodes = int(old["action_count"])
    start = time.monotonic()
    errors, changes, laststep, visits = 0, 0, 0, 0
    with gzip.open(episode_path, "rt", encoding="utf-8") as records:
        for line in records:
            rec = json.loads(line)
            step = int(rec["step"])
            if step != laststep + 1:
                raise RuntimeError("Noncontiguous source episode at " + str(step))
            tool = rec["tool"]
            if tool not in REQUIRED_TOOLS:
                raise RuntimeError("Unapproved tool in original action history: " + tool)
            result = st._perform(tool, rec["input"])
            if result.get("outcome") != rec["result"]:
                errors += 1
                if errors <= 4:
                    print("RESTORE_MISMATCH " + json.dumps({
                        "step":step, "tool":tool, "observed":result.get("outcome"),
                        "recorded":rec["result"]}), flush=True)
            st.families[tool] += 1
            st.effects[rec["result"]] += 1
            laststep = step
            visits += 1
            if visits % 50000 == 0:
                print("RESTORE_PROGRESS " + json.dumps({
                    "replayed_events":visits,
                    "words":len(st.words_studied),
                    "proposed_edges":len(st.edges),
                    "pending_links":len(st.edge_pending),
                    "elapsed_seconds":round(time.monotonic()-start,2)
                }), flush=True)
    if errors:
        raise RuntimeError(f"Restoration diverged from logged operation outcomes: {errors} mismatches")
    if visits != expected_episodes:
        raise RuntimeError(f"Missing source episodes: got {visits}; expected {expected_episodes}")
    # Compare each originally emitted, source-witnessed edge to reconstructed
    # network, including edge ID and associated original synset lineage.
    archive_edges=0
    with gzip.open(edge_path, "rt", encoding="utf-8") as records:
        for line in records:
            edge = json.loads(line)
            archived=st.edges.get(edge["edge_id"])
            if archived is None or any(archived.get(k)!=edge.get(k) for k in (
                "source","target","relation","source_synset","source_ref",
                "evidence_state","relation_domain"
            )):
                raise RuntimeError("Source edge mismatch for " + edge["edge_id"])
            archive_edges += 1
    expected={
        "actions": expected_episodes,
        "studied_words": old["words_with_senses_explored"],
        "proposed_edges": old["new_source_lexical_edges"],
        "proposed_cards": old["new_study_cards"],
        "definition_expansions": old["definition_expansions"],
        "neighbor_expansions": old["neighbor_expansions"],
        "pending_links": old["remaining_proposal_queue"],
        "archived_edges":old["new_source_lexical_edges"]
    }
    actual={
        "actions":visits,
        "studied_words":len(st.words_studied),
        "proposed_edges":len(st.edges),
        "proposed_cards":len(st.cards),
        "definition_expansions":len(st.definition_processed),
        "neighbor_expansions":len(st.neighbors_processed),
        "pending_links":len(st.edge_pending),
        "archived_edges":archive_edges
    }
    if actual != expected:
        raise RuntimeError("Recovered state does not match parent: " +
                           json.dumps({"expected":expected,"actual":actual}))
    old_policy=old["policy_state"]
    if set(old_policy) != REQUIRED_TOOLS:
        raise RuntimeError("Unknown action in saved reinforcement policy")
    if sum(x["n"] for x in old_policy.values()) != visits:
        raise RuntimeError("Policy visits do not match source operation count")
    st.arm={name:dict(stats) for name,stats in old_policy.items()}
    st.current_step=visits
    # The original experiment logged words, decisions and source edges but NOT
    # a Python RNG state. Thus it is impossible to restore its next random
    # bit-for-bit. We use a documented deterministic reseed for continuation.
    # The original completed with an empty frontier, so we preserve that state.
    if old.get("frontier_size_at_end") != 0:
        raise RuntimeError("Nonempty parent word frontier lacks exact queue archive")
    st.frontier.clear()
    metadata={
        "parent_id":old["id"],
        "parent_actions":visits,
        "parent_studied_words":len(st.words_studied),
        "parent_cards":len(st.cards),
        "parent_edges":len(st.edges),
        "parent_pending_links":len(st.edge_pending),
        "parent_policy_restored":True,
        "restoration_mismatches":errors,
        "restoration_seconds":time.monotonic()-start,
        "random_state":"deterministically_reseeded_because_original_rng_state_not_logged",
        "replay_not_counted_as_new_study":True,
        "full_corpus_used":True
    }
    print("ECHO019_RESTORED "+json.dumps(metadata), flush=True)
    return st, old, metadata

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--parent",required=True, type=Path)
    parser.add_argument("--out",required=True, type=Path)
    parser.add_argument("--seconds",type=float,default=300)
    args=parser.parse_args()
    st,previous,restoration=recover(args.parent)
    args.out.mkdir(parents=True,exist_ok=True)
    duration=args.seconds
    if duration<=0 or duration>300:
        raise RuntimeError("Elapsed-time setting exceeds approved 300s session")

    # Use the original study loop; no operation cap, no sleep or paced scheduler.
    result=st.run(seconds=duration,outdir=str(args.out))
    if result["elapsed_active_wall_seconds"] < duration:
        raise RuntimeError("Continuation did not reach the requested wall-clock window")

    increment={
        "new_study_actions":result["action_count"]-previous["action_count"],
        "new_words_with_senses_explored":
            result["words_with_senses_explored"]-previous["words_with_senses_explored"],
        "new_study_cards":result["new_study_cards"]-previous["new_study_cards"],
        "new_source_lexical_edges":
            result["new_source_lexical_edges"]-previous["new_source_lexical_edges"],
        "pending_links_end":result["remaining_proposal_queue"],
        "historical_actions_carried_forward":previous["action_count"],
        "historical_proposed_edges_carried_forward":
            previous["new_source_lexical_edges"]
    }
    if any(increment[x]<0 for x in (
        "new_study_actions","new_words_with_senses_explored",
        "new_study_cards","new_source_lexical_edges"
    )):
        raise RuntimeError("State regressed after resumed study")
    result.update({
        "id":"ECHO-019-FULL-WORDNET-RESUMED-300S",
        "parent_checkpoint":previous["id"],
        "parent_run":"https://github.com/AGI144348Outlook/Echo_Green_Future/actions/runs/43295960761",
        "restoration":restoration,
        "new_work":increment,
        "measurement_warning":"Historical replay preceded, but is not counted toward, the 300-second study window",
        "neon_status":"not live-connected from GitHub: output preserved as research artifact",
        "speaker_status":"no conversational output; Echo's study loop only",
        "provenance_status":"WordNet-derived evidence remains provisional"
    })
    (args.out/"echo019_resumed_summary.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"
    )
    # Preserve the prior original logs along with new-session logs so the next
    # continuation has the entire lineage even after GitHub artifact expiry.
    shutil.copy2(args.parent/"echo017_full_wordnet_episodes.jsonl.gz",
                 args.out/"parent_echo017_episodes.jsonl.gz")
    shutil.copy2(args.parent/"echo017_full_wordnet_proposed_edges.jsonl.gz",
                 args.out/"parent_echo017_edges.jsonl.gz")
    shutil.copy2(args.parent/"echo017_full_wordnet_summary.json",
                 args.out/"parent_echo017_summary.json")
    print("ECHO019_RESULT "+json.dumps({
        "elapsed_study_seconds":result["elapsed_active_wall_seconds"],
        "previous_actions":previous["action_count"],
        "all_actions":result["action_count"],
        "new_actions":increment["new_study_actions"],
        "previous_edges":previous["new_source_lexical_edges"],
        "all_edges":result["new_source_lexical_edges"],
        "new_edges":increment["new_source_lexical_edges"],
        "all_cards":result["new_study_cards"],
        "pending_links_end":result["remaining_proposal_queue"],
        "source_lemmas_available":result["wordnet_lemma_names_available"],
        "recovery_matched":True,
        "no_artificial_pacing":result["no_artificial_pacing"],
        "tool_errors":result["tool_errors"]
    }),flush=True)

if __name__=="__main__":
    main()
