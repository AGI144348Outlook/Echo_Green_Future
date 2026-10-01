# Functional applications

The mechanism can support:

- plugin registries that must match a declared layout before activation;
- migration/bootstrap pipelines that should expose state only after verification;
- notebook kernels that provision fixed namespaces before user execution;
- test fixtures that require ordered setup and fail-closed access;
- cache/index bundles whose schema must be complete before reads;
- local capability registries where construction and exposure are separate operations;
- reproducible experiment environments with auditable initialization order.

It should not be marketed as a security sandbox, login system, secrets vault, distributed lock, package signature verifier or protection from arbitrary code in the same process.

Future application reviews should look for fixed-layout initialization, partial-boot leakage, non-idempotent startup, missing verification gates and state exposure before migration completion.
