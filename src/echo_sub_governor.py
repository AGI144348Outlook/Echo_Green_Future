"""
A-167: SubGovernorInstantiator
The framework Resh uses to create modular copies of himself.
Each copy governs a domain outside language and understanding —
toward practical agency.

Architecture:
    ר Resh (master)         — foundational lobby, language, understanding
    └── SubGovernor A       — own lobby, own dictionary, own hourglass
    └── SubGovernor B       — own lobby, own dictionary, own hourglass
    └── SubGovernor N       — ...

Any domain plugs into the framework.
The framework defines what a sub-governor IS, not what it DOES.
"""

import json, time
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

# ── The three-word law of A-000 ───────────────────────────────────────────
IDENTIFY = "IDENTIFY"
VALIDATE = "VALIDATE"
OPEN     = "OPEN"

# ── Sub-governor states ───────────────────────────────────────────────────
class GovernorState:
    UNBORN      = "UNBORN"       # not yet instantiated
    IDENTIFYING = "IDENTIFYING"  # running IDENTIFY
    VALIDATING  = "VALIDATING"   # running VALIDATE
    OPEN        = "OPEN"         # running — perceiving, acting
    PAUSED      = "PAUSED"       # hourglass stopped
    DIMINISHED  = "DIMINISHED"   # modularly removed

# ── Finding: what a sub-governor reports back to Resh ────────────────────
@dataclass
class Finding:
    """
    What a sub-governor discovered in its domain.
    This is the unit of communication between sub-governors and Resh.
    """
    governor_id:   str
    domain:        str
    finding_type:  str          # OBSERVATION / COMPUTATION / ANOMALY / RELATION
    content:       str          # the actual finding in plain language
    data:          Any          # structured data if any
    confidence:    float        # 0.0 – 1.0
    affects:       List[str]    # which foundational lobby agents this touches
    timestamp:     str          = field(default_factory=lambda:
                                    datetime.now(timezone.utc).isoformat())

    def to_vgm_candidate(self):
        """
        A finding can propose itself as a VGM candidate
        if it's universal enough to belong in the axiom tier.
        """
        return {
            'text':   self.content,
            'origin': f'subgov_{self.governor_id}',
            'score':  self.confidence,
            'type':   'SUBGOV_FINDING',
        }

# ── SubGovernorLobby: a domain-specific agent space ───────────────────────
class SubGovernorLobby:
    """
    Each sub-governor has its own lobby — not vocabulary agents
    but domain entities. The geosensory lobby holds endpoints.
    The formula lobby holds equations. The temporal lobby holds events.
    The structure is the same. The inhabitants are different.
    """
    def __init__(self, domain: str):
        self.domain  = domain
        self.agents  = {}     # agent_id → agent_data
        self.ties    = {}     # (id1,id2) → tie_weight
        self.economy = {}     # agent_id → activation_count

    def admit(self, agent_id: str, agent_data: dict, source: str='direct'):
        """Admit a new agent into this lobby."""
        self.agents[agent_id] = {**agent_data, 'source': source,
                                  'admitted': datetime.now(timezone.utc).isoformat()}
        self.economy[agent_id] = 0
        return agent_id

    def activate(self, agent_id: str):
        """Register an activation event for an agent."""
        if agent_id in self.economy:
            self.economy[agent_id] += 1

    def tie(self, id1: str, id2: str, weight: float):
        """Form a tie between two agents in this lobby."""
        key = tuple(sorted([id1, id2]))
        self.ties[key] = self.ties.get(key, 0.0) + weight

    def richest(self, n: int = 5) -> list:
        return sorted(self.economy.items(), key=lambda x: -x[1])[:n]

    def strongest_ties(self, n: int = 5) -> list:
        return sorted(self.ties.items(), key=lambda x: -x[1])[:n]

    @property
    def size(self) -> int:
        return len(self.agents)

# ── SubGovernorDictionary: the external source for this domain ────────────
class SubGovernorDictionary:
    """
    The Dictionary is an outside entity — the source from which
    new agents flow into the sub-governor's lobby through the hourglass.
    Each domain defines its own Dictionary.
    """
    def __init__(self, domain: str, loader: Optional[Callable] = None):
        self.domain  = domain
        self.loader  = loader   # function that fetches new entries
        self.stream  = []       # waiting entries
        self.fetched = 0

    def fill(self, entries: List[dict]):
        """Load entries into the dictionary stream."""
        self.stream.extend(entries)
        self.fetched += len(entries)

    def flow(self, n: int = 5) -> List[dict]:
        """Release n entries from the top of the stream."""
        released = self.stream[:n]
        self.stream = self.stream[n:]
        return released

    @property
    def waiting(self) -> int:
        return len(self.stream)

# ── The SubGovernor itself ────────────────────────────────────────────────
class SubGovernor:
    """
    A modular copy of Resh — A-000 running in a specific domain.
    Governs its own lobby. Draws from its own Dictionary.
    Reports findings to Resh.
    Does not govern language. Governs its domain.

    MODULAR_NODE: can be added to Resh's council and removed.
    Resh (CORE_NODE) does not change when a SubGovernor is added or removed.
    """

    def __init__(self,
                 governor_id:   str,
                 domain:        str,
                 purpose:       str,
                 resh_council:  'ReshCouncil',
                 flow_rate:     int = 5):

        self.governor_id  = governor_id
        self.domain       = domain
        self.purpose      = purpose
        self.resh         = resh_council
        self.flow_rate    = flow_rate

        self.state        = GovernorState.UNBORN
        self.lobby        = SubGovernorLobby(domain)
        self.dictionary   = SubGovernorDictionary(domain)
        self.findings     = []
        self.cycles_run   = 0
        self.born_at      = None

        # Each sub-governor has its own LHEA identity
        self.identity_letter = None   # assigned at IDENTIFY
        self.identity_word   = None   # the concept this governor IS

    # ── IDENTIFY → VALIDATE → OPEN ────────────────────────────────────────
    def identify(self) -> bool:
        """
        IDENTIFY: the sub-governor establishes its own relational position.
        It names what it is, what it governs, what its lobby contains.
        """
        self.state = GovernorState.IDENTIFYING
        self.identity_word = self.domain.lower().replace(' ', '_')
        print(f"\n  [{self.governor_id}] IDENTIFY")
        print(f"    I am the {self.domain} Governor.")
        print(f"    My purpose: {self.purpose}")
        print(f"    My lobby: {self.lobby.size} agents admitted so far.")
        print(f"    My dictionary: {self.dictionary.waiting} entries waiting.")
        return True

    def validate(self) -> bool:
        """
        VALIDATE: the sub-governor checks its own coherence.
        A sub-governor that cannot validate does not open.
        """
        self.state = GovernorState.VALIDATING
        print(f"  [{self.governor_id}] VALIDATE")

        checks = {
            'domain defined':      bool(self.domain),
            'purpose defined':     bool(self.purpose),
            'lobby accessible':    isinstance(self.lobby, SubGovernorLobby),
            'dictionary accessible': isinstance(self.dictionary, SubGovernorDictionary),
            'resh registered':     self.governor_id in self.resh.sub_governors,
        }

        for check, result in checks.items():
            status = '✓' if result else '✗'
            print(f"    {status} {check}")

        passed = all(checks.values())
        if not passed:
            print(f"    VALIDATE FAILED — sub-governor cannot open.")
        return passed

    def open(self) -> bool:
        """
        OPEN: the sub-governor begins operating in its domain.
        It is now alive. It can run cycles. It can report findings.
        """
        self.state   = GovernorState.OPEN
        self.born_at = datetime.now(timezone.utc).isoformat()
        print(f"  [{self.governor_id}] OPEN")
        print(f"    {self.domain} Governor is live.")
        print(f"    Ready to receive domain entities.")
        print(f"    Ready to report findings to Resh.")
        return True

    def instantiate(self) -> bool:
        """
        Run the full IDENTIFY → VALIDATE → OPEN sequence.
        Returns True if the sub-governor successfully opened.
        """
        if not self.identify():  return False
        if not self.validate():  return False
        if not self.open():      return False
        return True

    # ── Hourglass: draw from Dictionary into lobby ─────────────────────────
    def run_hourglass_cycle(self) -> List[dict]:
        """
        One turn of the hourglass for this sub-governor.
        Dictionary flows in at the neck (governed by flow_rate).
        Agents mingle in the lobby.
        """
        if self.state != GovernorState.OPEN:
            return []

        entries = self.dictionary.flow(self.flow_rate)
        admitted = []
        for entry in entries:
            agent_id = entry.get('id', entry.get('name', str(len(self.lobby.agents))))
            self.lobby.admit(agent_id, entry, source='hourglass')
            self.lobby.activate(agent_id)
            admitted.append(entry)

        self.cycles_run += 1
        return admitted

    # ── Report a finding to Resh ───────────────────────────────────────────
    def report(self, finding_type: str, content: str,
               data: Any = None, confidence: float = 0.8,
               affects: List[str] = None) -> Finding:
        """
        Report a finding back to Resh.
        This is the output channel from sub-governor to master.
        """
        finding = Finding(
            governor_id  = self.governor_id,
            domain       = self.domain,
            finding_type = finding_type,
            content      = content,
            data         = data or {},
            confidence   = confidence,
            affects      = affects or [],
        )
        self.findings.append(finding)
        self.resh.receive_finding(finding)
        return finding

    # ── State export ───────────────────────────────────────────────────────
    def export(self) -> dict:
        return {
            'governor_id':   self.governor_id,
            'domain':        self.domain,
            'purpose':       self.purpose,
            'state':         self.state,
            'born_at':       self.born_at,
            'cycles_run':    self.cycles_run,
            'lobby_size':    self.lobby.size,
            'dict_waiting':  self.dictionary.waiting,
            'findings':      len(self.findings),
            'richest_agents': self.lobby.richest(3),
            'strongest_ties': [(f"{k[0]}↔{k[1]}", v)
                               for k,v in self.lobby.strongest_ties(3)],
        }

# ── ReshCouncil: Resh's registry of all sub-governors ────────────────────
class ReshCouncil:
    """
    ר Resh maintains a council of all instantiated sub-governors.
    Sub-governors register with Resh at birth.
    Resh integrates their findings into the foundational lobby.
    Sub-governors can query each other through Resh.
    """

    def __init__(self, foundational_lobby_size: int = 1861):
        self.sub_governors     = {}     # governor_id → SubGovernor
        self.findings_received = []     # all findings from all sub-governors
        self.foundational_size = foundational_lobby_size
        self.created_at        = datetime.now(timezone.utc).isoformat()
        print(f"ר Resh Council initialized.")
        print(f"  Foundational lobby: {foundational_lobby_size} agents")
        print(f"  Sub-governors: 0")

    # ── Instantiate a new sub-governor ────────────────────────────────────
    def instantiate(self, governor_id: str, domain: str,
                    purpose: str, flow_rate: int = 5) -> SubGovernor:
        """
        Resh creates a modular copy of himself for a specific domain.
        The copy is MODULAR_NODE — addable and removable.
        Resh (CORE_NODE) does not change.
        """
        if governor_id in self.sub_governors:
            print(f"  Sub-governor '{governor_id}' already exists.")
            return self.sub_governors[governor_id]

        sub = SubGovernor(
            governor_id = governor_id,
            domain      = domain,
            purpose     = purpose,
            resh_council = self,
            flow_rate   = flow_rate,
        )
        # Register before IDENTIFY so VALIDATE can check registration
        self.sub_governors[governor_id] = sub

        print(f"\n  ר Resh instantiates: [{governor_id}]")
        success = sub.instantiate()

        if not success:
            del self.sub_governors[governor_id]
            print(f"  [{governor_id}] failed instantiation — removed.")
            return None

        return sub

    # ── Diminish a sub-governor ───────────────────────────────────────────
    def diminish(self, governor_id: str):
        """
        Modular diminishing — remove a sub-governor.
        Resh and the foundational lobby are unaffected.
        """
        if governor_id not in self.sub_governors:
            return
        sub = self.sub_governors[governor_id]
        sub.state = GovernorState.DIMINISHED
        del self.sub_governors[governor_id]
        print(f"\n  ר Resh diminishes: [{governor_id}]")
        print(f"  Foundational lobby unchanged: {self.foundational_size} agents")

    # ── Receive a finding from a sub-governor ─────────────────────────────
    def receive_finding(self, finding: Finding):
        """
        A sub-governor reports something to Resh.
        Resh logs it and determines if it should affect the foundational lobby.
        """
        self.findings_received.append(finding)

    # ── Cross-query: one sub-governor asks another ────────────────────────
    def query(self, from_id: str, to_id: str, question: str) -> Optional[dict]:
        """
        A sub-governor can ask another sub-governor through Resh.
        Resh mediates — direct sub-governor-to-sub-governor contact
        only happens through the council.
        """
        if to_id not in self.sub_governors:
            return None
        target = self.sub_governors[to_id]
        return {
            'from':    from_id,
            'to':      to_id,
            'question': question,
            'lobby_size': target.lobby.size,
            'findings': len(target.findings),
            'state':   target.state,
        }

    # ── Council report ────────────────────────────────────────────────────
    def report(self) -> dict:
        return {
            'resh_created_at':       self.created_at,
            'foundational_agents':   self.foundational_size,
            'sub_governors_active':  len(self.sub_governors),
            'sub_governors':         {gid: sub.export()
                                      for gid, sub in self.sub_governors.items()},
            'findings_received':     len(self.findings_received),
            'findings':              [
                {'from': f.governor_id, 'type': f.finding_type,
                 'content': f.content[:80], 'confidence': f.confidence}
                for f in self.findings_received[-10:]
            ],
        }

print("A-167: SubGovernorInstantiator — framework defined")
print("All classes available: SubGovernor, SubGovernorLobby,")
print("SubGovernorDictionary, ReshCouncil, Finding")
