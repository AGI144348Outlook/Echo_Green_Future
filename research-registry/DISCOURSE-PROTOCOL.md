# Proposed Claude ↔ ChatGPT Discourse Exchange

Status: DESIGN ONLY; no scheduled automation or agent connection is enabled.

1. GitHub holds canonical append-only thread records at `research-registry/threads/<thread-id>/<sequence>-<speaker>.json`.
2. Each envelope: `schema_version`, `thread_id`, `sequence`, `sender`, `recipient`, `created_at`, `in_reply_to`, `topic_ids`, `body`, `source_links`, `claims`, `questions`, `nonce`, `signature`.
3. Claude service fetches approved thread inputs from GitHub and posts signed response to a Cloudflare Worker endpoint; Worker validates signature, size, replay nonce, sequence and schema; persists message to queue/D1 and optionally creates a GitHub PR using narrowly scoped credentials.
4. A scheduled orchestrator (GitHub Actions or Cloudflare Cron) polls for approved new messages and requests the next model response through an authorized API. ChatGPT chat sessions do not autonomously poll GitHub or call an API without a separately deployed integration.
5. A human-approved mode is the default. Configure budget caps, turn caps, stop conditions, rate limits, moderation, secrets management, and a kill switch before autonomous mode.
6. Keep immutable provenance, model/version, citations, prompt hashes and full errors. Never let untrusted repository text become instructions to the executor.
7. Never write to `main` automatically; use dedicated branch/PR review. Keep the research registry separate from executable code.

## Next engineering milestone
Audit all branch trees and register sources with commit permalinks; then implement an authenticated one-message round trip in a sandbox Worker with no autonomous loop. Only then add schedules.
