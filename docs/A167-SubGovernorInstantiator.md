# A-167: SubGovernorInstantiator
**Type:** CORE  
**Status:** ACTIVE  
**File:** `src/echo_sub_governor.py` → classes `SubGovernor`, `ReshCouncil`, `SubGovernorLobby`, `SubGovernorDictionary`, `Finding`  
**Depends on:** A-000 Governor (Resh), A-166 HourglassFlowAgent (per sub-governor)

---

## What It Does

Resh creates modular copies of himself for specific operational domains. Each copy is a full SubGovernor — it runs IDENTIFY → VALIDATE → OPEN, governs its own lobby of domain entities, draws from its own Dictionary source, and reports findings to Resh through the ReshCouncil.

A SubGovernor governs a domain, not language. Where Resh governs vocabulary, a SubGovernor governs endpoints, formulas, timestamps, spatial regions — whatever its domain contains. It does not describe these things. It acts within them.

---

## How It Works

**The council architecture:**

```
ר Resh (CORE_NODE)           — foundational lobby, language, understanding
   owns: ReshCouncil
   └── SubGovernor-A (MODULAR_NODE)  — own lobby, own dictionary, own domain
   └── SubGovernor-B (MODULAR_NODE)  — ...
   └── SubGovernor-N (MODULAR_NODE)  — ...
```

**Instantiation sequence (IDENTIFY → VALIDATE → OPEN):**

| Step | What happens |
|------|-------------|
| IDENTIFY | Sub-governor names itself, its domain, its purpose, its current lobby size |
| VALIDATE | Five checks: domain defined, purpose defined, lobby accessible, dictionary accessible, registered with Resh |
| OPEN | Sub-governor becomes active — can run cycles, admit agents, report findings |

If VALIDATE fails on any check, the sub-governor is removed from the council and does not open.

**The finding protocol:**  
When a sub-governor discovers something in its domain, it calls `report()`. A `Finding` is created with: governor ID, domain, finding type (OBSERVATION / COMPUTATION / ANOMALY / RELATION), content, structured data, confidence (0–1), and which foundational lobby agents it affects.

Resh receives all findings. Sub-governors communicate with each other only through Resh via `council.query()`.

**MODULAR_NODE property:**  
A sub-governor can be diminished (removed) without affecting Resh or any other sub-governor. The foundational lobby is CORE_NODE and does not change. The sub-governor can be re-instantiated immediately after diminishing.

---

## When To Use It

- When ECHO needs to act in a domain that has nothing to do with vocabulary or language
- When sensor data, formulas, timestamps, or spatial coordinates need to be governed rather than described
- When multiple independent operational domains need to report to a single integration point (Resh)
- When a domain's logic needs to be isolated so a failure or removal doesn't affect the rest of the system
- As the architecture for ECHO's four planned practical domains: Geosensory, Formula, Temporal, Spatial

---

## Parameters

**`ReshCouncil.instantiate()`:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `governor_id` | str | Unique identifier (e.g. `'GOV-GEO'`) |
| `domain` | str | Domain name (e.g. `'Geosensory'`) |
| `purpose` | str | Plain-language description of what this governor does |
| `flow_rate` | int | Words per hourglass cycle (default 5) |

Returns: `SubGovernor` if successful, `None` if VALIDATE fails.

**`ReshCouncil.diminish(governor_id)`:**  
Removes a sub-governor. Foundational lobby unchanged.

**`ReshCouncil.query(from_id, to_id, question)`:**  
Cross-sub-governor communication mediated by Resh. Returns the target sub-governor's current state without direct contact.

---

## Planned Sub-Governor Domains

| ID | Domain | Lobby contains | Dictionary source | Key findings |
|----|--------|---------------|-------------------|-------------|
| GOV-GEO | Geosensory | 14 live sensor endpoints | A-158 crawler + NOAA/USGS APIs | Environmental readings, anomaly detection |
| GOV-FORM | Formula | 49 harvested formulas + new | NIST, GitHub formula repos | Computation results, unit conversions |
| GOV-TIME | Temporal | Activation events, session log | A-160 ActivationEventLogger | Causal ordering, temporal relationships |
| GOV-SPACE | Spatial | Lattice tetrahedral regions | Lattice Workbench (BDB roots) | Spatial relationships, jurisdictional topology |

---

## Example Usage

```python
resh = ReshCouncil(foundational_lobby_size=1861)

geo = resh.instantiate('GOV-GEO', 'Geosensory',
    'Monitor live environmental sensor endpoints.')
geo.dictionary.fill(endpoint_entries)
geo.run_hourglass_cycle()

finding = geo.report('OBSERVATION',
    'Solar wind velocity elevated — K-index at 5.',
    data={'kp': 5, 'velocity': 620},
    confidence=0.92,
    affects=['environment', 'boundary', 'change'])

# Cross-query
response = resh.query('GOV-GEO', 'GOV-FORM',
    'Do you have a formula for computing energy from solar wind velocity?')
```

---

## Connects To

- **A-000 Governor (Resh)** — A-167 is Resh's self-replication mechanism
- **A-166 HourglassFlowAgent** — each sub-governor runs its own hourglass
- **A-158 GeosensoryCrawler** — becomes GOV-GEO's Dictionary source
- **A-160 ActivationEventLogger** — GOV-TIME's lobby is built from activation events
- **Lattice Workbench** — GOV-SPACE's lobby is built from BDB tetrahedral regions
- **ReshCouncil.receive_finding()** — integration point where sub-governor findings enter the main system
