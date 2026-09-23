# Resh–Lattice Agency Experiment

## Purpose

This branch is an experimental chamber for testing whether ECHO's governing architecture can encounter a separate computational environment, diagnose problems, select bounded actions, execute them, observe the result, and continue without the experimenters supplying the complete solution sequence.

The separate environment is the Lattice Workbench: Python programs, Hebrew/BDB lexical material, lattice-growth algorithms, geometric/tetrahedral routines, processed matrices, feedback experiments, and browser-workbench outputs developed during earlier Mashet/Lattice work.

The experiment deliberately keeps stable branches outside the writable chamber. `main`, `genesis-documentary`, and `autonomous-agency` are not experimental targets. Work occurs on `resh-lattice-agency` and, at runtime, primarily inside the disposable `agency_workspace`.

## What ECHO is in this experiment

ECHO should not be described here as a conventional chatbot or as a demonstrated general intelligence. The relevant object is its executable governance architecture: mechanisms that maintain/index information, evaluate conditions, identify deficiencies, select among possibilities, monitor results, and record what happened.

The governing pattern is referred to as **ר (Resh)**.

The distinction under test is the difference between a programmer prescribing an operation sequence and a governor operating a loop:

```text
prescribed program:
load file -> run A -> run B -> save answer

agency experiment:
observe -> diagnose -> choose -> act -> measure -> observe again
```

The latter loop is the subject of the experiment.

## Why the Lattice is kept unfamiliar

ECHO and the Lattice Workbench were developed as separate bodies of work. Rather than manually integrating them first, this branch asks whether the governing architecture can progressively determine how to operate the Workbench.

A human experimenter may repair laboratory infrastructure when necessary, but should not silently provide solutions to Workbench problems that are intended to test discovery or action selection.

For example, when the Workbench reported that `lattice_prototype` could not be imported, the experimenters already knew that a file named `src/core/lattice_prototype.py` existed. Manually repairing that import would make the Workbench run, but would erase the opportunity to test whether the experimental loop could discover and respond to the discrepancy itself.

## Laboratory isolation

GitHub Actions provides a fresh execution environment for each run. The Workbench ZIP is unpacked into a disposable workspace and observations are preserved as artifacts.

Conceptually:

```text
stable project
  main
  genesis-documentary
  autonomous-agency
          |
          | protected from experiment
          v
resh-lattice-agency
          |
          v
agency_workspace
(disposable runtime chamber)
```

This separation is intended to make failures informative and reversible.

## Runs #1–#3: repairing the laboratory

The earliest runs exposed environmental problems rather than interesting agency behavior.

Some existing ECHO test code referred to development-machine paths such as `/home/claude/...`. Those paths do not exist on GitHub runners, so the experimental branch was made repository-relative.

The English thesaurus corpus was also absent. The environment was changed so it could construct `en_thesaurus.jsonl` from WordNet. That revealed an NLTK dependency, which was then installed by the workflow.

These changes are classified as **laboratory plumbing**, not evidence that ECHO solved those problems.

## Run #4: executable self-governance baseline

After the laboratory became portable, ECHO's existing self-governance test executed successfully.

Observed results included:

- 23,917 indexed vocabulary units.
- Corpus-fitness evaluation.
- Detection of insufficient philosophical/abstract vocabulary in the resulting semantic pool.
- Threshold optimization; the observed run selected 0.30 with a reported composite score of 0.658.
- Pool-quality auditing.
- A seven-target acquisition plan.
- Fifteen generated seed sentences.
- A Governor self-log.
- Normal self-governance exit.

The run reported a corpus mismatch because philosophical vocabulary was absent or sparse in generated statements.

This establishes that the self-governance machinery is executable. It does **not** establish human-like understanding or general intelligence.

## Run #5: first bounded closed-loop probe

Run #5 introduced an experimental Agency Runner between the Workbench observation and bounded computer actions.

The intended architecture is:

```text
Lattice Workbench
      |
  observation
      v
   ר / Governor
      |
   diagnosis
      v
 action selection
      |
      v
   actuator
      |
      v
Lattice Workbench
      |
      +------ repeat ------+
```

The untouched Workbench initially failed with:

```text
ModuleNotFoundError: No module named 'lattice_prototype'
```

The runner inventoried the unfamiliar workspace and discovered:

```text
src/core/lattice_prototype.py
```

It diagnosed the condition as a missing-module visibility problem and selected a conservative action: extend Python's search path to expose the directory without editing the Workbench source.

That distinction matters: the runner found the candidate file from the environment rather than being given its location as the answer.

### Run #5 actuator failure

The selected environment change was not propagated into the subprocess that reran the Workbench. Consequently, the same import error occurred again and the same action was selected repeatedly for the six-turn budget.

Run #5 therefore ended:

```text
Final status: UNRESOLVED
```

The experimental workflow itself completed successfully because its purpose was to preserve the evidence even when the target failed.

The correct interpretation is:

```text
Perception       observed
Diagnosis        observed
Resource search  observed
Action selection observed
Actuation        malfunctioned
Adaptation       not yet demonstrated
```

The actuator should be repaired as laboratory infrastructure. The Workbench problem itself should remain initially untouched for the next trial.

## Evidence ladder

To prevent increasingly sophisticated behavior from being overstated, this branch uses the following conceptual evidence ladder:

```text
Level 0
Human specifies every operation.

Level 1
System detects predefined deficiencies.

Level 2
System selects among predefined responses.

Level 3
System discovers relevant environmental resources.

Level 4
System chooses and executes actions from evidence.

Level 5
System notices that its chosen strategy failed and selects
a genuinely different strategy.

Level 6
System constructs a new solution from available primitives.

Level 7
System tests its own construction, rejects inadequate versions,
and revises them.
```

These levels are experimental descriptions, not claims of consciousness, human cognition, or AGI.

## What success means

Making `lattice_workbench.py` start is only an early milestone.

If execution succeeds, subsequent questions include:

```text
What inputs does the lattice require?
        |
What Hebrew data is available?
        |
How is the data represented?
        |
Which lattice operation can consume it?
        |
What structure results?
        |
Does that structure satisfy its constraints?
        |
What is missing?
        |
What operation should happen next?
```

The longer-term experimental loop is therefore:

```text
Hebrew lexical substrate
        |
        v
lattice construction
        |
        v
relationships / cells
        |
        v
resulting structure
        |
        v
ECHO observes structure
        |
        v
ר evaluates
        |
        v
bounded modification / expansion
        |
        +------------- repeat
```

## Scientific caution

The Agency Runner itself contains engineered capabilities, including recognition of certain classes of software failures and a bounded vocabulary of permitted actions. A successful diagnosis must therefore not be represented as spontaneous general reasoning arising without prior machinery.

The useful experimental question is narrower and testable:

> Given an unfamiliar computational environment, how far can ECHO's governing architecture progress toward operating and developing it without the experimenters supplying the sequence of solutions?

Every run should preserve enough evidence to distinguish:

1. infrastructure supplied by the experimenters;
2. observations available to the system;
3. choices actually made by the system;
4. actions actually executed;
5. results observed after those actions;
6. revisions made in response to failed actions.

## Next experimental correction

Before the next run, the actuator should correctly pass selected environment changes into the subprocess.

Repeated ineffective actions should also become observations in their own right. A failed strategy should not be allowed to repeat indefinitely without affecting subsequent selection.

Then the untouched Workbench can be presented again and the next observation allowed to emerge naturally.


## Run #6 — closed-loop execution breakthrough

Run #6 repaired laboratory actuation rather than modifying the supplied Workbench. The runner now passes selected environment changes into the subprocess and records repeated ineffective observation/action pairs so repetition can become evidence for reconsideration.

### Observed progression

1. The untouched Workbench again reported `ModuleNotFoundError: No module named 'lattice_prototype'`.
2. The loop discovered `src/core/lattice_prototype.py` and selected `extend_pythonpath`.
3. With the actuator corrected, that action changed the environment and the original error disappeared.
4. A new observation emerged: `FileNotFoundError: bdb_roots.json`.
5. The loop searched the workspace, found the requested data under `data/processed`, and selected a different action: execute from the matching data context.
6. The next execution returned exit code 0.
7. Workbench output reached lattice behavior, including `REGION CLOSED after step 7` and a final hand-built region with four closed Flags.
8. The loop recognized successful target execution and stopped.

Final experimental status: `WORKBENCH_EXECUTED`.

This is stronger evidence than Run #5 because two different environmental states led to two different evidence-derived actions, and both actions measurably changed the subsequent observation. It remains a bounded engineered harness: its diagnostic categories and permitted actions were supplied by the experimenters. The result therefore supports a functioning multi-step perception/action feedback loop within those bounds, not a claim of AGI or human-like cognition.

The dependency audit of the supplied Workbench identified `nltk` as the only external Python import candidate; other imports were standard-library or Workbench-local modules.

### Next research boundary

The experiment has moved from **environmental troubleshooting** to **lattice operation**. The next question is whether the governing system can inspect the successfully produced lattice structures, characterize their state and constraints, formulate a next objective, select a lattice-level operation, and evaluate the resulting structural change without being handed the solution sequence.

## Research documentation protocol

From this point forward, researcher-facing documentation is part of the experimental protocol rather than an optional cleanup step.

After every meaningful progression on an experimental branch, the branch documentation should be updated in the same progression cycle. Each record should preserve:

1. **Objective** — what question the run or change was testing.
2. **Starting state** — relevant branch, environment, inputs, and protected boundaries.
3. **Experimenter-supplied infrastructure** — plumbing, dependencies, harness capabilities, or corrections supplied by humans/automation.
4. **System-visible evidence** — observations actually available to ECHO/Resh.
5. **Decision trace** — diagnoses, candidate/selected actions, and stated reasons when available.
6. **Executed actions** — what actually changed, distinguished from actions merely proposed.
7. **Observed results** — exit states, measurements, artifacts, structural outputs, and newly exposed problems.
8. **Interpretation** — what the evidence supports.
9. **Limitations / non-claims** — what the run does not establish, especially distinctions among engineered, demonstrated, and hypothesized behavior.
10. **Next research question** — the unresolved boundary exposed by the progression.
11. **Provenance** — run IDs, commit SHAs, artifact IDs, and other identifiers needed to reproduce or audit the result when available.

Documentation follows the same branch discipline as the experiment it describes. Experimental chronology remains on its experimental branch; it is not promoted to `main` or another stable branch without explicit direction.

The protocol also preserves negative results. Failed runs, repeated strategies, infrastructure defects, and capability gaps are evidence and should not be silently rewritten into successful narratives.


## Run #7 — first bounded lattice-level operation

**Provenance:** GitHub Actions run `35920775406`; workflow head `faca6f89d2676edf13d851b045c2de5c2261f9a1`; evidence artifact `10777595069`.

### Objective

Move beyond execution troubleshooting and test whether the harness can observe a successfully running lattice, derive a structural description, choose one bounded lattice-level operation from the algorithms already present in the unfamiliar Workbench, execute it, and observe a resulting structure.

### Starting state and experimenter-supplied infrastructure

The Workbench source remained untouched in the disposable workspace. Run #7 reused the runtime context established experimentally in Run #6: `src/core` was exposed on `PYTHONPATH` and execution occurred from the processed-data context. The experimenters also supplied the candidate-ranking policy: observed structural terms are compared with available algorithm filenames. This policy is an explicit harness mechanism and must not be mistaken for unconstrained semantic reasoning by ECHO/Resh.

### System-visible structural evidence

The baseline Workbench executed with exit code 0. In this run its stochastic/variable construction closed after step 8, with 9 bricks and 4 closed Flags:

- `כאה` — “be disheartened, cowed”
- `סרכ` — “chief, overseer”
- `ראה` — “see”
- `רכה` — “in Judah”

The difference from Run #6 (closure after step 7 with 8 bricks) is preserved as an observed run-to-run variation rather than normalized away.

### Candidate selection

The harness inventoried eleven available `lattice_*.py` operations. Against the observed closed-region/constraint description, the highest filename-semantic score (2) was shared by:

- `lattice_distinct_regions.py`
- `lattice_isolate_constraints.py`
- `lattice_themed_regions.py`

`lattice_lineage.py` scored 1; the remaining candidates scored 0. Deterministic alphabetical tie-breaking selected `lattice_distinct_regions.py`.

This tie is an important limitation: Run #7 did not demonstrate that the system understood that “distinct regions” was intrinsically preferable to “isolate constraints” or “themed regions.” The harness supplied the scoring and tie-break rule.

### Executed action and observation

`lattice_distinct_regions.py` executed successfully with exit code 0 and produced output distinct from the baseline Workbench. The preserved tail showed multiple independently seeded closed regions and cross-talk analysis among them. Examples included direct shared-stem relationships between some region pairs and indirect shared-glyph relationships between others.

The run ended with:

`Final status: LATTICE_OPERATION_EXECUTED`.

### Interpretation

Run #7 establishes that the experimental loop can cross the boundary from repairing the Workbench runtime to invoking a lattice-level operation selected from the Workbench's own available algorithms using an explicit evidence-derived ranking procedure. It also produced a new class of observable structure: multiple separately seeded regions and reported inter-region cross-talk.

It does **not** establish autonomous formulation of a research objective, unconstrained semantic understanding of the algorithms, or autonomous evaluation of which resulting region relationships are meaningful. The selection policy and its tie-break were experimenter supplied.

### Next research question

The next boundary is evaluation rather than mere execution: can the experimental governing layer inspect the multi-region/cross-talk output, turn measurable features of that result into competing next objectives or hypotheses, and choose among them using actual ECHO/Resh governance machinery rather than filename scoring alone?
