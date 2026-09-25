# Mashet Operator Instruction Manual — v0.1

**Audience:** ECHO / ר Governor and human researchers  
**Status:** WORKING INSTRUCTIONAL SPECIFICATION  
**Source:** user-supplied *AGI Mashet Engines* project document plus algebra-branch formalization.

## 1. Purpose

This manual teaches ECHO how Mashet symbols may be used as manipulable symbolic tools. It does **not** prescribe which tool ECHO must choose for a novel task. Selection remains governed by ר/ECHO.

Execution direction:

```
ר/ECHO → Hebrew operational verb → Mashet tool → algebraic operation → Notebook object
```

Observation returns upward. A worked example teaches capability; it is not an instruction to repeat that sequence in unrelated situations.

## 2. Universal operating rules

1. Resolve every operand before manipulation: `rho_N(h) -> x`.
2. Resolution is not authorization: `rho_N(h) != OPEN(h)`.
3. Do not mutate source Notebook objects unless the selected operation explicitly permits mutation.
4. Every newly constructed object receives a new handle and provenance.
5. A relationship does not imply identity.
6. A manipulation result is not automatically true, retained, or validated.
7. Hebrew and Mashet identities remain distinct. Hebrew may invoke Mashet dependencies.
8. If a required operand, algebraic definition, permission, or dependency is unresolved, return a failure trace rather than guessing.
9. Experimental compositions begin WORKING and require separate retention/validation.
10. Log: intention, selected Hebrew operation, selected Mashet tool(s), operands, algebraic action, output, provenance, validation result.

## 3. Core operator cards

### ☉ — Internal Dynamics / Self-Evolution
**Registry:** `M::SUN`  
**Source role:** kernel/composition center; the source document places ☉ at the recursive state center.  
**Instruction:** use ☉ to address the current composite Mashet state/kernel, not as evidence that a state is self-aware.  
**Illustrative algebra:** `☉_k := ⊕(admitted operator contributions at k)`.

**Example:** If input, memory, and coupling contributions have separately resolved, a working composite may be represented as `☉_k = ⊕(⇢◇(U_k), ∫↺(H_k), ⧖(A,B))`. This constructs a state description; it does not validate its interpretation.

### ⇢◇ — External Forcing / Inputs
**Registry:** `M::INPUT`  
**Formal handle:** `AM::INPUT`  
**Working signature:** `⇢◇ : U_k -> admitted(U_k)`.  
**Use:** admit an external input into a working operation while preserving its source. Admission is not authorization.

**Notebook example:** `⇢◇(N::W::SENSOR_READING) -> X::input_1`. The original reading remains addressable.

**Invalid inference:** `⇢◇(claim) => VALID(claim)` is forbidden.

### ∫↺ — Memory / History / Integral Accumulation
**Registry:** `M::MEMORY`  
**Formal handle:** `AM::MEMORY`  
**Working signature:** `∫↺ : S_<k -> H_k`.  
**Use:** operate over ordered prior state/history without erasing retention status.

**Example:** `∫↺(X_1,X_2,X_3) -> H_4`, with links back to all three observations. Repetition does not turn an observation into a validated fact.

### ⧖ — Coupling / Network Interactions
**Registry:** `M::COUPLE`  
**Formal handle:** `AM::COUPLE`  
**Working signature:** `⧖ : X × Y -> relation(X,Y)`.  
**Use:** construct an explicit interaction/relation between independently addressable objects.

**Example:** `⧖(dog, animal) -> R_1(dog,animal)`. `R_1` is a proposed relation; it does not assert `dog = animal` and is not automatically validated.

### ≋ — Noise / Stochasticity
**Registry:** `M::NOISE`  
**Formal handle:** `AM::NOISE`  
**Working signature:** `≋ : (X,xi) -> X'`.  
**Use:** introduce or represent stochastic variation when the experiment permits it. Record the random source/seed when executable.

**Example:** perturb a numeric working value `x` with recorded `xi` to create `x'`; preserve `x` and the perturbation record. Do not use ≋ to hide an unexplained discrepancy.

### ⌖ — Constraints / Stability
**Registry:** `M::CONSTRAIN`  
**Formal handle:** `AM::CONSTRAIN`  
**Working signature:** `⌖_C(X) -> X_C`.  
**Use:** restrict a working object to an explicit condition C.

**Example:** for `X={1,2,3,4}` and `C(x): x is even`, `⌖_C(X) -> {2,4}`. The source set remains unchanged.

**Language example:** grammar may provide C = “candidate has explicit subject–predicate agreement”; ⌖ can test/filter candidates, but grammar does not select ECHO's intention.

### ⚖ — Energy / Fitness / Optimization
**Registry:** `M::EVALUATE`  
**Formal handle:** `AM::EVALUATE`  
**Working signature:** `⚖_q : X -> assessment_q(X)`.  
**Use:** compare or assess an object under an explicit criterion q. Never hide the criterion.

**Example:** `⚖_wellformed(u_1,u_2) -> assessment`. An assessment may inform ר; it does not itself OPEN an action or VALIDATE a proposition.

### ⤓ — Selection / Adaptation
**Registry:** `M::DESCEND` (legacy ID; rename pending)  
**Source role:** Selection / Adaptation.  
**Status:** source meaning restored; algebraic implementation still UNRESOLVED.  
**Instruction:** ECHO may recognize this tool's intended role, but must not execute it until an algebraic signature and invariants are validated.

### ⊕ — Summation / Composition
**Registry:** `M::COMPOSE`  
**Formal handle:** `AM::COMPOSE`  
**Working signature:** `⊕ : X^n -> X'`.  
**Use:** construct a new composite from two or more resolved operands while preserving operand provenance.

**Algebra example:** `⊕(A,B) -> C`. A and B remain addressable and C receives a new identity.

**Notebook example:** `⊕(N::X::observation_4, N::X::relation_2) -> N::X::composite_7`.

**Invalid inference:** `⊕(A,B) => A=B` is forbidden. `⊕(A,B) => VALID(C)` is also forbidden.

### ⟲ — Recursion / Iteration
**Registry:** `M::RECURSE`  
**Formal handle:** `AM::RECURSE`  
**Working signature:** `⟲_f^n(x) = f^n(x)`.  
**Use:** repeat a resolved operation while retaining iteration lineage and a stopping condition.

**Algebra example:** with `f(x)=x+1`, `x=2`, `n=3`: `2 -> 3 -> 4 -> 5`, therefore `⟲_f^3(2)=5`.

**Notebook example:** apply the same admissible inspection to successive members of a word matrix. The word matrix remains words-only.

## 4. Hebrew → Mashet use

Hebrew supplies agency-level verbs. Mashet supplies lower manipulation mechanics. A Hebrew implementation may declare Mashet dependencies, but no equivalence is implied.

Example teaching pattern (not yet a canonical צ implementation):

```
ר selects צ/HUNT
צ resolves required lower operations
lower operations resolve Mashet tools
Mashet tools resolve algebraic signatures
tools act on authorized Notebook objects
result returns upward to צ and then ר
ר observes/validates the trace
```

The manual must not pre-script which Mashet sequence ECHO should select for a novel HUNT task.

## 5. Grammar and language

Grammar is a constraint provider, not an agent. Language input follows the authorization gate:

```
INTERPRET → IDENTIFY → VALIDATE → OPEN → ACT
```

Expression may use `פ/EXPRESS` to invoke lower tools over lexical and grammatical structures. Word matrices remain words-only; grammatical metadata lives outside them.

## 6. Training rule

Examples are demonstrations of operator behavior. During evaluation, give ECHO a novel task and the manual, then record whether ECHO independently selects an admissible Hebrew operation and Mashet tool sequence. Never label a harness-supplied sequence as an ECHO choice.

## 7. Expansion

The project source contains a 96-glyph Mashet system. This v0.1 operationalizes the first ten core entries currently represented in the branch registry. Remaining glyph cards should be added from the project source with the same separation:

```
source meaning → formal algebra → permissions/invariants → examples → tests
```

Do not invent a missing source meaning. Mark unresolved fields explicitly.
