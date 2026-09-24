# Candidate Agentic Algorithm List

**Status:** Candidate / pre-validation  
**Project:** PWA Hosting Environment / Dual-Order OS Matrix development  
**Purpose:** Identify agentic needs implied by the Dual-Order OS foundational RFC before deciding which algorithms belong to the Governor's invariant starting capacity.

This document is deliberately a candidate registry, not an implementation claim. An item being listed here does not mean its algorithm has been derived, validated, or admitted into the invariant set.

## Validation classes

Each candidate is to be evaluated as one of:

- **Invariant Agentic Capacity** — intrinsic capacity the Governor must validate before Dual-Order operation can function.
- **Employable Domain Algorithm** — an algorithm the Governor may recognize, validate, select, and employ without making it part of Governor identity.
- **Unresolved Requirement** — the architecture requires the capability, but the governing algorithm has not yet been earned.

## Candidate algorithms

### CAND-001 — Elemental Decomposition

**Agentic need:** Determine whether a structure is elemental or composite; decompose a framework into reusable elemental parts while preserving identity and provenance.

**RFC basis:** The system is intended to decompose frameworks into elemental, reusable parts and recombine them modularly.

**Candidate class:** To be determined.

---

### CAND-002 — Matrix / Index Traversal Recognition

**Agentic need:** Determine whether an encountered structure is presently functioning as a Matrix (content-first traversal) or an Index (lookup-first traversal).

**Constraint:** Matrix and Index are not permanent object types. Role depends upon traversal direction.

**Candidate class:** Strong invariant-capacity candidate.

---

### CAND-003 — Bidirectional Reachability Validation

**Agentic need:** Verify that every elemental part can be reached content-first and lookup-first.

**Failure recognition:**
- Matrix element with no Index path -> orphaned part.
- Index entry with no Matrix target -> empty Index.

**Candidate class:** Strong invariant-capacity candidate.

---

### CAND-004 — Relationship-Type Recognition

**Agentic need:** Determine what kind of relationship is being represented before choosing an Index mechanism.

**Known examples:** geometric/by-angle versus taxonomic/by-is-a.

**Constraint:** Distinct relationship types must not be forced through one Index merely because an existing mechanism partially works.

**Candidate class:** Strong invariant-capacity candidate.

---

### CAND-005 — Index Selection

**Agentic need:** Given a recognized relationship type, select the Index whose governing relation legitimately represents it.

**Candidate class:** To be determined.

---

### CAND-006 — Novel Index Requirement Recognition

**Agentic need:** Recognize when no existing Index legitimately represents an encountered relationship and signal the requirement for a differently typed Index.

**Important limitation:** The RFC supports the need to name relationship mismatches and add differently typed indices; it does not yet specify a fully agentic algorithm for autonomous Index invention.

**Candidate class:** Unresolved / generalization candidate.

---

### CAND-007 — Metric Validation

**Agentic need:** Validate a candidate similarity or comparison metric against a known failure case before accepting it as canonical.

**Constraint:** Directionally correct performance is insufficient; validation must establish a decisive result under the applicable test standard.

**Candidate class:** To be determined.

---

### CAND-008 — Prerequisite / Gate Ordering

**Agentic need:** Recognize when one operation must precede another and prevent downstream operations from executing before prerequisites are satisfied.

**Known example:** part-of-speech identification must precede candidate sense enumeration.

**Candidate class:** Strong invariant-capacity candidate.

---

### CAND-009 — Relational Bridge Discovery / Employment

**Agentic need:** When two structures cannot legitimately be compared directly, identify and employ a valid relation that bridges them.

**Known example:** verb sense -> derivationally related noun form -> comparison with fixed noun senses.

**Candidate class:** To be determined.

---

### CAND-010 — Identity vs Activation Discrimination

**Agentic need:** Distinguish a newly encountered entity from a repeated activation of an already instantiated entity.

**Constraint:** Repeated occurrence must update/log activation state rather than duplicate node identity.

**Candidate class:** Strong invariant-capacity candidate.

---

### CAND-011 — Generalization Detection

**Agentic need:** Distinguish actual system generalization from human-authored software-pattern reuse.

**Target condition:** Correctly infer treatment for a previously unconfigured category without new category-specific code.

**Candidate class:** Unresolved Requirement.

---

### CAND-012 — Operand / Operator Treatment Inference

**Agentic need:** Infer whether a previously unconfigured category should be treated as operand, operator, or another structural role without receiving category-specific implementation code.

**RFC status:** Explicitly identified as the bar for genuine generalization; not yet built.

**Candidate class:** Unresolved Requirement.

---

### CAND-013 — Ambiguity Resolution Beyond Two Simultaneous Terms

**Agentic need:** Resolve 3+ simultaneous ambiguous words without collapsing onto a spurious local optimum.

**RFC status:** Known failure; unresolved.

**Candidate class:** Unresolved Requirement.

---

### CAND-014 — Primitive Unification / Separation Recognition

**Agentic need:** Determine whether multiple observed behaviors are manifestations of one primitive or genuinely separate primitives.

**Known unresolved case:** Separation/Scindere — independent split, additive split, paired-regeneration split.

**Candidate class:** Unresolved Requirement.

---

### CAND-015 — Structural vs Operational Logic Recognition

**Agentic need:** Distinguish structural logic from operational logic and determine which governs an encountered relation or transformation.

**RFC status:** Not formally defined.

**Candidate class:** Unresolved Requirement.

---

### CAND-016 — Occupancy / Address Distinction

**Agentic need:** Preserve the distinction between a pre-given addressable field and progressive occupancy of that field.

**Constraint:** An unoccupied address is not a nonexistent address. Population changes occupancy, not the existence of coordinate space.

**Candidate class:** Matrix-side invariant candidate; requires reconciliation with the specific NVE materialization implementation before canonicalization.

---

### CAND-017 — Capacity vs Employment Distinction

**Agentic need:** Distinguish an algorithm the Governor is capable of employing from an actual employment/activation event.

**Purpose:** Permit invariant capacity validation without treating every potentially employable algorithm as continuously active.

**Status:** Derived from the current Governor capacity-validation discussion and the RFC's identity-versus-activation discipline; not yet a named RFC algorithm.

**Candidate class:** Strong invariant-capacity candidate, pending formal derivation.

---

## Governor boot hypothesis — not yet canonical

The current working hypothesis is:

```text
Governor candidate
    -> identity validation
    -> invariant agentic capacity validation
    -> potential employ set
    -> Matrix/Index encounter
    -> relationship + traversal recognition
    -> appropriate capacity employment
    -> Dual-Order operation
```

The secondary validation stage must not merely prove that the Governor matches its canonical identity in the Algorithm Matrix. It must validate the minimal invariant capacities by which that Governor can legitimately operate upon Matrices and Indices.

## Next review

Return to RFC-0000 from Section 1 onward. For each architectural statement ask:

> What must an agent be capable of doing for this statement to become operational?

Do not promote candidates into the invariant set merely because they are useful. Promotion requires showing that Dual-Order operation cannot function without that capacity.
