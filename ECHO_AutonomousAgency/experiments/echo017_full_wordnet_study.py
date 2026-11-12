#!/usr/bin/env python3
"""ECHO-017 FULL WORDNET: time-bounded, unpaced, self-directed algorithmic study.

Pre-test amendment: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/438
No 22-word fixture; the entire Princeton WordNet corpus is available at runtime.
The only discoverable tools are Dictionary / Catalog / Evidence (8 capabilities).

IMPORTANT: This is an in-process JSON-RPC/MCP-style research runtime; GitHub
Actions does not have a production or development Neon credential. Live Neon
card/evidence state must be reconciled by an authorized connector after the
run. Do not claim live Neon calls from this runner.
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

from nltk.corpus import wordnet as wn


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = json.loads((ROOT / "ECHO_AutonomousAgency/neon/echo017_full_wordnet_mcp_tools.json").read_text())
ALLOWED_SYSTEMS = {"dictionary", "catalog", "evidence"}
ALLOWED_TOOLS = {t["name"] for t in MANIFEST["tools"]}
WORD_RE = re.compile(r"[a-z][a-z_-]{2,}", re.I)


def word_normalize(word):
    return str(word).strip().lower().replace(" ", "_")


def key_hash(*parts):
    return hashlib.sha256("|".join(str(p) for p in parts).encode("utf8")).hexdigest()[:24]


class Study:
    def __init__(self, seed=17017):
        self.rng = random.Random(seed)
        self.start_at = None
        self.corpus_version = "Princeton WordNet via nltk.corpus.wordnet"
        # The complete WordNet lemma vocabulary: not a curated seed or fixed
        # sample, and not the 22-record Neon wordnet_chain experiment.
        self.full_lemmas = tuple(wn.all_lemma_names())
        self.lemma_set = set(self.full_lemmas)
        self.full_synsets = sum(1 for _ in wn.all_synsets())
        if len(self.full_lemmas) < 100000 or self.full_synsets < 100000:
            raise RuntimeError(
                f"WordNet corpus incomplete: lemmas={len(self.full_lemmas)} synsets={self.full_synsets}"
            )
        self.frontier = collections.deque()
        self.frontier_seen = set()
        self.words_studied = {}
        self.definition_processed = set()
        self.neighbors_processed = set()
        self.cards = {}
        self.nodes = {}
        self.edges = {}
        self.edge_pending = collections.deque()
        self.edge_queued = set()
        self.seen_card_reads = set()
        self.seen_node_reads = set()
        self.seen_edge_reads = set()
        self.current_step = 0
        self.effects = collections.Counter()
        self.names = sorted(ALLOWED_TOOLS)
        self.arm = {name: {"n": 0, "total": 0.0, "ema": 0.0} for name in self.names}
        self.families = collections.Counter()
        self.episodes_path = None
        self.edge_path = None
        self._episode_stream = None
        self._edge_stream = None
        self._newly_seen_words = set()

    def start_logging(self, outdir):
        outdir = Path(outdir)
        outdir.mkdir(parents=True, exist_ok=True)
        self.episodes_path = outdir / "echo017_full_wordnet_episodes.jsonl.gz"
        self.edge_path = outdir / "echo017_full_wordnet_proposed_edges.jsonl.gz"
        self._episode_stream = gzip.open(self.episodes_path, "wt", encoding="utf-8", compresslevel=3)
        self._edge_stream = gzip.open(self.edge_path, "wt", encoding="utf-8", compresslevel=3)

    def finish_logging(self):
        for stream in (self._episode_stream, self._edge_stream):
            if stream is not None:
                stream.close()

    def log_episode(self, entry):
        if self._episode_stream is not None:
            self._episode_stream.write(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n")

    def log_edge(self, entry):
        if self._edge_stream is not None:
            self._edge_stream.write(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n")

    def tools_list(self):
        return {"tools": [
            {"name": t["name"], "description": t["description"], "inputSchema": t["inputSchema"]}
            for t in MANIFEST["tools"]
        ]}

    def mcp_request(self, req):
        if req.get("jsonrpc") != "2.0":
            return {"jsonrpc": "2.0", "id": req.get("id"), "error": {"code": -32600, "message": "Invalid JSON-RPC"}}
        method = req.get("method")
        if method == "tools/list":
            return {"jsonrpc": "2.0", "id": req.get("id"), "result": self.tools_list()}
        if method != "tools/call":
            return {"jsonrpc": "2.0", "id": req.get("id"), "error": {"code": -32601, "message": "Method unavailable"}}
        params = req.get("params") or {}
        name = params.get("name")
        if name not in ALLOWED_TOOLS or name.split(".", 1)[0] not in ALLOWED_SYSTEMS:
            return {"jsonrpc": "2.0", "id": req.get("id"), "error": {"code": -32602, "message": "Tool unavailable"}}
        args = params.get("arguments") or {}
        schema = next(t["inputSchema"] for t in MANIFEST["tools"] if t["name"] == name)
        if not isinstance(args, dict) or set(args) != set(schema["required"]):
            return {"jsonrpc": "2.0", "id": req.get("id"), "error": {"code": -32602, "message": "Invalid arguments"}}
        try:
            response = self._perform(name, args)
        except Exception as exc:
            return {"jsonrpc": "2.0", "id": req.get("id"), "result": {
                "content": [{"type": "text", "text": json.dumps({"error": type(exc).__name__})}],
                "isError": True}}
        return {"jsonrpc": "2.0", "id": req.get("id"), "result": {
            "content": [{"type": "text", "text": json.dumps(response, ensure_ascii=False)}],
            "isError": False}}

    def _next_word(self):
        # An autonomous frontier, drawing from ALL WordNet lemma names when
        # no informative frontier items remain, not from a 22-word fixture.
        for _ in range(8):
            if self.frontier and self.rng.random() < 0.84:
                w = self.frontier.popleft()
            else:
                w = self.rng.choice(self.full_lemmas)
            if w in self.lemma_set and w not in self.words_studied:
                return w
        return self.rng.choice(self.full_lemmas)

    def _add_frontier(self, words):
        for raw in words:
            w = word_normalize(raw)
            if w in self.lemma_set and w not in self.frontier_seen and w not in self.words_studied:
                self.frontier.append(w)
                self.frontier_seen.add(w)

    def _study_senses(self, word):
        synsets = wn.synsets(word)  # ALL senses; no artificial 8-sense ceiling.
        if not synsets:
            return {"outcome": "absent", "word": word, "novel": False}
        new = word not in self.words_studied
        records = [
            {"synset": s.name(), "definition": s.definition(),
             "examples": list(s.examples()), "lemmas": [l.name() for l in s.lemmas()],
             "hypernyms": [x.name() for x in s.hypernyms()]}
            for s in synsets
        ]
        self.words_studied[word] = records
        self._newly_seen_words.add(word)
        for s in synsets:
            self.nodes.setdefault("wn:" + s.name(), {
                "node_id": "wn:" + s.name(), "source_ref": "Princeton WordNet:" + s.name(),
                "node_kind": "lexical_sense", "epistemic_state": "source_observation"})
            self._queue_edge({
                "source": "lemma:" + word, "target": "wn:" + s.name(),
                "relation": "lemma_has_sense", "source_synset": s.name(),
                "source_ref": "Princeton WordNet:" + s.name()})
        return {"outcome": "senses_loaded", "word": word, "novel": new,
                "synsets": len(records), "provenance": "Princeton WordNet"}

    def _queue_edge(self, edge):
        edge_id = key_hash(edge["source"], edge["target"], edge["relation"], edge["source_synset"])
        if edge_id not in self.edge_queued and edge_id not in self.edges:
            self.edge_pending.append((edge_id, edge))
            self.edge_queued.add(edge_id)

    def _perform(self, name, args):
        word = word_normalize(args.get("word", ""))
        if name == "dictionary.lexical_senses":
            return self._study_senses(word)

        if name == "dictionary.semantic_neighbors":
            records = self.words_studied.get(word)
            if records is None:
                return {"outcome": "no_prior_sense_context", "word": word}
            new = word not in self.neighbors_processed
            connected = []
            for s in wn.synsets(word):
                for h in s.hypernyms():
                    self._queue_edge({
                        "source": "wn:" + s.name(), "target": "wn:" + h.name(),
                        "relation": "hypernym", "source_synset": s.name(),
                        "source_ref": "Princeton WordNet:" + s.name()})
                    connected.extend(x.name() for x in h.lemmas())
                for l in s.lemmas():
                    connected.append(l.name())
                for h in s.hyponyms():
                    connected.extend(x.name() for x in h.lemmas())
            self._add_frontier(connected)
            self.neighbors_processed.add(word)
            return {"outcome": "neighbors_found", "word": word, "novel": new,
                    "related_lemmas": len(connected)}

        if name == "dictionary.definition_terms":
            records = self.words_studied.get(word)
            if records is None:
                return {"outcome": "no_prior_sense_context", "word": word}
            new = word not in self.definition_processed
            terms = []
            for record in records:
                terms.extend(WORD_RE.findall(record["definition"].lower()))
                for example in record["examples"]:
                    terms.extend(WORD_RE.findall(example.lower()))
            self._add_frontier(terms)
            self.definition_processed.add(word)
            return {"outcome": "definitions_explored", "word": word, "novel": new,
                    "definition_tokens": len(terms)}

        if name == "catalog.card.propose":
            records = self.words_studied.get(word)
            if records is None:
                return {"outcome": "no_prior_sense_context", "word": word}
            card_id = "wnword:" + word
            is_new = card_id not in self.cards
            if is_new:
                self.cards[card_id] = {
                    "card_id": card_id, "revision": 1, "card_kind": "lexical_context",
                    "source": "Princeton WordNet", "word": word,
                    "synsets": [rec["synset"] for rec in records],
                    "review_state": "proposed", "knowledge_status": "study_only"}
            return {"outcome": "card_proposed", "word": word, "novel": is_new,
                    "card_id": card_id, "revision": 1}

        if name == "catalog.card.read":
            card = self.cards.get(args["card_id"])
            if not card or args["revision"] != card["revision"]:
                return {"outcome": "no_pinned_card"}
            is_new = card["card_id"] not in self.seen_card_reads
            self.seen_card_reads.add(card["card_id"])
            return {"outcome": "pinned_card_read", "novel": is_new,
                    "card_id": card["card_id"], "revision": 1,
                    "review_state": card["review_state"]}

        if name == "evidence.node.get":
            node = self.nodes.get(args["node_id"])
            if node is None:
                return {"outcome": "no_source_node"}
            is_new = node["node_id"] not in self.seen_node_reads
            self.seen_node_reads.add(node["node_id"])
            return {"outcome": "node_read", "novel": is_new,
                    "source_ref": node["source_ref"]}

        if name == "evidence.edge.trace":
            edges = [e for e in self.edges.values()
                     if e["source"] == "lemma:" + word or
                     e["target"] == "lemma:" + word or
                     e["source"] in {"wn:" + r["synset"] for r in self.words_studied.get(word, [])}]
            new = any(e["edge_id"] not in self.seen_edge_reads for e in edges)
            self.seen_edge_reads.update(e["edge_id"] for e in edges)
            return {"outcome": "edges_traced", "word": word, "novel": new,
                    "source_backed_edges": len(edges), "verified_facts": 0}

        if name == "evidence.edge.propose":
            if not self.edge_pending:
                return {"outcome": "no_pending_evidence"}
            edge_id, candidate = self.edge_pending.popleft()
            if edge_id in self.edges:
                return {"outcome": "duplicate"}
            # WordNet synset must exist and must entail the typed lexical link.
            source_synset = wn.synset(candidate["source_synset"])
            if candidate["relation"] == "lemma_has_sense":
                valid = candidate["target"] == "wn:" + source_synset.name() and any(
                    "lemma:" + l.name().lower() == candidate["source"] for l in source_synset.lemmas())
            elif candidate["relation"] == "hypernym":
                valid = candidate["source"] == "wn:" + source_synset.name() and any(
                    "wn:" + s.name() == candidate["target"] for s in source_synset.hypernyms())
            else:
                valid = False
            if not valid:
                return {"outcome": "unsupported_proposal", "source_ref": candidate["source_ref"]}
            edge = {"edge_id": edge_id, **candidate, "relation_domain": "lexical",
                    "evidence_state": "proposed", "fact_verified": False,
                    "study_only": True}
            self.edges[edge_id] = edge
            self.log_edge(edge)
            return {"outcome": "provisional_edge", "novel": True,
                    "edge_id": edge_id, "source_ref": candidate["source_ref"]}
        raise KeyError("Tool outside authorized systems")

    def _available_for(self, name):
        if name == "dictionary.lexical_senses":
            return True
        if name in ("dictionary.semantic_neighbors", "dictionary.definition_terms",
                    "catalog.card.propose"):
            return bool(self.words_studied)
        if name == "catalog.card.read":
            return bool(self.cards)
        if name == "evidence.node.get":
            return bool(self.nodes)
        if name == "evidence.edge.trace":
            return bool(self.words_studied)
        if name == "evidence.edge.propose":
            return bool(self.edge_pending)
        return False

    def _select(self):
        total = sum(r["n"] for r in self.arm.values())
        choices = []
        for name in self.names:
            if not self._available_for(name):
                continue
            item = self.arm[name]
            if item["n"] == 0:
                score = float("inf")
            else:
                score = item["total"] / item["n"] + 0.65 * math.sqrt(
                    2 * math.log(max(total, 1) + 1) / item["n"])
            # No fixed task assignments; the policy favors outcomes and
            # autonomously explores unexplored tool affordances.
            choices.append((score, self.rng.random(), name))
        if not choices:
            raise RuntimeError("No eligible authorized tool")
        choices.sort(reverse=True)
        return choices[0][-1]

    def _target_args(self, action):
        if action == "dictionary.lexical_senses":
            return {"word": self._next_word()}
        if action == "dictionary.semantic_neighbors":
            pool = [w for w in self.words_studied if w not in self.neighbors_processed]
            return {"word": self.rng.choice(pool if pool else list(self.words_studied))}
        if action == "dictionary.definition_terms":
            pool = [w for w in self.words_studied if w not in self.definition_processed]
            return {"word": self.rng.choice(pool if pool else list(self.words_studied))}
        if action == "catalog.card.propose":
            pool = [w for w in self.words_studied if "wnword:" + w not in self.cards]
            return {"word": self.rng.choice(pool if pool else list(self.words_studied))}
        if action == "catalog.card.read":
            return {"card_id": self.rng.choice(list(self.cards)), "revision": 1}
        if action == "evidence.node.get":
            return {"node_id": self.rng.choice(list(self.nodes))}
        if action == "evidence.edge.trace":
            return {"word": self.rng.choice(list(self.words_studied))}
        if action == "evidence.edge.propose":
            return {"word": self.rng.choice(list(self.words_studied)) if self.words_studied else self._next_word()}
        raise ValueError("Unrecognized action")

    def _reward(self, action, response):
        if response is None:
            return -0.2
        outcome = response.get("outcome")
        new = response.get("novel", False)
        if outcome in ("unsupported_proposal", "no_prior_sense_context", "absent"):
            return -0.12
        if outcome == "provisional_edge":
            return 0.20
        if outcome == "senses_loaded":
            return 0.22 if new else 0.0
        if outcome == "neighbors_found":
            return 0.16 if new else 0.0
        if outcome == "definitions_explored":
            return 0.17 if new else 0.0
        if outcome == "card_proposed":
            return 0.14 if new else 0.0
        if outcome in ("pinned_card_read", "node_read"):
            return 0.06 if new else 0.0
        if outcome == "edges_traced":
            return 0.08 if new else 0.0
        return 0.0

    def run(self, seconds=300, outdir="echo017_full_wordnet_results"):
        if seconds <= 0 or seconds > 300:
            raise ValueError("Study duration must be positive, at most authorized 300 seconds")
        listed = {t["name"] for t in self.mcp_request({"jsonrpc": "2.0", "id": 0, "method": "tools/list"})["result"]["tools"]}
        if listed != ALLOWED_TOOLS or {n.split(".", 1)[0] for n in listed} != ALLOWED_SYSTEMS:
            raise RuntimeError("Tool discovery does not match the 3 authorized systems")
        self.start_logging(outdir)
        started = time.monotonic()
        last_progress = started
        errors = 0
        try:
            while time.monotonic() - started < seconds:
                tool = self._select()
                args = self._target_args(tool)
                self.current_step += 1
                reply = self.mcp_request({"jsonrpc": "2.0", "id": self.current_step,
                    "method": "tools/call", "params": {"name": tool, "arguments": args}})
                if reply.get("error") or reply.get("result", {}).get("isError"):
                    errors += 1
                    outcome = {"outcome": "tool_error"}
                else:
                    outcome = json.loads(reply["result"]["content"][0]["text"])
                reward = self._reward(tool, outcome)
                arm = self.arm[tool]
                arm["total"] += reward
                arm["ema"] = 0.2 * reward + 0.8 * arm["ema"]
                arm["n"] += 1
                status = outcome.get("outcome", "unknown")
                self.effects[status] += 1
                self.families[tool] += 1
                self.log_episode({
                    "step": self.current_step, "tool": tool,
                    "input": args, "result": status, "reward": reward,
                    "epistemic_state": "provisional", "source_system": "Princeton WordNet"})
                now = time.monotonic()
                if now - last_progress >= 30:
                    print("ECHO017_FULL_PROGRESS " + json.dumps({
                        "elapsed_seconds": round(now - started, 3),
                        "actions": self.current_step, "studied_words": len(self.words_studied),
                        "cards": len(self.cards), "evidence_edges": len(self.edges),
                        "queue": len(self.edge_pending), "frontier": len(self.frontier),
                        "errors": errors}), flush=True)
                    last_progress = now
        finally:
            self.finish_logging()
        elapsed = time.monotonic() - started
        summary = {
            "id": "ECHO-017-FULL-WORDNET-300S",
            "duration_requested_seconds": seconds,
            "elapsed_active_wall_seconds": elapsed,
            "action_count": self.current_step,
            "no_artificial_pacing": True,
            "wordnet_lemma_names_available": len(self.full_lemmas),
            "wordnet_total_synsets_available": self.full_synsets,
            "source": self.corpus_version,
            "dictionary_source_complete": True,
            "words_with_senses_explored": len(self.words_studied),
            "definition_expansions": len(self.definition_processed),
            "neighbor_expansions": len(self.neighbors_processed),
            "frontier_size_at_end": len(self.frontier),
            "new_study_cards": len(self.cards),
            "new_source_lexical_edges": len(self.edges),
            "remaining_proposal_queue": len(self.edge_pending),
            "study_action_distribution": dict(self.families),
            "outcomes": dict(self.effects),
            "tool_errors": errors,
            "policy_state": self.arm,
            "allowed_tool_names": sorted(ALLOWED_TOOLS),
            "allowed_systems": sorted(ALLOWED_SYSTEMS),
            "epistemic_status": "provisional dictionary source relations; no independent empirical truth certification",
            "no_automatic_corporate_authority": True,
            "no_new_knowledge_truth_promotions": True,
            "neon_connection": "not available from GitHub runner; results are an artifact for separate authorized Neon reconciliation",
            "mcp_transport": "in-process JSON-RPC tool API, not deployed MCP-over-HTTP",
            "artifact_paths": [str(self.episodes_path), str(self.edge_path)],
            "interpretation_limit": "Five minutes of autonomous bounded reinforcement study is not proof of general understanding."
        }
        result_path = Path(outdir) / "echo017_full_wordnet_summary.json"
        result_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
        print("ECHO017_FULL_RESULT " + json.dumps({
            k: summary[k] for k in [
                "elapsed_active_wall_seconds", "action_count", "wordnet_lemma_names_available",
                "wordnet_total_synsets_available", "words_with_senses_explored",
                "new_study_cards", "new_source_lexical_edges", "remaining_proposal_queue",
                "study_action_distribution", "tool_errors", "no_artificial_pacing"
            ]}), flush=True)
        return summary


def main():
    duration = float(os.environ.get("ECHO_STUDY_SECONDS", "300"))
    result = Study().run(seconds=duration,
                          outdir=os.environ.get("ECHO_STUDY_OUTDIR", "echo017_full_wordnet_results"))
    if result["elapsed_active_wall_seconds"] < duration:
        raise RuntimeError("Study terminated before requested wall-clock budget")
    if result["tool_errors"]:
        raise RuntimeError("Tool errors occurred; see complete log and artifacts")


if __name__ == "__main__":
    main()
