# Functional applications

The mechanism can support:

- plugin registries that must match a declared layout before activation;
- migration/bootstrap pipelines that should expose state only after verification;
- notebook kernels that provision fixed namespaces before user execution;
- test fixtures that require ordered setup and fail-closed access;
- cache/index bundles whose schema must be complete before reads;
- local capability registries where construction and exposure are separate operations;
- reproducible experiment environments with auditable initialization order;
- browser-local archive workbenches that keep extraction/export disabled until the runtime, parser, safe-path policy, quota and output writer are all present and verified.

For archive handling, readiness verification does not establish file trust. ZIP-bomb limits, path traversal and symlink defenses, storage quotas and explicit user permission remain separate requirements.

It should not be marketed as a security sandbox, login system, secrets vault, distributed lock, package signature verifier or protection from arbitrary code in the same process.

Future application reviews should look for fixed-layout initialization, partial-boot leakage, non-idempotent startup, missing verification gates and state exposure before migration completion.

