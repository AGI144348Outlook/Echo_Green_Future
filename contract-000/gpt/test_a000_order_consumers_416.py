#!/usr/bin/env python3
"""Run416: isolated source-transcribed Genesis order-consumer controls.
Actual source: genesis-documentary/src/echo_governor_skeleton.py blob 63eb982.
This fixture does not import or execute the full Governor.
"""
import json
from types import SimpleNamespace

STOPWORDS = frozenset({'the', 'of', 'in', 'and'})
DEFINITION_BOILERPLATE = frozenset({'genus', 'family'})

class LobbyExcerpt:
    # Behavior-bearing statements transcribed from Lobby._compute_genus_depths()
    # at Genesis lines 1274-1305; stand-in STOPWORDS/BOILERPLATE are restricted
    # to tokens absent from the discriminating fixtures.
    def __init__(self, agents):
        self.agents = agents
    def _compute_genus_depths(self):
        genus_of = {}
        for word, agent in self.agents.items():
            if not agent.definition_words:
                continue
            for dw in agent.definition_words:
                if (dw != word and dw in self.agents
                        and dw not in STOPWORDS
                        and dw not in DEFINITION_BOILERPLATE):
                    genus_of[word] = dw
                    break
        depths = {}
        def depth(w, seen=None):
            if seen is None: seen = set()
            if w in depths: return depths[w]
            if w in seen or w not in genus_of:
                depths[w] = 0
                return 0
            seen.add(w)
            d = 1 + depth(genus_of[w], seen)
            depths[w] = d
            return d
        for w in self.agents:
            depth(w)
        return depths

class LRMExcerpt:
    # Exact decision logic transcribed from LogicReasoningMatrix._is_genuine_subtype
    # Genesis lines 6279-6291, with a stand-in lobby.
    def __init__(self, lobby):
        self.lobby = lobby
    def _is_genuine_subtype(self, specific_word, abstract_word):
        agent = self.lobby.agents.get(specific_word)
        if not agent:
            return False
        if abstract_word in agent.definition_words:
            return True
        for dw in agent.definition_words[:5]:
            dw_agent = self.lobby.agents.get(dw)
            if dw_agent and abstract_word in dw_agent.definition_words:
                return True
        return False

def A(words): return SimpleNamespace(definition_words=list(words))

def main():
    tests = {}
    base = {'aleph': A(['pe']), 'ayin': A([]), 'pe': A([])}
    first = LobbyExcerpt({'resh': A(['aleph', 'ayin', 'pe', 'governor']), **base})
    second = LobbyExcerpt({'resh': A(['ayin', 'aleph', 'pe', 'governor']), **base})
    d1, d2 = first._compute_genus_depths(), second._compute_genus_depths()
    tests['same_resh_set'] = set(first.agents['resh'].definition_words) == set(second.agents['resh'].definition_words)
    tests['genus_depth_changes_with_order'] = (d1['resh'], d2['resh']) == (2, 1)
    tests['repeat_stable'] = first._compute_genus_depths() == d1
    tests['missing_resh_not_fabricated'] = 'missing' not in d1
    # LRM first-five cap: target 'abstract' is only reachable through 'bridge'
    # when bridge falls within first five, despite identical definition word set.
    refs = {'bridge': A(['abstract']), 'x1': A([]), 'x2': A([]), 'x3': A([]), 'x4': A([]), 'x5': A([])}
    yes = LRMExcerpt(SimpleNamespace(agents={'specific': A(['bridge','x1','x2','x3','x4','x5']), **refs}))
    no = LRMExcerpt(SimpleNamespace(agents={'specific': A(['x1','x2','x3','x4','x5','bridge']), **refs}))
    tests['same_subtype_word_set'] = set(yes.lobby.agents['specific'].definition_words) == set(no.lobby.agents['specific'].definition_words)
    tests['first_five_changes_indirect_subtype'] = yes._is_genuine_subtype('specific','abstract') and not no._is_genuine_subtype('specific','abstract')
    tests['direct_subtype_stable'] = (LRMExcerpt(SimpleNamespace(agents={'specific': A(['abstract'])}))._is_genuine_subtype('specific','abstract'))
    tests['absent_subtype_false'] = not yes._is_genuine_subtype('specific','nonexistent')
    # WordAgent.report() uses definition_words[:8] and study-group curriculum joins
    # the list; both are order-sensitive projections in the inspected source.
    tests['report_projection_changes'] = first.agents['resh'].definition_words[:8] != second.agents['resh'].definition_words[:8]
    tests['curriculum_projection_changes'] = ' '.join(first.agents['resh'].definition_words) != ' '.join(second.agents['resh'].definition_words)
    print(json.dumps({'source_blob':'63eb982989b4f3478d649430b555c8f4ba755c27','scope':'isolated source-transcribed excerpts; not full Genesis', 'genus_depths':[d1['resh'],d2['resh']], 'passed':sum(tests.values()),'total':len(tests),'tests':tests},indent=2))
    if not all(tests.values()): raise SystemExit(1)
if __name__=='__main__': main()
