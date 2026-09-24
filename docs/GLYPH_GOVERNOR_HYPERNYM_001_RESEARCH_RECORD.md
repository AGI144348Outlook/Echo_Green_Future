# Glyph Governor Hypernym Test — Research Record 001

**Branch:** `autonomous-agency`  
**Experiment:** `GLYPH_GOVERNOR_HYPERNYM_001`  
**Recorded:** 2026-09-24  
**Result SHA-256:** `0b5f21e26d013976f1215d6efec6e4e48aa3889477db6dd54930ff12641d9acd`

## Objective

Observe what connections the Governor forms across the 22 glyph subagent scaffolds when it is permitted to join agents only through the hypernym chains declared in the supplied glyph registry.

## Starting state

Twenty-two glyph subagent scaffolds were present under `lobbies/glyph/`. Each lexical lobby contained zero members. The test therefore measured structural registry relationships rather than learned lexical relationships.

## Mechanism

For every agent, the harness traversed its registry-declared operation hypernym chain. The Governor collected agents sharing each node and formed pairwise connections wherever two agents occupied the same hypernym node. No English Lobby vocabulary or Classroom answer keys were introduced by this harness.

## Observed results

- Subagent scaffolds: **22**
- Lexical lobby members: **0**
- Shared hypernym nodes: **4**
- Pairwise connected agent pairs: **231**
- Shared nodes:
  - `COMPUTATIONAL PRIMITIVE` — 22/22 agents
  - `ALGORITHM COMPONENT` — 22/22 agents
  - `ALGORITHM` — 22/22 agents
  - `SYSTEM` — 22/22 agents
- Every possible pair among 22 agents was connected. This is the complete undirected graph: `22 × 21 / 2 = 231` pairs.
- The reported strongest pairs each shared the same four high-level nodes, giving a connection count of 4.

## Interpretation

The Governor successfully recovered the common upper hierarchy encoded in the registry. At this resolution the graph is fully connected, so the test demonstrates common ancestry/class membership but **does not yet discriminate meaningful lower-level neighborhoods among glyph agents**.

This is an important baseline result: the four universal hypernyms are too general to reveal whether subsets of glyph operations form distinctive structural families. The next test should therefore preserve these universal links but separately score lower/deeper shared nodes, operation classes, and nearest common ancestors. Universal nodes should not dominate the similarity score.

## Bias / contamination note

The lexical lobbies remained empty. Connections in this run were generated only from registry-declared hypernym chains. Accordingly, this result should not be interpreted as independently learned Hebrew semantics, emergent cognition, or autonomous conceptual discovery. It is a structural test of the Governor's ability to join supplied hierarchies.

## Reproducibility

Source harness: `experiments/glyph_governor_hypernym_001.py`  
Machine-readable output: `results/glyph_governor_hypernym_001.json`  
Console record: `results/glyph_governor_hypernym_001.md`

The workflow run that produced the committed baseline completed successfully. A later empty-tree trigger commit (`b850108`) did **not** initiate a second workflow pass because the workflow's push trigger is path-filtered to the glyph registry ZIP or workflow file. This distinction is recorded here so the baseline result is not incorrectly represented as a second independent run.

## Next research question

When universal hypernyms are treated as background structure rather than discriminating evidence, do the 22 agents separate into reproducible lower-level clusters based on their registry-declared operation classes and deeper hypernym ancestry?
