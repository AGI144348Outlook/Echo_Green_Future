# Contract 000 — The Mirroring Children

**Status:** Draft, authored by Timothy (T.J.), recorded by Claude. Rules marked *(proposed)* await Timothy's approval.
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

## 3. Pick and prune

Each participant may pick and prune files and folders for each mirrored branch, as if applying a filter to how their Mirroring Child relates to the Parent Repository.

Order of work:
1. Start with everything inertly emptied.
2. Prune through the Library first, filling Layer 2 as each participant chooses.
3. Then prune Layer Z in each participant's own order.

Every change away from `INERT` is recorded with a reason in that participant's `PRUNE-LOG.md` *(proposed)*, so filters can be compared and anything pruned can be recovered.

## 4. Library sub-branches

Each Library holds sub-libraries not yet created in the real repository:

**Registries · Matrices · Indices · Codices · Logics · Algorithms · Formulas**

## 5. The shared Library

Both participants collaborate on their differences in these sub-libraries by contributing both collections into one whole, proposed as branch `library-shared`.

*(proposed)* Identical contributions (same blob fingerprint) merge automatically. Differing versions are kept side by side and flagged for Timothy, who rules on them.

## 6. Recursive Return Review (mandatory)

Each participant may reference the whole shared Library at any time, because the other may have contributed something new, or something may have been missed in an earlier pass. Returning to the Library is mandatory and recursive.

*(proposed)* Each review covers only what changed in the shared Library since that participant's last visit, so the review stays cheap.

## 7. Start gate for Contract 001 *(proposed)*

Contract 000 never finishes. Contract 001 may begin once 000 is *running*:
- both Mirroring Children exist with inert skeletons covering every branch,
- each participant has completed a first Library pruning pass with reasons recorded,
- the shared Library holds at least one merged contribution from each participant.

## 8. Standing rules for all later contracts

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
