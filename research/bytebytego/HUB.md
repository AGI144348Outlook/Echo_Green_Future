# ByteByteGo Hub — Independent, Attributed Research Catalog

This is an independent Echo_Green_Future study collection, **not affiliated with or endorsed by ByteByteGo**.

Sources: https://bytebytego.com/ and https://github.com/ByteByteGoHq/system-design-101

## Rights
The system-design-101 repository states CC BY-NC-ND 4.0. Attribution alone does not grant commercial or derivative redistribution rights. This public Hub stores **links and original research notes**, not copies of their diagrams. Review each source's rights separately. Do not confuse independent technical learning with permission to reproduce distinctive artwork.

## Relationship to study branches
- [User](../../tree/bytebytego-user): selections and annotations
- [GPT](../../tree/bytebytego-gpt): independent technical analysis
- [Claude](../../tree/bytebytego-claude): peer review and alternative analyses

Git branches cannot literally have permanent parent-child synchronization. Hub is the canonical selection catalog by convention. Research branches submit proposed records; approved original notes are cherry-picked or merged into Hub and then propagated as needed. No automatic sync has been installed.

## Discovery queue (2026-10-13)
Entries below are candidate studies, not imported images or approved implementations.

| ID | Priority | Source guide | Why it matters to Echo | Candidate experiment |
|---|---|---|---|---|
| BBG-001 | High | [Event sourcing](https://bytebytego.com/guides/how-do-we-incorporate-event-sourcing-into-the-systems/) | Presentiation history, replay and audit | Replay proposed/authorized/rejected transition records |
| BBG-002 | High | [Database selection](https://github.com/ByteByteGoHq/system-design-101/blob/main/data/guides/how-do-you-decide-which-type-of-database-to-use.md) | Distinguish registry storage, graph relations and time series | Benchmark 3 synthetic data models |
| BBG-003 | High | [Caching layers](https://github.com/ByteByteGoHq/system-design-101/blob/main/data/guides/cache-systems-every-developer-should-know.md) | Materialized views, indexed registry lookups | Rebuild caches without identity drift |
| BBG-004 | High | [System design building blocks](https://github.com/ByteByteGoHq/system-design-101/blob/main/data/guides/must-know-system-design-building-blocks.md) | API gateway, messaging, scheduling and isolation | Prototype scoped EVE/NVE message envelope |
| BBG-005 | Medium | [Caching strategies](https://github.com/ByteByteGoHq/system-design-101/blob/main/data/guides/top-5-caching-strategies.md) | Consistency between registry and derived indexes | Test invalidation and write-through behavior |
| BBG-006 | Medium | [Scalability strategies](https://github.com/ByteByteGoHq/system-design-101/blob/main/data/guides/8-must-know-scalability-strategies.md) | Distributed agent services and workload boundaries | Compare stateless worker vs stateful worker |
| BBG-007 | Medium | [System design blueprint](https://github.com/ByteByteGoHq/system-design-101/blob/main/data/guides/system-design-blueprint-the-ultimate-guide.md) | Structured architecture review checklist | Audit bridge/core/data/UI/security |
| BBG-008 | High | [System Design 101 index](https://github.com/ByteByteGoHq/system-design-101/blob/main/README.md) — GraphQL Adoption Patterns / How GraphQL Works at LinkedIn | GraphQL interfaces for registry-specific widgets | Query minimal field sets and enforce permissions |

## Nomination process
1. Study the linked guide and independently verify technical claims where possible.
2. Record source URL, diagram title/reference, retrieval date, findings, limitations, proposed Echo use, author, and rights status.
3. Write original diagrams and implementations rather than reproducing source images.
4. Nominate in your own research branch; Hub curator marks candidate / selected / tested / rejected.
5. Propagate reviewed records with traceable commits. Claude participation requires its own authorized connection.

## Selection principle
A compelling picture is not evidence of a correct architecture. Prefer concepts that can be tested and falsified.
