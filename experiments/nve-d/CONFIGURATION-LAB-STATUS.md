# NVE-D configuration lab — Steps 1–4 (provisional)

**Branch:** `library-source-transcriptions`  
**Source plan:** `docs/assessments/NVE-D-IMPROVEMENT-PLAN-2026-10-09.md`  
**Status:** Initial code committed; NOT NVE-D-021; no semantic findings or registry changes.

## Contents

- `configuration_lab.py`: 16-entity ordered-pair configurations; canonical SHA-256 identity; tested-set import/export; J-B independent-relation candidate judge and differently structured oracle; eight **proposed** Hebrew operators; Node/Link/Budget/Clock; random, sparse, and adaptive search scaffolds.
- `test_configuration_lab.py`: local standard-library tests for canonical identity, tamper detection, judge agreement, immutability, determinism and budget limits.

## Run

From `experiments/nve-d`:

```sh
python -m unittest -v test_configuration_lab.py
python configuration_lab.py --registry-manifest manifest.json --registry-ref "<REPO>@<40_HEX_COMMIT>:<SOURCE_PATH>" --budget 100 --seed 21 --output preparation.json
```

**Do not use a made-up ref:** the CLI requires a supplied reference, but does **not yet resolve it against GitHub**. Before an evidentiary trial, add a registry loader which verifies all sixteen MS IDs against the pinned source and records their source provenance. The test file's clearly labeled PIN placeholder is *only* a fixture.

## Limits and open work

1. **Step 1 partial:** schema, ordered-pair validation, digest and in-memory tested-set are implemented. Tested-set serialization is provided, but the CLI does not yet load or atomically persist a tested-set across cycles. No registry-resolution validation exists yet.
2. **Step 2 provisional:** J-B and its separately coded oracle are implemented. Both currently return `=` only when all four cycle edges are non-open and equal, otherwise `0`; they do **not** evaluate the full Governor formula, or issue `<`/`>`. A truly independent evaluator requires separate authorship/implementation and cross-runtime comparison before claiming E2.
3. **Step 3 partial:** eight letter-labeled candidate moves exist. They are *not* declared LHEA meanings. The `ס` protection is transient, `ת` is a no-op terminal signal rather than a node freeze, and `מ` is a basic chain copy. No LHEA credential detector is implemented. Same-step join/split exclusion is represented in the move API but the scheduler performs only one move per step.
4. **Step 4 partial:** three budget-capped arms are implemented with deterministic seeds. The 'sparse' and 'adaptive' arms are **minimal approximations**, not faithful complete implementations of A1+A2+D2+E2 and B1+B2+D1. They have no equal-count guarantee if a search stalls, no full lifecycle, no persistent anti-repetition across cycles, and no declared-space coverage report yet.
5. The current `score` is **synthetic non-open pair count**. It is not a discovery measure, and this code emits `evidence_level: NONE`. Replaying it cannot establish E1–E4.
6. NVE-D-021-IVS is separate and not implemented. IVS signs must not be silently mapped to Mashet MS IDs.
7. No production workflows, authoritative rules, Registry 0, existing trials or protected algorithms were changed.

## Next verification gates

- Pin and validate the real canonical registry entries; reject mismatched/missing IDs.
- Persist tested-set and manifest/checkpoint across hourly runs with crash-safe writes and replay.
- Complete each proposed move's state transition and the candidate algorithm arms; compare **equal actual tested budgets**, not merely equal caps.
- Implement a separately authored evaluator and differential tests; do not conflate agreement with semantic meaning.
- Only after these gates, propose a NVE-D-021 execution with an explicit declared sub-space and candidate judges. No automatic promotion of definitions or findings.

## 2026-10-09 verification update

- Added a branch-scoped GitHub Actions workflow: `.github/workflows/nve-d-configuration-checks.yml`. It runs the unit tests and a 25-configuration-cap smoke test on pushes touching the code/tests/workflow. **Workflow execution and outcome have not yet been confirmed.**
- The CLI now requires a source-pinned registry manifest. The validator checks 16 unique expected IDs, full commit SHA shape, source path and per-entry locators. It **does not independently fetch the upstream source or verify that the asserted entries are present**; do not label these entries authoritative or fully verified.
- No canonical Mashet 96 legend has been declared. `code_library_registry/symbol_registries/README.md` on `code-library-registry` explicitly says it is a planning record and the canonical 96 legend remains undecided.
- The workflow smoke test uses an explicit fake fixture, not a real registry. No E1–E4 evidence or NVE-D-021 result is produced.
- Local container network could not resolve GitHub raw content, so tests were not executed locally in this review. Verify the Actions job before treating tests as passed.
