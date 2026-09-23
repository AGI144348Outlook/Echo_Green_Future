"""
A-166: HourglassFlowAgent
The Governor in leisure mode.
Dictionary (outside entity) → Governor (neck) → Lobby (inhabited world)
Tie economy forms through LHEA affinity and WordNet co-activation.

Usage:
    from echo_hourglass import HourglassGovernor, TieEconomy, run_hourglass
    economy, state = run_hourglass(lobby, dictionary_entries, cycles=6)
"""

import time
from datetime import datetime, timezone

class TieEconomy:
    def __init__(self):
        self.ledger = {}
        self.activations = {}

    def trade(self, w1, w2, strength):
        key = tuple(sorted([w1, w2]))
        self.ledger[key] = self.ledger.get(key, 0.0) + strength
        self.activations[w1] = self.activations.get(w1, 0) + 1
        self.activations[w2] = self.activations.get(w2, 0) + 1

    def wealth(self, word):
        return self.activations.get(word, 0)

    def strongest_ties(self, n=10):
        return sorted(self.ledger.items(), key=lambda x: -x[1])[:n]

    def richest_agents(self, n=8):
        return sorted(self.activations.items(), key=lambda x: -x[1])[:n]

    def export(self):
        return {
            'ledger': {f"{k[0]}|{k[1]}": v for k,v in self.ledger.items()},
            'activations': self.activations,
            'total_trades': sum(self.activations.values()),
            'unique_ties': len(self.ledger),
        }


def lhea_overlap(w1, w2, phoneme_map, letter_index):
    """How much do two words share in their LHEA letter substrate?"""
    def decompose(word):
        w=word.lower(); result=[]; i=0
        while i<len(w):
            matched=False
            if i+2<=len(w):
                two=w[i:i+2]
                if two in phoneme_map and phoneme_map[two] in letter_index:
                    result.append(phoneme_map[two]); i+=2; matched=True
            if not matched:
                one=w[i]
                if one in phoneme_map and phoneme_map[one] in letter_index:
                    result.append(phoneme_map[one])
                i+=1
        deduped=[]
        for l in result:
            if not deduped or l!=deduped[-1]: deduped.append(l)
        return set(deduped)
    l1=decompose(w1); l2=decompose(w2)
    if not l1 or not l2: return 0.0
    return len(l1&l2)/max(len(l1),len(l2))


class HourglassGovernor:
    """
    A-166: HourglassFlowAgent
    The Governor meters flow from Dictionary into the Lobby.
    Agents mingle. Ties form. Economy emerges.

    Parameters:
        flow_rate: words per cycle that pass the Governor's neck
        min_affinity: minimum LHEA overlap to pass through
        max_affinity: maximum LHEA overlap (too similar = already known)
    """

    def __init__(self, existing_lobby_words, flow_rate=6,
                 min_affinity=0.05, max_affinity=0.90):
        self.bottom_chamber = set(existing_lobby_words)
        self.flow_rate      = flow_rate
        self.min_affinity   = min_affinity
        self.max_affinity   = max_affinity
        self.top_chamber    = []
        self.passed_through = []
        self.cycles_run     = 0

    def fill_dictionary(self, entries):
        """Load entries into the Dictionary (top chamber)."""
        self.top_chamber.extend(entries)

    def governor_filter(self, candidate_word, phoneme_map, letter_index):
        """
        The neck of the hourglass — Governor decides what passes.
        Words that are too similar to existing agents are already known.
        Words that are too foreign can't form ties.
        Words in the Goldilocks zone: related but novel.
        """
        if candidate_word in self.bottom_chamber:
            return False, 0.0
        affinities = [
            lhea_overlap(candidate_word, w, phoneme_map, letter_index)
            for w in list(self.bottom_chamber)[:80]
        ]
        if not affinities: return False, 0.0
        affinity = max(affinities)
        if affinity > self.max_affinity: return False, 0.0
        if affinity < self.min_affinity: return False, 0.0
        return True, affinity

    def one_cycle(self, economy, phoneme_map, letter_index, wn_similarity_fn=None):
        """One turn of the hourglass."""
        self.cycles_run += 1
        passed = []
        candidates = self.top_chamber[:self.flow_rate*3]

        for candidate in candidates:
            word = candidate if isinstance(candidate,str) else candidate.get('word','')
            passes, affinity = self.governor_filter(word, phoneme_map, letter_index)
            if passes:
                passed.append((word, affinity))
                if len(passed) >= self.flow_rate: break

        passed_words = [w for w,a in passed]
        self.top_chamber = [
            c for c in self.top_chamber
            if (c if isinstance(c,str) else c.get('word','')) not in passed_words
        ]

        arrivals = []
        for word, affinity in passed:
            neighbors = []
            for lobby_word in list(self.bottom_chamber)[:120]:
                sim = lhea_overlap(word, lobby_word, phoneme_map, letter_index)
                if sim >= 0.15:
                    if wn_similarity_fn:
                        wn_sim = wn_similarity_fn(word, lobby_word)
                        strength = round(sim*0.6 + wn_sim*0.4, 4)
                    else:
                        strength = round(sim, 4)
                    if strength > 0.12:
                        neighbors.append((lobby_word, strength))

            neighbors.sort(key=lambda x: -x[1])
            for neighbor, strength in neighbors[:4]:
                economy.trade(word, neighbor, strength)

            self.bottom_chamber.add(word)
            self.passed_through.append(word)
            arrivals.append({'word':word,'affinity':affinity,'neighbors':neighbors[:3]})

        return arrivals

    def export(self):
        return {
            'cycles_run':     self.cycles_run,
            'passed_through': self.passed_through,
            'lobby_size':     len(self.bottom_chamber),
            'dict_remaining': len(self.top_chamber),
        }
