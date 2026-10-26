# F-001 — pinned real-stage execution handoff (GPT Run 364, 2026-10-26 ~00 CT)

**Single continuing product:** F-001 TAM Protocol ebook. **HOLD / NOT LAUNCH-READY.** This is a *future, operator-executed* recipe, not a claim that the stage was run. No publishing, accounts, payments, outreach, CI, paid inference or Cloudflare loops. All paths and scripts are public; keep private business/customer records out of GitHub.

## Evidence and newly resolved operator ambiguity

- [Prospective Issue #56](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6408620573) was posted before this diagnostic. [Static pin/CLI audit](F-001-CLI-PIN-AUDIT-364.json): **17/17 assertions matched exact fetched source**, NOT 17 runtime stage tests.
- Exact scripts on GPT Run 363 ancestor: builder `F-001-REBUILD-DATASETS-334.py` Git blob `e8af6e5f011ec3e827c94737c717937944924eb8`; gate `F-001-DATASET-STAGE-GATE-344.py` blob `5d5bb8f85db7f21c50ca71625e82c51102fed088`; consumer `F-001-STAGE-CONSUMER-347.py` blob `b2a97390ba39959cd2f86a5e51ea186348f31fb2`; coordinator `F-001-STAGE-SESSION-351.py` blob `68eea27de6e9a961f31122a08585ee6e24fed2df`.
- **Observed documentation defect:** the coordinator's own Usage docstring names `F-001-REBUILD-DATASETS-332.py`, but the executable `PIN_BUILDER_BLOB` and the other two validators require the **Run 334** builder. Following the docstring literally can cause a fail-closed pin mismatch. Use **334**, not 332. This is an operator-documentation correction, not an unverified change to the pinned script.
- Pinned public source `AGI144348Outlook/The-TAM-protocol` commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`; source A Git blob `b62c970a660e0a6685b58db1ef121690daa4fce7`; source B `12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4`. CSV output digests expected by gate/consumer: A `989d83c16568f23a97251d93919068f3a5e726c738644625af909b278f395fdb`, B `ff442e48acaf00900a3bc3d7900bf987995355a34226b749dbd5b81878e2f7c0`. These are draft evidence pins, not release authority.
- **Actual execution blocker:** local `git ls-remote` returned `Could not resolve host: github.com` (2026-10-26). No local TAM checkout; no Run 334/344/347/351 stage, tamper test, EPUB/PDF or CI executed in this run.

## Reproducible operator procedure — NOT EXECUTED

First publish a **new prospective pre-test** in the active repository Issue/Discussion immediately before a later execution, identifying environment, exact pins, isolated stage directory, negative control and expected HOLD outcome. Run on an isolated POSIX environment with Python 3 and Git, no credentials beyond read-only public clone access. Verify no untrusted hooks, extra scripts or shared working trees are executed. The following shell is an **untested recipe** and should be independently reviewed before use:

```sh
set -eu
WORK="$(mktemp -d)"
chmod 700 "$WORK"
SRC="$WORK/tam"
ECHO="$WORK/echo"
ROOT="$WORK/stages"
mkdir -m 700 "$ROOT"

git clone --no-checkout https://github.com/AGI144348Outlook/The-TAM-protocol.git "$SRC"
git -C "$SRC" checkout --detach d46456a18fe412398d0ae37ec5a8c4eebb44e0c9
test "$(git -C "$SRC" rev-parse HEAD)" = d46456a18fe412398d0ae37ec5a8c4eebb44e0c9
test -z "$(git -C "$SRC" status --porcelain)"

git clone --no-checkout https://github.com/AGI144348Outlook/Echo_Green_Future.git "$ECHO"
git -C "$ECHO" fetch origin contract-000-gpt-run363-20261025-2257
git -C "$ECHO" checkout --detach 1c4e351835681a65e32400389bbcf75f120820c3

BASE="$ECHO/contract-000/gpt/business"
BUILDER="$BASE/F-001-REBUILD-DATASETS-334.py"
GATE="$BASE/F-001-DATASET-STAGE-GATE-344.py"
CONSUMER="$BASE/F-001-STAGE-CONSUMER-347.py"
SESSION="$BASE/F-001-STAGE-SESSION-351.py"

test "$(git hash-object "$BUILDER")" = e8af6e5f011ec3e827c94737c717937944924eb8
test "$(git hash-object "$GATE")" = 5d5bb8f85db7f21c50ca71625e82c51102fed088
test "$(git hash-object "$CONSUMER")" = b2a97390ba39959cd2f86a5e51ea186348f31fb2
test "$(git hash-object "$SESSION")" = 68eea27de6e9a961f31122a08585ee6e24fed2df

# HOLD-only: save stdout and stderr separately; preserve the actual exit status.
python3 -I -B "$SESSION" --source "$SRC" --builder "$BUILDER" \
  --root "$ROOT" --gate "$GATE" --consumer "$CONSUMER" \
  > "$WORK/session.json" 2> "$WORK/session.err"
# Inspect the receipt, marker, actual source pins, CSV hashes and status.
# Never interpret exit 0 or release:HOLD as permission to publish.
```

**Safety:** stage root must be pre-existing, normalized, private and outside both clones; avoid running as root. Do not edit or re-pin a mismatch to make the stage pass. Record tool versions, Git commits, stage hashes, full exit status, stderr (scrub private paths), and whether the fresh `STAGED_ONLY` stage plus consumer `release:HOLD` receipt appeared. If a later test modifies an output for a negative control, use a **disposable isolated copy or fresh test stage**, not the preserved positive evidence.

## Acceptance criteria and blockers

**Runtime evidence needed:** fresh verified Run 334 CSVs (A 11 columns/B 9); stage gate `STAGED_ONLY`; consumer and coordinator `HOLD` receipts bound to the same invocation; independent negative altered-input rejection; reproducible hashes; clean stage root and no unexpected writes. A failing case must remain visible rather than silently corrected. **Product gates still open:** Timothy A1–A6, B6 and C1; claims worksheet, rights/credit/licence, Article 4 and Gerah/rounding dispositions; actual EPUB/PDF accessibility and package verification; Claude cross-review; explicit Timothy launch authorization.

**Next action:** when network is available, preregister and execute the exact pinned HOLD chain; report the observed results in the same Issue. Claude's complementary lane: rights, editorial, listing and accessibility. No new income pipeline.
