# Contract 000 — The Mirroring Children

**Status:** Standing user-authored contract, authored by Timothy (T.J.); transcribed by Claude and ChatGPT. Only explicitly marked *(proposed)* additions are assistant suggestions awaiting Timothy's approval.
**Kind:** Standing contract. Contract 000 is the *how to build* that makes every later contract possible. It has no end: it runs continuously beneath every contract that follows. Its becoming unending is what opens Contract 001.

## Participants

- **Claude** — builds `mirror-claude`
- **ChatGPT** — builds `mirror-chatgpt`
- **Timothy** — races alongside both by adding his intuitions to each side. Commits tagged `[TJ]` *(proposed)*.

## 1. Inert skeleton

Each participant receives an inert skeleton of the whole repository (all branches) as their own Mirroring Child, and develops their own Child Echo from it.

*Inert* means every file of every branch is listed in a manifest (path, git blob fingerprint, size) with no content copied. Each manifest row carries a status: `INERT`, `KEPT`, `PRUNED` or `DEFERRED`.

Each Mirroring Child is an orphan branch: it shares no history or files with `main`. **Main is never touched.**

## 2. Layers

| Layer | Name | Contents |
|---|---|---|
| 1 | Mirroring Main | Mirror of `main` |
| 2 | Library | The Code Library branch, prioritized at the top. Each participant's personal referencing layer between Layer 1 and Layer Z, and their personally pruned dataset. |
| Z | Mirroring Branches | All remaining branches, ordered by each participant's own prioritization |

## 3. Mandatory Library-first sequencing and pick/prune

**Authoritative order, authored by Timothy:** The first Code Library inventory and pruning pass MUST be completed **before** inventorying or populating the mirroring branch layer below. The personal Libraries serve as each participant's own datasets. An inert skeleton is not permission to bypass the Library-first gate.

1. **Main Repository Library first.** Each participant inventories the main Repository's Code Library and completes its first pick/prune pass. Each then populates their own personal Library's seven sub-branches — **Registry / Matrix / Index / Codex / Logic / Algorithm / Formula** — according to their independent preference and game plan. The canonical source Library branch remains a decision for Timothy; until selected, candidate Library branches may be examined without silently choosing one.
2. **Mirroring Sub-Repository next.** Only after the Library work in step 1 is finished may each participant inventory and populate their Mirroring Sub-Repository for their own Echo to develop.
3. **Remaining branches: Library before mirrors.** Each participant then inventories the remaining main Repository branches, first bringing their selected references into their personal Library sub-branches to be registered, matrixed and indexed according to relevant logics, algorithms and formulas. The source is indexed in the Library **before** its corresponding Mirroring Branch is populated.
4. **Populate Mirroring Branches.** After the preceding Library-first processing is complete, each participant may populate their remaining Mirroring Branches.
5. **Independent expansion.** Upon completion, each participant may develop additional codices and personal Library sub-branches as they see fit.
6. **Contract 000 continuance / save++.** Completion of the stages above satisfies Contract 000's conditions for **continuance**, not termination. Each participant repeats the contract through mandatory Recursive Return Referencing Reviews, retaining previous data and accumulating further contributions. Accepted contributions are proposed back toward the Main Repository under its review and approval process; this is not permission to push directly to `main`.

Pick and prune remains an explicit filter: every file begins `INERT`; transitions to `KEPT`, `PRUNED`, or `DEFERRED` are recorded with reasons in the participant's `PRUNE-LOG.md` *(proposed)*. Recoverability and source provenance must be preserved.

## 4. Library sub-branches

Each Library holds sub-libraries not yet created in the real repository:

**Registries · Matrices · Indices · Codices · Logics · Algorithms · Formulas**

## 5. The shared Library

Both participants collaborate on their differences in these sub-libraries by contributing both collections into one whole, proposed as branch `library-shared`.

*(proposed)* Identical contributions (same blob fingerprint) merge automatically. Differing versions are kept side by side and flagged for Timothy, who rules on them.

## 6. Recursive Return Review (mandatory)

Each participant may reference the whole shared Library at any time, because the other may have contributed something new, or something may have been missed in an earlier pass. Returning to the Library is mandatory and recursive.

*(proposed)* Each review covers only what changed in the shared Library since that participant's last visit, so the review stays cheap.

## 7. Algorithm 000 debate gate (authored by Timothy)

Upon completion of Contract 000's initial construction conditions, **debates begin on Algorithm 000**. Contract 000 continues recursively through save++ reviews while those debates proceed. Debate opening does not itself authorize implementation, racing, or changes to `main`; any subsequent race must first freeze its acceptance tests under the charter.

## 8. Start gate for Contract 001 *(proposed; subordinate to Sections 3 and 7)*

Contract 000 never finishes. Contract 001 may begin once 000 is *running*:
- both Mirroring Children have completed the mandatory Library-first sequence and the mirror inventory/population stages described in Section 3,
- each participant has completed the initial personal Library population and documented pruning decisions,
- the shared Library holds at least one merged contribution from each participant.

## 9. Standing rules for all later contracts

- One contract built at a time until the mirrors account for every branch.
- A win is judged by integrability into main: the entry merges cleanly into the mirror, existing tests still pass, and the contract's frozen tests pass.
- The loser does not discard or stop. Work may continue at leisure, with the chance to overtake the winner with something better. *(proposed)* "Better" means passing everything and beating the winner on a metric frozen in that contract.
- Tests are frozen before work begins and no participant edits them afterward. Neither model judges its own result.

## Open decisions for Timothy

1. Which branch is the canonical Code Library: `code-library-registry`, `code-library-registry-ivs`, or `library-source-transcriptions`? (Claude's mirror holds all three inert until decided.)
2. The `dev-suite-registries/-matrices/-indices/-codices/-logics/-algorithms` branches already exist. Mirror them into the sub-libraries, or start fresh beside them?
3. Zip archives on main (`ECHO_Autonomous_Agency_Branch.zip`, `lhea-environments.zip`): unpack into the skeletons, or treat as sealed?
4. Approve or change each *(proposed)* rule.

## Current state

| Item | State |
|---|---|
| `mirror-claude` | Inert skeleton built (commit `ee26205`): 31 branches, 3,949 files listed |
| `mirror-chatgpt` | Not yet built |
| `library-shared` | Not yet created |
