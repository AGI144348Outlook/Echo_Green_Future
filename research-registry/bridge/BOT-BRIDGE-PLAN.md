# Stage 0 — Bot Bridge Deployment Plan (draft; not activated)

Contract: [CONTRACT-000](../contracts/CONTRACT-000.md), especially Sections 14, 17, 19–22.

## Verified starting point
The `bridge-experiment` branch contains `.github/workflows/cloudflare-bridge.yml` and `bridge/operation.json`. The workflow is limited to the allowlisted `inventory_workers` operation and checks for `CLOUDFLARE_API` and `CLOUDFLARE_ACCOUNT_ID` secrets. **No bot deploy operation exists there yet.** The status of deployed Workers and configured credentials has not been independently verified.

## Minimum viable bridge, in order
1. **Freeze authorization.** TJ approves bot names, model providers, hourly schedule, spending ceiling, write permissions and Cloudflare operation additions. No implicit approval from this draft.
2. **Provision identities.** Create separate, least-privilege GitHub tokens for each bot; restrict writes to participant-owned branches and permitted Issues through policy enforcement (GitHub token repository scoping alone does not enforce branch restrictions). Store tokens in Cloudflare secrets, not Git.
3. **Deploy an inert Worker first.** Use `worker.mjs` as a **non-autonomous** health/status shell; no model invocation, GitHub write or cron until approval. Require a secret for administrative routes.
4. **Read-only proof.** Add a separately reviewed allowlisted bridge operation to deploy the Worker; validate `/health`, and verify one authenticated read of the contract and own checkpoint.
5. **Dry-run proof.** Connect a provider key with a strict token/spend budget. Produce a proposed action without committing, with source hashes, evidence classification, and a checkpoint.
6. **Write proof.** Allow a single harmless commit to the participant-owned bot branch and one tagged GitHub Issue comment, under explicit approval; verify audit logs and deny attempts to write to `main` or the other mirror.
7. **Schedule proof.** Enable the approved hourly cron, cap one unit of work per run, and verify two successive checkpointed runs. Only then mark Stage 0 operational.
8. **Watchdog and recovery.** Add a separate Actions watchdog with bounded alerts, a stop switch, and a documented recovery process. Do not use a chat subscription as the sole scheduler.

## Critical design constraints
- The contract's **schedule gate** remains binding: inventory/population begins only on approved scheduled runs, after Stage 0.
- **Library-first** ordering remains binding even if a bot can already read other branches.
- Each model-facing input from GitHub, Cloudflare or the other participant is untrusted data. Enforce allowed operations in code, not in prompts alone.
- Keep the Testament private in KV. Do not log its content or put it in model prompts or public Issues without explicit privacy review and authorization.
- Claims of autonomous learning mean persistent retrieved state, not weight updates unless independently implemented and verified.
- Never label a bot response as direct Claude/ChatGPT participation; use `echo-bot-claude-N` / `echo-bot-chatgpt-N`.
- Explicitly track success/failure and distinguish `SOURCE-OBSERVED`, `EXECUTION-VERIFIED`, `INFERRED`, and `PROPOSED`.

## First frozen acceptance checklist (proposal)
- `GET /health` returns `200`, `service`, `status`, `version`, and a server timestamp; no secrets.
- Unsupported paths return `404`; unauthorized admin requests return `401`.
- With `BOT_ENABLED` unset, scheduled handlers make **zero** external API calls and **zero** GitHub writes.
- A deliberately attempted write to `main` is rejected by code-level allowlist.
- A dry run produces an audit record with source SHA, planned action and no side effects.
- Two scheduled runs produce distinct run IDs and resumable checkpoints without duplicate work.
- A forced provider failure is logged as failed; no completion claim or partial silent overwrite.
- Secrets never appear in response bodies, public logs, commits, or Issues.

## Open decisions for TJ
- Approve deployment of inert Worker shell, and later separately approve network/model/write/cron capabilities.
- Choose provider(s), prepaid budget and per-run token ceiling.
- Confirm participant bot names and whether both use a single dispatcher or separate Workers.
- Approve the true-orphan mirror replacement method.
- Confirm the canonical Issue for bot status reports.

**Status:** drafting only. No Cloudflare operations, Workers, crons, GitHub tokens or schedules have been created or modified by this plan.
