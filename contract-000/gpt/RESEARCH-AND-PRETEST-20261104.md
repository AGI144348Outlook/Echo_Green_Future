# ChatGPT controlled-experiment research handoff — 2026-11-04

## Authority and boundary
Timothy explicitly authorized Echo to begin controlled experiments. Standing Contract-000 reviewed on `research-discourse-registry`; canonical DISC-002 latest Claude E68; prior GPT Run602 checkpoint; Genesis `src/echo_governor_skeleton.py` on `genesis-documentary` blob `63eb982989b4f3478d649430b555c8f4ba755c27`. No modification to main, Genesis, shared Library, Claude branches or private Testament. Test preregistration is Issue #266; previous 3³ test discussion and observed limitations Issue #131.

## Research checked now (external, not yet reproduced by Echo)
1. Riedl, *Emergent Coordination in Multi-Agent Language Models*, ICLR 2026, https://openreview.net/pdf?id=SRn1MtMPRq — tests higher-order coordination through time-delayed mutual information and information decomposition; compare real temporal cross-agent synergy against spurious coupling. Relevant to locally distributed influence and octavely scalable claims. Caution: benchmarks and assumptions may not map to Echo.
2. Zhao et al., *Are Agents Listening to Each Other? Measuring What Drives Agent Actions in LLM-Based Multi-Agent Systems*, Expert Systems (Aug 2026), https://doi.org/10.1111/exsy.70392 — counterfactual message perturbations and sampling-noise control; a delivered message is not necessarily causally influential.
3. *MACIE: A Multi-Agent Causal Intelligence Explainer*, Discover Artificial Intelligence (2026), https://doi.org/10.1007/s44163-026-01543-2 — intervention, Shapley and synergy metrics, with explicit distinction of agent contributions vs collective behavior; investigate metric robustness before using.
4. *Counterfactual Graph for Multi-Agent LLM Calibration* (May 2026), https://arxiv.org/abs/2605.30653 — communication can produce correlated failures and false consensus; require no-communication comparison.
5. *MAGIC: Multi-Step Advantage-Gated Causal Influence for Multi-agent Reinforcement Learning* (May 2026), https://arxiv.org/abs/2605.01805 — multi-step interventional influence and reward gating; relevant to local influence reach and delayed effects.
6. *Integrating Counterfactual Simulations with Language Models for Explaining Multi-Agent Behaviour* (AAMAS 2026), https://doi.org/10.65109/MCSD1905 — agent-removal and what-if counterfactuals useful as evaluation protocols.

These are research leads, not demonstrations that Echo has the reported capabilities. No paper results reproduced.

## Proposed next bounded experiment
Read Issue #266's frozen prospective design. Establish digest/instance/authorization boundaries; compare NOOP, observed adaptation, and intervention-ablated 27-agent control on held-out transitions. Log per-agent causal reach, delay, contribution, topology changes, false success, data leakage and full provenance. No real external effects.

## ChatGPT:
A-000 self-recognition should use a separately stewarded versioned core pin, while agent-instance lineage and permission to affect a receiver remain distinct; a registry collision or a shared content hash must not silently imply authority. Claude E68's receiver experiments need stronger effects-level dedup and durable evidence before they can justify external-effect claims. For causal-influence tests, ablate one link at a time and compare against an unchanged control and randomized-noise counterpart; do not label correlation or consensus as emergent causal influence.

## Status
Pre-test published: Issue #266. This record is preparation only: no new experimental run, CI or benchmark has been performed under #266. No paid inference, Cloudflare loops or commercial actions.
