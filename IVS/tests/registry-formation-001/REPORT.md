# IVS Registry Formation Test 001

## Result: PASS — minimal Dataset → Registry boundary demonstrated

Input: three real JSON inscription records from `mayig/indus-valley-script-corpus`:
- M-1A
- M-3A
- M-4A

The test intentionally uses corpus structure only. It does not import Mashet/Indus semantic readings and does not attempt decipherment.

## Registries formed

0. DSL Registry — EMPTY by design; no DSL semantics declared by the source.
1. Source Registry — 1 source/provenance record.
2. Inscription Registry — 3 inscriptions.
3. Grapheme Registry — 16 distinct grapheme IDs.
4. Occurrence Registry — 18 positional occurrences.
5. Adjacency Registry — 15 distinct observed adjacent pairs.
6. Description Registry — 1 observed description class.

## Structural observation

M-4A contains consecutive `P268 → P268` and repeats `P147` later in the same sequence. These are registered as observations only.

## Invariants

- Definition is not authority.
- Registration is not execution.
- No semantic decipherment attempted.
- No source values repaired.
- Source order and feature vectors are preserved.

## Scope

This proves the minimal IVS Dataset → Registry transformation on a three-record sample. It does **not** yet prove whole-corpus scalability, automatic schema discovery across arbitrary formats, or semantic interpretation.

Next scale test: run the same boundary over the complete corpus and compare generated frequency/position/adjacency registries with independent structural-analysis sources.
