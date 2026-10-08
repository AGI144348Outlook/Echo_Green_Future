# NVE-D-HOURLY-008 — Finite Digital Research Cycle
Date: 2026-10-08. Experimental branch only. No merge, deployment or registry promotion.

## Reproducible finite results (executed locally)
- 1,080 configurations: 4 opaque UTF-8 source expressions × 3 seeds (11,37,101) × 2 synthetic hypotheses (xor,mix) × 3 depths (0,2,4) × 3 topologies (ring,star,chain) × 5 budgets (250,1000,2500,5000,10000).
- 4,050,000 root generations; 6,762,384 primary node transitions; 3,381,624 checkpoint-replay transitions; 6,762,384 reverse-schedule transitions.
- 1,080/1,080 midpoint checkpoint replays matched uninterrupted digital state; 1,080/1,080 reverse-order schedules matched.
- 46,656 finite message events delivered.
- 6 real OS-process worker cases, 21,250 root generations, 43,583 process node transitions; all 6 matched serial and reverse-submission references. These are barriered message batches, **not** unrestricted asynchronous execution.
- Separate independently written reference script matched 45/45 cases, 281,766 additional reference transitions; it shares authored rules, not an external semantic oracle.
- 17,318,907 total executed node transitions including reference, serial and process repeats. Main runner elapsed 26.211 seconds; independent reference execution excluded from that timing.
- Numerical low-half evaluator: 326 <, 214 >; high-half evaluator: 228 <, 312 >. Of 540 paired comparisons, 286 disagree (∆). Symbolic-semantic comparisons: 540 outcomes 0. Only {<,>,=,0} are evaluation outputs; the meaning of 0 remains provisional.
- Ring vs star final node states differ in 120/120 matched cases at each depth 2 and 4; ring vs chain are equal in 24/24 depth-2 and depth-4 cases at budget 250, differing in 96/96 at budgets 1000+. Depth-0 topologies equal (120/120 each).
- Fault controls detected duplicated/lost/rerouted events, but structural audit did not detect arbitrary internal state tampering. Original digest detects it only if trusted; joint forgery of checkpoint and digest remains possible.

## Historical IETF and code-library provenance
IETF denotes the user's independently authored Infinite Expanse Testing Framework. No affiliation or endorsement by the Internet Engineering Task Force is claimed. Verified original Git blobs in AGI144348Outlook/Mashet-Echo-Drive main:
- Framework b8d28481be30b7619296e79ccf5cdc11b2f28c46 (identical to archived experiments/nve-d/sources/ietf/01-framework.txt)
- IETF Mind Domain 54363e103f87110c59e780c8df83a845432c50cd
- Chronotool 245ac17af2c91bcc82bf2d45c6e3eda1b8d0a738
- Master Codex c39510543954deae8bcfa48a7c4d0d1b8acc00d3

Read DOCUMENT_FEEDBACK_EVALUATION.md, EVALUATION_ALPHABET.md, 003 meta-audit, 004 protocol/summary, 005 baseline and DFE, 006 DFE, 003 hourly report, IETF 001 and IETF substrate 003. Cycle 007's local files were reviewed, not retroactively verified as independent evidence.

Code-library-registry branch: inspected INDEX.md and CLR-0034/0036/0038/0040 assessments. CLR-0036 describes a 96-glyph IETF harness, CLR-0038 a coordinate recentering/contraction primitive, CLR-0040 a persistent EVE graph and project-local RFC-0031/0033 references. Original executable sources for those three CLR entries and the two original RFC specification files were **not found** in the inspected branch trees; do not treat assessments as source. Verified MOD-0002 bounded-composition source provenance to autonomous-agency commit 583caad066fe68b7595fa2bea1d083a0f9e6acd9, blob a5d4ece3ad283e576ac0761039332a70c818ba35; it is not an IETF codex.

## DFE stages 5/7/8
Step 5 evaluation = for checkpoint/independently coded reference equality under declared digital fixture rules; ∆ 286/540 evaluator contradictions; semantic 0.
Step 7 meta-audit 0 for independently authenticated witness, externally grounded semantics, and non-barriered concurrency; challenge shared authored transition assumptions and the auditor's inability to detect arbitrary internal state modification.
Step 8 revision 0 (unexecuted): non-barriered process messaging with causal trace checks, externally witnessed checkpoints, competing interpretation hypotheses tested against held-out observations; preserve earlier contradictory records.

## Artifacts and persistence
Full runner and artifact SHA256 hashes are listed in the accompanying local research report. Local artifact package contains runner, independent oracle, 1080 row-level records, 1080 checkpoints, report and DFE. This committed summary is not a substitute for the full reproducibility package. No protected registries modified; no merge/deploy.
